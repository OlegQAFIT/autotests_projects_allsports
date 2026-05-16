# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin, urlparse, urlunparse

import allure
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


pytestmark = [pytest.mark.release_gate]


KEY_PAGES = [
    "https://www.allsports.by/ru-by/",
    "https://www.allsports.by/ru-by/facilities",
    "https://www.allsports.by/ru-by/facilities-table",
    "https://www.allsports.by/ru-by/levels",
    "https://www.allsports.by/ru-by/companies",
    "https://www.allsports.by/ru-by/partners",
    "https://www.allsports.by/ru-by/contacts",
    "https://www.allsports.by/ru-by/app",
]

INTERNAL_HOSTS = {"www.allsports.by", "allsports.by"}
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "#")
ASSET_EXTENSIONS = (
    ".js",
    ".css",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".map",
)


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))


def _extract_canonical_href(html: str) -> str | None:
    for match in re.finditer(r"<link[^>]+>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        if not re.search(r"rel\s*=\s*['\"][^'\"]*canonical[^'\"]*['\"]", tag, flags=re.IGNORECASE):
            continue
        href_match = re.search(r"href\s*=\s*['\"]([^'\"]+)['\"]", tag, flags=re.IGNORECASE)
        if href_match:
            return href_match.group(1).strip()
    return None


def _accept_cookie_if_present(driver):
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookie-primary-modal__confirm"))
        ).click()
    except Exception:
        pass


def _collect_internal_links(driver):
    links = set()
    for page_url in KEY_PAGES:
        driver.get(page_url)
        _accept_cookie_if_present(driver)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        for anchor in anchors:
            raw_href = (anchor.get_attribute("href") or "").strip()
            if not raw_href:
                continue
            if raw_href.startswith(SKIP_PREFIXES):
                continue

            absolute = urljoin(page_url, raw_href)
            parsed = urlparse(absolute)
            if parsed.scheme not in ("http", "https"):
                continue
            if parsed.netloc.lower() not in INTERNAL_HOSTS:
                continue

            normalized = _normalize_url(absolute)
            if "/_nuxt/" in normalized:
                continue
            if normalized.endswith(ASSET_EXTENSIONS):
                continue

            links.add(normalized)
    return sorted(links)


@allure.feature("Links")
@allure.severity("Critical")
@allure.story("Crawler внутренних ссылок: HTTP + canonical + final URL")
def test_internal_links_crawler_http_and_canonical(driver):
    links = _collect_internal_links(driver)
    assert links, "Crawler не собрал ни одной внутренней ссылки"

    bad_links = []

    for link in links:
        # 1) Проверяем, что ссылка не уходит в 4xx/5xx сразу.
        first = requests.get(link, timeout=20, allow_redirects=False)
        if first.status_code >= 400:
            bad_links.append(f"{link} -> first_status={first.status_code}")
            continue

        # 2) Проверяем финальный переход (с учетом редиректов).
        final = requests.get(link, timeout=20, allow_redirects=True)
        if final.status_code >= 400:
            bad_links.append(f"{link} -> final_status={final.status_code}")
            continue

        final_url = _normalize_url(final.url)

        # 3) Проверяем canonical на HTML страницах.
        content_type = (final.headers.get("Content-Type") or "").lower()
        if "text/html" in content_type:
            canonical_href = _extract_canonical_href(final.text or "")
            if canonical_href:
                canonical_abs = urljoin(final.url, canonical_href)
                canonical_url = _normalize_url(canonical_abs)
                if canonical_url != final_url:
                    bad_links.append(
                        f"{link} -> canonical_mismatch: canonical={canonical_url} final={final_url}"
                    )

    assert not bad_links, "Обнаружены проблемы внутренних ссылок:\n" + "\n".join(bad_links[:40])

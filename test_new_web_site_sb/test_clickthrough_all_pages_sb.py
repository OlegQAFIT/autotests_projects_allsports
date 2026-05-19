# -*- coding: utf-8 -*-
from urllib.parse import urljoin, urlparse

import allure
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.new_web_site_sb.base_page_sb import BasePageSb


KEY_PAGES = [
    "https://www.sportbenefit.eu/en-cy",
    "https://www.sportbenefit.eu/en-cy/facilities",
    "https://www.sportbenefit.eu/en-cy/facilities-table",
    "https://www.sportbenefit.eu/en-cy/levels",
    "https://www.sportbenefit.eu/en-cy/companies",
    "https://www.sportbenefit.eu/en-cy/partners",
    "https://www.sportbenefit.eu/en-cy/contacts",
    "https://www.sportbenefit.eu/en-cy/app",
    "https://www.sportbenefit.eu/en-cy/license",
    "https://www.sportbenefit.eu/en-cy/user-agreements",
]

HOSTS = {"www.sportbenefit.eu", "sportbenefit.eu"}
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "#")


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return f"{parsed.scheme}://{parsed.netloc.lower()}{path}"


def _collect_internal_anchors(driver, page_url):
    links = set()
    for anchor in driver.find_elements(By.CSS_SELECTOR, "a[href]"):
        href = (anchor.get_attribute("href") or "").strip()
        if not href or href.startswith(SKIP_PREFIXES):
            continue
        absolute = urljoin(page_url, href)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc.lower() not in HOSTS:
            continue
        links.add(_normalize_url(absolute))
    return sorted(links)


def _collect_clickable_targets(driver):
    raw = driver.execute_script(
        """
        const nodes = Array.from(document.querySelectorAll(
          "button, [role='button'], .select-tab__option, a[href]"
        ));

        const visible = (el) => {
          const style = window.getComputedStyle(el);
          const hasSize = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
          return hasSize && style.visibility !== 'hidden' && style.display !== 'none';
        };

        return nodes
          .filter(visible)
          .map((el, idx) => {
            const tag = (el.tagName || '').toLowerCase();
            const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
            const href = (el.getAttribute('href') || '').trim();
            const type = (el.getAttribute('type') || '').trim().toLowerCase();
            const cls = (el.className || '').toString();
            const path = `${tag}:${text}:${href}:${cls}:${idx}`;
            return { index: idx, tag, text, href, type, path };
          });
        """
    )
    unique = []
    seen = set()
    for item in raw:
        key = item.get("path", "")
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def _safe_close_modal(driver):
    close_buttons = driver.find_elements(By.CSS_SELECTOR, ".modal .modal-header .icon-btn, .modal .icon-btn")
    if close_buttons:
        driver.execute_script("arguments[0].click();", close_buttons[0])
        WebDriverWait(driver, 6).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal input, .modal textarea"))
        )


@allure.feature("SB Clickthrough")
@allure.severity("Critical")
@pytest.mark.pre_release
def test_internal_links_clickthrough_status_sb(driver):
    """Проверка внутренних ссылок: корректные переходы и отсутствие 4xx/5xx статусов."""
    page = BasePageSb(driver)
    broken = []

    for page_url in KEY_PAGES:
        page.open_url(page_url)
        page.accept_cookie_consent()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        links = _collect_internal_anchors(driver, page_url)
        assert links, f"No internal links collected from {page_url}"

        for link in links:
            first = requests.get(link, timeout=20, allow_redirects=False)
            if first.status_code >= 400:
                broken.append(f"{link} -> first_status={first.status_code}")
                continue

            final = requests.get(link, timeout=20, allow_redirects=True)
            if final.status_code >= 400:
                broken.append(f"{link} -> final_status={final.status_code}")

    assert not broken, "Broken links in clickthrough check:\n" + "\n".join(broken[:80])


@allure.feature("SB Clickthrough")
@allure.severity("Critical")
@pytest.mark.pre_release
def test_primary_buttons_tabs_clickthrough_sb(driver):
    """Проверка кликабельности основных кнопок и вкладок на ключевых страницах."""
    page = BasePageSb(driver)
    issues = []

    skip_button_text = {"send", "confirm", "accept", "reject"}

    for page_url in KEY_PAGES:
        page.open_url(page_url)
        page.accept_cookie_consent()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        targets = _collect_clickable_targets(driver)
        assert targets, f"No clickable targets found on {page_url}"

        for target in targets:
            tag = (target.get("tag") or "").lower()
            text = (target.get("text") or "").strip().lower()
            href = (target.get("href") or "").strip()
            btn_type = (target.get("type") or "").lower()
            index = int(target.get("index") or 0)

            if tag == "a":
                continue
            if btn_type == "submit":
                continue
            if text in skip_button_text:
                continue

            try:
                clicked = driver.execute_script(
                    """
                    const nodes = Array.from(document.querySelectorAll(
                      "button, [role='button'], .select-tab__option, a[href]"
                    ));
                    const idx = arguments[0];
                    const el = nodes[idx];
                    if (!el) return false;
                    const style = window.getComputedStyle(el);
                    const visible = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
                      && style.visibility !== 'hidden'
                      && style.display !== 'none';
                    if (!visible) return false;
                    el.click();
                    return true;
                    """,
                    index,
                )
                if not clicked:
                    continue
                _safe_close_modal(driver)
            except Exception as exc:
                issues.append(
                    f"{page_url} -> click failed for tag='{tag}' text='{target.get('text')}' href='{href}': {exc}"
                )

        assert "sportbenefit.eu" in driver.current_url, (
            f"Unexpected host after clickthrough on {page_url}: {driver.current_url}"
        )

    assert not issues, "Button/tab clickthrough issues found:\n" + "\n".join(issues[:80])

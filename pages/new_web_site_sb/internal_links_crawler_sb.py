# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.new_web_site_sb.base_page_sb import BasePageSb


class InternalLinksCrawlerSb(BasePageSb):
    KEY_PAGES = [
        "https://www.sportbenefit.eu/en-cy",
        "https://www.sportbenefit.eu/en-cy/facilities",
        "https://www.sportbenefit.eu/en-cy/facilities-table",
        "https://www.sportbenefit.eu/en-cy/levels",
        "https://www.sportbenefit.eu/en-cy/companies",
        "https://www.sportbenefit.eu/en-cy/partners",
        "https://www.sportbenefit.eu/en-cy/contacts",
        "https://www.sportbenefit.eu/en-cy/app",
    ]
    INTERNAL_HOSTS = {"www.sportbenefit.eu", "sportbenefit.eu"}
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

    @staticmethod
    def normalize_url(url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path or "/"
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))

    @staticmethod
    def extract_canonical_href(html: str) -> str | None:
        for match in re.finditer(r"<link[^>]+>", html, flags=re.IGNORECASE):
            tag = match.group(0)
            if not re.search(r"rel\s*=\s*['\"][^'\"]*canonical[^'\"]*['\"]", tag, flags=re.IGNORECASE):
                continue
            href_match = re.search(r"href\s*=\s*['\"]([^'\"]+)['\"]", tag, flags=re.IGNORECASE)
            if href_match:
                return href_match.group(1).strip()
        return None

    def collect_internal_links(self):
        links = set()
        for page_url in self.KEY_PAGES:
            self.open_url(page_url)
            self.accept_cookie_consent()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            for anchor in self.driver.find_elements(By.CSS_SELECTOR, "a[href]"):
                raw_href = (anchor.get_attribute("href") or "").strip()
                if not raw_href or raw_href.startswith(self.SKIP_PREFIXES):
                    continue

                absolute = urljoin(page_url, raw_href)
                parsed = urlparse(absolute)
                if parsed.scheme not in ("http", "https"):
                    continue
                if parsed.netloc.lower() not in self.INTERNAL_HOSTS:
                    continue

                normalized = self.normalize_url(absolute)
                if "/_nuxt/" in normalized:
                    continue
                if normalized.endswith(self.ASSET_EXTENSIONS):
                    continue

                links.add(normalized)

        return sorted(links)

    def check_internal_links_http_and_canonical(self):
        links = self.collect_internal_links()
        assert links, "Crawler did not collect any internal links"

        bad_links = []
        for link in links:
            first = requests.get(link, timeout=20, allow_redirects=False)
            if first.status_code >= 400:
                bad_links.append(f"{link} -> first_status={first.status_code}")
                continue

            final = requests.get(link, timeout=20, allow_redirects=True)
            if final.status_code >= 400:
                bad_links.append(f"{link} -> final_status={final.status_code}")
                continue

            final_url = self.normalize_url(final.url)
            content_type = (final.headers.get("Content-Type") or "").lower()
            if "text/html" not in content_type:
                continue

            canonical_href = self.extract_canonical_href(final.text or "")
            if not canonical_href:
                continue

            canonical_abs = urljoin(final.url, canonical_href)
            canonical_url = self.normalize_url(canonical_abs)
            if canonical_url != final_url:
                bad_links.append(
                    f"{link} -> canonical_mismatch: canonical={canonical_url} final={final_url}"
                )

        assert not bad_links, "Internal links issues found:\n" + "\n".join(bad_links[:50])

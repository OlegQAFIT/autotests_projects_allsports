# -*- coding: utf-8 -*-
from urllib.parse import urljoin, urlparse

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.new_web_site_sb.base_page_sb import BasePageSb


class ClickthroughSb(BasePageSb):
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

    @staticmethod
    def normalize_url(url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path or "/"
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        return f"{parsed.scheme}://{parsed.netloc.lower()}{path}"

    def collect_internal_anchors(self, page_url):
        links = set()
        for anchor in self.driver.find_elements(By.CSS_SELECTOR, "a[href]"):
            href = (anchor.get_attribute("href") or "").strip()
            if not href or href.startswith(self.SKIP_PREFIXES):
                continue
            absolute = urljoin(page_url, href)
            parsed = urlparse(absolute)
            if parsed.scheme not in ("http", "https"):
                continue
            if parsed.netloc.lower() not in self.HOSTS:
                continue
            links.add(self.normalize_url(absolute))
        return sorted(links)

    def collect_clickable_targets(self):
        raw = self.driver.execute_script(
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

    def safe_close_modal(self):
        close_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".modal .modal-header .icon-btn, .modal .icon-btn")
        if close_buttons:
            self.driver.execute_script("arguments[0].click();", close_buttons[0])
            WebDriverWait(self.driver, 6).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal input, .modal textarea"))
            )

    def check_internal_links_clickthrough_status(self):
        broken = []

        for page_url in self.KEY_PAGES:
            self.open_url(page_url)
            self.accept_cookie_consent()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            links = self.collect_internal_anchors(page_url)
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

    def check_primary_buttons_tabs_clickthrough(self):
        issues = []
        skip_button_text = {"send", "confirm", "accept", "reject"}

        for page_url in self.KEY_PAGES:
            self.open_url(page_url)
            self.accept_cookie_consent()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            targets = self.collect_clickable_targets()
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
                    clicked = self.driver.execute_script(
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
                    self.safe_close_modal()
                except Exception as exc:
                    issues.append(
                        f"{page_url} -> click failed for tag='{tag}' text='{target.get('text')}' href='{href}': {exc}"
                    )

            assert "sportbenefit.eu" in self.driver.current_url, (
                f"Unexpected host after clickthrough on {page_url}: {self.driver.current_url}"
            )

        assert not issues, "Button/tab clickthrough issues found:\n" + "\n".join(issues[:80])

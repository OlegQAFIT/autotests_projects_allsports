# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin, urlparse

import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.regression_pages_locators_sb import RegressionPagesLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


CYRILLIC_WORD_RE = re.compile(r"[А-Яа-яЁёІіЇїЄєЎў]+")


class RegressionPagesSb(BasePageSb):
    def __init__(self, driver):
        super().__init__(driver)
        self._image_status_cache = {}

    def _wait_body(self):
        WebDriverWait(self.driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    @staticmethod
    def _collect_cyrillic_words(text):
        return sorted(set(CYRILLIC_WORD_RE.findall(text or "")))

    def _logo_loaded(self):
        logos = self.driver.find_elements(By.CSS_SELECTOR, L.LOGO_SELECTOR)
        assert len(logos) >= 1, f"Header logo not found on {self.driver.current_url}"

        for logo in logos:
            rendered = self.driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;", logo
            )
            if rendered:
                return

        raise AssertionError(f"Header logo is not rendered correctly on {self.driver.current_url}")

    def _collect_image_urls(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('img'))
              .map((img) => img.currentSrc || img.getAttribute('src') || '')
              .filter(Boolean);
            """
        )

    def _collect_visible_broken_images(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('img'))
              .filter((img) => {
                const src = img.currentSrc || img.getAttribute('src') || '';
                if (!src) return false;
                const style = window.getComputedStyle(img);
                const visible = style && style.display !== 'none' && style.visibility !== 'hidden' && img.offsetParent !== null;
                if (!visible) return false;
                return !img.complete || img.naturalWidth === 0;
              })
              .map((img) => img.currentSrc || img.getAttribute('src') || '');
            """
        )

    @staticmethod
    def _is_internal_image(url):
        parsed = urlparse(url)
        if parsed.scheme in ("data", "blob"):
            return False
        return parsed.netloc.lower() in L.INTERNAL_IMAGE_HOSTS or parsed.netloc == ""

    def _assert_internal_image_urls_available(self, page_url, image_urls):
        checked = 0
        for raw_url in image_urls:
            absolute_url = urljoin(page_url, raw_url)
            if not self._is_internal_image(absolute_url):
                continue

            if absolute_url in self._image_status_cache:
                status_code = self._image_status_cache[absolute_url]
            else:
                response = requests.get(absolute_url, timeout=25, allow_redirects=True)
                status_code = response.status_code
                self._image_status_cache[absolute_url] = status_code

            checked += 1
            assert status_code < 400, (
                f"Broken image URL on page {page_url}: {absolute_url} -> {status_code}"
            )

        assert checked >= 1, f"No internal image URLs were checked on {page_url}"

    def _collect_page_body_cyrillic_words(self):
        body_text = (self.driver.find_element(By.TAG_NAME, "body").text or "").strip()
        assert len(body_text) >= 40, f"Body content is unexpectedly short on {self.driver.current_url}"
        return self._collect_cyrillic_words(body_text)

    def _is_internal_html_page_url(self, absolute_url):
        parsed = urlparse(absolute_url)
        if parsed.scheme not in ("http", "https"):
            return False

        if parsed.netloc.lower() not in L.INTERNAL_PAGE_HOSTS:
            return False

        path = (parsed.path or "/").lower()
        if not path.startswith(L.INTERNAL_PAGE_PATH_PREFIX):
            return False

        if any(part in path for part in L.SKIP_PATH_PARTS):
            return False

        if path.endswith(L.SKIP_EXTENSIONS):
            return False

        return True

    def _collect_internal_links_from_page(self, page_url):
        self.driver.set_page_load_timeout(45)
        self.open_url(page_url)
        self.accept_cookie_consent()
        self._wait_body()

        links = set()
        anchors = self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
        for anchor in anchors:
            raw_href = (anchor.get_attribute("href") or "").strip()
            if not raw_href:
                continue

            if raw_href.lower().startswith(L.SKIP_HREF_PREFIXES):
                continue

            absolute = urljoin(page_url, raw_href)
            if not self._is_internal_html_page_url(absolute):
                continue

            links.add(self.normalize_url(absolute))

        return links

    def _build_pages_for_cyrillic_scan(self):
        pages = {self.normalize_url(url) for url in L.ALL_CHECK_PAGES}

        for seed_url in L.KEY_PAGES:
            pages.update(self._collect_internal_links_from_page(seed_url))

        return sorted(pages)

    def _open_filter_modal_and_collect_cyrillic(self, trigger_locator, context, required=True):
        buttons = self.driver.find_elements(*trigger_locator)
        if not buttons:
            if required:
                raise AssertionError(f"Filter button not found for context {context}")
            return []

        self.driver.execute_script("arguments[0].click();", buttons[0])

        try:
            modal = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, L.FILTER_MODAL_ROOT_CSS))
            )
        except Exception as exc:
            if required:
                raise AssertionError(f"Filter modal did not open for context {context}") from exc
            return []

        modal_text = (modal.text or "").strip()
        assert modal_text, f"Filter modal text is empty for context {context}"
        words = self._collect_cyrillic_words(modal_text)

        apply_buttons = self.driver.find_elements(By.XPATH, L.FILTER_MODAL_APPLY_XPATH)
        if apply_buttons:
            self.driver.execute_script("arguments[0].click();", apply_buttons[0])
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, L.FILTER_MODAL_ROOT_CSS))
            )

        return words

    def _collect_interactive_cyrillic_words(self, url, viewport_label):
        words = []

        if url == L.FACILITIES_TABLE_PAGE:
            words.extend(
                self._open_filter_modal_and_collect_cyrillic(
                    (By.CSS_SELECTOR, L.TABLE_FILTER_BUTTON_CSS),
                    f"facilities-table filters [{viewport_label}]",
                    required=False,
                )
            )

        if url == L.FACILITIES_PAGE:
            words.extend(
                self._open_filter_modal_and_collect_cyrillic(
                    (By.XPATH, L.GENERIC_FILTER_BUTTON_XPATH),
                    f"facilities filters [{viewport_label}]",
                    required=False,
                )
            )

        return sorted(set(words))

    def check_legal_pages(self):
        for url in L.LEGAL_PAGES:
            self.open_url(url)
            self.accept_cookie_consent()
            self._wait_body()
            body_text = (self.driver.find_element(By.TAG_NAME, "body").text or "").strip()
            assert len(body_text) > 80, f"Legal page looks empty: {url}"

    def check_mobile_layouts(self):
        for width, height in L.MOBILE_VIEWPORTS:
            self.driver.set_window_size(width, height)
            for url in L.KEY_PAGES:
                self.open_url(url)
                self.accept_cookie_consent()
                self._wait_body()
                assert "sportbenefit.eu" in self.driver.current_url, (
                    f"Unexpected URL on viewport {width}x{height}: {self.driver.current_url}"
                )
                header_links = self.driver.find_elements(By.CSS_SELECTOR, "header a[href]")
                assert len(header_links) >= 1, f"Header links missing on {url} [{width}x{height}]"

    def _check_page_copywriting_and_ui_integrity(self, url, viewport_label):
        context = f"{url} [{viewport_label}]"

        self.driver.set_page_load_timeout(45)
        self.open_url(url)
        self.accept_cookie_consent()
        self._wait_body()

        assert "sportbenefit.eu" in self.driver.current_url, (
            f"Unexpected host on {context}: {self.driver.current_url}"
        )

        header_links = self.driver.find_elements(By.CSS_SELECTOR, "header a[href]")
        assert len(header_links) >= 1, f"Header links are missing on {context}"

        self._logo_loaded()
        self.assert_canonical_matches_current()

        if url not in L.PAGES_WITHOUT_FOOTER:
            footer_links = self.driver.find_elements(By.CSS_SELECTOR, "footer a[href]")
            assert len(footer_links) >= 1, f"Footer links are missing on {context}"

        body_words = self._collect_page_body_cyrillic_words()
        interactive_words = self._collect_interactive_cyrillic_words(url, viewport_label)

        found_words = sorted(set(body_words + interactive_words))
        assert not found_words, (
            f"Cyrillic words detected on EN page {context}: {found_words[:20]}"
        )

    def check_copywriting_and_ui_integrity_on_all_pages(self):
        pages_to_check = self._build_pages_for_cyrillic_scan()
        assert pages_to_check, "No pages were collected for EN Cyrillic scan"

        failures = []
        for width, height in L.COPYWRITING_VIEWPORTS:
            self.driver.set_window_size(width, height)
            viewport_label = f"{width}x{height}"
            for url in pages_to_check:
                try:
                    self._check_page_copywriting_and_ui_integrity(url, viewport_label)
                except TimeoutException as exc:
                    failures.append(f"Timeout while opening page {url} [{viewport_label}]: {exc}")
                except AssertionError as exc:
                    failures.append(str(exc))

        assert not failures, (
            "Cyrillic/UI integrity issues found across pages/viewports:\n"
            + "\n".join(f"- {item}" for item in failures[:120])
        )

    def check_cyrillic_fast_gate(self):
        pages_to_check = [self.normalize_url(url) for url in L.KEY_PAGES]

        failures = []
        for width, height in L.CYRILLIC_GATE_VIEWPORTS:
            self.driver.set_window_size(width, height)
            viewport_label = f"{width}x{height}"

            for url in pages_to_check:
                context = f"{url} [{viewport_label}]"
                try:
                    self.driver.set_page_load_timeout(25)
                    self.open_url(url)
                    self.accept_cookie_consent()
                    self._wait_body()

                    assert "sportbenefit.eu" in self.driver.current_url, (
                        f"Unexpected host on {context}: {self.driver.current_url}"
                    )

                    body_words = self._collect_page_body_cyrillic_words()
                    interactive_words = self._collect_interactive_cyrillic_words(url, viewport_label)
                    found_words = sorted(set(body_words + interactive_words))
                    assert not found_words, (
                        f"Cyrillic words detected on EN page {context}: {found_words[:20]}"
                    )
                except TimeoutException as exc:
                    failures.append(f"Timeout while opening page {url} [{viewport_label}]: {exc}")
                except AssertionError as exc:
                    failures.append(str(exc))

        assert not failures, (
            "Cyrillic fast gate issues found:\n"
            + "\n".join(f"- {item}" for item in failures[:80])
        )

    def check_images_and_logo_assets_on_key_pages(self):
        for url in L.KEY_PAGES:
            self.open_url(url)
            self.accept_cookie_consent()
            self._wait_body()

            self._logo_loaded()

            image_urls = self._collect_image_urls()
            assert len(image_urls) >= 1, f"No images found on {url}"

            broken_visible_images = self._collect_visible_broken_images()
            assert not broken_visible_images, (
                f"Visible broken images found on {url}: {broken_visible_images[:10]}"
            )

            self._assert_internal_image_urls_available(url, image_urls)

    def check_mobile_facilities_table_filter_modal_copywriting(self):
        width, height = L.MOBILE_VIEWPORTS[0]
        self.driver.set_window_size(width, height)

        self.open_url(L.FACILITIES_TABLE_PAGE)
        self.accept_cookie_consent()
        self._wait_body()

        cyrillic_words = self._open_filter_modal_and_collect_cyrillic(
            (By.CSS_SELECTOR, L.TABLE_FILTER_BUTTON_CSS),
            f"facilities-table mobile modal [{width}x{height}]",
        )

        assert not cyrillic_words, (
            "Cyrillic words detected in mobile facilities-table filter modal: "
            f"{cyrillic_words[:20]}"
        )

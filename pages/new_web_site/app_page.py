# -*- coding: utf-8 -*-
import time
from urllib.parse import urlparse, urlunparse

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.base import BasePage
from locators.elements_for_new_web_site.for_app_page import AppPageLocators as L


class AppPage(BasePage):
    @staticmethod
    def _normalize_url(url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path or "/"
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))

    @staticmethod
    def _filtered_console_errors(raw_logs):
        severe = [entry for entry in raw_logs if entry.get("level") == "SEVERE"]
        filtered = []
        for entry in severe:
            msg = (entry.get("message") or "").lower()
            source = (entry.get("source") or "").lower()
            if "sentry" in msg:
                continue
            if "content security policy" in msg or "csp" in msg:
                continue
            if source in ("security", "network"):
                continue
            filtered.append(entry)
        return filtered

    @allure.step("Открыть страницу App")
    def open(self):
        self.driver.get(L.BASE_URL)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(L.PAGE_ROOT)
        )
        return self

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        try:
            self.click_if_visible(L.COOKIE_ACCEPT_BTN, timeout=3)
        except Exception:
            pass

    @allure.step("Проверить, что открыта страница App")
    def check_page_opened(self):
        WebDriverWait(self.driver, 20).until(EC.url_contains("/app"))
        assert "/app" in self.driver.current_url, f"Открыт неверный URL: {self.driver.current_url}"
        self.assert_element_present(L.DOWNLOAD_HEADING)

    @allure.step("Проверить title и meta-description страницы App")
    def check_meta(self):
        title = self.driver.title.strip()
        assert title, "Title страницы /app пуст"
        assert "allsports" in title.lower(), f"Title не содержит Allsports: {title}"

        description = self.driver.execute_script(
            "const m = document.querySelector('meta[name=\"description\"]');"
            "return m ? (m.getAttribute('content') || '').trim() : '';"
        )
        assert description, "meta description страницы /app пустой"

    @allure.step("Проверить ссылки на магазины приложений")
    def check_store_links(self):
        apple = self.driver.find_elements(*L.APPLE_LINKS)
        google = self.driver.find_elements(*L.GOOGLE_LINKS)
        huawei = self.driver.find_elements(*L.HUAWEI_LINKS)

        assert apple, "Ссылки AppStore не найдены на /app"
        assert google, "Ссылки Google Play не найдены на /app"
        assert huawei, "Ссылки AppGallery не найдены на /app"

        for el in apple:
            href = (el.get_attribute("href") or "").strip()
            assert "apps.apple.com" in href, f"Некорректная ссылка AppStore: {href}"
        for el in google:
            href = (el.get_attribute("href") or "").strip()
            assert "play.google.com" in href, f"Некорректная ссылка Google Play: {href}"
        for el in huawei:
            href = (el.get_attribute("href") or "").strip()
            assert "appgallery.huawei.com" in href, f"Некорректная ссылка AppGallery: {href}"

    @allure.step("Проверить canonical страницы App")
    def check_canonical(self):
        canonical = self.driver.find_element(*L.CANONICAL_LINK).get_attribute("href") or ""
        assert canonical, "Canonical ссылка отсутствует на /app"
        current = self._normalize_url(self.driver.current_url)
        canonical_normalized = self._normalize_url(canonical)
        assert canonical_normalized == current, (
            f"Canonical не совпадает с текущим URL: canonical={canonical_normalized}, current={current}"
        )

    @allure.step("Проверить отсутствие критичных console errors на /app")
    def check_no_severe_console_errors(self):
        # Небольшая пауза, чтобы браузер успел отдать финальные логи после гидрации.
        time.sleep(0.3)
        logs = self.driver.get_log("browser")
        filtered = self._filtered_console_errors(logs)
        assert not filtered, f"SEVERE ошибки в консоли /app: {filtered}"

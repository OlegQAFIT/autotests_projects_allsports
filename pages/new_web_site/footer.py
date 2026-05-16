# -*- coding: utf-8 -*-
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from helpers.base import BasePage
from locators.elements_for_new_web_site.footer_elements_new_web_site import FooterLocators as L


class FooterPage(BasePage):
    L = L

    def _ensure_footer_loaded(self):
        for _ in range(6):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if self.driver.find_elements(By.TAG_NAME, "footer"):
                return
            self.driver.execute_script("window.scrollBy(0, 800);")
        assert self.driver.find_elements(By.TAG_NAME, "footer"), "Футер не найден на странице"

    def _assert_document_page_loaded(self):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//main")))
        text_len = self.driver.execute_script(
            "return (document.body && document.body.innerText) ? document.body.innerText.trim().length : 0;"
        )
        html_len = len(self.driver.page_source or "")
        assert (text_len and text_len > 120) or html_len > 5000, (
            "Страница документа загружена некорректно: мало контента в DOM"
        )

    def _filter_console_noise(self, errors):
        filtered = []
        for error in errors:
            msg = (error.get("message") or "").lower()
            source = (error.get("source") or "").lower()

            # Типовые внешние/инфраструктурные шумы, не относящиеся к регрессии UI.
            if "sentry" in msg:
                continue
            if "content security policy" in msg or "csp" in msg:
                continue
            if source in ("security", "network"):
                continue
            if "failed to load search list" in msg and "/api/v2/map/search" in msg:
                continue
            if "signal is aborted without reason" in msg:
                continue

            filtered.append(error)
        return filtered

    # --- BASE ---

    @allure.step("Открыть страницу сайта")
    def open(self, url=L.BASE_URL):
        self.driver.get(url)
        self.accept_cookie_consent()
        self._ensure_footer_loaded()
        return self

    @allure.step("Принять cookies (если показано)")
    def accept_cookie_consent(self):
        try:
            accept_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-primary-modal__confirm'))
            )
            accept_button.click()
        except (WebDriverException, TimeoutException):
            pass

    # --- FOOTER ELEMENTS ---

    @allure.step("Проверить телефон и email в футере")
    def check_footer_contacts(self):
        self.accept_cookie_consent()
        self._ensure_footer_loaded()
        phones = self.driver.find_elements(*L.PHONE)
        emails = self.driver.find_elements(*L.EMAIL)
        assert phones, "Телефонная ссылка в футере не найдена"
        assert emails, "Email-ссылка в футере не найдена"
        assert any("tel:" in (p.get_attribute("href") or "") for p in phones), "Некорректный href телефона"
        assert any("contact@allsports.by" in (e.get_attribute("href") or "") for e in emails), (
            "Некорректный href email"
        )

    @allure.step("Проверить соцсети (Instagram и LinkedIn)")
    def check_social_links(self):
        self.accept_cookie_consent()
        self._ensure_footer_loaded()
        self.assert_element_present(L.INSTAGRAM)
        self.assert_element_present(L.LINKEDIN)
        ig = self.driver.find_element(*L.INSTAGRAM).get_attribute("href") or ""
        li = self.driver.find_element(*L.LINKEDIN).get_attribute("href") or ""
        assert "instagram.com" in ig, f"Некорректная ссылка Instagram: {ig}"
        assert "linkedin.com" in li, f"Некорректная ссылка LinkedIn: {li}"

    @allure.step("Проверить магазины приложений")
    def check_app_store_links(self):
        self.accept_cookie_consent()
        self._ensure_footer_loaded()
        for locator in [L.APPSTORE, L.GOOGLEPLAY, L.APPGALLERY]:
            self.assert_element_present(locator)
        appstore = self.driver.find_element(*L.APPSTORE).get_attribute("href") or ""
        googleplay = self.driver.find_element(*L.GOOGLEPLAY).get_attribute("href") or ""
        appgallery = self.driver.find_element(*L.APPGALLERY).get_attribute("href") or ""
        assert "apple.com" in appstore, f"Некорректная ссылка AppStore: {appstore}"
        assert "play.google.com" in googleplay, f"Некорректная ссылка GooglePlay: {googleplay}"
        assert "appgallery.huawei.com" in appgallery, f"Некорректная ссылка AppGallery: {appgallery}"

    @allure.step("Проверить все основные навигационные ссылки футера")
    def check_footer_navigation_links(self):
        self.accept_cookie_consent()
        self._ensure_footer_loaded()
        mapping = [
            (L.NAV_COMPANIES, L.COMPANIES_URL, L.TEXT_COMPANIES_H1),
            (L.NAV_PARTNERS, L.PARTNERS_URL, L.TEXT_PARTNERS_H1),
            (L.NAV_FACILITIES, L.FACILITIES_URL, None),
            (L.NAV_LEVELS, L.LEVELS_URL, L.TEXT_LEVELS),
            (L.NAV_CONTACTS, L.CONTACTS_URL, L.TEXT_CONTACTS),
        ]
        for locator, url, expected_text in mapping:
            self.scroll_to_element(locator)
            self.hard_click(locator)
            WebDriverWait(self.driver, 10).until(EC.url_contains(url))
            self.assert_url_contains(url)
            if expected_text:
                self.assert_text_on_page(expected_text)
            self.driver.back()
            self.accept_cookie_consent()

    @allure.step("Проверить копирайт и регистрационный номер поставщика услуг")
    def check_copyright_and_provider(self):
        self.accept_cookie_consent()
        self._ensure_footer_loaded()
        self.assert_element_present(L.COPYRIGHT)
        self.assert_element_present(L.PROVIDER_NUMBER)

        # Проверяем переход по ссылке
        current_handles = self.driver.window_handles
        self.hard_click(L.PROVIDER_NUMBER)

        # ждем загрузку новой страницы (в этом или новом окне)
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/providing-payment-service-rules")
        )

        # если открылась новая вкладка — переключаемся
        new_handles = self.driver.window_handles
        if len(new_handles) > len(current_handles):
            self.switch_to_new_window()

        # Проверка содержимого
        self.assert_url_contains("/providing-payment-service-rules")
        self._assert_document_page_loaded()

        # Закрываем вкладку, если она новая
        if len(new_handles) > len(current_handles):
            self.close_current_window()
            self.switch_to_parent_window()

        # Проверка языка и JS
        self.check_for_words("russian")
        filtered = self._filter_console_noise(self.get_js_console_errors())
        assert len(filtered) == 0, f"JS ошибки: {filtered}"

    @allure.step("Проверить документы для юридических лиц")
    def check_legal_documents(self):
        self.accept_cookie_consent()
        urls = [
            L.POLICY_PD,
            L.LICENSE_INTERMEDIARY,
        ]
        for url in urls:
            self.driver.get(url)
            self.accept_cookie_consent()
            self.assert_url_contains(url)
            self._assert_document_page_loaded()
            self.check_for_words("russian")
            filtered = self._filter_console_noise(self.get_js_console_errors())
            assert len(filtered) == 0, f"JS ошибки (реальные!) на странице {url}: {filtered}"

    @allure.step("Проверить пользовательские соглашения и политики")
    def check_user_agreements(self):
        self.accept_cookie_consent()
        urls = [
            L.USER_AGREEMENTS,
            L.INDIVIDUAL_LICENSE,
            L.POLICY_PD,
            L.RULE_ACCESS,
            L.COOKIE_POLICY,
        ]
        for url in urls:
            self.driver.get(url)
            self.accept_cookie_consent()
            self.assert_url_contains(url)
            self._assert_document_page_loaded()
            self.check_for_words("russian")
            filtered = self._filter_console_noise(self.get_js_console_errors())
            assert len(filtered) == 0, f"JS ошибки на {url}: {filtered}"

    @allure.step("Проверить целостность футера (все элементы присутствуют)")
    def check_footer_integrity(self):
        self.accept_cookie_consent()
        self._ensure_footer_loaded()
        self.check_footer_contacts()
        self.check_social_links()
        self.check_app_store_links()
        self.check_footer_navigation_links()
        self.check_copyright_and_provider()
        self.check_legal_documents()
        self.check_user_agreements()

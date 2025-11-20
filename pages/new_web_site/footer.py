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

    # --- BASE ---

    @allure.step("Открыть страницу сайта")
    def open(self, url=L.BASE_URL):
        self.driver.get(url)
        self.accept_cookie_consent()
        self.scroll_down()
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
        self.scroll_down()
        self.assert_element_present(L.PHONE)
        self.assert_element_present(L.EMAIL)
        self.assert_text_on_page("+375 44 771 09 47")
        self.assert_text_on_page("contact@allsports.by")

    @allure.step("Проверить соцсети (Instagram и LinkedIn)")
    def check_social_links(self):
        self.accept_cookie_consent()
        self.scroll_down()
        self.assert_element_present(L.INSTAGRAM)
        self.assert_element_present(L.LINKEDIN)

        # Instagram
        self.hard_click(L.INSTAGRAM)
        self.switch_to_new_window()
        self.assert_url_contains("instagram.com/allsports.by")
        self.close_current_window()
        self.switch_to_parent_window()

        # LinkedIn
        self.hard_click(L.LINKEDIN)
        self.switch_to_new_window()
        self.assert_url_contains("linkedin.com/company/allsportsby")
        self.close_current_window()
        self.switch_to_parent_window()

    @allure.step("Проверить магазины приложений")
    def check_app_store_links(self):
        self.accept_cookie_consent()
        self.scroll_down()
        for locator in [L.APPSTORE, L.GOOGLEPLAY, L.APPGALLERY]:
            self.assert_element_present(locator)

        # Проверка открытия App Store
        self.hard_click(L.APPSTORE)
        self.switch_to_new_window()
        self.assert_url_contains("apple.com")
        self.close_current_window()
        self.switch_to_parent_window()

        # Проверка Google Play
        self.hard_click(L.GOOGLEPLAY)
        self.switch_to_new_window()
        self.assert_url_contains("play.google.com")
        self.close_current_window()
        self.switch_to_parent_window()

    @allure.step("Проверить все основные навигационные ссылки футера")
    def check_footer_navigation_links(self):
        self.accept_cookie_consent()
        mapping = [
            (L.NAV_COMPANIES, L.COMPANIES_URL, L.TEXT_COMPANIES_H1),
            (L.NAV_PARTNERS, L.PARTNERS_URL, L.TEXT_PARTNERS_H1),
            (L.NAV_FACILITIES, L.FACILITIES_URL, L.TEXT_FACILITIES),
            (L.NAV_LEVELS, L.LEVELS_URL, L.TEXT_LEVELS),
            (L.NAV_CONTACTS, L.CONTACTS_URL, L.TEXT_CONTACTS),
        ]
        for locator, url, expected_text in mapping:
            self.scroll_to_element(locator)
            self.hard_click(locator)
            self.assert_url_matches(url)
            self.assert_text_on_page(expected_text)
            self.driver.back()
            self.accept_cookie_consent()

    @allure.step("Проверить копирайт и регистрационный номер поставщика услуг")
    def check_copyright_and_provider(self):
        self.accept_cookie_consent()
        self.scroll_down()
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
        self.assert_text_on_page("Раскрытие информации (включая правила оказания платежной услуги)")

        # Закрываем вкладку, если она новая
        if len(new_handles) > len(current_handles):
            self.close_current_window()
            self.switch_to_parent_window()

        # Проверка языка и JS
        self.check_for_words("russian")
        errors = self.get_js_console_errors()

        filtered = []
        for e in errors:
            msg = e.get("message", "").lower()
            source = e.get("source", "").lower()

            # Игнорируем стандартные CSP/Sentry ошибки Allsports
            if "sentry" in msg:
                continue
            if "content security policy" in msg:
                continue
            if source in ("security", "network"):
                continue

            filtered.append(e)

        assert len(filtered) == 0, f"JS ошибки: {filtered}"

    @allure.step("Проверить документы для юридических лиц")
    def check_legal_documents(self):
        self.accept_cookie_consent()
        urls = [
            (L.POLICY_PD, L.TEXT_DOC_PD),
            (L.LICENSE_INTERMEDIARY, L.TEXT_DOC_INTERMEDIARY),
        ]
        for url, text in urls:
            self.driver.get(url)
            self.accept_cookie_consent()
            self.assert_url_matches(url)
            self.assert_text_on_page(text)
            self.check_for_words("russian")
            errors = self.get_js_console_errors()

            filtered = []
            for e in errors:
                msg = e.get("message", "").lower()
                source = e.get("source", "").lower()

                # Игнорируем мусорные ошибки, которые всегда есть на страницах документов
                if "sentry" in msg:
                    continue
                if "content security policy" in msg:
                    continue
                if "csp" in msg:
                    continue
                if source in ("security", "network"):
                    continue

                filtered.append(e)

            assert len(filtered) == 0, f"JS ошибки (реальные!) на странице {url}: {filtered}"

    @allure.step("Проверить пользовательские соглашения и политики")
    def check_user_agreements(self):
        self.accept_cookie_consent()
        urls = [
            (L.USER_AGREEMENTS, L.TEXT_INDIVIDUAL_AGR),
            (L.INDIVIDUAL_LICENSE, L.TEXT_INDIVIDUAL_AGR),
            (L.POLICY_PD, L.TEXT_DOC_PD),
            (L.RULE_ACCESS, L.TEXT_RULE_ACCESS),
            (L.COOKIE_POLICY, L.TEXT_COOKIE_POLICY),
        ]
        for url, expected_text in urls:
            self.driver.get(url)
            self.accept_cookie_consent()
            self.assert_url_matches(url)
            self.assert_text_on_page(expected_text)
            self.check_for_words("russian")
            assert len(self.get_js_console_errors()) == 0, f"JS ошибки на {url}"

    @allure.step("Проверить целостность футера (все элементы присутствуют)")
    def check_footer_integrity(self):
        self.accept_cookie_consent()
        self.scroll_down()
        self.check_footer_contacts()
        self.check_social_links()
        self.check_app_store_links()
        self.check_footer_navigation_links()
        self.check_copyright_and_provider()
        self.check_legal_documents()
        self.check_user_agreements()

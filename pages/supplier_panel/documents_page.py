import allure

from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
from locators.supplier_panel.for_documents_page_locators import DocumentsPageLocators
from selenium.webdriver.support.ui import Select


class SupplierPanelDocuments(LoginPageSupplierPanel, DocumentsPageLocators, BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Open supplier panel login page")
    def open_sp(self):
        self.driver.get("https://xn--80ann.xn--k1aahcehedi.xn--90ais/login")

    @allure.step("Open documents tab")
    def click_documents(self):
        if self.is_element_visible(self.DOCUMENTS_TAB_RU):
            self.hard_click(self.DOCUMENTS_TAB_RU)
            return
        self.hard_click(self.DOCUMENTS_TAB_EN)

    @allure.step("Select language")
    def select_language(self, language="English (en)"):
        dropdown = self.find_element("//select[@class='language-switcher_list']")
        Select(dropdown).select_by_visible_text(language)

    @allure.step("Assert documents tab visibility")
    def assert_documents_tab_visible(self):
        assert self.is_element_visible(self.DOCUMENTS_TAB_RU) or self.is_element_visible(self.DOCUMENTS_TAB_EN), (
            "Вкладка Documents не отображается в сайдбаре"
        )

    @allure.step("Assert documents tab not visible")
    def assert_documents_tab_not_visible(self):
        assert not self.is_element_visible(self.DOCUMENTS_TAB_RU) and not self.is_element_visible(self.DOCUMENTS_TAB_EN), (
            "Вкладка Documents отображается, хотя не должна для данной роли"
        )

    @allure.step("Assert documents page elements in Russian")
    def assert_documents_page_ru(self):
        self.wait_for_visible(self.HEADER_RU)
        self.wait_for_visible(self.DATE_LABEL_RU)
        self.wait_for_visible(self.DATE_INPUT)
        self.wait_for_visible(self.FOR_ALL_TIME_BUTTON_RU)

    @allure.step("Assert documents page elements in English")
    def assert_documents_page_en(self):
        self.wait_for_visible(self.HEADER_EN)
        self.wait_for_visible(self.DATE_LABEL_EN)
        self.wait_for_visible(self.DATE_INPUT)
        self.wait_for_visible(self.FOR_ALL_TIME_BUTTON_EN)

    @allure.step("Assert documents table headers in Russian")
    def assert_documents_headers_ru(self):
        self.wait_for_visible(self.TABLE_HEADER_NUMBER)
        self.wait_for_visible(self.TABLE_HEADER_SUPPLIER_RU)
        self.wait_for_visible(self.TABLE_HEADER_NAME_RU)
        self.wait_for_visible(self.TABLE_HEADER_FROM_RU)
        self.wait_for_visible(self.TABLE_HEADER_TILL_RU)
        self.wait_for_visible(self.TABLE_HEADER_CREATED_RU)

    @allure.step("Assert documents table headers in English")
    def assert_documents_headers_en(self):
        self.wait_for_visible(self.TABLE_HEADER_NUMBER)
        self.wait_for_visible(self.TABLE_HEADER_SUPPLIER_EN)
        self.wait_for_visible(self.TABLE_HEADER_NAME_EN)
        self.wait_for_visible(self.TABLE_HEADER_FROM_EN)
        self.wait_for_visible(self.TABLE_HEADER_TILL_EN)
        self.wait_for_visible(self.TABLE_HEADER_CREATED_EN)

    @allure.step("Assert documents table has data")
    def assert_documents_table_has_rows(self):
        rows = self.find_elements(self.TABLE_ROWS)
        assert len(rows) > 0, "Таблица документов пустая"

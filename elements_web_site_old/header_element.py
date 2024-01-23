import allure

from helpers import BasePage
from locators.web_site_old.for_header_testing import HeaderLocators


class HeaderElement(BasePage, HeaderLocators):

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get('https://www.allsports.fit/by/')

    @allure.step("Open the web page")
    def open(self):
        self.driver.get('https://www.allsports.fit/by/')

    @allure.step("Click on 'Objects' button")
    def click_on_button_objects(self):
        self.click_on(self.OBJECT_LOCATOR)

    @allure.step("Click on 'Subscription Types' button")
    def click_on_button_subscription_types(self):
        self.click_on(self.SUBSCRIPTION_TYPES)

    @allure.step("Click on 'Become a Partner' button")
    def click_on_button_become_partner(self):
        self.click_on(self.BECOME_PARTNER)

    @allure.step("Click on 'Contacts' button")
    def click_on_button_contacts(self):
        self.click_on(self.CONTACTS)

    @allure.step("Click on 'Locale Dropdown' button")
    def click_on_button_locale_dropdown(self):
        self.click_on(self.LOCALE_DROPDOWN_SELECTION)

    @allure.step("Click on 'BY' locale link")
    def click_on_BY(self):
        self.click_on(self.BY_LOCALE)

    @allure.step("Click on 'AM' locale link")
    def click_on_AM(self):
        self.click_on(self.AM_LOCALE)

    @allure.step("Click on 'AM EN' locale link")
    def click_on_AM_EN(self):
        self.click_on(self.AM_EN_LOCALE)

    @allure.step("Click on 'RU' locale link")
    def click_on_RU(self):
        self.click_on(self.RU_LOCALE)

    @allure.step("Click on 'Select City Dropdown' button")
    def click_on_select_city_dropdown(self):
        self.click_on(self.CITY_LOCATOR)

    @allure.step("Assert current 'Object' page")
    def assert_current_object_page(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_OBJECT_PAGE)

    @allure.step("Assert current 'Subscription types' page")
    def assert_current_subscription_types_page(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_SUBSCRIPTION_TYPES_PAGE)

    @allure.step("Assert current become a partner page")
    def assert_current_become_partner_page(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_BECOME_PARTNER_PAGE)

    @allure.step("Assert current 'Contacts' page")
    def assert_current_contacts_page(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_CONTACTS_PAGE)

    @allure.step("Assert city by 'AM locale' visibility")
    def assert_city_by_locale_AM_visible(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_AM_LOCALE)

    @allure.step("Assert city by 'BY locale' visibility")
    def assert_city_by_locale_BY_visible(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_BY_LOCALE)

    @allure.step("Assert city by 'AM EN locale' visibility")
    def assert_city_by_locale_AM_EN_visible(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_AM_EN_LOCALE)

    @allure.step("Assert city by 'RU locale' visibility")
    def assert_city_by_locale_RU_visible(self):
        self.assert_text_on_page(self.FOUND_TEXT_ON_RU_LOCALE)

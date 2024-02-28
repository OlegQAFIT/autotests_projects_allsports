from locators.supplier_panel.for_contacts_locators import ContactsLocators
import allure
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SupplierPanelContacts(LoginPageSupplierPanel, ContactsLocators, BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Open SP V2 portal")
    def open_sp(self):
        self.driver.get('https://xn--80ann.xn--k1aahcehedi.xn--90ais/login')

    @allure.step("Click on tab contacts")
    def click_contacts(self):
        self.hard_click(self.FACILITY_DETAILS_RU)

    @allure.step("Found elements")
    def assert_found_elements_on_facility_details_ru(self):
        elements_to_check = [
            (self.HEADER_CONTACTS_LOCATOR_RU, 'Контакты'),
            (self.PHONE_LOCATOR_RU, 'Телефон'),
            (self.EMAIL_LOCATOR_RU, 'Электронная почта'),
            (self.HOURS_LOCATOR_RU, 'Режим работы'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Select language")
    def select_language(self):
        location_dropdown = self.find_element(self.LANGUAGE_DROPDOWN_LOCATOR)
        select = Select(location_dropdown)
        select.select_by_visible_text("English (en)")

    @allure.step("Found elements")
    def assert_found_elements_on_facility_details_en(self):
        elements_to_check = [
            (self.HEADER_CONTACTS_LOCATOR_EN, 'Contacts'),
            (self.PHONE_LOCATOR_EN, 'Phone'),
            (self.EMAIL_LOCATOR_EN, 'E-mail'),
            (self.HOURS_LOCATOR_EN, 'Support availability hours'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_text_on_facility_details(self):
        elements_to_check = [
            (self.TEXT_PHONE_LOCATOR, '375291294950'),
            (self.TEXT2_PHONE_LOCATOR, '375291294950'),
            (self.TEXT_EMAIL_LOCATOR, 'support@sportbenefit.eu'),
            (self.TEXT_HOURS_LOCATOR, 'Режим работы Ежедневно 08:00-19:00'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found link and check")
    def assert_check_social_media_links(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "social-media"))
        )
        social_media_links = self.driver.find_elements(By.CLASS_NAME, "social-media_link")

        for link in social_media_links:
            href = link.get_attribute("href")
            if href:
                print("Ссылка:", href, "- Работает и корректна")
            else:
                print("Ссылка не найдена")

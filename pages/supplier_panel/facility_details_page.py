from locators.supplier_panel.for_facility_details_locators import FacilityDetailsLocators
import allure
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class SupplierPanelFacilityDetails(LoginPageSupplierPanel, FacilityDetailsLocators, BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Open Journal")
    def open_jn(self):
        self.driver.get('https://xn--d1aey.xn--k1aahcehedi.xn--90ais/login')
        time.sleep(5)

    @allure.step("Open SP V2 portal")
    def open_sp(self):
        self.driver.get('https://xn--80ann.xn--k1aahcehedi.xn--90ais/login')

    @allure.step("Click on tab facility details")
    def click_facility_details(self):
        self.hard_click(self.FACILITY_DETAILS_RU)

    @allure.step("Click on button change data")
    def click_change_button(self):
        self.hard_click(self.BUTTON_CHANGE_DATA_LOCATOR_EN)

    @allure.step("Click on button change data")
    def click_change_button_ru(self):
        self.hard_click(self.BUTTON_CHANGE_DATA_LOCATOR_RU)

    @allure.step("Found elements")
    def assert_found_elements_on_facility_details_ru(self):
        elements_to_check = [
            (self.HEADER_FACILITY_DETAILS_LOCATOR_RU, 'Описание обьекта'),
            (self.FACILITY_NAME_LOCATOR_RU, 'Название объекта:'),
            (self.DESCRIPTION_LOCATOR_RU, 'Описание:'),
            (self.VISITING_RULES_LOCATOR_RU, 'Правила посещения:'),
            (self.ADDRESS_LOCATOR_RU, 'Адрес:'),
            (self.CONTACT_PHONE_LOCATOR_RU, 'Контактный телефон:'),
            (self.WEBSITE_LOCATOR_RU, 'Веб-сайт:'),
            (self.WORKING_HOURS_LOCATOR_RU, 'Режим работы:'),
            (self.KINDS_OF_SERVICE_LOCATOR_RU, 'Виды услуг:'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_on_facility_details_en(self):
        elements_to_check = [
            (self.HEADER_FACILITY_DETAILS_LOCATOR_EN, 'Facility details'),
            (self.FACILITY_NAME_LOCATOR_EN, 'Facility name:'),
            (self.DESCRIPTION_LOCATOR_EN, 'Description:'),
            (self.VISITING_RULES_LOCATOR_EN, 'Visiting rules:'),
            (self.ADDRESS_LOCATOR_EN, 'Address:'),
            (self.CONTACT_PHONE_LOCATOR_EN, 'Contact phone:'),
            (self.WEBSITE_LOCATOR_EN, 'Website:'),
            (self.WORKING_HOURS_LOCATOR_EN, 'Working hours:'),
            (self.KINDS_OF_SERVICE_LOCATOR_EN, 'Kinds of service:'),
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
    def assert_found_text_on_facility_details(self):
        elements_to_check = [
            (self.TEXT_FACILITY_NAME_LOCATOR, 'Gym1'),
            (self.TEXT_ADDRESS_LOCATOR, 'есенина 73'),
            (self.TEXT_CONTACT_PHONE_LOCATOR, '+375000000000;+375123456789'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_button_on_facility_details_ru(self):
        elements_to_check = [
            (self.BUTTON_REFRESH_INFO_LOCATOR_RU, 'Обновить информацию'),
            (self.BUTTON_CHANGE_DATA_LOCATOR_RU, 'Изменить данные'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_button_on_facility_details_en(self):
        elements_to_check = [
            (self.BUTTON_REFRESH_INFO_LOCATOR_EN, 'Refresh info'),
            (self.BUTTON_CHANGE_DATA_LOCATOR_EN, 'Change data'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert clickable button")
    def assert_clickable_button(self):
        # Пример использования метода is_button_clickable
        if self.is_button_clickable(self.BUTTON_REFRESH_INFO_LOCATOR_RU):
            print("Кнопка 'Обновить информацию' кликабельна")
        else:
            print("Кнопка 'Обновить информацию' не кликабельна")

        if self.is_button_clickable(self.BUTTON_CHANGE_DATA_LOCATOR_RU):
            print("Кнопка 'Изменить данные' кликабельна")
        else:
            print("Кнопка 'Изменить данные' не кликабельна")

    @allure.step("Found elements")
    def assert_found_elements_modal_on_facility_details_en(self):
        elements_to_check = [
            (self.CHANGE_DATA_LOCATOR_EN, 'Change data'),
            (self.TEXT_INFO_LOCATOR_EN, 'In order to change the data you need to contact technical support:'),
            (self.PHONE_NUMBER_LOCATOR, '375291294950'),
            (self.EMAIL_LOCATOR, 'support@sportbenefit.eu'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_modal_on_facility_details_ru(self):
        elements_to_check = [
            (self.CHANGE_DATA_LOCATOR_RU, 'Изменить данные'),
            (self.TEXT_INFO_LOCATOR_RU, 'Для того, чтобы изменить данные вам необходимо связаться с тех. поддержкой:'),
            (self.PHONE_NUMBER_LOCATOR, '375291294950'),
            (self.EMAIL_LOCATOR, 'support@sportbenefit.eu'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

import string
import random

import allure
from faker import Faker
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from helpers import BasePage
from helpers.authorization import LoginPage
from locators.journal.for_company_page_locators import CompanyPageLocators
from selenium.webdriver.support.ui import Select
import time


class Company(LoginPage, CompanyPageLocators, BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.faker = Faker()
        self.created_company_name = None
        self.company_input_value = None

    @allure.step("Open HR portal")
    def open_hr(self):
        self.driver.get('https://xn--e1affem4a.xn--k1aahcehedi.xn--90ais/login')

    @allure.step("Open Journal")
    def open_jn(self):
        self.driver.get('https://xn--d1aey.xn--k1aahcehedi.xn--90ais/login')

    @allure.step("Open SP")
    def open_sp(self):
        self.driver.get('https://xn--80akdrtu.xn--k1aahcehedi.xn--90ais/registration/bepaid')

    @allure.step("Click and open Company tab")
    def click_and_open_company_tab(self):
        self.hard_click(self.FOOTER_COMPANY)

    @allure.step("Click delete Company ")
    def click_delete_company(self):
        self.hard_click(self.BUTTON_DELETE)

    @allure.step("Click open portal user ")
    def click_open_portal_user(self):
        self.hard_click(self.BUTTON_PORTAL_USER)

    @allure.step("Click add portal user modal ")
    def click_add_portal_user(self):
        self.hard_click(self.BUTTON_ADD_LOCATOR)

    @allure.step("")
    def click_save_portal_user(self):
        self.hard_click(self.MODAL_BUTTON_ADD_LOCATOR)

    @allure.step("Click Create Company tab")
    def click_create_company_tab(self):
        self.hard_click(self.CREATE_COMPANY)

    @allure.step("Drop City selection")
    def drop_city_selection(self):
        location_dropdown = self.find_element(self.LOCATION_DROP_DOWN)
        location_dropdown.click()
        minsk_option = self.find_element(self.MINSK_VALUE)
        minsk_option.click()

    @allure.step("Drop Locale selection")
    def drop_locale_selection(self):
        locale_dropdown = self.driver.find_element(By.XPATH, self.LOCALE_DROP_DOWN)
        locale_dropdown.click()
        ru_option = self.driver.find_element(By.XPATH, self.RU_VALUE)
        ru_option.click()

    @allure.step("Drop Timezone selection")
    def drop_timezone_selection(self):
        self.hard_click(self.TIMEZONE_DROP_DOWN)
        self.hard_click(self.MINSK_VALUE_TIMEZONE)

    @allure.step("Drop Sell Strategy selection")
    def drop_sell_strategy_selection(self):
        self.hard_click(self.SELL_STRATEGY_DROP_DOWN)
        self.hard_click(self.BY3_VALUE)

    @allure.step("Drop Registration Type selection")
    def drop_registration_type_selection(self):
        self.hard_click(self.REGISTRATION_TYPE_STANDARD)
        self.hard_click(self.REGISTRATION_TYPE_FORM)

    # @allure.step("Drop Registration Type dropdown")
    # def drop_registration_type_dropdown(self):
    #     registration_type_dropdown = self.find_element(self.dropdown)
    #     select = Select(registration_type_dropdown)
    #     select.select_by_visible_text("REGISTRATION_FORM")

    @allure.step("Drop Manager selection")
    def drop_manager_selection(self):
        self.hard_click(self.MANAGER_DROP_DOWN)
        self.hard_click(self.MANAGER_VALUE)

    @allure.step("Drop MANAGER")
    def drop_manager_selection_for_select(self):
        self.hard_click(self.MANAGER_SELECT)
        self.hard_click(self.MANAGER_VALUE)


    @allure.step("Fill fields with random values")
    def fill_fields(self):
        custom_name = self.faker.word()
        self.created_company_name = f"AT Company {custom_name}"
        self.company_input_value = self.created_company_name

        self.fill(CompanyPageLocators.COMPANY_INPUT, self.company_input_value)
        self.fill(CompanyPageLocators.VAT_NUMBER_INPUT, self.VAT_NUMBER_TEXT)
        self.fill(CompanyPageLocators.LEGAL_NAME_INPUT, self.company_input_value)
        self.fill(CompanyPageLocators.LEGAL_ADDRESS_INPUT, self.LEGAL_ADDRESS_TEXT)
        self.fill(CompanyPageLocators.CONTACT_PHONE_INPUT, self.CONTACT_PHONE_TEXT)

    @allure.step("Fill fields with max company name")
    def fill_fields_name_company(self):
        self.fill(CompanyPageLocators.COMPANY_INPUT, self.MAX_COMPANY_NAME_TEXT)
        self.fill(CompanyPageLocators.LEGAL_NAME_INPUT, self.MAX_COMPANY_NAME_TEXT)
        self.fill(CompanyPageLocators.VAT_NUMBER_INPUT, self.VAT_NUMBER_TEXT)
        self.fill(CompanyPageLocators.LEGAL_ADDRESS_INPUT, self.LEGAL_ADDRESS_TEXT)
        self.fill(CompanyPageLocators.CONTACT_PHONE_INPUT, self.CONTACT_PHONE_TEXT)

    @allure.step("Fill fields with max company name")
    def fill_fields_name_min_company(self):
        self.fill(CompanyPageLocators.COMPANY_INPUT, self.MIN_COMPANY_NAME_TEXT)
        self.fill(CompanyPageLocators.LEGAL_NAME_INPUT, self.MIN_COMPANY_NAME_TEXT)
        self.fill(CompanyPageLocators.VAT_NUMBER_INPUT, self.VAT_NUMBER_TEXT_MIN)
        self.fill(CompanyPageLocators.LEGAL_ADDRESS_INPUT, self.LEGAL_ADDRESS_TEXT)
        self.fill(CompanyPageLocators.CONTACT_PHONE_INPUT, self.CONTACT_PHONE_TEXT)

    @allure.step("fill fields UNN min")
    def fill_fields_UNN_min(self):
        self.fill(CompanyPageLocators.COMPANY_INPUT, self.company_input_value)
        self.fill(CompanyPageLocators.LEGAL_NAME_INPUT, self.company_input_value)
        self.fill(CompanyPageLocators.VAT_NUMBER_INPUT, self.VAT_NUMBER_TEXT)
        self.fill(CompanyPageLocators.LEGAL_ADDRESS_INPUT, self.LEGAL_ADDRESS_TEXT)
        self.fill(CompanyPageLocators.CONTACT_PHONE_INPUT, self.CONTACT_PHONE_TEXT)

    @allure.step("Fill fields without legal name")
    def fill_fields_legal_name(self):
        custom_name = self.faker.word()
        self.created_company_name = f"AT Company {custom_name}"
        self.company_input_value = self.created_company_name

        self.fill(CompanyPageLocators.COMPANY_INPUT, self.company_input_value)
        self.fill(CompanyPageLocators.VAT_NUMBER_INPUT, self.VAT_NUMBER_TEXT)
        self.fill(CompanyPageLocators.LEGAL_ADDRESS_INPUT, self.LEGAL_ADDRESS_TEXT)
        self.fill(CompanyPageLocators.CONTACT_PHONE_INPUT, self.CONTACT_PHONE_TEXT)

    @allure.step("Fill fields without VAT number")
    def fill_fields_vat_number(self):
        custom_name = self.faker.word()
        self.created_company_name = f"AT Company {custom_name}"
        self.company_input_value = self.created_company_name

        self.fill(CompanyPageLocators.COMPANY_INPUT, self.company_input_value)
        self.fill(CompanyPageLocators.VAT_NUMBER_INPUT, self.VAT_NUMBER_TEXT)
        self.fill(CompanyPageLocators.LEGAL_ADDRESS_INPUT, self.LEGAL_ADDRESS_TEXT)
        self.fill(CompanyPageLocators.CONTACT_PHONE_INPUT, self.CONTACT_PHONE_TEXT)

    @allure.step("")
    def search_field_company(self):
        self.fill(CompanyPageLocators.SEARCH_FIELDS, self.SEARCH_COMPANY)

    @allure.step("Click save company button")
    def click_save_company(self):
        self.hard_click(self.SAVE_AND_CONTINUE_BUTTON)
        time.sleep(5)

    @allure.step("Assert find new company")
    def assert_find_new_company(self):
        time.sleep(5)
        assert self.search_text_on_page(
            self.company_input_value), f"Текст '{self.company_input_value}' не найден на странице"

    @allure.step("Assert found elements on add company page")
    def assert_found_elements_on_add_company_page(self):
        elements_to_check = [
            (self.ADD_COMPANY, 'Add company'),
            (self.HR_SETTINGS, 'HR SETTINGS'),
            (self.DATA_FOR_THE_CONTRACT, 'DATA FOR THE CONTRACT'),
            (self.BENEFIARY, 'BENEFIARY'),
            (self.OPTIONAL, 'OPTIONAL')
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found error text")
    def assert_found_errore_text(self):
        elements_to_check = [
            (self.ERRORE_TEXT, 'Количество символов в поле Имя не может превышать 191.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("found errore min text")
    def assert_found_errore_min_text(self):
        elements_to_check = [
            (self.ERRORE_TEXT_MIN, 'Количество символов в поле Имя должно быть не менее 4.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("found errore UNN min text")
    def assert_found_errore_UNN_min_text(self):
        elements_to_check = [
            (self.ERRORE_TEXT_MIN_UNN, 'НДС должен содержать только цифры и состоять из девяти символов'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found error text for legal name")
    def assert_found_errore_text_legal_name(self):
        elements_to_check = [
            (self.ERRORE_TEXT_LEGAL_NAME, 'Такое значение поля legal name уже существует.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found text after searching VAT number")
    def assert_found_text_after_searching_vat_number(self):
        elements_to_check = [
            (self.ERRORE_TEXT_legal_name, 'Такое значение поля legal name уже существует.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert required fields")
    def assert_required_fields(self):
        elements_to_check = [
            (self.Locale_required_fields, 'Обязательное поле'),
            (self.Timezone_required_fields, 'Обязательное поле'),
            (self.Sell_Strategy_required_fields, 'Обязательное поле'),
            (self.Company_Name_required_fields, 'Обязательное поле'),
            (self.VAT_NUMBER_required_fields, 'Обязательное поле'),
            (self.Legal_Name_required_fields, 'Обязательное поле'),
            (self.Legal_Address_required_fields, 'Обязательное поле'),
            (self.Contact_Phone_required_fields, 'Обязательное поле')
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert disabled elements")
    def assert_disable_elements(self):
        locators = ("compensation_amount", "DATE", "MIN_ORDER_ITEMS_INPUT")

        for locator in locators:
            input_element = self.driver.find_element(By.XPATH, getattr(CompanyPageLocators, locator))

            is_disabled = input_element.get_attribute('disabled')

            assert is_disabled is not None and is_disabled.lower() == 'true', f"Поле {locator} не задизэйблено"

    @allure.step("Assert disabled elements with select registration type")
    def assert_disable_elements_with_select_registration_type(self):
        compensation_amount_input = self.driver.find_element(By.XPATH, self.compensation_amount)
        date_input = self.driver.find_element(By.XPATH, self.DATE)
        min_order_items_input = self.driver.find_element(By.XPATH, self.MIN_ORDER_ITEMS_INPUT)

        assert not compensation_amount_input.is_enabled(), "Поле 'Compensation Amount' не задизейблено"
        assert not date_input.is_enabled(), "Поле 'Date' не задизейблено"
        assert not min_order_items_input.is_enabled(), "Поле 'Min Order Items' не задизейблено"

    @allure.step("Assert disabled elements in new company")
    def assert_disable_elements_in_new_company(self):
        id_amount_input = self.driver.find_element(By.XPATH, self.ID)
        compensation_amount_input = self.driver.find_element(By.XPATH, self.compensation_amount)
        date_input = self.driver.find_element(By.XPATH, self.DATE)
        min_order_items_input = self.driver.find_element(By.XPATH, self.MIN_ORDER_ITEMS_INPUT)

        assert not id_amount_input.is_enabled(), "Поле 'ID' не задизейблено"
        assert not compensation_amount_input.is_enabled(), "Поле 'Compensation Amount' не задизейблено"
        assert not date_input.is_enabled(), "Поле 'Date' не задизейблено"
        assert not min_order_items_input.is_enabled(), "Поле 'Min Order Items' не задизейблено"

    @allure.step("open last dropdown and edit")
    def open_last_dropdown_and_edit(self):
        dropdown_buttons = self.find_elements("//button[@data-v-d162a11e='']/*[name()='svg']/*[name()='circle'][3]")

        if dropdown_buttons:
            last_dropdown_button = dropdown_buttons[-1]
            last_dropdown_button.click()

            edit_buttons = self.find_elements("//a[contains(text(), 'Редактировать')]")

            if edit_buttons:
                edit_buttons[-1].click()
            else:
                print("Кнопок 'Редактировать' не найдено.")
        else:
            print("Кнопок дропдауна не найдено.")

    @allure.step("open and found new company")
    def assert_open_and_found_new_company(self):
        elements_to_check = [
            (self.EDIT_COMPANY, 'Edit company'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert find company with select manager")
    def assert_find_company_with_manager(self):
        elements_to_check = [
            (self.COMPANY_WITH_SELECT_MANAGER, 'cascsa'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert find company ")
    def assert_find_company_search_field(self):
        elements_to_check = [
            (self.FOUND_COMPANY, 'CompanyA'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("delete last company ")
    def delete_last_company(self):
        dropdown_buttons = self.find_elements("//button[@data-v-d162a11e='']/*[name()='svg']/*[name()='circle'][3]")

        if dropdown_buttons:
            last_dropdown_button = dropdown_buttons[-1]
            last_dropdown_button.click()

            edit_buttons = self.find_elements("//a[contains(text(), ' Удалить ')]")

            if edit_buttons:
                edit_buttons[-1].click()
            else:
                print("Кнопок 'Редактировать' не найдено.")
        else:
            print("Кнопок дропдауна не найдено.")

    @allure.step("Assert company not found")
    def assert_company_not_found(self):
        time.sleep(5)
        assert not self.search_text_on_page(
            self.company_input_value), f"Текст '{self.company_input_value}' найден на странице"

    @allure.step("")
    def open_page_add_portal_user(self):
        dropdown_buttons = self.find_elements("//button[@data-v-d162a11e='']/*[name()='svg']/*[name()='circle'][3]")

        if dropdown_buttons:
            last_dropdown_button = dropdown_buttons[-1]
            last_dropdown_button.click()

            portal_user_buttons = self.find_elements("//a[contains(text(), 'Portal Users')]")

            if portal_user_buttons:
                portal_user_buttons[-1].click()
            else:
                print("Кнопок 'Редактировать' не найдено.")
        else:
            print("Кнопок дропдауна не найдено.")

    @allure.step("Assert elements on page portal user")
    def assert_page_portal_user(self):
        elements_to_check = [
            (self.HEADLINE_HR_EMPLOYEES, 'HR сотрудники'),
            (self.PHONE_LOCATOR, 'Телефон'),
            (self.NAME_LOCATOR, 'Имя'),
            (self.POSITION_LOCATOR, 'Позиция'),
            (self.EMAIL_LOCATOR, 'Почта'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert elements on modal window portal user")
    def assert_page_modal_portal_user(self):
        elements_to_check = [
            (self.MODAL_PHONE_LOCATOR, 'Телефон:'),
            (self.MODAL_NAME_LOCATOR, 'Имя'),
            (self.MODAL_POSITION_LOCATOR, 'Позиция'),
            (self.MODAL_EMAIL_LOCATOR, 'Почта'),
            (self.MODAL_LOCAL_LOCATOR, 'Локаль'),
            (self.MODAL_TIMEZONE_LOCATOR, 'Часовой пояс'),
            (self.MODAL_BUTTON_CANCEL_LOCATOR, 'Отменить'),
            (self.MODAL_BUTTON_ADD_LOCATOR, 'Добавить'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert clickable cancel buttom")
    def assert_clickable_cancel_button(self):
        cancel_button_locator = self.MODAL_BUTTON_CANCEL_LOCATOR
        cancel_button_element = self.find_element(cancel_button_locator)
        is_clickable = self.is_element_clickable(cancel_button_element)
        assert is_clickable, f"Cancel button is not clickable"

    @allure.step("Assert not clickable add buttom")
    def assert_not_clickabel_add_buttom(self):
        add_buttom_locator = self.MODAL_BUTTON_ADD_LOCATOR
        add_buttom_locator = self.find_element(add_buttom_locator)
        is_not_clickabel = self.is_element_not_clickable(add_buttom_locator)
        assert is_not_clickabel, f"Add button is clickable"

    @allure.step("")
    def generate_new_portal_user(self):
        remaining_digits = ''.join(random.choice(string.digits) for _ in range(7))
        self.phone_number = f"37544{remaining_digits}"
        self.generation_phone_number = self.phone_number

        time.sleep(2)
        self.fills(CompanyPageLocators.INPUT_MODAL_PHONE_LOCATOR, self.generation_phone_number)
        time.sleep(5)
        self.fills(CompanyPageLocators.INPUT_MODAL_NAME_LOCATOR, self.MODAL_NAME_TEXT)
        self.fills(CompanyPageLocators.INPUT_MODAL_POSITION_LOCATOR, self.MODAL_POSITION_TEXT)

        custom_email = self.faker.word()
        self.created_email = f"{custom_email}@gmail.com"
        self.email_input_value = self.created_email

        self.fill(CompanyPageLocators.INPUT_MODAL_EMAIL_LOCATOR, self.email_input_value)

        self.hard_click(self.DROP_MODAL_LOCAL_LOCATOR)
        self.hard_click(self.EN)

        self.hard_click(self.DROP_MODAL_TIMEZONE_LOCATOR)
        self.fills(CompanyPageLocators.INPUT_TIMEZONE, self.MODAL_TIMEZONE_TEXT)
        self.hard_click(self.SELECT_TIMEZONE_MINSK)

    @allure.step("")
    def assert_new_portal_user(self):
        assert self.search_text_on_page(
            self.generation_phone_number), f"Текст '{self.generation_phone_number}' не найден на странице"

    def add_new_portal_user_by_phone(self):
        self.fills(CompanyPageLocators.INPUT_MODAL_PHONE_LOCATOR, self.PORTAL_USER_PHONE)
        time.sleep(5)

    def add_new_portal_user_by_phone_1(self):
        self.fills(CompanyPageLocators.INPUT_MODAL_PHONE_LOCATOR, self.PORTAL_USER_PHONE)
        time.sleep(3)

    def add_new_portal_user_by_email(self):
        self.fills(CompanyPageLocators.INPUT_MODAL_EMAIL_LOCATOR, self.PORTAL_USER_EMAIL)
        time.sleep(3)

    def add_new_portal_user_by_cy(self):
        self.fills(CompanyPageLocators.INPUT_MODAL_PHONE_LOCATOR, self.PORTAL_USER_PHONE_BY_CY)
        time.sleep(3)

    @allure.step("")
    def assert_new_portal_user_by_phone(self):
        time.sleep(3)
        assert self.search_text_on_page(
            self.PORTAL_USER_PHONE), f"Текст '{self.PORTAL_USER_PHONE}' не найден на странице"

    @allure.step("")
    def add_wrong_email(self):
        self.fills(CompanyPageLocators.INPUT_MODAL_EMAIL_LOCATOR, self.WRONG_EMAIL_ERRORE)

    @allure.step("")
    def add_already_added_portal_user(self):
        self.fills(CompanyPageLocators.INPUT_MODAL_PHONE_LOCATOR, self.ADDED_PORTAL_USER_PHONE)

    @allure.step("Assert found error text")
    def assert_found_errore_text_added_portal_user(self):
        elements_to_check = [
            (self.WRONG_PORTAL_USER_ERRORE_LOCATOR, 'Формат данных неверен'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found error text")
    def assert_found_errore_text_portal_user(self):
        elements_to_check = [
            (self.WRONG_EMAIL_ERRORE_LOCATOR, 'Формат данных неверен'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("open last dropdown and edit")
    def open_sms_for_portal_user(self):
        dropdown_buttons = self.find_elements("/html/body/div/div/div[2]/div[3]/table/tbody/tr/td[5]/div/button")

        if dropdown_buttons:
            last_dropdown_button = dropdown_buttons[-1]
            last_dropdown_button.click()

            edit_buttons = self.find_elements("//a[contains(text(), ' SMS коды ')]")

            if edit_buttons:
                edit_buttons[-1].click()
            else:
                print("Кнопок ' SMS коды ' не найдено.")
        else:
            print("Кнопок дропдауна не найдено.")

    @allure.step("open last dropdown and edit")
    def open_edit_portal_user(self):
        dropdown_buttons = self.find_elements("/html/body/div/div/div[2]/div[3]/table/tbody/tr/td[5]/div/button")

        if dropdown_buttons:
            last_dropdown_button = dropdown_buttons[-1]
            last_dropdown_button.click()

            edit_buttons = self.find_elements("//a[contains(text(), ' Редактировать ')]")

            if edit_buttons:
                edit_buttons[-1].click()
            else:
                print("Кнопок ' SMS коды ' не найдено.")
        else:
            print("Кнопок дропдауна не найдено.")

    def change_portal_user(self):
        self.fill(CompanyPageLocators.INPUT_MODAL_NAME_LOCATOR, self.MODAL_NAME_TEXT_CHANGE)

    def assert_search_change_portal_user(self):
        self.find_elements("//td[text()='AQA OLEG CHANGE']")

    def assert_search_portal_user_by_cy(self):
        time.sleep(3)
        assert self.search_text_on_page(
            self.PORTAL_USER_PHONE_BY_CY), f"Текст '{self.PORTAL_USER_PHONE_BY_CY}' не найден на странице"

    def assert_and_extract_sms_code(create_portal_user):
        sms_code_locator = (By.XPATH, '//*[contains(text(), "Sms code:")]')
        sms_code_element = create_portal_user.find_element_portal(sms_code_locator)
        sms_code_text = sms_code_element.text
        sms_code = ''.join(filter(str.isdigit, sms_code_text))
        print("Extracted SMS Code:", sms_code)
        assert len(sms_code) == 4, "SMS Code should be 4 digits"

    @allure.step("open last dropdown and delete")
    def delete_for_portal_user(self):
        dropdown_buttons = self.find_elements("/html/body/div/div/div[2]/div[3]/table/tbody/tr/td[5]/div/button")

        if dropdown_buttons:
            last_dropdown_button = dropdown_buttons[-1]
            last_dropdown_button.click()

            edit_buttons = self.find_elements("//a[contains(text(), ' Удалить ')]")

            if edit_buttons:
                edit_buttons[-1].click()
            else:
                print("Кнопок ' SMS коды ' не найдено.")
        else:
            print("Кнопок дропдауна не найдено.")


    @allure.step("Search deleted portal user")
    def assert_deleted_portal_user(self):
        try:
            self.find_elements("//td[text()='AQA OLEG']")
        except NoSuchElementException:
            print("Portal user 'AQA OLEG' удален.")
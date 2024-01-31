import allure
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
from locators.supplier_panel.for_login_page_locators import LoginPageLocators
from selenium.webdriver.support.ui import Select


class SupplierPanel(LoginPageSupplierPanel, LoginPageLocators, BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Open SP V2 portal")
    def open_sp(self):
        self.driver.get('https://xn--80ann.xn--k1aahcehedi.xn--90ais/login')

    @allure.step("Assert found elements on login page in Russian")
    def assert_found_elements_on_login_page_ru(self):
        elements_to_check = [
            (self.LOG_IN, 'Войти'),
            (self.CONTACTS, 'Контакты'),
            (self.TEXT_LOGIN, 'Войти'),
            (self.SIGNIN_BUTTON_SUPPLER_PANEL, 'Продолжить'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found elements on login page in English")
    def assert_found_elements_on_login_page_en(self):
        elements_to_check = [
            (self.LOG_IN, 'Login'),
            (self.CONTACTS, 'Contacts'),
            (self.TEXT_LOGIN, 'Login'),
            (self.SIGNIN_BUTTON_SUPPLER_PANEL, 'Continue'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Select language")
    def select_language(self):
        location_dropdown = self.find_element(self.CHANGE_LANGUAGE_DROPDOWN)
        select = Select(location_dropdown)
        select.select_by_visible_text("English (en)")

    @allure.step("Login with wrong credentials")
    def login_wrong_user_supplier_panel(self):
        self.fill(self.LOGIN_FIELD_SUPPLER_PANEL, self.WRONG_LOGIN_TEXT_SUPPLER_PANEL)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)
        self.fill(self.PASSWORD_FIELD_SUPPLER_PANEL, self.WRONG_PASSWORD_TEXT_SUPPLER_PANEL)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)

    @allure.step("Assert found error text for wrong user in Russian")
    def assert_found_errore_text_wrong_user(self):
        elements_to_check = [
            (self.LOCATOR_TEXT_ERRORE_WRONG_EMAIL, 'Выбранное значение для email не найдено в списке.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found error text for wrong user in English")
    def assert_found_errore_text_wrong_user_en(self):
        elements_to_check = [
            (self.LOCATOR_TEXT_ERRORE_WRONG_USER, 'The selected email is invalid.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Login email field validation")
    def login_email_field_validation_supplier_panel(self):
        self.fill(self.LOGIN_FIELD_SUPPLER_PANEL, self.WRONG_TEXT_SUPPLER_PANEL)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)

    @allure.step("Assert found error text for email field validation in Russian")
    def assert_found_errore_text_email_field_validation(self):
        elements_to_check = [
            (self.LOCATOR_TEXT_ERRORE_WRONG_FORMAT, 'Проверьте правильность введенных данных.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found error text for email field validation in English")
    def assert_found_errore_text_email_field_validation_en(self):
        elements_to_check = [
            (self.LOCATOR_TEXT_ERRORE_WRONG_FORMAT_EN, 'Check that the entered data is correct.'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Login password field validation")
    def login_password_field_validation_supplier_panel(self):
        self.fill(self.LOGIN_FIELD_SUPPLER_PANEL, self.LOGIN_TEXT_SUPPLER_PANEL)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)
        self.fill(self.PASSWORD_FIELD_SUPPLER_PANEL, self.WRONG_PASSWORD_FORMAT_TEXT_SUPPLER_PANEL)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)

    @allure.step("Assert found error text for password field validation in Russian")
    def assert_found_errore_text_pasword_field_validation(self):
        elements_to_check = [
            (self.LOCATOR_TEXT_ERRORE_WRONG_PASSWORD, 'Неверный пароль'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert found error text for password field validation in English")
    def assert_found_errore_text_pasword_field_validation_en(self):
        elements_to_check = [
            (self.LOCATOR_TEXT_ERRORE_WRONG_PASSWORD_EN, 'Invalid password'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

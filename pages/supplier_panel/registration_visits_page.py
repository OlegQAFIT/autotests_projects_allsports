import allure
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
from locators.supplier_panel.for_registration_of_visits_pade_locators import RegistrationVisitsLocators
from helpers.add_visit import login_and_create_visit as external_login_and_create_visit

import time
from selenium.webdriver.support.ui import Select


class SupplierPanelRegistrationVisits(LoginPageSupplierPanel, RegistrationVisitsLocators, BasePage):

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

    @allure.step("reset user")
    def open_user_card(self):
        self.driver.get('https://xn--d1aey.xn--k1aahcehedi.xn--90ais/helpdesk/mobile/holder/41232')
        time.sleep(5)

    @allure.step("Steps to click reset activations")
    def steps_to_click_reset_activations(self):
        self.hard_click(self.HELPDESK_MOBILE_LOCATOR)
        self.hard_click(self.HOLDER_BUTTON)
        self.fill(self.SEARCH_INPUT, self.PHONE)
        time.sleep(5)
        self.hard_click(self.HOLDER_USER)
        self.hard_click(self.RESET_BUTTON)

    @allure.step("Login and create visit")
    def login_and_create_visit(self, phone_number="+375000000088", sms_code="5566",
                               gym_token="https://holder.allsports.by/s/3b8b", attraction_id=14225):
        external_login_and_create_visit(phone_number, sms_code, gym_token, attraction_id)

    @allure.step("Login in SP V2")
    def login(self):
        self.fill(self.LOGIN_FIELD, self.LOGIN_TEXT)
        self.fill(self.PASSWORD_FIELD, self.PASSWORD_TEXT)
        self.hard_click(self.SIGNIN_BUTTON)

    @allure.step("Found elements")
    def assert_found_elements_on_registrarion_visitspage_ru(self):
        elements_to_check = [
            (self.LOGO_REGISTRATION_VISITS_LOCATOR, 'Регистрация визитов'),
            (self.TEXT_ADMINISTRATOR_LOCATOR, 'Администратор'),
            (self.SHORT_INSTRUCTION_LOCATOR, 'Краткая инструкция:'),
            (self.FIRST_INSTRUCTION_LOCATOR, 'Нажмите кнопку “Новые визиты”.'),
            (self.SECOND_INSTRUCTION_LOCATOR, 'Для подтверждения посещения нажмите кнопку “Принять”.'),
            (self.THIRD_INSTRUCTION_LOCATOR,
             'Ответьте на вопрос о схожести посетителя с фото (Ответ не влияет на подтверждение визита).'),
            (self.BUTTON_NEW_VISITS_LOCATOR, 'Новые визиты'),
            (self.SIDEBAR_VISITS_HISTORY_LOCATOR, 'Регистрация визитов'),
            (self.SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR, 'История визитов'),
            (self.SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR, 'Визиты на исправлении'),
            (self.SIDEBAR_FACILITY_DETAILS_LOCATOR, 'Описание обьекта'),
            (self.SIDEBAR_CONTACTS_LOCATOR, 'Контакты'),
            (self.SIDEBAR_DOCUMENTS_LOCATOR, 'Документы'),
            (self.BUTTON_LOGOUT_LOCATOR, 'Выйти'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_on_registrarion_visitspage_en(self):
        elements_to_check = [
            (self.LOGO_REGISTRATION_VISITS_LOCATOR_EN, 'Registration of visits'),
            (self.TEXT_ADMINISTRATOR_LOCATOR_EN, 'Administrator'),
            (self.SHORT_INSTRUCTION_LOCATOR_EN, 'Short instruction:'),
            (self.FIRST_INSTRUCTION_LOCATOR, 'Press the “New visits” button.'),
            (self.SECOND_INSTRUCTION_LOCATOR, 'To confirm the visit, press the “Accept” button.'),
            (self.THIRD_INSTRUCTION_LOCATOR,
             "Answer the question about the visitor's resemblance to the photo (The answer does not affect the visit confirmation)."),
            (self.BUTTON_NEW_VISITS_LOCATOR_EN, 'New visits'),
            (self.SIDEBAR_VISITS_HISTORY_LOCATOR_EN, 'Registration of visits'),
            (self.SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR_EN, 'Visit history'),
            (self.SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR_EN, 'Visits under correction'),
            (self.SIDEBAR_FACILITY_DETAILS_LOCATOR_EN, 'Facility details'),
            (self.SIDEBAR_CONTACTS_LOCATOR_EN, 'Contacts'),
            (self.SIDEBAR_DOCUMENTS_LOCATOR_EN, 'Documents'),
            (self.BUTTON_LOGOUT_LOCATOR_EN, 'Logout'),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_on_confirm_visit_modal(self):
        elements_to_check = [
            (self.TEXT_QUESTION_ACCEPT_LOCATOR, 'Является ли клиент человеком на фото?'),
            (self.BUTTON_LOOKS_LIKE_LOCATOR, 'Похож'),
            (self.BUTTON_NOT_SURE_LOCATOR, 'Не уверен'),
            (self.FOTO_LOCATOR_MODAL, None),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_on_confirm_visit_modal_en(self):
        elements_to_check = [
            (self.TEXT_QUESTION_ACCEPT_LOCATOR_EN, 'Is the visitor the person in the photo?'),
            (self.BUTTON_LOOKS_LIKE_LOCATOR_EN, 'Looks like'),
            (self.BUTTON_NOT_SURE_LOCATOR_EN, 'Not sure'),
            (self.FOTO_LOCATOR_MODAL, None),
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Select language")
    def select_language(self):
        location_dropdown = self.find_element(self.CHANGE_LANGUAGE_DROPDOWN_LOCATOR)
        select = Select(location_dropdown)
        select.select_by_visible_text("English (en)")

    @allure.step("Found elements")
    def assert_found_elements_with_wisit_page_ru(self):
        elements_to_check = [
            (self.SUPPLIER_NAME_LOCATOR, 'Gym1'),
            (self.NAME_USER_LOCATOR, 'Oleg Atr'),
            (self.LEVEL_USER_LOCATOR, 'platinum'),
            (self.ATTRACTION_USER_LOCATOR, 'Посещение SGP'),
            (self.DECLINE_BUTTON_LOCATOR, 'Отклонить'),
            (self.ACCEPT_BUTTON_LOCATOR, 'Принять'),
            (self.FOTO_LOCATOR, None),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_with_wisit_page_en(self):
        elements_to_check = [
            (self.SUPPLIER_NAME_LOCATOR, 'Gym1'),
            (self.NAME_USER_LOCATOR, 'Oleg Atr'),
            (self.LEVEL_USER_LOCATOR, 'platinum'),
            (self.ATTRACTION_USER_LOCATOR, 'Посещение SGP'),
            (self.DECLINE_BUTTON_LOCATOR_EN, 'Decline'),
            (self.ACCEPT_BUTTON_LOCATOR_EN, 'Accept'),
            (self.FOTO_LOCATOR, None),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Click reject visit")
    def click_reject_visit(self):
        self.hard_click(self.DECLINE_BUTTON_LOCATOR)

    @allure.step("Click reject visit")
    def click_reject_visit_en(self):
        self.hard_click(self.DECLINE_BUTTON_LOCATOR_EN)

    @allure.step("Click confirm visit")
    def click_confirm_visit_ru(self):
        self.hard_click(self.ACCEPT_BUTTON_LOCATOR)

    @allure.step("Click confirm visit")
    def click_confirm_visit_en(self):
        self.hard_click(self.ACCEPT_BUTTON_LOCATOR_EN)

    @allure.step("Found elements")
    def assert_found_elements_modal_reject_visit_page_ru(self):
        elements_to_check = [
            (self.REJECT_VISIT_TEXT_LOCATOR, 'Отклонить визит'),
            (self.REASON_TEXT_LOCATOR, 'Причина'),
            (self.BUTTON_SAVE_LOCATOR, 'Сохранить'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_modal_reject_visit_page_en(self):
        elements_to_check = [
            (self.REJECT_VISIT_TEXT_LOCATOR_EN, 'Reject the visit'),
            (self.REASON_TEXT_LOCATOR_EN, 'Reason'),
            (self.BUTTON_SAVE_LOCATOR_EN, 'Save'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Add reason visit")
    def enter_reason_visit(self):
        self.fill(self.INPUT_REASON_REJECT_LOCATOR, self.INPUT_REASON_REJECT_TEXT_LOCATOR)

    @allure.step("Save reject visit")
    def click_save_reject_visit(self):
        self.hard_click(self.CLICK_BUTTON_SAVE)

    @allure.step("Save reject visit")
    def click_save_reject_visit_en(self):
        self.hard_click(self.CLICK_BUTTON_SAVE_EN)

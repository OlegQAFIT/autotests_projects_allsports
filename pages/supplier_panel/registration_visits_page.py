import allure
import pytest
import os
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
from helpers.supplier_panel_data import role_has_documents
from locators.supplier_panel.for_registration_of_visits_pade_locators import RegistrationVisitsLocators
from helpers.add_visit import (
    VisitDailyLimitReachedError,
    create_test_visit as external_create_test_visit,
    login_and_create_visit as external_login_and_create_visit,
)

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
    def login_and_create_visit(self, phone_number=None, sms_code=None, gym_token=None, attraction_id=None):
        try:
            if all(value is not None for value in [phone_number, sms_code, gym_token, attraction_id]):
                external_login_and_create_visit(phone_number, sms_code, gym_token, attraction_id)
                return
            external_create_test_visit()
        except VisitDailyLimitReachedError as exc:
            pytest.skip(f"Создание нового визита недоступно: {exc}")

    @allure.step("Login with credentials")
    def login_supplier_panel(self, role=None, login=None, password=None):
        default_role = os.getenv("SUPPLIER_VISIT_UI_ROLE", "finance")
        effective_role = role or default_role
        return super().login_supplier_panel(role=effective_role, login=login, password=password)

    @allure.step("Login in SP V2")
    def login(self):
        self.fill(self.LOGIN_FIELD, self.LOGIN_TEXT)
        self.fill(self.PASSWORD_FIELD, self.PASSWORD_TEXT)
        self.hard_click(self.SIGNIN_BUTTON)

    def _assert_text_contains_any(self, locator, expected_fragments):
        actual_value = self.find_element_text(locator)
        assert any(fragment in actual_value for fragment in expected_fragments), (
            f"Текст элемента по локатору {locator} не соответствует ожидаемому. "
            f"Ожидался один из фрагментов: {expected_fragments}, фактически: '{actual_value}'"
        )

    def _has_visit_card_actions(self):
        has_reject = self.is_element_visible(self.DECLINE_BUTTON_LOCATOR) or self.is_element_visible(
            self.DECLINE_BUTTON_LOCATOR_EN
        )
        has_accept = self.is_element_visible(self.ACCEPT_BUTTON_LOCATOR) or self.is_element_visible(
            self.ACCEPT_BUTTON_LOCATOR_EN
        )
        return has_reject and has_accept

    def _click_new_visits_if_available(self):
        if self.is_element_visible(self.BUTTON_NEW_VISITS_LOCATOR):
            self.hard_click(self.BUTTON_NEW_VISITS_LOCATOR)
            return
        if self.is_element_visible(self.BUTTON_NEW_VISITS_LOCATOR_EN):
            self.hard_click(self.BUTTON_NEW_VISITS_LOCATOR_EN)
            return
        self.driver.refresh()

    def _try_create_visit_if_missing(self):
        if not getattr(self.driver, "live_api", False):
            pytest.skip(
                "Нет доступного нового визита. Запустите тесты с флагом --live-api, "
                "чтобы автотест смог создать визит через API."
            )

        try:
            self.login_and_create_visit()
        except VisitDailyLimitReachedError as exc:
            pytest.skip(f"Пропуск: достигнут дневной лимит создания визитов ({exc}).")
        for _ in range(5):
            self._click_new_visits_if_available()
            if self._has_visit_card_actions():
                return True
            time.sleep(1.5)
        return self._has_visit_card_actions()

    def _ensure_visit_card_actions_available(self):
        if self._has_visit_card_actions():
            return
        if self._try_create_visit_if_missing():
            return
        raise AssertionError(
            "Визит был создан, но карточка нового визита (Accept/Decline) не появилась в supplier panel. "
            "Проверьте соответствие данных визита текущему аккаунту поставщика "
            "(SUPPLIER_VISIT_GYM_TOKEN / SUPPLIER_VISIT_ATTRACTION_ID)."
        )

    def _assert_new_visits_button_text(self, expected_fragments):
        locators = [self.BUTTON_NEW_VISITS_LOCATOR, self.BUTTON_NEW_VISITS_LOCATOR_EN]
        for locator in locators:
            if self.is_element_visible(locator):
                self._assert_text_contains_any(locator, expected_fragments)
                return
        raise AssertionError("Не найдена кнопка проверки новых визитов.")

    @allure.step("Found elements")
    def assert_found_elements_on_registrarion_visitspage_ru(self, role="reception"):
        elements_to_check = [
            (self.LOGO_REGISTRATION_VISITS_LOCATOR, 'Регистрация визитов'),
            (self.TEXT_ADMINISTRATOR_LOCATOR, 'Администратор'),
            (self.SHORT_INSTRUCTION_LOCATOR, 'Краткая инструкция:'),
            (self.SIDEBAR_REGISTRATION_VISITS_LOCATOR, 'Регистрация визитов'),
            (self.SIDEBAR_VISITS_HISTORY_LOCATOR, 'История визитов'),
            (self.SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR, 'Визиты на исправлении'),
            (self.SIDEBAR_FACILITY_DETAILS_LOCATOR, 'Описание обьекта'),
            (self.SIDEBAR_CONTACTS_LOCATOR, 'Контакты'),
            (self.BUTTON_LOGOUT_LOCATOR, 'Выйти'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

        self._assert_new_visits_button_text(["Проверить новые визиты", "Новые визиты"])
        self._assert_text_contains_any(
            self.FIRST_INSTRUCTION_LOCATOR,
            [
                "Предложите пользователю отсканировать QR-код Allsports",
                "Нажмите кнопку «Проверить новые визиты».",
            ],
        )
        self._assert_text_contains_any(
            self.SECOND_INSTRUCTION_LOCATOR,
            [
                "Нажмите кнопку «Проверить новые визиты».",
                "Для подтверждения посещения нажмите кнопку",
            ],
        )
        self._assert_text_contains_any(
            self.THIRD_INSTRUCTION_LOCATOR,
            [
                "Для подтверждения посещения нажмите кнопку",
                "Ответьте на вопрос о схожести посетителя",
            ],
        )
        if self.is_element_visible(self.FOURTH_INSTRUCTION_LOCATOR):
            self._assert_text_contains_any(
                self.FOURTH_INSTRUCTION_LOCATOR,
                ["Ответьте на вопрос о схожести посетителя"],
            )

        has_documents = self.is_element_visible(self.SIDEBAR_DOCUMENTS_LOCATOR)
        expected_documents = role_has_documents(role)
        assert has_documents == expected_documents, (
            f"Ожидалась доступность вкладки Документы={expected_documents}, фактически={has_documents}"
        )

    @allure.step("Found elements")
    def assert_found_elements_on_registrarion_visitspage_en(self, role="reception"):
        elements_to_check = [
            (self.LOGO_REGISTRATION_VISITS_LOCATOR_EN, 'Registration of visits'),
            (self.TEXT_ADMINISTRATOR_LOCATOR_EN, 'Administrator'),
            (self.SHORT_INSTRUCTION_LOCATOR_EN, 'Short instruction:'),
            (self.SIDEBAR_REGISTRATION_VISITS_LOCATOR_EN, 'Registration of visits'),
            (self.SIDEBAR_VISITS_HISTORY_LOCATOR_EN, 'Visit history'),
            (self.SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR_EN, 'Visits under correction'),
            (self.SIDEBAR_FACILITY_DETAILS_LOCATOR_EN, 'Facility details'),
            (self.SIDEBAR_CONTACTS_LOCATOR_EN, 'Contacts'),
            (self.BUTTON_LOGOUT_LOCATOR_EN, 'Logout'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

        self._assert_new_visits_button_text(["Check new visits", "New visits", "Проверить новые визиты"])
        self._assert_text_contains_any(
            self.FIRST_INSTRUCTION_LOCATOR,
            [
                "Suggest that the visitor scan the Allsports QR code",
                "Press the 'Check New Visits' button.",
            ],
        )
        self._assert_text_contains_any(
            self.SECOND_INSTRUCTION_LOCATOR,
            [
                "Press the 'Check New Visits' button.",
                "To confirm the visit, press the “Accept” button.",
            ],
        )
        self._assert_text_contains_any(
            self.THIRD_INSTRUCTION_LOCATOR,
            [
                "To confirm the visit, press the “Accept” button.",
                "Answer the question about the visitor's resemblance",
            ],
        )
        if self.is_element_visible(self.FOURTH_INSTRUCTION_LOCATOR):
            self._assert_text_contains_any(
                self.FOURTH_INSTRUCTION_LOCATOR,
                ["Answer the question about the visitor's resemblance"],
            )

        has_documents = self.is_element_visible(self.SIDEBAR_DOCUMENTS_LOCATOR_EN)
        expected_documents = role_has_documents(role)
        assert has_documents == expected_documents, (
            f"Expected Documents tab visibility={expected_documents}, actual={has_documents}"
        )

    @allure.step("Found elements")
    def assert_found_elements_on_confirm_visit_modal(self):
        elements_to_check = [
            (self.TEXT_QUESTION_ACCEPT_LOCATOR, 'Является ли клиент человеком на фото?'),
            (self.BUTTON_LOOKS_LIKE_LOCATOR, 'Похож'),
            (self.BUTTON_NOT_SURE_LOCATOR, 'Не уверен'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    @allure.step("Found elements")
    def assert_found_elements_on_confirm_visit_modal_en(self):
        elements_to_check = [
            (self.TEXT_QUESTION_ACCEPT_LOCATOR_EN, 'Is the visitor the person in the photo?'),
            (self.BUTTON_LOOKS_LIKE_LOCATOR_EN, 'Looks like'),
            (self.BUTTON_NOT_SURE_LOCATOR_EN, 'Not sure'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    @allure.step("Select language")
    def select_language(self):
        location_dropdown = self.find_element(self.CHANGE_LANGUAGE_DROPDOWN_LOCATOR)
        select = Select(location_dropdown)
        select.select_by_visible_text("English (en)")

    @allure.step("Found elements")
    def assert_found_elements_with_wisit_page_ru(self):
        self._ensure_visit_card_actions_available()
        dynamic_fields = [
            (self.SUPPLIER_NAME_LOCATOR, "название объекта"),
            (self.NAME_USER_LOCATOR, "имя пользователя"),
            (self.LEVEL_USER_LOCATOR, "уровень пользователя"),
            (self.ATTRACTION_USER_LOCATOR, "услуга"),
        ]
        for element_locator, field_name in dynamic_fields:
            actual_value = self.find_element_text(element_locator).strip()
            assert actual_value, f"Не заполнено поле '{field_name}' по локатору {element_locator}"

        self._assert_text_contains_any(self.DECLINE_BUTTON_LOCATOR, ["Отклонить"])
        self._assert_text_contains_any(self.ACCEPT_BUTTON_LOCATOR, ["Принять"])

    @allure.step("Found elements")
    def assert_found_elements_with_wisit_page_en(self):
        self._ensure_visit_card_actions_available()
        dynamic_fields = [
            (self.SUPPLIER_NAME_LOCATOR, "supplier name"),
            (self.NAME_USER_LOCATOR, "user name"),
            (self.LEVEL_USER_LOCATOR, "user level"),
            (self.ATTRACTION_USER_LOCATOR, "attraction"),
        ]
        for element_locator, field_name in dynamic_fields:
            actual_value = self.find_element_text(element_locator).strip()
            assert actual_value, f"Field '{field_name}' is empty for locator {element_locator}"

        self._assert_text_contains_any(self.DECLINE_BUTTON_LOCATOR_EN, ["Decline"])
        self._assert_text_contains_any(self.ACCEPT_BUTTON_LOCATOR_EN, ["Accept"])

    @allure.step("Click reject visit")
    def click_reject_visit(self):
        self._ensure_visit_card_actions_available()
        if self.is_element_visible(self.DECLINE_BUTTON_LOCATOR):
            self.hard_click(self.DECLINE_BUTTON_LOCATOR)
        elif self.is_element_visible(self.DECLINE_BUTTON_LOCATOR_EN):
            self.hard_click(self.DECLINE_BUTTON_LOCATOR_EN)
        else:
            pytest.skip("Кнопка Reject недоступна: нет активного нового визита.")

    @allure.step("Click reject visit")
    def click_reject_visit_en(self):
        self._ensure_visit_card_actions_available()
        if self.is_element_visible(self.DECLINE_BUTTON_LOCATOR_EN):
            self.hard_click(self.DECLINE_BUTTON_LOCATOR_EN)
        elif self.is_element_visible(self.DECLINE_BUTTON_LOCATOR):
            self.hard_click(self.DECLINE_BUTTON_LOCATOR)
        else:
            pytest.skip("Reject button is unavailable: no active new visit.")

    @allure.step("Click confirm visit")
    def click_confirm_visit_ru(self):
        self._ensure_visit_card_actions_available()
        if self.is_element_visible(self.ACCEPT_BUTTON_LOCATOR):
            self.hard_click(self.ACCEPT_BUTTON_LOCATOR)
        elif self.is_element_visible(self.ACCEPT_BUTTON_LOCATOR_EN):
            self.hard_click(self.ACCEPT_BUTTON_LOCATOR_EN)
        else:
            pytest.skip("Кнопка Accept недоступна: нет активного нового визита.")

    @allure.step("Click confirm visit")
    def click_confirm_visit_en(self):
        self._ensure_visit_card_actions_available()
        if self.is_element_visible(self.ACCEPT_BUTTON_LOCATOR_EN):
            self.hard_click(self.ACCEPT_BUTTON_LOCATOR_EN)
        elif self.is_element_visible(self.ACCEPT_BUTTON_LOCATOR):
            self.hard_click(self.ACCEPT_BUTTON_LOCATOR)
        else:
            pytest.skip("Accept button is unavailable: no active new visit.")

    @allure.step("Found elements")
    def assert_found_elements_modal_reject_visit_page_ru(self):
        elements_to_check = [
            (self.REJECT_VISIT_TEXT_LOCATOR, 'Отклонить визит'),
            (self.REASON_TEXT_LOCATOR, 'Причина'),
            (self.BUTTON_SAVE_LOCATOR, 'Сохранить'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    @allure.step("Found elements")
    def assert_found_elements_modal_reject_visit_page_en(self):
        elements_to_check = [
            (self.REJECT_VISIT_TEXT_LOCATOR_EN, 'Reject the visit'),
            (self.REASON_TEXT_LOCATOR_EN, 'Reason'),
            (self.BUTTON_SAVE_LOCATOR_EN, 'Save'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    @allure.step("Add reason visit")
    def enter_reason_visit(self):
        self.fill(self.INPUT_REASON_REJECT_LOCATOR, self.INPUT_REASON_REJECT_TEXT_LOCATOR)

    @allure.step("Save reject visit")
    def click_save_reject_visit(self):
        self.hard_click(self.CLICK_BUTTON_SAVE)

    @allure.step("Save reject visit")
    def click_save_reject_visit_en(self):
        self.hard_click(self.CLICK_BUTTON_SAVE_EN)

    @allure.step("Assert sidebar visibility by role")
    def assert_sidebar_visibility_by_role(self, role):
        mandatory_tabs = [
            self.SIDEBAR_REGISTRATION_VISITS_LOCATOR,
            self.SIDEBAR_VISITS_HISTORY_LOCATOR,
            self.SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR,
            self.SIDEBAR_FACILITY_DETAILS_LOCATOR,
            self.SIDEBAR_CONTACTS_LOCATOR,
        ]
        for locator in mandatory_tabs:
            assert self.is_element_visible(locator), f"Обязательная вкладка отсутствует: {locator}"

        has_documents = self.is_element_visible(self.SIDEBAR_DOCUMENTS_LOCATOR)
        expected_documents = role_has_documents(role)
        assert has_documents == expected_documents, (
            f"Ожидалась доступность вкладки Документы={expected_documents}, фактически={has_documents}"
        )

    @allure.step("Logout from supplier panel")
    def logout_supplier_panel(self):
        if self.is_element_visible(self.BUTTON_LOGOUT_LOCATOR):
            self.hard_click(self.BUTTON_LOGOUT_LOCATOR)
        else:
            self.hard_click(self.BUTTON_LOGOUT_LOCATOR_EN)

        assert self.is_element_visible("//button[normalize-space()='Продолжить']") or self.is_element_visible(
            "//button[normalize-space()='Continue']"
        ), "После logout не открылась страница логина"

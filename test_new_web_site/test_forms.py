# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site.companies import CompaniesPage
from pages.new_web_site.contacts import ContactsPage
from pages.new_web_site.header import HeaderPage
from pages.new_web_site.levels import LevelsPage
from pages.new_web_site.main_page import MainPage
from pages.new_web_site.partners import PartnersPage


# ===================== HEADER FORMS =======================

@allure.feature('Offer Modal')
@allure.story('Открытие модалки')
def test_open_modal_offer(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()


@allure.feature('Offer Modal')
@allure.story('Проверка вкладок в модалке')
def test_check_offer_tabs(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_tabs()


@allure.feature('Offer Modal')
@allure.story('Проверка переключения вкладок')
def test_check_offer_tabs_switch(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_tabs_switch()


@allure.feature('Offer Modal')
@allure.story('Проверка обязательных полей')
def test_check_offer_fields(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_fields()


@allure.feature('Offer Modal')
@allure.story('Проверка ссылки политики (UI и 200)')
def test_check_offer_policy_link(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_policy_link()


@allure.feature('Offer Modal')
@allure.story('Проверка неактивности кнопки без чекбокса')
def test_check_offer_button_disabled(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_button_disabled()


@allure.feature('Offer Modal')
@allure.story('Проверка закрытия модалки крестиком')
def test_check_offer_close(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_close()


@allure.feature('Offer Modal')
@allure.story('Проверка телефонного номера в модалке')
def test_check_offer_phone(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_phone()


@allure.feature('Offer Modal')
@allure.severity('Critical')
@allure.story('Проверка логики активности кнопки "Отправить" в зависимости от заполнения формы')
def test_offer_button_validation_logic(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_button_validation_logic()


@allure.feature('Offer Modal')
@allure.severity('Critical')
@allure.story('Проверка валидации при неверном email')
def test_modal_offer_invalid_email_validation(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_offer_invalid_email_validation()


@allure.feature('Partner Modal')
@allure.story('Проверка вкладки Стать партнёром')
def test_check_partner_tab(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_partner_tab()


@allure.feature('Partner Modal')
@allure.story('Проверка структуры формы партнёра')
def test_check_partner_fields(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_partner_fields()


@allure.feature('Partner Modal')
@allure.story('Проверка политики в форме партнёра (UI и 200)')
def test_check_partner_policy_link(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_partner_policy_link()


@allure.feature('Partner Modal')
@allure.severity('Normal')
@allure.story('Проверка ошибки при неверном email в форме партнёра')
def test_partner_invalid_email_validation(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_partner_invalid_email_validation()


@allure.feature('Partner Modal')
@allure.severity('Normal')
@allure.story('Проверка ошибки при неверном телефоне в форме партнёра')
def test_partner_invalid_phone_validation(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.check_partner_invalid_phone_validation()


@allure.feature('Question Modal')
@allure.story('Проверка полей формы')
def test_check_question_fields(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_question()
    page.check_question_fields()


@allure.feature('Question Modal')
@allure.story('Проверка ссылки политики (UI и 200)')
def test_check_question_policy_link(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_question()
    page.check_question_policy_link()


@allure.feature('Question Modal')
@allure.story('Проверка неактивности кнопки')
def test_check_question_button_disabled(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_question()
    page.check_question_button_disabled()


@allure.feature('Offer Modal')
@allure.severity('Critical')
@allure.story('Успешная отправка формы "Получить предложение"')
def test_header_offer_form_submission(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.submit_and_check_offer_form()


@allure.feature('Partner Modal')
@allure.severity('Critical')
@allure.story('Успешная отправка формы "Стать партнёром"')
def test_header_partner_form_submission(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_offer()
    page.submit_and_check_partner_form()


@allure.feature('Question Modal')
@allure.severity('Critical')
@allure.story('Успешная отправка формы "Задать вопрос"')
def test_header_question_form_submission(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_question()
    page.submit_and_check_question_form()


@allure.feature('Header E2E')
@allure.severity('Normal')
@allure.story('Проверка открытия всех ссылок политики из модалок в новой вкладке и код 200')
def test_all_policy_links_open_in_new_tab(driver):
    page = HeaderPage(driver)
    page.open()

    page.open_modal_offer()
    page.check_offer_policy_link()
    page.check_offer_close()

    page.open_modal_offer()
    page.check_partner_tab()
    page.check_partner_policy_link()
    page.check_offer_close()

    page.open_modal_question()
    page.check_question_policy_link()


# ===================== LEVELS FORM =======================

@allure.feature('Levels Page')
@allure.story('Inline-форма — структура и активация кнопки')
@allure.severity('Normal')
def test_levels_join_form_full(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_form_full()


@allure.feature('Levels Page')
@allure.story('Inline-форма — ошибки валидации телефона и email')
@allure.severity('Critical')
def test_levels_join_form_validation_errors(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.validate_join_phone_errors()
    page.validate_join_email_errors()


@allure.feature('Levels Page')
@allure.story('Inline-форма — успешная отправка')
@allure.severity('Critical')
def test_levels_join_form_submission(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form()


# ===================== CONTACTS FORMS =======================

@allure.feature('Send form')
@allure.severity('Critical')
@allure.story('Проверка успешной отправки формы (Подключить компанию)')
@pytest.mark.live_api
def test_contacts_send_form_valid_get_offer(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_valid_get_offer()
    page.check_success_modal()
    page.assert_form_get_offer()


@allure.feature('Send form')
@allure.severity('Critical')
@allure.story('Проверка успешной отправки формы (Стать партнёром)')
@pytest.mark.live_api
def test_contacts_send_form_valid_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_valid_become_partner()
    page.check_success_modal()
    page.assert_form_become_partner()


@allure.feature('Send form')
@allure.severity('Critical')
@allure.story('Проверка, что кнопка Отправить активна (после заполнения и чекбокса)')
def test_contacts_send_button_enabled(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.switch_to_get_offer()
    page.fill_form_standard(page.text_name, page.text_phone_valid, page.text_email_valid, page.text_company)
    page.clc_checkbox(True)
    page.check_send_button_enabled()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным email (get-offer)')
def test_contacts_invalid_email(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(email=True)
    page.assert_email_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным телефоном (get-offer)')
def test_contacts_invalid_phone(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(phone=True)
    page.assert_phone_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы с пустыми полями (get-offer)')
def test_contacts_empty_fields(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(empty=True)
    page.check_button_state_disabled()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы без согласия на обработку данных (get-offer)')
def test_contacts_without_agree_checkbox(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(no_agree=True)
    page.check_button_state_disabled()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным email (become-partner)')
def test_contacts_invalid_email_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, email=True)
    page.assert_email_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным телефоном (become-partner)')
def test_contacts_invalid_phone_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, phone=True)
    page.assert_phone_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы с пустыми полями (become-partner)')
def test_contacts_empty_fields_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, empty=True)
    page.check_button_state_disabled()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы без согласия (become-partner)')
def test_contacts_without_checkbox_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, no_agree=True)
    page.check_button_state_disabled()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка: невалидный email, затем валидный (get-offer)')
@pytest.mark.live_api
def test_contacts_invalid_email_then_valid(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(email=True)
    page.assert_email_error()
    page.submit_form_valid_get_offer()
    page.check_success_modal()
    page.assert_form_get_offer()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка: невалидный телефон, затем валидный (get-offer)')
@pytest.mark.live_api
def test_contacts_invalid_phone_then_valid(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(phone=True)
    page.assert_phone_error()
    page.submit_form_valid_get_offer()
    page.check_success_modal()
    page.assert_form_get_offer()


@allure.feature('Form')
@allure.severity('Normal')
@allure.story('Проверка наличия всех обязательных полей (Имя, Телефон, Email, Компания/Сообщение)')
def test_contacts_presence_of_all_form_fields(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    assert page.is_element_exist(page.INPUT_NAME), "Поле Имя отсутствует"
    assert page.is_element_exist(page.INPUT_PHONE), "Поле Телефон отсутствует"
    assert page.is_element_exist(page.INPUT_EMAIL), "Поле Email отсутствует"
    assert page.is_element_exist(page.INPUT_MESSAGE), "Поле Сообщение/Компания отсутствует"


@allure.feature('E2E')
@allure.severity('Blocker')
@allure.story('Полный путь пользователя: проверка инфо + отправка формы (get-offer)')
@pytest.mark.live_api
def test_contacts_e2e_contacts_page_flow(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_header()
    page.check_address_block()
    page.verify_tel_links_format()
    page.verify_mailto_links_format()
    page.check_google_map()
    page.submit_form_valid_get_offer()
    page.check_success_modal()
    page.assert_form_get_offer()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Кнопка неактивна, пока не заполнены все поля и не нажат чекбокс')
def test_contacts_button_inactive_without_checkbox_or_fields(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.assert_button_inactive_until_all_required()


# ===================== COMPANIES FORMS =======================

@allure.feature("Companies Page")
@allure.severity("Normal")
@allure.story("FAQ — форма 'Не нашли ответ на вопрос'")
def test_companies_faq_form_button(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_form_button()


@allure.story("Открытие форм из хедера")
@allure.severity("Critical")
def test_companies_open_header_offer_modal(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_header_offer_modal()
    page.check_modal_common("Получить предложение")


@allure.story("Открытие формы 'Задать вопрос' из хедера")
@allure.severity("Critical")
def test_companies_open_header_question_modal(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_header_question_modal()
    page.check_modal_common("Задать вопрос")


@allure.story("Открытие форм из промо-блока")
@allure.severity("Critical")
def test_companies_open_promo_offer_modal(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.check_modal_common("Получить предложение")


@allure.story("Открытие формы 'Задать вопрос' из промо-блока")
@allure.severity("Critical")
def test_companies_open_promo_question_modal(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_question_modal()
    page.check_modal_common("Задать вопрос")


@allure.story("Открытие формы из блока FAQ")
@allure.severity("Critical")
def test_companies_open_faq_question_modal(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_question_modal()
    page.check_modal_common("Задать вопрос")


@allure.story("Валидации — телефон и email в модалке")
@allure.severity("Critical")
def test_companies_modal_validation_phone_email(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.validate_phone_errors_in_modal()
    page.validate_email_errors_in_modal()


@allure.story("Активация кнопки — 'Получить предложение'")
@allure.severity("Critical")
def test_companies_offer_submit_activation(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.check_offer_submit_activation()


@allure.story("Активация кнопки — 'Задать вопрос'")
@allure.severity("Critical")
def test_companies_question_submit_activation(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_question_modal()
    page.check_question_submit_activation()


@allure.story("Inline-форма 'Присоединяйтесь к Allsports'")
@allure.severity("Major")
def test_companies_join_form_full(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_form_full()


@allure.feature("Companies Page")
@allure.story("Форма — 'Получить предложение' (Промо-блок)")
@allure.severity("Critical")
def test_companies_promo_offer_form_submission(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.submit_promo_offer_form()


@allure.feature("Companies Page")
@allure.story("Форма — 'Задать вопрос' (Промо-блок)")
@allure.severity("Critical")
def test_companies_promo_question_form_submission(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_question_modal()
    page.submit_promo_question_form()


@allure.feature("Companies Page")
@allure.story("Форма — 'Задать вопрос' (FAQ)")
@allure.severity("Critical")
def test_companies_faq_question_form_submission(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_question_modal()
    page.submit_faq_question_form()


@allure.feature("Companies Page")
@allure.story("Inline-форма — 'Присоединяйтесь к Allsports'")
@allure.severity("Major")
def test_companies_join_form_submission(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form()


@allure.feature("Companies Page")
@allure.story("Гиперссылки — политика и телефон")
@allure.severity("Normal")
def test_companies_forms_links_validity(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.check_modal_common("Получить предложение")


@allure.feature("Companies Page")
@allure.story("Ссылки на политику обработки персональных данных во всех формах")
@allure.severity("Critical")
def test_companies_policy_link_in_all_forms(driver):
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_policy_link_in_all_forms()


# ===================== MAIN PAGE FORM ENTRYPOINTS =======================

@allure.feature("Main Page")
@allure.severity("Critical")
@allure.story("FAQ — Модалка 'Задать вопрос' корректно открывается и закрывается")
def test_main_faq_modal_open_close(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_tab("Пользователям")
    page.check_form_present()
    page.check_modal_open_close()


@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Пользователям' и модалки 'Задать вопрос'")
def test_main_advantages_users_modal(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_tab_users()


@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Компаниям' и модалки 'Получить предложение'")
def test_main_advantages_companies_modal(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_tab_companies()


@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Партнёрам' и модалки 'Стать партнёром'")
def test_main_advantages_partners_modal(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_tab_partners()


# ===================== PARTNERS FORMS =======================

@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Промо-блок — кнопка Стать партнёром')
def test_promo_become_partner_button(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_become_partner()


@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Промо-блок — кнопка Задать вопрос')
def test_promo_ask_question_button(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_ask_question()

@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Форма Join — наличие полей')
def test_partners_join_form_fields(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_form_fields()


@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — чекбокс политики')
def test_partners_join_policy_checkbox(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_policy_checkbox()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Форма Join — валидация телефона')
def test_partners_join_phone_validation(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_phone_validation()


@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Форма Join — валидация email')
def test_partners_join_email_validation(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_email_validation()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Форма Join — успешная отправка')
def test_partners_join_form_submit(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form_success()


@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — disabled кнопка при пустых полях')
def test_partners_join_button_disabled_initially(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_button_disabled()


@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Форма Join — отображение текста-подсказки')
def test_partners_join_help_text(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_help_text()


@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — клик по ссылке политики')
def test_partners_join_policy_link(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_policy_link()


@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — заполнение валидными данными')
def test_partners_join_valid_data(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.fill_join_form_valid()


@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Форма Join — очистка полей')
def test_partners_join_clear_fields(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_clear_fields()


@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('FAQ — кнопка Задать вопрос')
def test_partners_faq_button(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_button()


@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('FAQ — наличие кнопки Задать вопрос под списком')
def test_faq_bottom_button(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_bottom_button()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — открытие модалки вопроса')
def test_partners_faq_modal_open(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — отправка вопроса')
def test_partners_faq_modal_submit(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()
    page.submit_faq_question()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Промо — отправка формы через кнопку "Стать партнёром"')
def test_partners_submit_become_partner_form(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_become_partner()
    page.submit_become_partner_modal()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Промо — отправка формы через кнопку "Задать вопрос"')
def test_partners_submit_question_modal_top(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_ask_question()
    page.submit_question_modal()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — отправка вопроса из блока FAQ')
def test_partners_submit_question_modal_faq(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()
    page.submit_question_modal()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Join форма — успешная отправка')
def test_partners_join_form_real_submit(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form_success()
    page.verify_success_modal()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — валидация формы "Задать вопрос" (ошибки ввода)')
def test_partners_faq_modal_validation_errors(driver):
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()
    page.verify_faq_question_errors()

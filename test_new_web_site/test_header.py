# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.header import HeaderPage


# =======================
# == Основной хедер ==
# =======================

@allure.feature('Header')
@allure.severity('Blocker')
@allure.story('Проверка логотипа')
def test_logo(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_logo()


@allure.feature('Header')
@allure.severity('Normal')
@allure.story('Проверка перехода по логотипу')
def test_logo_navigation(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_logo_navigation()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Объекты')
def test_link_facilities(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_facilities()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Типы подписок')
def test_link_levels(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_levels()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Компаниям')
def test_link_companies(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_companies()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Партнерам')
def test_link_partners(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_partners()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Контакты')
def test_link_contacts(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_contacts()


@allure.feature('Header Buttons')
@allure.story('Проверка наличия кнопок в хедере')
def test_header_buttons(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_header_buttons()


# =======================
# == Модалка «Получить предложение» ==
# =======================

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


# @allure.feature('Offer Modal')
# @allure.story('Успешная отправка формы "Получить предложение"')
# def test_offer_form_success(driver):
#     page = HeaderPage(driver)
#     page.open()
#     page.open_modal_offer()
#     page.submit_and_check_offer_form()


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


# ====== Валидация (Offer) ======
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



# =======================
# == Вкладка «Стать партнёром» ==
# =======================

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


# @allure.feature('Partner Modal')
# @allure.story('Успешная отправка формы "Стать партнёром"')
# def test_partner_form_success(driver):
#     page = HeaderPage(driver)
#     page.open()
#     page.open_modal_offer()
#     page.submit_and_check_partner_form()


# ====== Валидации (Partner) ======



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


# =======================
# == Модалка «Задать вопрос» ==
# =======================

@allure.feature('Question Modal')
@allure.story('Открытие модалки')
def test_open_modal_question(driver):
    page = HeaderPage(driver)
    page.open()
    page.open_modal_question()


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


# @allure.feature('Question Modal')
# @allure.story('Успешная отправка формы "Задать вопрос"')
# def test_question_form_success(driver):
#     page = HeaderPage(driver)
#     page.open()
#     page.open_modal_question()
#     page.submit_and_check_question_form()

@allure.feature('Header E2E')
@allure.severity('Normal')
@allure.story('Проверка открытия всех ссылок политики из модалок в новой вкладке и код 200')
def test_all_policy_links_open_in_new_tab(driver):
    page = HeaderPage(driver)
    page.open()

    # Offer
    page.open_modal_offer()
    page.check_offer_policy_link()
    page.check_offer_close()

    # Partner tab
    page.open_modal_offer()
    page.check_partner_tab()
    page.check_partner_policy_link()
    page.check_offer_close()

    # Question
    page.open_modal_question()
    page.check_question_policy_link()

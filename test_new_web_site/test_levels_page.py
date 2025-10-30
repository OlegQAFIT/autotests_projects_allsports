# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.levels import LevelsPage


# === LEVELS BLOCK ===
@allure.feature('Levels Page')
@allure.story('Типы подписок — наличие блока и карточек')
@allure.severity('Normal')
def test_levels_section_present(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_levels_section_present()
    page.check_subscription_cards_present()


@allure.feature('Levels Page')
@allure.story('Типы подписок — тексты карточек')
@allure.severity('Normal')
def test_levels_cards_texts(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_card_texts_regular()


@allure.feature('Levels Page')
@allure.story('Типы подписок — переходы по ссылкам')
@allure.severity('Critical')
def test_levels_links(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_links_regular_cards()


@allure.feature('Levels Page')
@allure.story('Архивные типы подписок — модалка и карточки')
@allure.severity('Normal')
def test_levels_archive(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_archive_modal()
    page.check_card_texts_archive()
    page.close_archive_modal()


@allure.feature('Levels Page')
@allure.story('Типы подписок — полный сценарий блока')
@allure.severity('High')
def test_levels_full_flow(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_levels_section_present()
    page.check_card_texts_regular()
    page.check_links_regular_cards()
    page.open_archive_modal()
    page.check_card_texts_archive()
    page.close_archive_modal()


# === INLINE JOIN FORM ===
@allure.feature('Levels Page')
@allure.story('Inline-форма — структура и активация кнопки')
@allure.severity('Normal')
def test_join_form_full(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_form_full()


@allure.feature('Levels Page')
@allure.story('Inline-форма — ошибки валидации телефона и email')
@allure.severity('Critical')
def test_join_form_validation_errors(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.validate_join_phone_errors()
    page.validate_join_email_errors()


@allure.feature('Levels Page')
@allure.story('Inline-форма — успешная отправка')
@allure.severity('Critical')
def test_join_form_submission(driver):
    page = LevelsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form()

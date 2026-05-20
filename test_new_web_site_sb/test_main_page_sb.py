# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.main_page_sb import MainPageSb
from test_new_web_site_sb.form_helpers_sb import (
    assert_modal_send_disabled,
    assert_modal_send_enabled,
    clear_submit_spy,
    close_modal_if_open,
    ensure_modal_checkbox_checked,
    fill_modal_input,
    fill_modal_textarea,
    install_submit_spy,
    open_modal_by_cta_text,
    submit_modal_and_collect_contact_urls,
)


@allure.feature("Main SB")
@allure.severity("Critical")
def test_main_page_basics_sb(driver):
    """Проверка базовой структуры главной страницы."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_main_page_basics()


@allure.feature("Main SB")
@allure.severity("Critical")
def test_main_page_cta_buttons_sb(driver):
    """Проверка наличия ключевых CTA-кнопок на главной странице."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_main_cta_buttons()


@allure.feature("Main SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_main_page_offer_modal_flow_sb(driver):
    """Проверка полного flow модального окна Get an Offer на главной странице."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_main_offer_modal_flow()


@allure.feature("Main SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_main_get_offer_form_submit_endpoint_sb(driver):
    """Проверка отправки формы Get an Offer с главной на endpoint /contact/get_offer."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    page.open_get_offer_modal()
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@sportbenefit.eu", "qa.bot@example.com")
    fill_modal_input(driver, "Company", "QA Company")
    fill_modal_input(driver, "Enter the city", "Limassol")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"

    close_modal_if_open(driver)


@allure.feature("Main SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_main_ask_question_form_submit_endpoint_sb(driver):
    """Проверка отправки формы Ask Us a Question с главной на endpoint /contact/ask_question."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Ask Us a Question", required_placeholder="qwerty@allsports.by")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@allsports.by", "qa.ask@example.com")
    fill_modal_textarea(driver, "Question from automated tests")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )

    close_modal_if_open(driver)

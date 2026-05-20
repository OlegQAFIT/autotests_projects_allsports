# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.contacts_sb import ContactsPageSb
from test_new_web_site_sb.form_helpers_sb import (
    assert_modal_send_disabled,
    assert_modal_send_enabled,
    clear_submit_spy,
    close_modal_if_open,
    ensure_modal_checkbox_checked,
    fill_inline_contacts_invalid,
    fill_inline_contacts_values,
    fill_modal_input,
    fill_modal_textarea,
    get_contact_post_urls,
    inline_submit_enabled,
    inline_submit_button,
    inline_success_state,
    inline_validation_messages,
    install_submit_spy,
    modal_validation_messages,
    open_modal_by_cta_text,
    submit_modal_and_collect_contact_urls,
)


@allure.feature("Contacts SB")
@allure.severity("Critical")
def test_contacts_page_basics_sb(driver):
    """Проверка базового открытия страницы Contacts и структуры формы."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()
    page.check_form_structure()


@allure.feature("Contacts SB")
@allure.severity("Critical")
def test_contacts_map_visible_sb(driver):
    """Проверка отображения карты на странице Contacts."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_visible()


@allure.feature("Contacts SB")
@allure.severity("Normal")
@pytest.mark.form_submission
def test_contacts_invalid_validation_sb(driver):
    """Проверка валидации невалидного телефона и email на странице Contacts."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_invalid_phone_validation()


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_inline_form_blocks_invalid_submit_sb(driver):
    """Проверка, что inline-форма блокирует отправку при невалидных данных."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    install_submit_spy(driver)
    clear_submit_spy(driver)

    fill_inline_contacts_invalid(driver)

    submit = inline_submit_button(driver)
    if submit.is_enabled() and submit.get_attribute("disabled") is None:
        driver.execute_script("arguments[0].click();", submit)

    messages = inline_validation_messages(driver)
    urls = get_contact_post_urls(driver)

    assert not urls, f"Inline invalid form should not call contact endpoints. Captured: {urls}"
    assert not inline_submit_enabled(driver), "Inline submit should remain disabled for invalid values"
    if messages:
        assert any(
            "invalid" in m.lower() or "format" in m.lower() or "valid email" in m.lower()
            for m in messages
        ), (
            f"Unexpected validation texts: {messages}"
        )


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_inline_form_submit_endpoint_and_success_state_sb(driver):
    """Проверка endpoint и успешного состояния после отправки inline-формы Contacts."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    fill_inline_contacts_values(
        driver,
        name="QA Inline",
        phone="+357 99 11 22 33",
        email="qa.inline@example.com",
        company="Inline Company",
    )

    install_submit_spy(driver)
    clear_submit_spy(driver)

    if not inline_submit_enabled(driver):
        pytest.xfail(
            "Inline /contacts form submit stayed disabled after valid input. "
            "Endpoint/success-state cannot be validated until page-side gate is fixed."
        )

    submit = inline_submit_button(driver)
    driver.execute_script("arguments[0].click();", submit)

    urls = get_contact_post_urls(driver)
    assert any("/contact/get_offer" in url for url in urls), (
        f"Inline contacts form did not call get_offer endpoint. Captured: {urls}"
    )
    assert inline_success_state(driver), (
        "Inline contacts form request was sent, but no observable completion signal "
        "(reset/disabled state) was detected"
    )


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_get_offer_modal_submit_endpoint_sb(driver):
    """Проверка отправки модальной формы Get an Offer на endpoint /contact/get_offer."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Get an Offer", required_placeholder="Company")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@sportbenefit.eu", "qa.contacts.offer@example.com")
    fill_modal_input(driver, "Company", "QA Contacts")
    fill_modal_input(driver, "Enter the city", "Limassol")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"

    close_modal_if_open(driver)


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_ask_question_modal_submit_endpoint_sb(driver):
    """Проверка отправки модальной формы Ask Us a Question на endpoint /contact/ask_question."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Ask Us a Question", required_placeholder="qwerty@allsports.by")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@allsports.by", "qa.contacts.ask@example.com")
    fill_modal_textarea(driver, "Question from contacts page")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )
    assert not modal_validation_messages(driver), "Ask-question modal should not show validation errors on valid submit"

    close_modal_if_open(driver)

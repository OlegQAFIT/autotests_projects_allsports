# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.partners_sb import PartnersPageSb
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


@allure.feature("Partners SB")
@allure.severity("Critical")
def test_partners_become_partner_modal_sb(driver):
    """Проверка открытия и структуры модального окна Become a Partner."""
    page = PartnersPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_become_partner_modal()
    page.check_partner_modal_structure()


@allure.feature("Partners SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_partners_get_offer_submit_endpoint_sb(driver):
    """Проверка отправки формы Get an Offer на странице Partners."""
    page = PartnersPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Get an Offer", required_placeholder="Company")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@sportbenefit.eu", "qa.partners.offer@example.com")
    fill_modal_input(driver, "Company", "QA Partners")
    fill_modal_input(driver, "Enter the city", "Nicosia")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"

    close_modal_if_open(driver)


@allure.feature("Partners SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_partners_become_partner_submit_endpoint_sb(driver):
    """Проверка отправки формы Become a Partner на endpoint /contact/become_partner."""
    page = PartnersPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    page.open_become_partner_modal()
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@sportbenefit.eu", "qa.partners.partner@example.com")
    fill_modal_input(driver, "Facility name", "QA Facility")
    fill_modal_input(driver, "Enter the city", "Larnaca")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/become_partner" in url for url in urls), (
        f"become_partner endpoint was not called. Captured: {urls}"
    )

    close_modal_if_open(driver)


@allure.feature("Partners SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_partners_ask_question_submit_endpoint_sb(driver):
    """Проверка отправки формы Ask Us a Question на странице Partners."""
    page = PartnersPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Ask Us a Question", required_placeholder="qwerty@allsports.by")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@allsports.by", "qa.partners.ask@example.com")
    fill_modal_textarea(driver, "Question from partners page")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )

    close_modal_if_open(driver)

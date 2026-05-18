# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.companies_sb import CompaniesPageSb
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


@allure.feature("Companies SB")
@allure.severity("Critical")
def test_companies_offer_modal_sb(driver):
    page = CompaniesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_get_offer_modal()
    page.check_companies_modal_structure()


@allure.feature("Companies SB Forms")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_companies_get_offer_submit_endpoint_sb(driver):
    page = CompaniesPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    page.open_get_offer_modal()
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@sportbenefit.eu", "qa.companies@example.com")
    fill_modal_input(driver, "Company", "QA Companies")
    fill_modal_input(driver, "Enter the city", "Limassol")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"

    close_modal_if_open(driver)


@allure.feature("Companies SB Forms")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_companies_ask_question_submit_endpoint_sb(driver):
    page = CompaniesPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Ask Us a Question", required_placeholder="qwerty@allsports.by")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Bot")
    fill_modal_input(driver, "Enter phone number", "+357 00 00 00 00")
    fill_modal_input(driver, "qwerty@allsports.by", "qa.ask.companies@example.com")
    fill_modal_textarea(driver, "Question from companies page")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    urls = submit_modal_and_collect_contact_urls(driver)
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )

    close_modal_if_open(driver)

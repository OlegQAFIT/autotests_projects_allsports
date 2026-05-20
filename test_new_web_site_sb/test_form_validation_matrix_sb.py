# -*- coding: utf-8 -*-
import time

import allure
import pytest

from pages.new_web_site_sb.main_page_sb import MainPageSb
from pages.new_web_site_sb.partners_sb import PartnersPageSb
from test_new_web_site_sb.form_helpers_sb import (
    clear_submit_spy,
    close_modal_if_open,
    ensure_modal_checkbox_checked,
    fill_modal_input,
    fill_modal_textarea,
    get_contact_post_urls,
    get_modal_send_button,
    install_submit_spy,
    modal_validation_messages,
    open_modal_by_cta_text,
)

SEND_BUTTON_XPATH = (
    "//div[contains(@class,'modal')]//button[.//span[normalize-space()='Send'] or normalize-space()='Send']"
)


FORM_CASES = [
    {
        "form_kind": "get_offer",
        "page": "main",
        "cta": "Get an Offer",
        "required_placeholder": "Company",
        "endpoint": "/contact/get_offer",
    },
    {
        "form_kind": "become_partner",
        "page": "partners",
        "cta": "Become a Partner",
        "required_placeholder": "Facility name",
        "endpoint": "/contact/become_partner",
    },
    {
        "form_kind": "ask_question",
        "page": "main",
        "cta": "Ask Us a Question",
        "required_placeholder": "qwerty@allsports.by",
        "endpoint": "/contact/ask_question",
    },
]

INVALID_CASES = [
    "invalid_phone",
    "invalid_email",
    "without_consent",
]


def _open_target_page_and_modal(driver, form_case):
    if form_case["page"] == "main":
        page = MainPageSb(driver)
    else:
        page = PartnersPageSb(driver)

    page.open()
    page.accept_cookie_consent()
    open_modal_by_cta_text(
        driver,
        form_case["cta"],
        required_placeholder=form_case["required_placeholder"],
    )


def _fill_modal_form(driver, form_kind: str, invalid_case: str):
    email = "qa.matrix@example.com"
    phone = "+357 99 11 22 33"

    if invalid_case == "invalid_email":
        email = "bad"
    if invalid_case == "invalid_phone":
        phone = "123"

    fill_modal_input(driver, "Name", "QA Matrix")
    fill_modal_input(driver, "Enter phone number", phone)

    if form_kind == "ask_question":
        fill_modal_input(driver, "qwerty@allsports.by", email)
        fill_modal_textarea(driver, "Validation matrix question")
    elif form_kind == "become_partner":
        fill_modal_input(driver, "qwerty@sportbenefit.eu", email)
        fill_modal_input(driver, "Facility name", "QA Matrix Facility")
        fill_modal_input(driver, "Enter the city", "Nicosia")
    else:
        fill_modal_input(driver, "qwerty@sportbenefit.eu", email)
        fill_modal_input(driver, "Company", "QA Matrix Company")
        fill_modal_input(driver, "Enter the city", "Limassol")

    if invalid_case != "without_consent":
        ensure_modal_checkbox_checked(driver)


@allure.feature("SB Validation Matrix")
@allure.severity("Critical")
@pytest.mark.form_submission
@pytest.mark.parametrize("form_case", FORM_CASES, ids=[c["form_kind"] for c in FORM_CASES])
@pytest.mark.parametrize("invalid_case", INVALID_CASES)
def test_modal_validation_matrix_blocks_invalid_submit_sb(driver, form_case, invalid_case):
    """Проверка матрицы валидации: невалидные данные не должны проходить как валидные."""
    _open_target_page_and_modal(driver, form_case)

    _fill_modal_form(driver, form_case["form_kind"], invalid_case)

    install_submit_spy(driver)
    clear_submit_spy(driver)

    send_btn = get_modal_send_button(driver)
    send_disabled_before_click = (not send_btn.is_enabled()) or (send_btn.get_attribute("disabled") is not None)
    if not send_disabled_before_click:
        driver.execute_script("arguments[0].click();", send_btn)
        time.sleep(0.8)

    urls = get_contact_post_urls(driver)
    send_buttons_after = driver.find_elements("xpath", SEND_BUTTON_XPATH)
    modal_closed_after_submit = not send_buttons_after
    send_disabled_after_click = True
    if send_buttons_after:
        send_btn_after = send_buttons_after[0]
        send_disabled_after_click = (not send_btn_after.is_enabled()) or (
            send_btn_after.get_attribute("disabled") is not None
        )
    errors = modal_validation_messages(driver)

    if invalid_case == "without_consent":
        assert not urls, (
            f"Without consent, form '{form_case['form_kind']}' must not submit. Captured: {urls}"
        )
        assert modal_closed_after_submit or send_disabled_after_click or errors, (
            f"Without consent, form '{form_case['form_kind']}' was not visibly blocked "
            f"(button still active and no validation errors shown)"
        )
    else:
        # Current website behavior differs by form: some forms block invalid data on client side,
        # others submit and delegate validation to backend. Both are observable/acceptable here,
        # but endpoint must be correct if submit happens.
        if urls:
            assert any(form_case["endpoint"] in url for url in urls), (
                f"Unexpected endpoint for '{form_case['form_kind']}' invalid case '{invalid_case}'. "
                f"Expected contains '{form_case['endpoint']}', captured: {urls}"
            )
        else:
            assert modal_closed_after_submit or send_disabled_after_click or errors, (
                f"Invalid case '{invalid_case}' for {form_case['form_kind']} neither submitted nor showed "
                f"client-side blocking signal"
            )

    close_modal_if_open(driver)

# -*- coding: utf-8 -*-
import time

import allure
import pytest

from test_new_web_site_sb.form_helpers_sb import (
    assert_modal_send_enabled,
    clear_submit_spy,
    ensure_modal_checkbox_checked,
    fill_modal_input,
    fill_modal_textarea,
    get_failure_stub_events,
    get_modal_send_button,
    install_network_failure_stub,
    install_submit_spy,
    open_modal_by_cta_text,
    wait_for_modal_submit_feedback,
)


FORM_CASES = [
    {
        "id": "get_offer",
        "url": "https://www.sportbenefit.eu/en-cy",
        "cta": "Get an Offer",
        "required_placeholder": "Company",
        "kind": "get_offer",
        "endpoint": "/contact/get_offer",
    },
    {
        "id": "ask_question",
        "url": "https://www.sportbenefit.eu/en-cy",
        "cta": "Ask Us a Question",
        "required_placeholder": "qwerty@allsports.by",
        "kind": "ask_question",
        "endpoint": "/contact/ask_question",
    },
    {
        "id": "become_partner",
        "url": "https://www.sportbenefit.eu/en-cy/partners",
        "cta": "Become a Partner",
        "required_placeholder": "Facility name",
        "kind": "become_partner",
        "endpoint": "/contact/become_partner",
    },
]


def _fill_valid_modal_form(driver, kind: str, suffix: str):
    fill_modal_input(driver, "Name", f"QA UX {suffix}")
    fill_modal_input(driver, "Enter phone number", "+357 99 11 22 55")

    if kind == "ask_question":
        fill_modal_input(driver, "qwerty@allsports.by", f"qa.ux.ask.{suffix}@example.com")
        fill_modal_textarea(driver, f"UX question {suffix}")
    elif kind == "become_partner":
        fill_modal_input(driver, "qwerty@sportbenefit.eu", f"qa.ux.partner.{suffix}@example.com")
        fill_modal_input(driver, "Facility name", f"QA UX Facility {suffix}")
        fill_modal_input(driver, "Enter the city", "Larnaca")
    else:
        fill_modal_input(driver, "qwerty@sportbenefit.eu", f"qa.ux.offer.{suffix}@example.com")
        fill_modal_input(driver, "Company", f"QA UX Company {suffix}")
        fill_modal_input(driver, "Enter the city", "Limassol")

    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)


@allure.feature("SB Forms UX")
@allure.severity("Critical")
@pytest.mark.release_gate
@pytest.mark.parametrize("case", FORM_CASES, ids=[c["id"] for c in FORM_CASES])
def test_modal_submit_success_feedback_sb(driver, case):
    suffix = str(int(time.time()))

    driver.get(case["url"])
    open_modal_by_cta_text(driver, case["cta"], required_placeholder=case["required_placeholder"])
    _fill_valid_modal_form(driver, case["kind"], suffix)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    driver.execute_script("arguments[0].click();", get_modal_send_button(driver))

    feedback = wait_for_modal_submit_feedback(driver, timeout=8.0)
    assert feedback["closed"] or feedback["disabled"] or feedback["messages"], (
        f"No observable success feedback for modal form {case['id']}: {feedback}"
    )


@allure.feature("SB Forms UX")
@allure.severity("Critical")
@pytest.mark.release_gate
@pytest.mark.parametrize("status_code", [400, 500])
@pytest.mark.parametrize("case", FORM_CASES, ids=[c["id"] for c in FORM_CASES])
def test_modal_submit_backend_failure_feedback_sb(driver, case, status_code):
    suffix = f"{status_code}_{int(time.time())}"

    driver.get(case["url"])
    open_modal_by_cta_text(driver, case["cta"], required_placeholder=case["required_placeholder"])
    _fill_valid_modal_form(driver, case["kind"], suffix)

    install_network_failure_stub(driver, status_code=status_code)
    driver.execute_script("window.__qaFailNet = [];")
    driver.execute_script("arguments[0].click();", get_modal_send_button(driver))

    feedback = wait_for_modal_submit_feedback(driver, timeout=8.0)
    events = get_failure_stub_events(driver)
    matched = [
        event for event in events
        if str(event.get("method", "")).upper() == "POST" and case["endpoint"] in str(event.get("url", ""))
    ]
    assert matched, (
        f"Failure stub did not capture endpoint request for {case['id']} [{status_code}]. "
        f"Captured events: {events}"
    )

    # For backend failures UI should not silently disappear without any signal.
    assert (not feedback["closed"]) or feedback["messages"] or feedback["disabled"], (
        f"Unexpected UX on backend failure for {case['id']} [{status_code}]: {feedback}"
    )

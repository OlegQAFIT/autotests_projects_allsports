# -*- coding: utf-8 -*-
import time
from urllib.parse import urlparse

import allure
import pytest

from test_new_web_site_sb.form_helpers_sb import (
    accept_cookie_if_present,
    assert_modal_send_disabled,
    assert_modal_send_enabled,
    clear_real_network_probe,
    ensure_modal_checkbox_checked,
    fill_inline_contacts_values,
    fill_modal_input,
    fill_modal_textarea,
    get_modal_send_button,
    inline_submit_button,
    inline_success_state,
    install_real_network_probe,
    open_modal_by_cta_text,
    wait_for_contact_network_events,
    wait_for_modal_submit_feedback,
)


pytestmark = [pytest.mark.live_api, pytest.mark.release_gate]


FORM_CASES = [
    {
        "id": "main_get_offer",
        "path": "/en-cy",
        "cta": "Get an Offer",
        "required_placeholder": "Company",
        "endpoint": "/contact/get_offer",
        "kind": "get_offer",
    },
    {
        "id": "main_ask_question",
        "path": "/en-cy",
        "cta": "Ask Us a Question",
        "required_placeholder": "qwerty@allsports.by",
        "endpoint": "/contact/ask_question",
        "kind": "ask_question",
    },
    {
        "id": "partners_become_partner",
        "path": "/en-cy/partners",
        "cta": "Become a Partner",
        "required_placeholder": "Facility name",
        "endpoint": "/contact/become_partner",
        "kind": "become_partner",
    },
    {
        "id": "companies_get_offer",
        "path": "/en-cy/companies",
        "cta": "Get an Offer",
        "required_placeholder": "Company",
        "endpoint": "/contact/get_offer",
        "kind": "get_offer",
    },
    {
        "id": "contacts_get_offer",
        "path": "/en-cy/contacts",
        "cta": "Get an Offer",
        "required_placeholder": "Company",
        "endpoint": "/contact/get_offer",
        "kind": "get_offer",
    },
    {
        "id": "contacts_ask_question",
        "path": "/en-cy/contacts",
        "cta": "Ask Us a Question",
        "required_placeholder": "qwerty@allsports.by",
        "endpoint": "/contact/ask_question",
        "kind": "ask_question",
    },
]


def _require_staging_base(request):
    base_url = request.config.getoption("--base-url").rstrip("/")
    parsed = urlparse(base_url)
    host = (parsed.netloc or "").lower()

    if "sportbenefit" not in host or "staging" not in host:
        pytest.skip(
            "UI live form E2E is allowed only on staging SportBenefit hosts. "
            f"Current --base-url host: {host or '<empty>'}"
        )

    return f"{parsed.scheme}://{parsed.netloc}".rstrip("/")


def _fill_modal_form_for_case(driver, case_kind: str, suffix: str):
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", f"QA Live {suffix}")
    fill_modal_input(driver, "Enter phone number", "+357 99 11 22 33")

    if case_kind == "ask_question":
        fill_modal_input(driver, "qwerty@allsports.by", f"qa.live.ask.{suffix}@example.com")
        fill_modal_textarea(driver, f"Live ask-question check {suffix}")
    elif case_kind == "become_partner":
        fill_modal_input(driver, "qwerty@sportbenefit.eu", f"qa.live.partner.{suffix}@example.com")
        fill_modal_input(driver, "Facility name", f"QA Facility {suffix}")
        fill_modal_input(driver, "Enter the city", "Nicosia")
    else:
        fill_modal_input(driver, "qwerty@sportbenefit.eu", f"qa.live.offer.{suffix}@example.com")
        fill_modal_input(driver, "Company", f"QA Company {suffix}")
        fill_modal_input(driver, "Enter the city", "Limassol")

    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)


@allure.feature("SB Live UI E2E")
@allure.severity("Blocker")
@pytest.mark.parametrize("case", FORM_CASES, ids=[c["id"] for c in FORM_CASES])
def test_modal_forms_live_e2e_submit_and_response_sb(request, driver, case):
    base = _require_staging_base(request)
    stamp = str(int(time.time()))

    driver.get(f"{base}{case['path']}")
    accept_cookie_if_present(driver)

    open_modal_by_cta_text(driver, case["cta"], required_placeholder=case["required_placeholder"])
    _fill_modal_form_for_case(driver, case["kind"], stamp)

    install_real_network_probe(driver)
    clear_real_network_probe(driver)

    send_button = get_modal_send_button(driver)
    driver.execute_script("arguments[0].click();", send_button)

    events = wait_for_contact_network_events(driver, case["endpoint"], timeout=30.0)
    assert events, f"No real POST event captured for endpoint {case['endpoint']}"

    last_event = events[-1]
    status = int(last_event.get("status") or 0)
    assert status in (200, 201, 202, 204), (
        f"Unexpected response status for {case['endpoint']}: {status}, event={last_event}"
    )

    response_text = str(last_event.get("responseText") or "").lower()
    assert "<!doctype html" not in response_text, (
        f"Expected API response, got HTML for {case['endpoint']}: {(response_text or '')[:240]}"
    )

    feedback = wait_for_modal_submit_feedback(driver, timeout=12.0)
    assert feedback["closed"] or feedback["disabled"] or feedback["messages"], (
        f"No observable post-submit feedback for case {case['id']}: {feedback}"
    )


@allure.feature("SB Live UI E2E")
@allure.severity("Critical")
def test_contacts_inline_form_live_e2e_submit_and_response_sb(request, driver):
    base = _require_staging_base(request)
    stamp = str(int(time.time()))

    driver.get(f"{base}/en-cy/contacts")
    accept_cookie_if_present(driver)

    fill_inline_contacts_values(
        driver,
        name=f"QA Inline {stamp}",
        phone="+357 99 11 22 44",
        email=f"qa.inline.{stamp}@example.com",
        company=f"QA Inline Co {stamp}",
    )

    install_real_network_probe(driver)
    clear_real_network_probe(driver)

    submit = inline_submit_button(driver)
    driver.execute_script("arguments[0].click();", submit)

    events = wait_for_contact_network_events(driver, "/contact/get_offer", timeout=30.0)
    assert events, "No real POST event captured for inline /contact/get_offer"

    last_event = events[-1]
    status = int(last_event.get("status") or 0)
    assert status in (200, 201, 202, 204), (
        f"Unexpected inline response status: {status}, event={last_event}"
    )

    assert inline_success_state(driver), "No observable inline success state after live submit"

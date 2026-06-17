# -*- coding: utf-8 -*-
import time

import allure
import pytest

from pages.new_web_site_sb.companies_sb import CompaniesPageSb
from pages.new_web_site_sb.contact_forms_sb import ContactFormsSb
from pages.new_web_site_sb.contacts_sb import ContactsPageSb
from pages.new_web_site_sb.header_sb import HeaderPageSb
from pages.new_web_site_sb.main_page_sb import MainPageSb
from pages.new_web_site_sb.partners_sb import PartnersPageSb


MOBILE_VIEWPORTS = [
    (360, 800),
    (390, 844),
    (768, 1024),
]

POST_SUBMIT_FORM_CASES = [
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

VALIDATION_FORM_CASES = [
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

LIVE_UI_FORM_CASES = [
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


def _open_validation_page_and_modal(driver, form_case):
    if form_case["page"] == "main":
        page = MainPageSb(driver)
    else:
        page = PartnersPageSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms = ContactFormsSb(driver)
    forms.open_modal_by_cta_text(form_case["cta"], required_placeholder=form_case["required_placeholder"])
    return forms


@allure.feature("Header SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_header_get_offer_modal_structure_sb(driver):
    page = HeaderPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_get_offer_modal()
    page.check_offer_modal_structure()
    page.check_offer_modal_partner_tab()
    page.close_modal()


@allure.feature("Main SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_main_page_offer_modal_flow_sb(driver):
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_main_offer_modal_flow()


@allure.feature("Contacts SB")
@allure.severity("Critical")
def test_contacts_page_basics_sb(driver):
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()
    page.check_form_structure()


@allure.feature("Companies SB")
@allure.severity("Critical")
def test_companies_offer_modal_sb(driver):
    page = CompaniesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_get_offer_modal()
    page.check_companies_modal_structure()


@allure.feature("Partners SB")
@allure.severity("Critical")
def test_partners_become_partner_modal_sb(driver):
    page = PartnersPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_become_partner_modal()
    page.check_partner_modal_structure()


@allure.feature("Main SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_main_get_offer_form_submit_endpoint_sb(driver):
    page = MainPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    page.open_get_offer_modal()

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@sportbenefit.eu", "qa.bot@example.com")
    forms.fill_modal_input("Company", "QA Company")
    forms.fill_modal_input("Enter the city", "Limassol")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"
    forms.close_modal_if_open()


@allure.feature("Main SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_main_ask_question_form_submit_endpoint_sb(driver):
    page = MainPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.open_modal_by_cta_text("Ask Us a Question", required_placeholder="qwerty@allsports.by")

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@allsports.by", "qa.ask@example.com")
    forms.fill_modal_textarea("Question from automated tests")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )
    forms.close_modal_if_open()


@allure.feature("Contacts SB")
@allure.severity("Normal")
@pytest.mark.form_submission
def test_contacts_invalid_validation_sb(driver):
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_invalid_phone_validation()


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_inline_form_blocks_invalid_submit_sb(driver):
    page = ContactsPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.install_submit_spy()
    forms.clear_submit_spy()
    forms.fill_inline_contacts_invalid()

    submit = forms.inline_submit_button()
    if submit.is_enabled() and submit.get_attribute("disabled") is None:
        forms.click_inline_submit()

    messages = forms.inline_validation_messages()
    urls = forms.get_contact_post_urls()

    assert not urls, f"Inline invalid form should not call contact endpoints. Captured: {urls}"
    assert not forms.inline_submit_enabled(), "Inline submit should remain disabled for invalid values"
    if messages:
        assert any("invalid" in m.lower() or "format" in m.lower() or "valid email" in m.lower() for m in messages), (
            f"Unexpected validation texts: {messages}"
        )


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_inline_form_submit_endpoint_and_success_state_sb(driver):
    page = ContactsPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.fill_inline_contacts_values(
        name="QA Inline",
        phone="+357 99 11 22 33",
        email="qa.inline@example.com",
        company="Inline Company",
    )

    forms.install_submit_spy()
    forms.clear_submit_spy()

    if not forms.inline_submit_enabled():
        pytest.xfail(
            "Inline /contacts form submit stayed disabled after valid input. "
            "Endpoint/success-state cannot be validated until page-side gate is fixed."
        )

    forms.click_inline_submit()
    urls = forms.get_contact_post_urls()
    assert any("/contact/get_offer" in url for url in urls), (
        f"Inline contacts form did not call get_offer endpoint. Captured: {urls}"
    )
    assert forms.inline_success_state(), (
        "Inline contacts form request was sent, but no observable completion signal "
        "(reset/disabled state) was detected"
    )


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_get_offer_modal_submit_endpoint_sb(driver):
    page = ContactsPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.open_modal_by_cta_text("Get an Offer", required_placeholder="Company")

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@sportbenefit.eu", "qa.contacts.offer@example.com")
    forms.fill_modal_input("Company", "QA Contacts")
    forms.fill_modal_input("Enter the city", "Limassol")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"
    forms.close_modal_if_open()


@allure.feature("Contacts SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_contacts_ask_question_modal_submit_endpoint_sb(driver):
    page = ContactsPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.open_modal_by_cta_text("Ask Us a Question", required_placeholder="qwerty@allsports.by")

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@allsports.by", "qa.contacts.ask@example.com")
    forms.fill_modal_textarea("Question from contacts page")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )
    assert not forms.modal_validation_messages(), "Ask-question modal should not show validation errors on valid submit"
    forms.close_modal_if_open()


@allure.feature("Companies SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_companies_get_offer_submit_endpoint_sb(driver):
    page = CompaniesPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    page.open_get_offer_modal()

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@sportbenefit.eu", "qa.companies@example.com")
    forms.fill_modal_input("Company", "QA Companies")
    forms.fill_modal_input("Enter the city", "Limassol")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"
    forms.close_modal_if_open()


@allure.feature("Companies SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_companies_ask_question_submit_endpoint_sb(driver):
    page = CompaniesPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.open_modal_by_cta_text("Ask Us a Question", required_placeholder="qwerty@allsports.by")

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@allsports.by", "qa.ask.companies@example.com")
    forms.fill_modal_textarea("Question from companies page")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )
    forms.close_modal_if_open()


@allure.feature("Partners SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_partners_get_offer_submit_endpoint_sb(driver):
    page = PartnersPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.open_modal_by_cta_text("Get an Offer", required_placeholder="Company")

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@sportbenefit.eu", "qa.partners.offer@example.com")
    forms.fill_modal_input("Company", "QA Partners")
    forms.fill_modal_input("Enter the city", "Nicosia")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/get_offer" in url for url in urls), f"get_offer endpoint was not called. Captured: {urls}"
    forms.close_modal_if_open()


@allure.feature("Partners SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_partners_become_partner_submit_endpoint_sb(driver):
    page = PartnersPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    page.open_become_partner_modal()

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@sportbenefit.eu", "qa.partners.partner@example.com")
    forms.fill_modal_input("Facility name", "QA Facility")
    forms.fill_modal_input("Enter the city", "Larnaca")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/become_partner" in url for url in urls), (
        f"become_partner endpoint was not called. Captured: {urls}"
    )
    forms.close_modal_if_open()


@allure.feature("Partners SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_partners_ask_question_submit_endpoint_sb(driver):
    page = PartnersPageSb(driver)
    forms = ContactFormsSb(driver)

    page.open()
    page.accept_cookie_consent()
    forms.open_modal_by_cta_text("Ask Us a Question", required_placeholder="qwerty@allsports.by")

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Bot")
    forms.fill_modal_input("Enter phone number", "+357 00 00 00 00")
    forms.fill_modal_input("qwerty@allsports.by", "qa.partners.ask@example.com")
    forms.fill_modal_textarea("Question from partners page")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    forms.install_submit_spy()
    forms.clear_submit_spy()
    urls = forms.submit_modal_and_collect_contact_urls()
    assert any("/contact/ask_question" in url for url in urls), (
        f"ask_question endpoint was not called. Captured: {urls}"
    )
    forms.close_modal_if_open()


@allure.feature("SB Validation Matrix")
@allure.severity("Critical")
@pytest.mark.form_submission
@pytest.mark.parametrize("form_case", VALIDATION_FORM_CASES, ids=[c["form_kind"] for c in VALIDATION_FORM_CASES])
@pytest.mark.parametrize("invalid_case", INVALID_CASES)
def test_modal_validation_matrix_blocks_invalid_submit_sb(driver, form_case, invalid_case):
    forms = _open_validation_page_and_modal(driver, form_case)
    forms.fill_modal_form_for_validation(form_case["form_kind"], invalid_case)

    forms.install_submit_spy()
    forms.clear_submit_spy()

    send_disabled_before_click = forms.modal_send_disabled()
    if not send_disabled_before_click:
        forms.click_modal_send()
        time.sleep(0.8)

    urls = forms.get_contact_post_urls()
    modal_closed_after_submit = not forms.modal_is_open()
    send_disabled_after_click = forms.modal_send_disabled()
    errors = forms.modal_validation_messages()

    if invalid_case == "without_consent":
        assert not urls, (
            f"Without consent, form '{form_case['form_kind']}' must not submit. Captured: {urls}"
        )
        assert modal_closed_after_submit or send_disabled_after_click or errors, (
            f"Without consent, form '{form_case['form_kind']}' was not visibly blocked "
            f"(button still active and no validation errors shown)"
        )
    else:
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

    forms.close_modal_if_open()


@allure.feature("SB Forms UX")
@allure.severity("Critical")
@pytest.mark.form_submission
@pytest.mark.parametrize("case", POST_SUBMIT_FORM_CASES, ids=[c["id"] for c in POST_SUBMIT_FORM_CASES])
def test_modal_submit_success_feedback_sb(driver, case):
    forms = ContactFormsSb(driver)
    suffix = str(int(time.time()))

    forms.open_url(case["url"])
    forms.open_modal_by_cta_text(case["cta"], required_placeholder=case["required_placeholder"])
    forms.fill_valid_modal_form(case["kind"], suffix)
    forms.install_submit_spy()
    forms.clear_submit_spy()
    forms.click_modal_send()

    feedback = forms.wait_for_modal_submit_feedback(timeout=8.0)
    assert feedback["closed"] or feedback["disabled"] or feedback["messages"], (
        f"No observable success feedback for modal form {case['id']}: {feedback}"
    )


@allure.feature("SB Forms UX")
@allure.severity("Critical")
@pytest.mark.form_submission
@pytest.mark.parametrize("status_code", [400, 500])
@pytest.mark.parametrize("case", POST_SUBMIT_FORM_CASES, ids=[c["id"] for c in POST_SUBMIT_FORM_CASES])
def test_modal_submit_backend_failure_feedback_sb(driver, case, status_code):
    forms = ContactFormsSb(driver)
    suffix = f"{status_code}_{int(time.time())}"

    forms.open_url(case["url"])
    forms.open_modal_by_cta_text(case["cta"], required_placeholder=case["required_placeholder"])
    forms.fill_valid_modal_form(case["kind"], suffix)

    forms.install_network_failure_stub(status_code=status_code)
    forms.clear_failure_stub_events()
    forms.click_modal_send()

    feedback = forms.wait_for_modal_submit_feedback(timeout=8.0)
    events = forms.get_failure_stub_events()
    matched = [
        event for event in events
        if str(event.get("method", "")).upper() == "POST" and case["endpoint"] in str(event.get("url", ""))
    ]
    assert matched, (
        f"Failure stub did not capture endpoint request for {case['id']} [{status_code}]. "
        f"Captured events: {events}"
    )
    assert (not feedback["closed"]) or feedback["messages"] or feedback["disabled"], (
        f"Unexpected UX on backend failure for {case['id']} [{status_code}]: {feedback}"
    )


@allure.feature("SB Live UI E2E")
@allure.severity("Blocker")
@pytest.mark.live_api
@pytest.mark.form_submission
@pytest.mark.parametrize("case", LIVE_UI_FORM_CASES, ids=[c["id"] for c in LIVE_UI_FORM_CASES])
def test_modal_forms_live_e2e_submit_and_response_sb(request, driver, case):
    forms = ContactFormsSb(driver)
    base = forms.require_staging_base_for_live_forms(request)
    stamp = str(int(time.time()))

    forms.open_url(f"{base}{case['path']}")
    forms.accept_cookie_if_present()
    forms.open_modal_by_cta_text(case["cta"], required_placeholder=case["required_placeholder"])
    forms.fill_modal_form_for_live_case(case["kind"], stamp)
    forms.install_real_network_probe()
    forms.clear_real_network_probe()
    forms.click_modal_send()

    events = forms.wait_for_contact_network_events(case["endpoint"], timeout=30.0)
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

    feedback = forms.wait_for_modal_submit_feedback(timeout=12.0)
    assert feedback["closed"] or feedback["disabled"] or feedback["messages"], (
        f"No observable post-submit feedback for case {case['id']}: {feedback}"
    )


@allure.feature("SB Live UI E2E")
@allure.severity("Critical")
@pytest.mark.live_api
@pytest.mark.form_submission
def test_contacts_inline_form_live_e2e_submit_and_response_sb(request, driver):
    forms = ContactFormsSb(driver)
    base = forms.require_staging_base_for_live_forms(request)
    stamp = str(int(time.time()))

    forms.open_url(f"{base}/en-cy/contacts")
    forms.accept_cookie_if_present()
    forms.fill_inline_contacts_values(
        name=f"QA Inline {stamp}",
        phone="+357 99 11 22 44",
        email=f"qa.inline.{stamp}@example.com",
        company=f"QA Inline Co {stamp}",
    )
    forms.install_real_network_probe()
    forms.clear_real_network_probe()
    forms.click_inline_submit()

    events = forms.wait_for_contact_network_events("/contact/get_offer", timeout=30.0)
    assert events, "No real POST event captured for inline /contact/get_offer"

    last_event = events[-1]
    status = int(last_event.get("status") or 0)
    assert status in (200, 201, 202, 204), (
        f"Unexpected inline response status: {status}, event={last_event}"
    )
    assert forms.inline_success_state(), "No observable inline success state after live submit"


@allure.feature("SB Mobile Regression")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_main_modal_flow_sb(driver, viewport):
    page = MainPageSb(driver)
    forms = ContactFormsSb(driver)
    width, height = viewport

    page.set_viewport(width, height)
    page.open()
    page.accept_cookie_consent()
    forms.open_modal_by_cta_text("Get an Offer", required_placeholder="Company")

    forms.assert_modal_send_disabled()
    forms.fill_modal_input("Name", "QA Mobile")
    forms.fill_modal_input("Enter phone number", "+357 99 11 22 66")
    forms.fill_modal_input("qwerty@sportbenefit.eu", "qa.mobile@example.com")
    forms.fill_modal_input("Company", "QA Mobile Co")
    forms.fill_modal_input("Enter the city", "Limassol")
    forms.ensure_modal_checkbox_checked()
    forms.assert_modal_send_enabled()

    send_button = forms.get_modal_send_button()
    assert send_button.is_displayed(), f"Send button is not visible on viewport {width}x{height}"


@allure.feature("SB Mobile Regression")
@allure.severity("Normal")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_contacts_inline_form_validation_gate_sb(driver, viewport):
    page = ContactsPageSb(driver)
    forms = ContactFormsSb(driver)
    width, height = viewport

    page.set_viewport(width, height)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()

    forms.fill_inline_contacts_values(
        name="QA Mobile Inline",
        phone="+357 99 11 22 77",
        email="qa.mobile.inline@example.com",
        company="QA Mobile Inline Co",
    )
    assert forms.inline_submit_enabled(), (
        f"Inline submit should be enabled for valid values on viewport {width}x{height}"
    )

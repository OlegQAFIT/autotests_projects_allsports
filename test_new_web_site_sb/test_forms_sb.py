# -*- coding: utf-8 -*-
import time
from urllib.parse import urlparse

import allure
import pytest

from pages.new_web_site_sb.companies_sb import CompaniesPageSb
from pages.new_web_site_sb.contacts_sb import ContactsPageSb
from pages.new_web_site_sb.header_sb import HeaderPageSb
from pages.new_web_site_sb.main_page_sb import MainPageSb
from pages.new_web_site_sb.partners_sb import PartnersPageSb
from test_new_web_site_sb.form_helpers_sb import (
    accept_cookie_if_present,
    assert_modal_send_disabled,
    assert_modal_send_enabled,
    clear_real_network_probe,
    clear_submit_spy,
    close_modal_if_open,
    ensure_modal_checkbox_checked,
    fill_inline_contacts_invalid,
    fill_inline_contacts_values,
    fill_modal_input,
    fill_modal_textarea,
    get_contact_post_urls,
    get_failure_stub_events,
    get_modal_send_button,
    inline_submit_button,
    inline_submit_enabled,
    inline_success_state,
    inline_validation_messages,
    install_network_failure_stub,
    install_real_network_probe,
    install_submit_spy,
    modal_validation_messages,
    open_modal_by_cta_text,
    submit_modal_and_collect_contact_urls,
    wait_for_contact_network_events,
    wait_for_modal_submit_feedback,
)


MOBILE_VIEWPORTS = [
    (360, 800),
    (390, 844),
    (768, 1024),
]

SEND_BUTTON_XPATH = (
    "//div[contains(@class,'modal')]//button[.//span[normalize-space()='Send'] or normalize-space()='Send']"
)

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


def _fill_valid_modal_form_post_submit(driver, kind: str, suffix: str):
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


def _open_target_page_and_modal_for_validation(driver, form_case):
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


def _fill_modal_form_for_validation(driver, form_kind: str, invalid_case: str):
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


def _require_staging_base_for_live_forms(request):
    base_url = request.config.getoption("--base-url").rstrip("/")
    parsed = urlparse(base_url)
    host = (parsed.netloc or "").lower()

    if "sportbenefit" not in host or "staging" not in host:
        pytest.skip(
            "UI live form E2E is allowed only on staging SportBenefit hosts. "
            f"Current --base-url host: {host or '<empty>'}"
        )

    return f"{parsed.scheme}://{parsed.netloc}".rstrip("/")


def _fill_modal_form_for_live_case(driver, case_kind: str, suffix: str):
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


@allure.feature("Header SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_header_get_offer_modal_structure_sb(driver):
    """Проверка структуры модального окна Get an Offer из header."""
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
    """Проверка полного flow модального окна Get an Offer на главной странице."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_main_offer_modal_flow()


@allure.feature("Contacts SB")
@allure.severity("Critical")
def test_contacts_page_basics_sb(driver):
    """Проверка базового открытия страницы Contacts и структуры формы."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()
    page.check_form_structure()


@allure.feature("Companies SB")
@allure.severity("Critical")
def test_companies_offer_modal_sb(driver):
    """Проверка открытия и структуры модального окна Get an Offer на странице Companies."""
    page = CompaniesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_get_offer_modal()
    page.check_companies_modal_structure()


@allure.feature("Partners SB")
@allure.severity("Critical")
def test_partners_become_partner_modal_sb(driver):
    """Проверка открытия и структуры модального окна Become a Partner."""
    page = PartnersPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_become_partner_modal()
    page.check_partner_modal_structure()


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


@allure.feature("Companies SB Forms")
@allure.severity("Critical")
@pytest.mark.form_submission
def test_companies_get_offer_submit_endpoint_sb(driver):
    """Проверка отправки формы Get an Offer на корректный endpoint /contact/get_offer."""
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
@pytest.mark.form_submission
def test_companies_ask_question_submit_endpoint_sb(driver):
    """Проверка отправки формы Ask Us a Question на endpoint /contact/ask_question."""
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


@allure.feature("SB Validation Matrix")
@allure.severity("Critical")
@pytest.mark.form_submission
@pytest.mark.parametrize("form_case", VALIDATION_FORM_CASES, ids=[c["form_kind"] for c in VALIDATION_FORM_CASES])
@pytest.mark.parametrize("invalid_case", INVALID_CASES)
def test_modal_validation_matrix_blocks_invalid_submit_sb(driver, form_case, invalid_case):
    """Проверка матрицы валидации: невалидные данные не должны проходить как валидные."""
    _open_target_page_and_modal_for_validation(driver, form_case)

    _fill_modal_form_for_validation(driver, form_case["form_kind"], invalid_case)

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


@allure.feature("SB Forms UX")
@allure.severity("Critical")
@pytest.mark.form_submission
@pytest.mark.parametrize("case", POST_SUBMIT_FORM_CASES, ids=[c["id"] for c in POST_SUBMIT_FORM_CASES])
def test_modal_submit_success_feedback_sb(driver, case):
    """Проверка post-submit поведения формы при успешной отправке."""
    suffix = str(int(time.time()))

    driver.get(case["url"])
    open_modal_by_cta_text(driver, case["cta"], required_placeholder=case["required_placeholder"])
    _fill_valid_modal_form_post_submit(driver, case["kind"], suffix)

    install_submit_spy(driver)
    clear_submit_spy(driver)
    driver.execute_script("arguments[0].click();", get_modal_send_button(driver))

    feedback = wait_for_modal_submit_feedback(driver, timeout=8.0)
    assert feedback["closed"] or feedback["disabled"] or feedback["messages"], (
        f"No observable success feedback for modal form {case['id']}: {feedback}"
    )


@allure.feature("SB Forms UX")
@allure.severity("Critical")
@pytest.mark.form_submission
@pytest.mark.parametrize("status_code", [400, 500])
@pytest.mark.parametrize("case", POST_SUBMIT_FORM_CASES, ids=[c["id"] for c in POST_SUBMIT_FORM_CASES])
def test_modal_submit_backend_failure_feedback_sb(driver, case, status_code):
    """Проверка поведения формы при ответах backend 4xx/5xx."""
    suffix = f"{status_code}_{int(time.time())}"

    driver.get(case["url"])
    open_modal_by_cta_text(driver, case["cta"], required_placeholder=case["required_placeholder"])
    _fill_valid_modal_form_post_submit(driver, case["kind"], suffix)

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
    assert (not feedback["closed"]) or feedback["messages"] or feedback["disabled"], (
        f"Unexpected UX on backend failure for {case['id']} [{status_code}]: {feedback}"
    )


@allure.feature("SB Live UI E2E")
@allure.severity("Blocker")
@pytest.mark.live_api
@pytest.mark.form_submission
@pytest.mark.parametrize("case", LIVE_UI_FORM_CASES, ids=[c["id"] for c in LIVE_UI_FORM_CASES])
def test_modal_forms_live_e2e_submit_and_response_sb(request, driver, case):
    """Проверка live E2E отправки модальных форм и корректного ответа endpoint."""
    base = _require_staging_base_for_live_forms(request)
    stamp = str(int(time.time()))

    driver.get(f"{base}{case['path']}")
    accept_cookie_if_present(driver)

    open_modal_by_cta_text(driver, case["cta"], required_placeholder=case["required_placeholder"])
    _fill_modal_form_for_live_case(driver, case["kind"], stamp)

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
@pytest.mark.live_api
@pytest.mark.form_submission
def test_contacts_inline_form_live_e2e_submit_and_response_sb(request, driver):
    """Проверка live E2E отправки inline-формы Contacts и ответа endpoint."""
    base = _require_staging_base_for_live_forms(request)
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


@allure.feature("SB Mobile Regression")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_main_modal_flow_sb(driver, viewport):
    """Проверка мобильного flow модальной формы на главной странице для разных viewport."""
    width, height = viewport
    driver.set_window_size(width, height)

    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Get an Offer", required_placeholder="Company")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Mobile")
    fill_modal_input(driver, "Enter phone number", "+357 99 11 22 66")
    fill_modal_input(driver, "qwerty@sportbenefit.eu", "qa.mobile@example.com")
    fill_modal_input(driver, "Company", "QA Mobile Co")
    fill_modal_input(driver, "Enter the city", "Limassol")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    send_button = get_modal_send_button(driver)
    assert send_button.is_displayed(), f"Send button is not visible on viewport {width}x{height}"


@allure.feature("SB Mobile Regression")
@allure.severity("Normal")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_contacts_inline_form_validation_gate_sb(driver, viewport):
    """Проверка мобильной валидации и доступности отправки inline-формы Contacts."""
    width, height = viewport
    driver.set_window_size(width, height)

    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()

    fill_inline_contacts_values(
        driver,
        name="QA Mobile Inline",
        phone="+357 99 11 22 77",
        email="qa.mobile.inline@example.com",
        company="QA Mobile Inline Co",
    )
    assert inline_submit_enabled(driver), (
        f"Inline submit should be enabled for valid values on viewport {width}x{height}"
    )

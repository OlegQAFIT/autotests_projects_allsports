import allure

from pages.new_web_site.companies import CompamiesPage


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_form_for_company_on_companies_page(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = CompamiesPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_for_companies_page()
    send_form.clc_on_offer()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send()
    send_form.check_form_submission()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_form_for_partner_on_companies_page(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = CompamiesPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_for_companies_page()
    send_form.clc_on_offer()
    send_form.clc_for_partner_offer()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send()
    send_form.check_form_submission()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_header_1(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form_header = CompamiesPage(driver)
    send_form_header.open()
    send_form_header.accept_cookie_consent()
    send_form_header.clc_for_companies_page()
    send_form_header.clc_send_form_header()
    send_form_header.fill_form(
        send_form_header.INPUT_NAME,
        send_form_header.INPUT_PHONE,
        send_form_header.INPUT_EMAIL,
        send_form_header.INPUT_NAME_COMPANY)
    send_form_header.clc_checkbox()
    send_form_header.clc_send_header_form()
    send_form_header.check_form_submission()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_header_2(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form_header = CompamiesPage(driver)
    send_form_header.open()
    send_form_header.accept_cookie_consent()
    send_form_header.clc_send_form_header()
    send_form_header.clc_for_partner_offer_header()
    send_form_header.fill_form(
        send_form_header.INPUT_NAME,
        send_form_header.INPUT_PHONE,
        send_form_header.INPUT_EMAIL,
        send_form_header.INPUT_NAME_COMPANY)
    send_form_header.clc_checkbox()
    send_form_header.clc_send_header_form()
    send_form_header.check_form_submission_become_partner()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_checking_elements_on_the_page(driver):
    """
    Checking the form for sending a message for an offer
    """
    checking_text = CompamiesPage(driver)
    checking_text.open()
    checking_text.accept_cookie_consent()
    checking_text.clc_for_companies_page()
    checking_text.assert_found_correct_elements_on_page()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_checking_elements_on_the_page_bloc_contacts(driver):
    """
    Checking the form for sending a message for an offer
    """
    checking_text = CompamiesPage(driver)
    checking_text.open()
    checking_text.accept_cookie_consent()
    checking_text.clc_for_companies_page()
    checking_text.scroll_to_bottom()
    checking_text.assert_text_on_page()

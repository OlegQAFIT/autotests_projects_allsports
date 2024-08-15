import allure

from pages.new_web_site.levels import LevelPage


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_header_1(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = LevelPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_send_form_header()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_header_2(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = LevelPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_send_form_header()
    send_form.clc_button_become_partner()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission_become_partner()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_join_company(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = LevelPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.fill_form_main(
        send_form.INPUT_NAME_LEVEL_PAGE,
        send_form.INPUT_PHONE_LEVEL_PAGE,
        send_form.INPUT_EMAIL_LEVEL_PAGE,
        send_form.INPUT_NAME_COMPANY_LEVEL_PAGE)
    send_form.clc_checkbox_maim()
    send_form.clc_send_maim()
    send_form.check_form_submission_join_company_maim()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_join_partner(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = LevelPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_join_partner_maim()
    send_form.fill_form_main(
        send_form.INPUT_NAME_LEVEL_PAGE,
        send_form.INPUT_PHONE_LEVEL_PAGE,
        send_form.INPUT_EMAIL_LEVEL_PAGE,
        send_form.INPUT_NAME_COMPANY_LEVEL_PAGE)
    send_form.clc_checkbox_maim()
    send_form.clc_send_maim()
    send_form.check_form_submission_join_partner_maim()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_correct_silver_subscription(driver):
    """

    """
    level_page = LevelPage(driver)
    level_page.open()
    level_page.accept_cookie_consent()
    level_page.clc_type_subscription()
    level_page.assert_found_correct_elements_on_page()

@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_number_suppliers(driver):
    """

    """
    level_page = LevelPage(driver)
    level_page.open()
    level_page.accept_cookie_consent()
    level_page.clc_type_subscription()
    level_page.assert_change_number_suppliers()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_number_vid(driver):
    """

    """
    level_page = LevelPage(driver)
    level_page.open()
    level_page.accept_cookie_consent()
    level_page.clc_type_subscription()
    level_page.assert_change_number_vid()

@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_link_personal_data_processing_policy(driver):
    """

    """
    level_page = LevelPage(driver)
    level_page.open()
    level_page.accept_cookie_consent()
    level_page.clc_type_subscription()
    level_page.clc_link_personal_data_processing_policy()
    level_page.switch_to_new_window_with_another_page()
    level_page.assert_personal_data_processing_policy_page()



@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_link_personal_data_processing_policy_header(driver):
    """

    """
    level_page = LevelPage(driver)
    level_page.open()
    level_page.accept_cookie_consent()
    level_page.clc_type_subscription()
    level_page.clc_send_form_header()
    level_page.clc_link_personal_data_processing_policy_header()
    level_page.switch_to_new_window_with_another_page()
    level_page.assert_personal_data_processing_policy_page()



@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_form_field_errors(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = LevelPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_type_subscription()
    send_form.fill_form_main_wrong(
        send_form.INPUT_PHONE_LEVEL_PAGE,
        send_form.INPUT_EMAIL_LEVEL_PAGE,
        send_form.INPUT_NAME_LEVEL_PAGE)
    send_form.assert_found_wrong_errore()


# @allure.feature('Send form')
# @allure.severity('Blocker')
# @allure.story('Checking the form for sending a message for an offer')
# def test_form_disabled_buttom_send(driver):
#     """
#     Checking the form for sending a message for an offer
#     """
#     send_form = LevelPage(driver)
#     send_form.open()
#     send_form.accept_cookie_consent()
#     send_form.clc_type_subscription()
#     send_form.assert_disabled_buttom_send()











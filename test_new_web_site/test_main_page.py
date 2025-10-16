import allure

from pages.new_web_site.main_page import MainPage


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_main_page_1(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_button_get_offer()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.assert_form()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_main_page_2(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_button_get_offer()
    send_form.clc_button_become_partner()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.assert_form_become_partner()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_header_1(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
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
    send_form.assert_form_become_partner()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_header_2(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
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
    send_form.assert_form_become_partner()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_ask_question(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_ask_questin()
    send_form.fill_form_questin(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_QUESTION)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission_question()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_for_company(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_for_company()
    send_form.clc_get_offer_company()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission_or_company()



@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_for_partners(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_get_offer_for_partners()
    send_form.fill_form(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_EMAIL,
        send_form.INPUT_NAME_COMPANY)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission_for_partners()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_question_user(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_question_user()
    send_form.fill_form_questin(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_QUESTION)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission_question_user()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_question_company(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_question_company()
    send_form.clc_question_get_offer_company()
    send_form.fill_form_questin(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_QUESTION)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission_question__get_offer_company()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_question_partner(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_question_partner()
    send_form.clc_question_get_offer_partner()
    send_form.fill_form_questin(
        send_form.INPUT_NAME,
        send_form.INPUT_PHONE,
        send_form.INPUT_QUESTION)
    send_form.clc_checkbox()
    send_form.clc_send_1()
    send_form.check_form_submission_question__get_offer_partner()


@allure.feature('Send form')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form_join_company(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.fill_form_main(
        send_form.INPUT_NAME_MAIN,
        send_form.INPUT_PHONE_MAIN,
        send_form.INPUT_EMAIL_MAIN,
        send_form.INPUT_NAME_COMPANY_MAIN)
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
    send_form = MainPage(driver)
    send_form.open()
    send_form.accept_cookie_consent()
    send_form.clc_join_partner_maim()
    send_form.fill_form_main(
        send_form.INPUT_NAME_MAIN,
        send_form.INPUT_PHONE_MAIN,
        send_form.INPUT_EMAIL_MAIN,
        send_form.INPUT_NAME_COMPANY_MAIN)
    send_form.clc_checkbox_maim()
    send_form.clc_send_maim()
    send_form.check_form_submission_join_partner_maim()


#########################################################################################################################################################################################
#########################################################################################################################################################################################
#########################################################################################################################################################################################

@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking elements on the main page')
def test_found_elements_on_main_page(driver):
    """
    We go to the main page and check that it has locators that relate only to this page and display the text from them
    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.assert_found_elements_on_main_page()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_page_for_users(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.click_on_list_objects_for_users()
    main_page.assert_user_redirect_facilities_page()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_page_for_companis(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.clc_for_company()
    main_page.click_on_list_objects_for_companis()
    main_page.assert_user_redirect_companis_page()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_page_for_partners(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.clc_get_offer_for_partners()
    main_page.click_on_list_objects_for_partners()
    main_page.assert_user_redirect_partners_page()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_number_suppliers(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.assert_change_number_suppliers()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_number_vid(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.assert_change_number_vid()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_page_old_site_list_subscription(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.click_on_list_objects()
    main_page.switch_to_new_window_with_old_site()
    main_page.assert_user_redirect_list_objects_page_old_site()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_correct_platinum_subscription(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.click_on_subscription()
    main_page.assert_found_correct_platinum_subscription()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_correct_gold_subscription(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.click_on_gold_level()
    main_page.click_on_subscription()
    main_page.assert_found_correct_gold_subscription()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_correct_region_subscription(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.click_on_region_level()
    main_page.click_on_subscription()
    main_page.assert_found_correct_region_subscription()


@allure.feature('')
@allure.severity('critical')
@allure.story('')
def test_redirect_correct_silver_subscription(driver):
    """

    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.click_on_silver_level()
    main_page.click_on_subscription()
    main_page.assert_found_correct_silver_subscription()




# @allure.feature('')
# @allure.severity('critical')
# @allure.story('')
# def test_clickable_button_send_form(driver):
#     """
#
#     """
#     main_page = MainPage(driver)
#     main_page.open()
#     main_page.accept_cookie_consent()
#     main_page.clc_button_get_offer()
#     main_page.clc_button_get_offer()
#     main_page.clc_button_get_offer()
#     main_page.clc_button_get_offer()
#     main_page.clc_button_get_offer()
#     main_page.clc_button_get_offer()


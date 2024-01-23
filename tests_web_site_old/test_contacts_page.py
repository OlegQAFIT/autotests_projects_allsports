import allure

from pages.web_site_old.contacts_page import Contacts


@allure.feature('Contacts')
@allure.severity('critical')
@allure.story('URL Verification')
def test_check_current_url_contacts_page(driver):
    """
    Test to check the current URL of the Contacts page.
    """
    current_page = Contacts(driver)
    current_page.open()
    current_page.click_contacts_tab()
    current_page.assert_current_url_page()


@allure.feature('Contacts')
@allure.severity('normal')
@allure.story('Elements Verification')
def test_found_actual_elements_on_contacts_page(driver):
    """
    Test to verify the presence of expected elements on the Contacts page.
    """
    сontacts_elements = Contacts(driver)
    сontacts_elements.open()
    сontacts_elements.click_contacts_tab()
    сontacts_elements.assert_found_elements_on_contacts_page()


@allure.feature('Contacts')
@allure.severity('normal')
@allure.story('Clickable Buttons')
def test_checking_clickable_bottom_on_contacts_page(driver):
    """
    Test to check the clickable buttons on the Contacts page.
    """
    clicable_buttom = Contacts(driver)
    clicable_buttom.open()
    clicable_buttom.click_contacts_tab()
    clicable_buttom.assert_found_clickable_buttom()


@allure.feature('Contacts')
@allure.severity('critical')
@allure.story('Form Submission')
def test_checking_send_form_on_contacts_page(driver):
    """
    Test to verify the submission of a form on the Contacts page.
    """
    clicable_buttom = Contacts(driver)
    clicable_buttom.open()
    clicable_buttom.click_contacts_tab()
    clicable_buttom.drop_clc()
    clicable_buttom.fill_form()
    clicable_buttom.click_on_get_offer_button()
    clicable_buttom.assert_form()

import allure

from pages.web_site_old.become_a_partner import BecomePartner


@allure.feature('Testing Become a Partner Page')
@allure.severity('normal')
@allure.story('Verifying Elements')
def test_found_actual_elements_on_become_partner_page(driver):
    """
    Checking the presence of all elements on the Become a Partner page.
    """
    become_partner_elements = BecomePartner(driver)
    become_partner_elements.open()
    become_partner_elements.click_become_partner_tab()
    become_partner_elements.assert_found_elements_on_become_partner_page()


@allure.feature('Testing Become a Partner Page')
@allure.severity('critical')
@allure.story('URL Check')
def test_check_current_url_become_partner_page(driver):
    """
    Checking the current URL of the Become a Partner page.
    """
    current_page = BecomePartner(driver)
    current_page.open()
    current_page.click_become_partner_tab()
    current_page.assert_current_url_page()


@allure.feature('Testing Become a Partner Page')
@allure.severity('normal')
@allure.story('Button Click Verification')
def test_checking_clickable_bottom_on_page(driver):
    """
    Verifying the clickability of buttons on the page.
    """
    clicable_buttom = BecomePartner(driver)
    clicable_buttom.open()
    clicable_buttom.click_become_partner_tab()
    clicable_buttom.assert_found_clickable_buttom()


@allure.feature('Testing Become a Partner Page')
@allure.severity('critical')
@allure.story('Form Submission')
def test_submitting_the_form(driver):
    """
    Checking form submission on the Become a Partner page.
    """
    send_form = BecomePartner(driver)
    send_form.open()
    send_form.click_become_partner_tab()
    send_form.click_get()
    send_form.fill_form(
        send_form.COMPANY,
        send_form.TYPE_SERVICE,
        send_form.PHONE,
        send_form.CITY,
        send_form.NAME,
        send_form.EMAIL
    )
    send_form.click_get_2()
    send_form.assert_form()

import allure

from pages.web_site_old.objects_page import ObjectPage


@allure.feature('Object Page')
@allure.severity('Critical')
@allure.story('Checking Current Page URL')
def test_checking_current_page_url(driver):
    """
    This test checks if the current page URL matches the expected URL.
    """
    object_page = ObjectPage(driver)
    object_page.open()
    object_page.click_on_tab_objects()
    object_page.assert_checking_current_page_url()


@allure.feature('Object Page')
@allure.severity('Normal')
@allure.story('Finding Actual Elements on "Main" Page')
def test_found_actual_elements_on_main_page(driver):
    """
    This test checks if the expected elements are present on the main page of the object page.
    """
    object_page_elements = ObjectPage(driver)
    object_page_elements.open()
    object_page_elements.click_on_tab_objects()
    object_page_elements.assert_found_elements_on_object_page()


@allure.feature('Object Page')
@allure.severity('Normal')
@allure.story('Checking Element Enabled')
def test_checking_element_enabled(driver):
    """
    This test checks if a specific element is enabled on the object page.
    """
    object_page_elements = ObjectPage(driver)
    object_page_elements.open()
    object_page_elements.click_on_tab_objects()
    object_page_elements.assert_activ_element_on_object_page()


@allure.feature('Object Page')
@allure.severity('Critical')
@allure.story('Submitting the Form on "Object" Page')
def test_submitting_the_form_on_object_page(driver):
    """
    This test checks the functionality of submitting a form for sending a message for an offer.
    """
    send_form = ObjectPage(driver)
    send_form.open()
    send_form.click_on_tab_objects()
    send_form.drop_click()
    send_form.fill_form(
        send_form.NAME_COMPANY,
        send_form.PHONE_NUMBER,
        send_form.CITY,
        send_form.NAME_EMPLOY,
        send_form.EMAIL
    )
    send_form.click_get()
    send_form.assert_form()


@allure.feature('Object Page')
@allure.severity('Critical')
@allure.story('Searching for a Gold Supplier on the "Object" Page')
def test_search_gold_supplier_on_object_page(driver):
    """
    This test searches for a Gold Supplier on the Object Page and asserts if the element is found.
    """
    search_gold_supplier = ObjectPage(driver)
    search_gold_supplier.open()
    search_gold_supplier.click_on_tab_objects()
    search_gold_supplier.select_gold_level()
    search_gold_supplier.found_search_click()
    search_gold_supplier.click_supplier()
    search_gold_supplier.assert_element()

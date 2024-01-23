import allure

from pages.web_site_old.main_page import MainPage


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer')
def test_submitting_the_form(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.enter_email()
    send_form.clc_get_1()
    send_form.drop_clc()
    send_form.fill_form(
        send_form.EMAIL,
        send_form.NAME,
        send_form.PHONE,
        send_form.CITY,
        send_form.EMPLOYEE
    )
    send_form.clc_get_2()
    send_form.assert_form()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Selecting Silver Subscription')
def test_level_search(driver):
    """
    From the drop-down list, try to select a silver subscription
    """
    check_level = MainPage(driver)
    check_level.open()
    check_level.clc()
    check_level.assert_main()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking the form for sending a message for an offer (2)')
def test_submitting_the_form_2(driver):
    """
    Checking the form for sending a message for an offer
    """
    send_form = MainPage(driver)
    send_form.open()
    send_form.enter_email_2()
    send_form.clc_get_1()
    send_form.drop_clc()
    send_form.fill_form(
        send_form.EMAIL,
        send_form.NAME,
        send_form.PHONE,
        send_form.CITY,
        send_form.EMPLOYEE
    )
    send_form.clc_get_2()
    send_form.assert_form()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking elements on the main page')
def test_found_actual_elements_on_main_page(driver):
    """
    We go to the main page and check that it has locators that relate only to this page and display the text from them
    """
    main_page = MainPage(driver)
    main_page.open()
    main_page.assert_found_elements_on_main_page()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Supplier Search in Gomel')
def test_supplier_in_gomel(driver):
    """
    This test checks the functionality of finding a supplier in Gomel.
    It selects the Platinum level, Gomel city, a specific activity, and additional possibilities.
    Then, it asserts the presence of a specific supplier.
    """
    gomel_supplier = MainPage(driver)
    gomel_supplier.open()
    gomel_supplier.select_platinum_level()
    gomel_supplier.select_gomel_city_1()
    gomel_supplier.select_activ()
    gomel_supplier.select_possibilities()
    gomel_supplier.assert_found_supplier_1()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Supplier Search in Grodno')
def test_supplier_in_grodno(driver):
    """
    This test checks the functionality of finding a supplier in Grodno.
    It selects the Regional level, Grodno city, a different activity, and additional possibilities.
    """
    grodno_supplier = MainPage(driver)
    grodno_supplier.open()
    grodno_supplier.select_region_level()
    grodno_supplier.select_grodno_city_1()
    grodno_supplier.select_activ_1()
    grodno_supplier.select_possibilities()
    grodno_supplier.select_possibilities_1()
    grodno_supplier.assert_found_supplier()


@allure.feature('Element on page')
@allure.severity('Normal')
@allure.story('Checking Numbers')
def test_actual_value(driver):
    """
    Test to check actual values.
    """
    actual_value = MainPage(driver)
    actual_value.open()
    actual_value.assert_compare_number_ojects()
    actual_value.assert_compare_number_activitis()

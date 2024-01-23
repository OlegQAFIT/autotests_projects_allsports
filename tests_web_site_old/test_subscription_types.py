import allure

from pages.web_site_old.subscription_types_page import SubscriptionTypes


@allure.feature('Subscription Types Page')
@allure.severity('Critical')
@allure.story('Checking Expected Elements on Subscription Types Page')
def test_found_actual_elements_on_subscription_types_page(driver):
    """
    This test checks the presence of expected elements on the "Subscription Types" page.
    """
    subscription_types_elements = SubscriptionTypes(driver)
    subscription_types_elements.open()
    subscription_types_elements.click_subscription_types_tab()
    subscription_types_elements.assert_found_elements_on_subscription_types_page()


@allure.feature('Subscription Types Page')
@allure.severity('Critical')
@allure.story('Checking Subscription Levels on Subscription Types Page')
def test_found_levels_on_subscription_types_page(driver):
    """
    This test checks the presence of subscription levels on the "Subscription Types" page.
    """
    subscription_types_elements = SubscriptionTypes(driver)
    subscription_types_elements.open()
    subscription_types_elements.click_subscription_types_tab()
    subscription_types_elements.find_element()
    subscription_types_elements.click_on_buttom_back()
    subscription_types_elements.assert_find_element_regional_level()


@allure.feature('Subscription Types Page')
@allure.severity('Critical')
@allure.story('Checking Suppliers for Silver Level')
def test_checking_supplier_for_silver_level(driver):
    """
    This test checks the presence of suppliers for the "Silver" level on the "Subscription Types" page.
    """
    supplier_for_silver_level = SubscriptionTypes(driver)
    supplier_for_silver_level.open()
    supplier_for_silver_level.click_subscription_types_tab()
    supplier_for_silver_level.click_on_silver_buttom()
    supplier_for_silver_level.find_element_for_silver()
    supplier_for_silver_level.assert_found_suppliers()


@allure.feature('Subscription Types Page')
@allure.severity('Critical')
@allure.story('Checking Suppliers for Gold Level')
def test_checking_supplier_for_gold_level(driver):
    """
    This test checks the presence of suppliers for the "Gold" level on the "Subscription Types" page.
    """
    supplier_for_gold_level = SubscriptionTypes(driver)
    supplier_for_gold_level.open()
    supplier_for_gold_level.click_subscription_types_tab()
    supplier_for_gold_level.click_on_gold_buttom()
    supplier_for_gold_level.click_on_supplier()
    supplier_for_gold_level.assert_found_suppliers()


@allure.feature('Subscription Types Page')
@allure.severity('Critical')
@allure.story('Checking Clickable Buttons on Subscription Types Page')
def test_checking_clicable_buttom_on_page(driver):
    """
    This test checks that all buttons on the "Subscription Types" page are clickable.
    """
    clicable_buttom = SubscriptionTypes(driver)
    clicable_buttom.open()
    clicable_buttom.click_subscription_types_tab()
    clicable_buttom.assert_found_clickable_buttom()


@allure.feature('Subscription Types')
@allure.severity('Critical')
@allure.story('Checking Form Opening on Subscription Types Page')
def test_form_opening_check(driver):
    """
    This test checks the opening of the form on the "Subscription Types" page after clicking on buttons.
    """
    supplier_for_gold_level = SubscriptionTypes(driver)
    supplier_for_gold_level.open()
    supplier_for_gold_level.click_subscription_types_tab()
    supplier_for_gold_level.click_on_buttom_order_1()
    supplier_for_gold_level.found_element_on_page()
    supplier_for_gold_level.refresh_page()
    supplier_for_gold_level.click_on_buttom_order_2()
    supplier_for_gold_level.found_element_on_page()
    supplier_for_gold_level.refresh_page()
    supplier_for_gold_level.click_on_buttom_order_3()
    supplier_for_gold_level.found_element_on_page()
    supplier_for_gold_level.refresh_page()
    supplier_for_gold_level.click_on_get_offer_button()
    supplier_for_gold_level.assert_found_form()


@allure.feature('Subscription Types Page')
@allure.severity('Critical')
@allure.story('Filling and Submitting Form on Subscription Types Page')
def test_send_form(driver):
    """
    This test fills out a form on the "Subscription Types" page and checks its submission.
    """
    send_form = SubscriptionTypes(driver)
    send_form.open()
    send_form.click_subscription_types_tab()
    send_form.click_on_get_offer_button()
    send_form.drop_click()
    send_form.fill_form()
    send_form.click_on_get_offer_button()
    send_form.assert_form()  # Нашел баг благодаря тесту


@allure.feature('Subscription Types Page')
@allure.severity('Critical')
@allure.story('Checking URL After Switching to Supplier Website')
def test_checking_supplier_website(driver):
    """
    This test checks that the URL after switching to the supplier's website matches the expected one.
    """
    checking_supplier = SubscriptionTypes(driver)
    checking_supplier.open()
    checking_supplier.click_subscription_types_tab()
    checking_supplier.click_on_gold_buttom()
    checking_supplier.click_on_supplier()
    checking_supplier.click_on_sait_supplier()
    checking_supplier.switch_to_new_window_supplier()
    checking_supplier.assert_web_sait_supplier()

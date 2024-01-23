from elements_web_site_old import HeaderElement

import allure


@allure.feature('Header Navigation')
@allure.severity('critical')
@allure.story('Checking header links')
def test_open_page_objects(driver):
    """
    Checking the opening of a page with objects through the header
    """
    page_objects = HeaderElement(driver)
    page_objects.open()
    page_objects.click_on_button_objects()
    page_objects.assert_current_object_page()


@allure.feature('Header Navigation')
@allure.severity('critical')
@allure.story('Checking header links')
def test_open_page_subscription_types(driver):
    """
    Checking the opening of a page with subscription types through the header
    """
    page_subscription_types = HeaderElement(driver)
    page_subscription_types.open()
    page_subscription_types.click_on_button_subscription_types()
    page_subscription_types.assert_current_subscription_types_page()


@allure.feature('Header Navigation')
@allure.severity('critical')
@allure.story('Checking header links')
def test_open_page_become_partner(driver):
    """
    Checking the opening of a "Become a Partner" page through the header
    """
    page_become_partner = HeaderElement(driver)
    page_become_partner.open()
    page_become_partner.click_on_button_become_partner()
    page_become_partner.assert_current_become_partner_page()


@allure.feature('Header Navigation')
@allure.severity('critical')
@allure.story('Checking header links')
def test_open_page_contacts(driver):
    """
    Checking the opening of a "Contacts" page through the header
    """
    page_contacts = HeaderElement(driver)
    page_contacts.open()
    page_contacts.click_on_button_contacts()
    page_contacts.assert_current_contacts_page()


@allure.feature('Header Navigation')
@allure.severity('critical')
@allure.story('Checking locale selection')
def test_locale_selection(driver):
    """
    Checking the locale selection through the header
    """
    locale_selection = HeaderElement(driver)
    locale_selection.open()
    locale_selection.click_on_button_locale_dropdown()
    locale_selection.assert_current_contacts_page()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking city selection for AM locale')
def test_checking_the_city_by_locale_AM(driver):
    """
    Checking the city selection for the AM locale through the header
    """
    city_by_locale = HeaderElement(driver)
    city_by_locale.open()
    city_by_locale.click_on_button_locale_dropdown()
    city_by_locale.click_on_AM()
    city_by_locale.click_on_select_city_dropdown()
    city_by_locale.assert_city_by_locale_AM_visible()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking city selection for AM-EN locale')
def test_checking_the_city_by_locale_AM_EN(driver):
    """
    Checking the city selection for the AM-EN locale through the header
    """
    city_by_locale = HeaderElement(driver)
    city_by_locale.open()
    city_by_locale.click_on_button_locale_dropdown()
    city_by_locale.click_on_AM_EN()
    city_by_locale.click_on_select_city_dropdown()
    city_by_locale.assert_city_by_locale_AM_EN_visible()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking city selection for RU locale')
def test_checking_the_city_by_locale_RU(driver):
    """
    Checking the city selection for the RU locale through the header
    """
    city_by_locale = HeaderElement(driver)
    city_by_locale.open()
    city_by_locale.click_on_button_locale_dropdown()
    city_by_locale.click_on_RU()
    city_by_locale.click_on_select_city_dropdown()
    city_by_locale.assert_city_by_locale_RU_visible()


@allure.feature('Header Navigation')
@allure.severity('Blocker')
@allure.story('Checking city selection for BY locale')
def test_checking_the_city_by_locale_BY(driver):
    """
    Checking the city selection for the BY locale through the header
    """
    city_by_locale = HeaderElement(driver)
    city_by_locale.open()
    city_by_locale.click_on_button_locale_dropdown()
    city_by_locale.click_on_RU()
    city_by_locale.click_on_select_city_dropdown()
    city_by_locale.assert_city_by_locale_RU_visible()
    city_by_locale.click_on_button_locale_dropdown()
    city_by_locale.click_on_BY()
    city_by_locale.click_on_select_city_dropdown()
    city_by_locale.assert_city_by_locale_BY_visible()

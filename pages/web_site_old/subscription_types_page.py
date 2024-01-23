import time

import allure
from faker import Faker

from helpers import BasePage
from locators.web_site_old import SubscriptionTypesLocators


class SubscriptionTypes(BasePage, SubscriptionTypesLocators):

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Click on 'ALLSPORTS' page")
    def open(self):
        self.driver.get('https://www.allsports.fit/by/')

    @allure.step("Click on 'Subscription Types Tab'")
    def click_subscription_types_tab(self):
        self.hard_click(self.BUTTON_SUBSCRIPTION_TYPES_TAB)

    @allure.step("Find Element")
    def find_element(self):
        self.wait_for_element_is_displayed(self.SILVER_LEVEL)
        self.wait_for_element_is_displayed(self.GOLD_LEVEL)
        self.wait_for_element_is_displayed(self.PLATINUM_LEVEL)

    @allure.step("Click on 'Back' Button")
    def click_on_buttom_back(self):
        self.hard_click(self.BACK_BUTTON)

    @allure.step("Assert Found Regional Level")
    def assert_find_element_regional_level(self):
        self.wait_for_element_is_displayed(self.REGIONAL_LEVEL)

    @allure.step("Click on Gold Button")
    def click_on_gold_buttom(self):
        self.hard_click(self.VIEW_OBJECTS_GOLD)

    @allure.step("Click on Silver Button")
    def click_on_silver_buttom(self):
        self.hard_click(self.VIEW_OBJECTS_SILVER)

    @allure.step("Click on Supplier Button")
    def click_on_supplier(self):
        self.hard_click(self.SUPPLIER)

    @allure.step("Find Element for Silver")
    def find_element_for_silver(self):
        self.wait_for_element_is_displayed(self.CHECKING_ELEMENT_FOR_ALL_OBJECT)
        self.wait_for_element_is_displayed(self.CHECKING_ELEMENT_FOR_ALL_ACTIVITY)
        self.wait_for_element_is_displayed(self.ELEMENT_MINSK)
        self.wait_for_element_is_displayed(self.SUPPLIER_MINSK)

    @allure.step("Assert Found Suppliers")
    def assert_found_suppliers(self):
        self.wait_for_element_is_displayed(self.SUPPLIER_MINSK)
        screenshot_filename = "silversupplier.png"
        self.take_screenshot(screenshot_filename)

    @allure.step("Assert Found Clickable Button")
    def assert_found_clickable_buttom(self):
        self.wait_for_visible(self.VIEW_OBJECTS_SILVER)
        self.wait_for_visible(self.VIEW_OBJECTS_GOLD)
        self.wait_for_visible(self.VIEW_OBJECTS_PLATINUM)
        self.wait_for_visible(self.VIEW_ACTIVITY_SILVER)
        self.wait_for_visible(self.VIEW_ACTIVITY_GOLD)
        self.wait_for_visible(self.VIEW_ACTIVITY_PLATINUM)
        self.wait_for_visible(self.BUTTON_ORDER_1)
        self.wait_for_visible(self.BUTTON_ORDER_2)
        self.wait_for_visible(self.BUTTON_ORDER_3)
        self.wait_for_visible(self.GET_OFFER_BUTTON)

    @allure.step("Refresh Page")
    def refresh_page(self):
        self.driver.refresh()

    @allure.step("Click on 'Order 1' Button")
    def click_on_buttom_order_1(self):
        self.hard_click(self.BUTTON_ORDER_1)

    @allure.step("Click on 'Order 2' Button")
    def click_on_buttom_order_2(self):
        self.hard_click(self.BUTTON_ORDER_2)

    @allure.step("Click on 'Order 3' Button")
    def click_on_buttom_order_3(self):
        self.hard_click(self.BUTTON_ORDER_3)

    @allure.step("Click on 'Get Offer' Button")
    def click_on_get_offer_button(self):
        time.sleep(2)
        self.hard_click(self.GET_OFFER_BUTTON)

    @allure.step("Click on 'Supplier' Button")
    def click_on_sait_supplier(self):
        self.hard_click(self.WEB_SUPPLIER)

    @allure.step("Found Element on Page")
    def found_element_on_page(self):
        self.wait_for_element_is_displayed(self.NAME_COMPANY)

    @allure.step("Assert Found Form")
    def assert_found_form(self):
        self.wait_for_element_is_displayed(self.FORM)

    fake = Faker()
    name = fake.name()
    phone = fake.phone_number()
    city = fake.city()
    email = fake.email()
    company = fake.company()

    @allure.step("Fill Form")
    def fill_form(self, name_company=None, phone_number=None, city_locator=None, name_employ=None, email_locator=None):
        self.fill(name_company or self.NAME_COMPANY, self.company)
        self.fill(phone_number or self.PHONE_NUMBER, self.phone)
        self.fill(city_locator or self.CITY_LOCATOR, self.city)
        self.fill(name_employ or self.NAME_EMPLOY, self.name)
        self.fill(email_locator or self.EMAIL_LOCATOR, self.email)

    @allure.step("Click on 'Number of Employees' Button")
    def drop_click(self):
        self.hard_click(self.NUMBER_EMPLOYEES_BUTTON)
        self.hard_click(self.NUMBER_EMPLOYEES)

    @allure.step("Assert Form")
    def assert_form(self):
        time.sleep(2)
        self.handle_alert("Спасибо! Мы скоро свяжемся с вами!")

    @allure.step("Switch to New Window for Supplier")
    def switch_to_new_window_supplier(self):
        self.switch_to_new_window()

    @allure.step("Assert Web Sait Supplier")
    def assert_web_sait_supplier(self):
        current_url = self.get_current_url()
        print("Текущий URL (instagram):", current_url)
        assert self.get_current_url() == 'http://rgolympic.by/'

    @allure.step("Assert Found Elements on Subscription Types Page")
    def assert_found_elements_on_subscription_types_page(self):
        elements_to_check = [
            (self.ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE, 'Типы подписки'),
            (self.ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_1, 'Gold'),
            (self.ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_2, 'Количество объектов'),
            (self.ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_3, 'Заказать'),
            (self.ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_4, 'Активности'),
            (self.ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_5, 'Количество посещений в месяц'),
            (self.ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_6, 'Период отмены')
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

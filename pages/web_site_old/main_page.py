import time
import allure
from selenium.common import WebDriverException
from helpers.base import BasePage
from locators.web_site_old import MainPageLocators


class MainPage(BasePage, MainPageLocators):

    def __init__(self, driver):
        self.text_employe = 'Олег'
        self.text_city = 'Минск'
        self.text_phone = '375 29 111 22 33'
        self.text_name = 'ОАО Проверка'
        self.text_email = 'test@gmail.com'
        self.driver = driver

    def open(self):
        self.driver.get('https://www.allsports.fit/by/')

    @allure.step("Select Platinum Level")
    def select_platinum_level(self):
        self.click_and_select_option_in_dropdown(self.TYPE_SUBSCRIPTION, self.PLATINUM_LEVEL)

    @allure.step("Select Regional Level")
    def select_region_level(self):
        self.click_and_select_option_in_dropdown(self.TYPE_SUBSCRIPTION, self.REGION_LEVEL_1)

    @allure.step("Select Gomel City")
    def select_gomel_city_1(self):
        self.click_and_select_option_in_dropdown(self.CITY_SELECT, self.GOMEL_CITY_1)

    @allure.step("Select Grodno City")
    def select_grodno_city_1(self):
        self.click_and_select_option_in_dropdown(self.CITY_SELECT, self.GRODNO_CITY)

    @allure.step("Select Activity")
    def select_activ(self):
        self.click_and_select_option_in_dropdown(self.ACTIV_SELECT, self.POOL_1)

    @allure.step("Select Activity")
    def select_activ_1(self):
        self.click_and_select_option_in_dropdown(self.ACTIV_SELECT, self.POOL)

    @allure.step("Select Possibilities")
    def select_possibilities(self):
        self.click_and_select_option_in_dropdown(self.POSSIBILITIES_SELECT, self.RESERVATION_REQUIRED_1)

    @allure.step("Select Possibilities")
    def select_possibilities_1(self):
        self.click_and_select_option_in_dropdown(self.POSSIBILITIES_SELECT, self.RESERVATION_REQUIRED)

    @allure.step("Click on Subscription")
    def clc(self):
        self.hard_click(self.TYPE_SUBSCRIPTION)

    @allure.step("Click on Type Subscription")
    def click_on_type_subscription(self):
        self.hard_click(self.TYPE_SUBSCRIPTION)

    @allure.step("Assert Supplier Found")
    def assert_found_supplier_1(self):
        self.assert_element_present(self.SUPPLIER_2)

    @allure.step("Assert Supplier Found")
    def assert_found_supplier(self):
        self.assert_element_present(self.SUPPLIER)

    @allure.step("Assert Reservation Found")
    def assert_found_reservation(self):
        self.hard_click(self.RESERVATION_REQUIRED)

    @allure.step("Assert visible element")
    def assert_main(self):
        self.wait_for_visible(self.LEVEL)

    @allure.step("Enter Email")
    def enter_email(self):
        self.fill(self.EMAIL, self.text_email)

    @allure.step("Enter Email")
    def enter_email_2(self):
        self.fill(self.EMAIL_2, self.text_email)

    @allure.step("Click on locator")
    def clc_get_1(self):
        self.hard_click(self.GET)

    @allure.step("Click on Dropdown")
    def drop_clc(self):
        self.hard_click(self.VALUE)
        self.hard_click(self.OPTION)

    @allure.step("Fill Form")
    def fill_form(self, EMAIL, NAME, PHONE, CITY, EMPLOYEE):
        self.fill(EMAIL, self.text_email)
        self.fill(NAME, self.text_name)
        self.fill(PHONE, self.text_phone)
        self.fill(CITY, self.text_city)
        self.fill(EMPLOYEE, self.text_employe)

    @allure.step("Click Get")
    def clc_get_2(self):
        self.hard_click(self.GET_2)

    @allure.step("Assert Form")
    def assert_form(self):
        time.sleep(2)
        self.handle_alert("Спасибо! Мы скоро свяжемся с вами!")

    @allure.step("Assert Found Elements on Main Page")
    def assert_found_elements_on_main_page(self):
        elements_to_check = [
            (self.LOCATOR_ON_MAIN_PAGE, 'Сервис Allsports'),
            (self.LOCATOR_ON_MAIN_PAGE_2, 'Заголовок 2'),
            (self.LOCATOR_ON_MAIN_PAGE_3, 'Делаем спорт частью корпоративной жизни'),
            (self.LOCATOR_ON_MAIN_PAGE_4, 'Отзывы наших клиентов')
        ]

        found_elements = []

        for locator, expected_text in elements_to_check:
            try:
                element = self.wait_for_visible(locator)
                found_text = element.text
                found_elements.append((locator, found_text))
            except WebDriverException:
                assert False, f"Элемент с локатором '{locator}' и текстом '{expected_text}' отсутствует на странице."

        for locator, found_text in found_elements:
            print(f"Найден элемент с локатором '{locator}' и текстом '{found_text}'")

    @allure.step("Search and correct quantity display ojects")
    def assert_compare_number_ojects(self):
        actual_value = self.get_number_from_element(self.OBJECTS)
        expected_value = 561
        if actual_value < expected_value:
            print("Число в элементе меньше ожидаемого значения.")
        else:
            print("Число в элементе НЕ меньше ожидаемого значения.")

    @allure.step("Search and correct quantity display activitis")
    def assert_compare_number_activitis(self):
        actual_value = self.get_number_from_element(self.ACTIVITIS)
        expected_value = 59
        if actual_value < expected_value:
            print("Число в элементе меньше ожидаемого значения.")
        else:
            print("Число в элементе НЕ меньше ожидаемого значения.")

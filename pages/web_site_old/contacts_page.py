import allure
import time
from faker import Faker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import BasePage
from locators.web_site_old import ContactsLocators


class Contacts(BasePage, ContactsLocators):

    def __init__(self, driver):
        self.driver = driver
        self.fake = Faker()
        self.company = self.fake.company()
        self.city = self.fake.city()
        self.name = self.fake.name()
        self.phone = self.fake.phone_number()
        self.email = self.fake.email()

    # Methods for page navigation
    @allure.step("Click on 'ALLSPORTS' page")
    def open(self):
        self.driver.get('https://www.allsports.fit/by/')

    # Methods for interacting with the 'Contacts' tab
    @allure.step("Click on 'Become a Partner' Tab")
    def click_contacts_tab(self):
        self.hard_click(self.BUTTON_CONTACTS_TAB)

    # Methods for asserting elements on the 'Contacts' page
    @allure.step("Assert Current URL of the Page")
    def assert_current_url_page(self):
        expected_url = 'https://www.allsports.fit/by/contact/'
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be(expected_url))
        current_url = self.get_current_url()
        print("Текущий URL (CONTACTS):", current_url)
        assert current_url == expected_url, f"Ожидаемый URL: {expected_url}, текущий URL: {current_url}"

    @allure.step("Assert Found Elements on Contacts Page")
    def assert_found_elements_on_contacts_page(self):
        elements_to_check = [
            (self.ELEMENT_ON_CONTACTS_PAGE_1, 'Контакты'),
            (self.ELEMENT_ON_CONTACTS_PAGE_2, 'Техподдержка объектов'),
            (self.ELEMENT_ON_CONTACTS_PAGE_3, 'Региональный представитель по Брестской области'),
            (self.ELEMENT_ON_CONTACTS_PAGE_4, 'Региональный представитель по Витебской области'),
            (self.ELEMENT_ON_CONTACTS_PAGE_5, 'Региональный представитель по Гродненской области'),
            (self.ELEMENT_ON_CONTACTS_PAGE_6, 'Стань партнером Allsports сегодня!')
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Assert Found Clickable Button")
    def assert_found_clickable_buttom(self):
        buttons_to_check = [self.BUTTON_1, self.BUTTON_2, self.BUTTON_3, self.BUTTON_4, self.BUTTON_5, self.BUTTON_6]
        for button in buttons_to_check:
            self.wait_for_element_is_displayed(button)

    # Methods for filling and interacting with the form
    @allure.step("Fill Form")
    def fill_form(self, name_company=None, phone_number=None, city_locator=None, name_employ=None, email_locator=None):
        self.fill(name_company or self.NAME_COMPANY, self.company)
        self.fill(phone_number or self.PHONE_NUMBER, self.phone)
        self.fill(city_locator or self.CITY, self.city)
        self.fill(name_employ or self.NAME_EMPLOY, self.name)
        self.fill(email_locator or self.EMAIL, self.email)

    @allure.step("Click on Dropdown")
    def drop_clc(self):
        time.sleep(2)
        self.hard_click(self.VALUE)
        self.hard_click(self.OPTION)

    @allure.step("Click on 'Get Offer' Button")
    def click_on_get_offer_button(self):
        self.hard_click(self.GET_OFFER_BUTTON)

    @allure.step("Assert Form")
    def assert_form(self):
        time.sleep(2)
        self.handle_alert("Спасибо! Мы скоро свяжемся с вами!")
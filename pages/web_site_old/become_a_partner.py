import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import BasePage
from locators.web_site_old.for_Become_partner import BecomePartnerLocators


class BecomePartner(BasePage, BecomePartnerLocators):

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Click on 'ALLSPORTS' page")
    def open(self):
        self.driver.get('https://www.allsports.fit/by/')

    @allure.step("Click on 'Become а Partner' Tab")
    def click_become_partner_tab(self):
        self.hard_click(self.BUTTON_Become_Partner_TAB)

    @allure.step("Assert Found Elements on Become Partner Page")
    def assert_found_elements_on_become_partner_page(self):
        elements_to_check = [
            (self.ELEMENT_ON_Become_Partner_PAGE, 'Развивайте ваш бизнес с нами!'),
            (self.ELEMENT_ON_Become_Partner_PAGE_1, 'Что Allsports дает вашему фитнес-клубу?'),
            (self.ELEMENT_ON_Become_Partner_PAGE_2, 'Как это работает?'),
            (self.ELEMENT_ON_Become_Partner_PAGE_3, 'Наши партнеры'),
            (self.ELEMENT_ON_Become_Partner_PAGE_4, 'Стань партнером Allsports сегодня!')
        ]

        for element, expected_text in elements_to_check:
            self.assert_element_text_equal(element, expected_text)

    @allure.step("Enter Email")
    def enter_email(self):
        self.fill(self.EMAIL, self.EMAIL_TEXT)

    @allure.step("Fill Form")
    def fill_form(self, COMPANY, TYPE_SERVICE, PHONE, CITY, NAME, EMAIL):
        self.fill(COMPANY, self.COMPANY_TEXT)
        self.fill(TYPE_SERVICE, self.TYPE_SERVICE_TEXT)
        self.fill(PHONE, self.PHONE_TEXT)
        self.fill(CITY, self.CITY_TEXT)
        self.fill(NAME, self.NAME_TEXT)
        self.fill(EMAIL, self.EMAIL_TEXT)

    @allure.step("Click Get")
    def click_get(self):
        self.hard_click(self.BUTTOM_GET)

    @allure.step("Click Get 2")
    def click_get_2(self):
        self.hard_click(self.BUTTOM_GET_2)

    @allure.step("Assert Form Submission")
    def assert_form(self):
        time.sleep(2)
        self.handle_alert("Спасибо! Мы скоро свяжемся с вами!") \

    @allure.step("Assert Current URL of the Page")
    def assert_current_url_page(self):
        expected_url = 'https://www.allsports.fit/by/affiliates/'
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
        current_url = self.get_current_url()
        print("Текущий URL (affiliates):", current_url)
        assert current_url == expected_url, f"Ожидаемый URL: {expected_url}, текущий URL: {current_url}"


    @allure.step("Assert Found Clickable Button")
    def assert_found_clickable_buttom(self):
        buttons_to_check = [self.BUTTON_1, self.BUTTON_2, self.BUTTON_3, self.BUTTON_4]
        for button in buttons_to_check:
            self.wait_for_element_is_displayed(button)

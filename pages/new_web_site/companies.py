import re
import requests
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from helpers.base import BasePage
from locators.elements_for_new_web_site.for_companies_page import CompaniesPageLocators
from locators.elements_for_new_web_site.header_elements_new_web_site import HeaderLocators


class CompamiesPage(BasePage, CompaniesPageLocators, HeaderLocators):

    def __init__(self, driver):
        self.text_name = 'Олег'
        self.text_phone = '375 29 758 72 34'
        self.text_phone_wrong = '375 29 758 72 34 52'
        self.text_email_wrong = '.'
        self.text_email = 'testOleg@gmail.com'
        self.text_name_company = 'ОАО Проверка Oleg'
        self.text_questin = 'Проверка теста вопроса'
        self.driver = driver

    def open(self):
        self.driver.get('https://www.allsports.by/ru-by')

    @allure.step("Click on locator")
    def clc_for_companies_page(self):
        self.hard_click(self.COMPANIES)

    @allure.step("Click on locator")
    def clc_on_offer(self):
        self.hard_click(self.BUTTON_SEND_OFFER)

    def accept_cookie_consent(self):
        try:
            accept_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-primary-modal__confirm'))
            )
            accept_button.click()
        except (WebDriverException, TimeoutException):
            pass

    @allure.step("Fill Form")
    def fill_form(self, INPUT_NAME, INPUT_PHONE, INPUT_EMAIL, INPUT_NAME_COMPANY):
        self.fills_fild(INPUT_NAME, self.text_name)
        self.fills_fild(INPUT_PHONE, self.text_phone)
        self.fills_fild(INPUT_EMAIL, self.text_email)
        self.fills_fild(INPUT_NAME_COMPANY, self.text_name_company)

    @allure.step("Click on locator")
    def clc_checkbox(self):
        self.hard_click(self.CHECKBOX)

    @allure.step("Click on locator")
    def clc_send(self):
        self.hard_click(self.BUTTON_SEND)

    def check_form_submission(self, expected_status_code=204):
        url = 'https://www.allsports.by/api/www/2.0.0/contact/get_offer'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': 'allsports_agr=%7B%22technical%22%3Atrue%2C%22analytical%22%3Afalse%7D; country=ru-by',
            'Referer': 'https://www.allsports.by/ru-by',
            'Origin': 'https://www.allsports.by',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        payload = {
            'companyName': 'ОАО Проверка Oleg',
            'name': 'Олег',
            'email': 'testOleg@gmail.com',
            'phone': '375297587234',
            'country': 'by',
            'location': 'default',
            'processPersonalData': True
        }

        response = requests.post(url, headers=headers, json=payload)
        print(f"Получен статус-код: {response.status_code}")
        assert response.status_code == expected_status_code, f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"

    @allure.step("Click on locator")
    def clc_for_partner_offer(self):
        self.hard_click(self.BECOME_PARTNER)


    @allure.step("Click on locator")
    def clc_send_form_header(self):
        self.hard_click(self.BUTTON_GET_OFFER_HEADER)

    @allure.step("Click on locator")
    def clc_send_header_form(self):
        self.hard_click(self.BUTTON_SEND)

    @allure.step("Click on locator")
    def clc_for_partner_offer_header(self):
        self.hard_click(self.BECOME_PARTNER_HEADER)

    def check_form_submission_become_partner(self, expected_status_code=204):
        url = 'https://www.allsports.by/api/www/2.0.0/contact/become_partner'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': 'allsports_agr=%7B%22technical%22%3Atrue%2C%22analytical%22%3Afalse%7D; country=ru-by',
            'Referer': 'https://www.allsports.by/ru-by',
            'Origin': 'https://www.allsports.by',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        payload = {
            'companyName': 'ОАО Проверка Oleg',
            'name': 'Олег',
            'email': 'testOleg@gmail.com',
            'phone': '375297587234',
            'country': 'by',
            'location': 'default',
            'processPersonalData': True
        }

        response = requests.post(url, headers=headers, json=payload)
        print(f"Получен статус-код: {response.status_code}")
        assert response.status_code == expected_status_code, f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"


    @allure.step("correct subscription")
    def assert_found_correct_elements_on_page(self):
        elements_to_check = [
            (self.TEXT_ON_PAGE, 'Для компаний'),
            (self.TEXT_ON_PAGE_ADVANTAGES, 'Преимущества'),
            (self.TEXT_ON_PAGE_COOPERATE, 'Сотрудничать с Allsports — легко!'),
            (self.TEXT_ON_PAGE_REVIEWS, 'Нам доверяют'),
            (self.TEXT_ON_PAGE_QUESTIONS, 'Часто задаваемые вопросы'),
            (self.TEXT_ON_PAGE_CONTACTS, 'Наши контакты')
        ]

        for locator, expected_text in elements_to_check:
            try:
                element = self.wait_for_visible(locator)
                found_text = element.text

                assert found_text == expected_text, (
                    f"Текст элемента с локатором '{locator}' не соответствует ожидаемому. "
                    f"Ожидаемый текст: '{expected_text}', найденный текст: '{found_text}'"
                )

                print(f"Найден элемент с локатором '{locator}' и текстом '{found_text}'")

            except WebDriverException:
                assert False, f"Элемент с локатором '{locator}' отсутствует на странице."

    # @allure.step("Проверка текста на странице")
    # def assert_found_correct_text(self):
    #     """
    #     Метод для проверки текста элементов на странице.
    #     Проверяет текст для указанных элементов на странице.
    #     """
    #     elements_to_check = [
    #         (self.TEXT_ON_PAGE_CONTACTS, 'Наши контакты'),
    #         (self.TEXT_ON_PAGE_PHONE, '+375 44 771 09 47'),
    #         (self.TEXT_ON_PAGE_PHONE_TEH, '+375 44 525 38 92'),
    #         (self.TEXT_ON_PAGE_ADREAS, '220030 г. Минск, ул. Интернациональная, 36-2, офисы 2-20, 1-21'),
    #         (self.TEXT_ON_PAGE_EMAIL, 'contact@allsports.by'),
    #         (self.TEXT_ON_PAGE_TIME, 'пн-пт: 09:00-18:00'),
    #         (self.TEXT_ON_PAGE_TIME_2, 'сб-вс: выходной')
    #     ]
    #
    #     for locator, expected_text in elements_to_check:
    #         try:
    #             element = self.wait_for_visible_3(locator)
    #             found_text = element.text
    #
    #             assert found_text == expected_text, (
    #                 f"Текст элемента с локатором '{locator}' не соответствует ожидаемому. "
    #                 f"Ожидаемый текст: '{expected_text}', найденный текст: '{found_text}'"
    #             )
    #
    #             print(f"Найден элемент с локатором '{locator}' и текстом '{found_text}'")
    #
    #         except WebDriverException:
    #             assert False, f"Элемент с локатором '{locator}' отсутствует на странице."

    def assert_text_on_page(self, timeout=10):
        """
        Метод для проверки наличия текстов на странице.

        :param timeout: время ожидания в секундах
        """
        texts_to_find = [
            "Наши контакты",
            "+375 44 771 09 47",
            "+375 44 525 38 92",
            "220030 г. Минск, ул. Интернациональная, 36-2, офисы 2-20, 1-21",
            "contact@allsports.by",
            "пн-пт: 09:00-18:00",
            "сб-вс: выходной"
        ]

        for text_to_find in texts_to_find:
            try:
                # Ожидание, что текст будет присутствовать на странице
                WebDriverWait(self.driver, timeout).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, "//*[contains(text(), '{}')]".format(text_to_find)),
                        text_to_find
                    )
                )
                print(f"Текст '{text_to_find}' найден на странице.")

            except TimeoutException:
                assert False, f"Текст '{text_to_find}' не найден на странице в течение {timeout} секунд."


    @allure.step("Scroll down to the bottom of the page")
    def scroll_to_bottom(self):
        self.scroll_to_bottom()




















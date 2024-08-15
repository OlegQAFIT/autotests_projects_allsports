import time
import re
import requests
from selenium.webdriver.support import expected_conditions as EC

import allure
from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from helpers.base import BasePage
from locators.elements_for_new_web_site.for_main_page import MainPageLocators
from locators.elements_for_new_web_site.header_elements_new_web_site import HeaderLocators


class MainPage(BasePage, MainPageLocators, HeaderLocators):

    def __init__(self, driver):
        self.text_name = 'Олег'
        self.text_phone = '375 29 758 72 34'
        self.text_email = 'testOleg@gmail.com'
        self.text_name_company = 'ОАО Проверка Oleg'
        self.text_questin = 'Проверка теста вопроса'
        self.driver = driver

    def open(self):
        self.driver.get('https://www.allsports.by/ru-by')

    def accept_cookie_consent(self):
        try:
            accept_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-primary-modal__confirm'))
            )
            accept_button.click()
        except (WebDriverException, TimeoutException):
            pass

    @allure.step("Click on locator")
    def clc_button_get_offer(self):
        self.hard_click(self.BUTTON_GET_OFFER)

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
    def clc_send_1(self):
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

    def assert_form(self):
        # self.assert_text_in_element(MainPageLocators.text_modal_send, MainPageLocators.expected_text)
        self.check_form_submission()

    @allure.step("Click on locator")
    def clc_button_become_partner(self):
        self.hard_click(self.BECOME_PARTNER)

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

    def assert_form_become_partner(self):
        self.check_form_submission_become_partner()

    @allure.step("Click on locator")
    def clc_send_form_header(self):
        self.hard_click(self.BUTTON_GET_OFFER_HEADER)

    @allure.step("Click on locator")
    def clc_ask_questin(self):
        self.hard_click(self.ASK_QUESTION)

    @allure.step("Fill Form")
    def fill_form_questin(self, INPUT_QUESTION_NAME, INPUT_QUESTION_PHONE, INPUT_QUESTION):
        self.fills_fild(INPUT_QUESTION_NAME, self.text_name)
        self.fills_fild(INPUT_QUESTION_PHONE, self.text_phone)
        self.fills_fild(INPUT_QUESTION, self.text_questin)

    def check_form_submission_question(self, expected_status_code=204):
        url = 'https://www.allsports.by/api/www/2.0.0/contact/ask_question'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': 'allsports_agr=%7B%22technical%22%3Atrue%2C%22analytical%22%3Afalse%7D; country=ru-by',
            'Referer': 'https://www.allsports.by/ru-by',
            'Origin': 'https://www.allsports.by',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        payload = {
            'name': 'Олег',
            'phone': '375297587234',
            'question': 'Проверка теста вопроса',
            'country': 'by',
            'processPersonalData': True
        }

        response = requests.post(url, headers=headers, json=payload)
        print(f"Получен статус-код: {response.status_code}")
        assert response.status_code == expected_status_code, f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"

    @allure.step("Click on locator")
    def clc_for_company(self):
        self.hard_click(self.COMPANY)

    @allure.step("Click on locator")
    def clc_get_offer_company(self):
        self.hard_click(self.BUTTON_GET_OFFER_COMPANY)

    def check_form_submission_or_company(self, expected_status_code=204):
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
            'companyName': 'Проверка теста вопроса',
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
    def clc_get_offer_for_partners(self):
        self.hard_click(self.PARTNERS)

    @allure.step("Click on locator")
    def clc_get_offer_for_partners(self):
        self.hard_click(self.BUTTON_GET_OFFER_PARTNERS)

    def check_form_submission_for_partners(self, expected_status_code=204):
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
            'companyName': 'Проверка теста вопроса',
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

    #########################################################################################################################################################################################
    @allure.step("Click on locator")
    def clc_question_user(self):
        self.hard_click(self.ASK_QUESTION_USER)

    def check_form_submission_question_user(self, expected_status_code=204):
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
            'companyName': 'Проверка теста вопроса',
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
    def clc_question_company(self):
        self.hard_click(self.ASK_QUESTION_COMPANY)

    @allure.step("Click on locator")
    def clc_question_get_offer_company(self):
        self.hard_click(self.ASK_QUESTION_GET_OFFER_COMPANY)

    def check_form_submission_question__get_offer_company(self, expected_status_code=204):
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
            'companyName': 'Проверка теста вопроса',
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
    def clc_question_partner(self):
        self.hard_click(self.ASK_QUESTION_PARTNERS)

    @allure.step("Click on locator")
    def clc_question_get_offer_partner(self):
        self.hard_click(self.ASK_QUESTION_GET_OFFER_PARTNERS)

    def check_form_submission_question__get_offer_partner(self, expected_status_code=204):
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
            'companyName': 'Проверка теста вопроса',
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

    @allure.step("Fill Form")
    def fill_form_main(self, INPUT_NAME_MAIN, INPUT_PHONE_MAIN, INPUT_EMAIL_MAIN, INPUT_NAME_COMPANY_MAIN):
        self.fills_fild(INPUT_NAME_MAIN, self.text_name)
        self.fills_fild(INPUT_PHONE_MAIN, self.text_phone)
        self.fills_fild(INPUT_EMAIL_MAIN, self.text_email)
        self.fills_fild(INPUT_NAME_COMPANY_MAIN, self.text_name_company)

    @allure.step("Click on locator")
    def clc_checkbox_maim(self):
        self.hard_click(self.CHECKBOX_MAIN)

    @allure.step("Click on locator")
    def clc_send_maim(self):
        self.hard_click(self.BUTTON_SEND_MAIN)

    def check_form_submission_join_company_maim(self, expected_status_code=204):
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
            'companyName': 'Проверка теста вопроса',
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
    def clc_join_partner_maim(self):
        self.hard_click(self.JOIN_COMPANY)

    def check_form_submission_join_partner_maim(self, expected_status_code=204):
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
            'companyName': 'Проверка теста вопроса',
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

    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################

    @allure.step("Assert Found Elements on Main Page")
    def assert_found_elements_on_main_page(self):
        elements_to_check = [
            (self.LOGO_TEXT, 'Весь спорт в одном приложении'),
            (self.ADVANTAGES_TEXT, 'Преимущества Allsports'),
            (self.SUBSCRIPTION_TYPES_TEXT, 'Типы подписок'),
            (self.REVIEWS_TEXT, 'Нам доверяют'),
            (self.QUESTION_TEXT, 'Часто задаваемые вопросы'),
            (self.CONTACTS_TEXT, 'Наши контакты')
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

    @allure.step("Click on 'List of objects for users' link")
    def click_on_list_objects_for_users(self):
        self.hard_click(self.LIST_OBJECTS)

    def assert_user_redirect_facilities_page(self):
        current_url = self.get_current_url()
        print("Текущий URL (facilities):", current_url)
        assert self.get_current_url() == 'https://www.allsports.by/ru-by/facilities'

    @allure.step("Click on 'List of objects for companis' link")
    def click_on_list_objects_for_companis(self):
        self.hard_click(self.FOR_COMPANY)

    def assert_user_redirect_companis_page(self):
        current_url = self.get_current_url()
        print("Текущий URL (companies):", current_url)
        assert self.get_current_url() == 'https://www.allsports.by/ru-by/companies'

    @allure.step("Click on 'List of objects for partners' link")
    def click_on_list_objects_for_partners(self):
        self.hard_click(self.FOR_PARTNERS)

    def assert_user_redirect_partners_page(self):
        current_url = self.get_current_url()
        print("Текущий URL (partners):", current_url)
        assert self.get_current_url() == 'https://www.allsports.by/ru-by/partners'

    @allure.step("Click on gold level")
    def click_on_gold_level(self):
        self.hard_click(self.GOLD)

    @allure.step("Click on region level")
    def click_on_region_level(self):
        self.hard_click(self.REGIN)

    @allure.step("Click on silver level")
    def click_on_silver_level(self):
        self.hard_click(self.SILVER)

    @allure.step("Extract number from text")
    def extract_number(self, text):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        raise ValueError("Число не найдено в тексте")

    @allure.step("Assert change in number of suppliers")
    def assert_change_number_suppliers(self):
        platinum_text = self.driver.find_element(By.XPATH, MainPageLocators.PLATINUM_TEXT).text
        platinum_number = self.extract_number(platinum_text)

        self.click_on_gold_level()
        gold_text = self.driver.find_element(By.XPATH, MainPageLocators.GOLD_TEXT).text
        gold_number = self.extract_number(gold_text)

        assert platinum_number != gold_number, f"Число поставщиков не изменилось: {platinum_number}"

        self.click_on_region_level()
        region_text = self.driver.find_element(By.XPATH, MainPageLocators.REGIN_TEXT).text
        region_number = self.extract_number(region_text)

        assert gold_number != region_number, f"Число поставщиков не изменилось: {gold_number}"

        self.click_on_silver_level()
        silver_text = self.driver.find_element(By.XPATH, MainPageLocators.SILVER_TEXT).text
        silver_number = self.extract_number(silver_text)

        assert region_number != silver_number, f"Число поставщиков не изменилось: {region_number}"
        print("Текущий число Платина:", platinum_number)
        print("Текущий число Золотая:", gold_number)
        print("Текущий число Серебро:", silver_number)
        print("Текущий число Регион:", region_number)

    @allure.step("Assert change in number vid")
    def assert_change_number_vid(self):
        platinum_text = self.driver.find_element(By.XPATH, MainPageLocators.PLATINUM_VID_TEXT).text
        platinum_number = self.extract_number(platinum_text)

        self.click_on_gold_level()
        gold_text = self.driver.find_element(By.XPATH, MainPageLocators.GOLD_VID_TEXT).text
        gold_number = self.extract_number(gold_text)

        assert platinum_number != gold_number, f"Число поставщиков не изменилось: {platinum_number}"

        self.click_on_region_level()
        region_text = self.driver.find_element(By.XPATH, MainPageLocators.REGIN_VID_TEXT).text
        region_number = self.extract_number(region_text)

        assert gold_number != region_number, f"Число поставщиков не изменилось: {gold_number}"

        self.click_on_silver_level()
        silver_text = self.driver.find_element(By.XPATH, MainPageLocators.SILVER_VID_TEXT).text
        silver_number = self.extract_number(silver_text)

        assert region_number != silver_number, f"Число поставщиков не изменилось: {region_number}"
        print("Текущий число Платина:", platinum_number)
        print("Текущий число Золотая:", gold_number)
        print("Текущий число Серебро:", silver_number)
        print("Текущий число Регион:", region_number)

    @allure.step("")
    def click_on_list_objects(self):
        self.hard_click(self.LIST_OBJECTS_OLD_SITE)

    @allure.step("Switch to New Window")
    def switch_to_new_window_with_old_site(self):
        self.switch_to_new_window()

    def assert_user_redirect_list_objects_page_old_site(self):
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be('https://www.allsports.fit/by/price_details/#objects')
        )
        current_url = self.get_current_url()
        print("Текущая страница с списком обьектов:", current_url)
        assert current_url == 'https://www.allsports.fit/by/price_details/#objects'

    @allure.step("Click on silver level")
    def click_on_subscription(self):
        self.hard_click(self.SUBSCRIPTION_OBJECTS)

    @allure.step("correct subscription")
    def assert_found_correct_platinum_subscription(self):
        elements_to_check = [
            (self.SELECT_SUBSCRIPTION, 'Платиновая подписка')
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

    @allure.step("correct subscription")
    def assert_found_correct_gold_subscription(self):
        elements_to_check = [
            (self.SELECT_SUBSCRIPTION, 'Золотая подписка')
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

    @allure.step("correct subscription")
    def assert_found_correct_region_subscription(self):
        elements_to_check = [
            (self.SELECT_SUBSCRIPTION, 'Региональная подписка')
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

    @allure.step("correct subscription")
    def assert_found_correct_silver_subscription(self):
        elements_to_check = [
            (self.SELECT_SUBSCRIPTION, 'Серебряная подписка')
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
















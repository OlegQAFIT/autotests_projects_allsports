import time
import re
import requests
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from helpers.base import BasePage
from locators.elements_for_new_web_site.for_levels_page import LevelPageLocators
from locators.elements_for_new_web_site.header_elements_new_web_site import HeaderLocators


class LevelPage(BasePage, LevelPageLocators, HeaderLocators):

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
    def clc_send_form_header(self):
        self.hard_click(self.BUTTON_GET_OFFER_HEADER)

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
    def clc_send_1(self):
        self.hard_click(self.BUTTON_SEND)

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
    def clc_button_become_partner(self):
        self.hard_click(self.BECOME_PARTNER)


    @allure.step("Fill Form")
    def fill_form_main(self, INPUT_NAME_LEVEL_PAGE, INPUT_PHONE_LEVEL_PAGE, INPUT_EMAIL_LEVEL_PAGE, INPUT_NAME_COMPANY_LEVEL_PAGE):
        self.fills_fild(INPUT_NAME_LEVEL_PAGE, self.text_name)
        self.fills_fild(INPUT_PHONE_LEVEL_PAGE, self.text_phone)
        self.fills_fild(INPUT_EMAIL_LEVEL_PAGE, self.text_email)
        self.fills_fild(INPUT_NAME_COMPANY_LEVEL_PAGE, self.text_name_company)

    @allure.step("Click on locator")
    def clc_checkbox_maim(self):
        self.hard_click(self.CHECKBOX_LEVEL_PAGE)

    @allure.step("Click on locator")
    def clc_send_maim(self):
        self.hard_click(self.BUTTON_SEND_LEVEL_PAGE)

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
        self.hard_click(self.BECOME_PARTNER_LEVEL_PAGE)


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


    @allure.step("correct subscription")
    def assert_found_correct_elements_on_page(self):
        elements_to_check = [
            (self.TYPE_SUBSCRIPTIONS, 'Типы подписок'),
            (self.JOIN_WITH_ALLSPORTS, 'Присоединяйтесь к Allsports')
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

    @allure.step("Click on locator")
    def clc_type_subscription(self):
        self.hard_click(self.SUBSCRIPTION_TYPES)



    @allure.step("Extract number from text")
    def extract_number(self, text):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        raise ValueError("Число не найдено в тексте")

    @allure.step("Click on gold level")
    def click_on_gold_level(self):
        self.hard_click(self.GOLD)

    @allure.step("Click on region level")
    def click_on_region_level(self):
        self.hard_click(self.REGIN)

    @allure.step("Click on silver level")
    def click_on_silver_level(self):
        self.hard_click(self.SILVER)

    @allure.step("Assert change in number of suppliers")
    def assert_change_number_suppliers(self):
        platinum_text = self.driver.find_element(By.XPATH, LevelPageLocators.PLATINUM_TEXT).text
        platinum_number = self.extract_number(platinum_text)

        self.click_on_gold_level()
        gold_text = self.driver.find_element(By.XPATH, LevelPageLocators.GOLD_TEXT).text
        gold_number = self.extract_number(gold_text)

        assert platinum_number != gold_number, f"Число поставщиков не изменилось: {platinum_number}"

        self.click_on_region_level()
        region_text = self.driver.find_element(By.XPATH, LevelPageLocators.REGIN_TEXT).text
        region_number = self.extract_number(region_text)

        assert gold_number != region_number, f"Число поставщиков не изменилось: {gold_number}"

        self.click_on_silver_level()
        silver_text = self.driver.find_element(By.XPATH, LevelPageLocators.SILVER_TEXT).text
        silver_number = self.extract_number(silver_text)

        assert region_number != silver_number, f"Число поставщиков не изменилось: {region_number}"
        print("Текущий число Платина:", platinum_number)
        print("Текущий число Золотая:", gold_number)
        print("Текущий число Серебро:", silver_number)
        print("Текущий число Регион:", region_number)


    @allure.step("Assert change in number vid")
    def assert_change_number_vid(self):
        platinum_text = self.driver.find_element(By.XPATH, LevelPageLocators.PLATINUM_VID_TEXT).text
        platinum_number = self.extract_number(platinum_text)

        self.click_on_gold_level()
        gold_text = self.driver.find_element(By.XPATH, LevelPageLocators.GOLD_VID_TEXT).text
        gold_number = self.extract_number(gold_text)

        assert platinum_number != gold_number, f"Число поставщиков не изменилось: {platinum_number}"

        self.click_on_region_level()
        region_text = self.driver.find_element(By.XPATH, LevelPageLocators.REGIN_VID_TEXT).text
        region_number = self.extract_number(region_text)

        assert gold_number != region_number, f"Число поставщиков не изменилось: {gold_number}"

        self.click_on_silver_level()
        silver_text = self.driver.find_element(By.XPATH, LevelPageLocators.SILVER_VID_TEXT).text
        silver_number = self.extract_number(silver_text)

        assert region_number != silver_number, f"Число поставщиков не изменилось: {region_number}"
        print("Текущий число Платина:", platinum_number)
        print("Текущий число Золотая:", gold_number)
        print("Текущий число Серебро:", silver_number)
        print("Текущий число Регион:", region_number)


    @allure.step("Click on locator")
    def clc_link_personal_data_processing_policy(self):
        self.hard_click(self.LINK_PERSONAL_DATE)

    @allure.step("Click on locator")
    def clc_link_personal_data_processing_policy_header(self):
        self.hard_click(self.LINK_PERSONAL_DATE_HEADER)

    @allure.step("Switch to New Window")
    def switch_to_new_window_with_another_page(self):
        self.switch_to_new_window()

    def assert_personal_data_processing_policy_page(self):
        expected_url = 'https://www.allsports.by/ru-by/policy/231109_processing_personal_data'
        current_url = self.get_current_url()
        print("Текущий URL (partners):", current_url)

        assert current_url == expected_url, f"URL mismatch: expected {expected_url}, got {current_url}"

        try:
            response = requests.get(expected_url)
            if response.status_code == 404:
                print(f"404 Error: {expected_url}")
            else:
                print(f"Accessible: {expected_url} (Status Code: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {expected_url}: {e}")


    @allure.step("Click on locator")
    def clc_send_form_header(self):
        self.hard_click(self.BUTTON_GET_OFFER_HEADER)




    @allure.step("Fill Form")
    def fill_form_main_wrong(self, INPUT_PHONE_LEVEL_PAGE, INPUT_EMAIL_LEVEL_PAGE, INPUT_NAME_LEVEL_PAGE):
        self.fills_fild(INPUT_PHONE_LEVEL_PAGE, self.text_phone_wrong)
        self.fills_fild(INPUT_EMAIL_LEVEL_PAGE, self.text_email_wrong)
        self.fills_fild(INPUT_NAME_LEVEL_PAGE, self.text_name)


    @allure.step("correct subscription")
    def assert_found_wrong_errore(self):
        elements_to_check = [
            (self.ERROR_TEXT_PHONE_NUMBER, 'Неверный формат номера. Правильный формат: +375 00 000 00 00'),
            (self.ERROR_TEXT_EMAIL, 'Адрес электронной почты должен быть действительным.')
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


    # @allure.step("Click on locator")
    # def assert_disabled_buttom_send(self):
    #     self.assert_element_disabld(self.BUTTON_SEND_LEVEL_PAGE)













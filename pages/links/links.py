import allure
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.base import BasePage
from locators.elements_from_links.for_elements_from_links import LocatorsFromPagesLinks
from urllib.parse import urlparse, urlunparse


class ElementsFromLinks(BasePage, LocatorsFromPagesLinks):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def check_links_one(self):
        for link in self.stay_links:
            full_url = self.domain_test + link
            # full_url = self.domain_production + link

            try:
                response = requests.get(full_url)
                if response.status_code == 404:
                    print(f"404 Error: {full_url}")
                else:
                    print(f"Accessible: {full_url} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {full_url}: {e}")

        for link in self.stay_links:
            full_url = self.domain_test + link
            # full_url = self.domain_production + link

            self.driver.get(full_url)

            try:
                WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                current_url = self.driver.current_url
                translated_current_url = self.translate_url_one(current_url)

                assert full_url == translated_current_url, f"URL mismatch: {full_url} != {translated_current_url}"
            except TimeoutException:
                print(f"TimeoutException: Page did not load for {full_url}")
            except AssertionError as e:
                print(f"\nAssertionError: {str(e)}")
            except Exception as e:
                print(f"Exception: {str(e)}")

    def translate_url_one(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'xn--k1aahcehedi.xn--90ais':
            translated_domain = 'оллспортс.бел'
            translated_url = urlunparse((parsed_url.scheme, translated_domain, parsed_url.path, parsed_url.params,
                                         parsed_url.query, parsed_url.fragment))
            return translated_url
        elif parsed_url.netloc == 'xn--80aswg.xn--k1aahcehedi.xn--90ais':
            translated_domain = 'сайт.оллспортс.бел'
            translated_url = urlunparse((parsed_url.scheme, translated_domain, parsed_url.path, parsed_url.params,
                                         parsed_url.query, parsed_url.fragment))
            return translated_url
        else:
            return url












    def check_links_two(self):
        for page_link in self.pages_links:
            url = self.domain_test + page_link
            # url = self.domain_production + page_link

            try:
                response = requests.get(url)
                if response.status_code == 404:
                    print(f"404 Error: {url}")
                else:
                    print(f"Accessible: {url} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {url}: {e}")

        for page_link in self.pages_links:
            url = self.domain_test + page_link
            # url = self.domain_production + page_link
            self.driver.get(url)
            self.accept_cookie_consent()
            current_url = self.get_current_url()
            translated_url = self.translate_url(current_url)
            self.verify_domain_test_new(page_link, translated_url)

    def accept_cookie_consent(self):
        try:
            accept_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-primary-modal__confirm'))
            )
            accept_button.click()
        except (WebDriverException, TimeoutException):
            pass

    @allure.step("Get Current URL")
    def get_current_url(self):
        return self.driver.current_url

    def translate_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'xn--80aswg.xn--k1aahcehedi.xn--90ais':
            translated_domain = 'сайт.оллспортс.бел'
            translated_path = parsed_url.path.replace('//by', '')
            translated_url = urlunparse(('https', translated_domain, translated_path, '', '', ''))
            return translated_url
        else:
            return url

    def verify_domain_test_new(self, original_url, translated_url):
        expected_url = self.domain_test_new + original_url.replace(self.domain_test, '')

        if translated_url != expected_url:
            if translated_url.endswith('/'):
                translated_url = translated_url[:-1]
            if expected_url.endswith('/'):
                expected_url = expected_url[:-1]

            if translated_url != expected_url:
                print(f"\nURL {translated_url} does NOT match the expected URL {expected_url}")









    def check_links_three(self):
        for pages_link_three, expected_redirect in self.mappings.items():
            url = self.domain_test + pages_link_three
            # url = self.domain_production + pages_link_three
            try:
                response = requests.get(url)
                if response.status_code == 404:
                    print(f"404 Error: {url}")
                else:
                    print(f"Accessible: {url} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {url}: {e}")

        for pages_link_three, expected_redirect in self.mappings.items():
            url = self.domain_test + pages_link_three
            # url = self.domain_production + pages_link_three
            self.driver.get(url)
            self.accept_cookie_consent()
            current_url = self.get_current_url_three()
            translated_url = self.translate_url_three(current_url)
            self.verify_domain_test_new_three(pages_link_three, translated_url)
            self.check_redirects_to_pages(translated_url, expected_redirect)

    def accept_cookie_consent(self):
        try:
            accept_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-primary-modal__confirm'))
            )
            accept_button.click()
        except (WebDriverException, TimeoutException):
            pass

    @allure.step("Получить текущий URL")
    def get_current_url_three(self):
        return self.driver.current_url

    def translate_url_three(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'xn--80aswg.xn--k1aahcehedi.xn--90ais':
            translated_domain = 'сайт.оллспортс.бел'
            translated_path = parsed_url.path.replace('//by', '')
            translated_url = urlunparse(('https', translated_domain, translated_path, '', '', ''))
            return translated_url
        else:
            return url

    def check_redirects_to_pages(self, current_url, expected_redirect):
        if current_url != expected_redirect:
            print(f"\nError: URL {current_url} does NOT match the expected redirect: {expected_redirect}")

    def verify_domain_test_new_three(self, original_url, translated_url):
        pass












    def check_links_four(self):
        for index, link in enumerate(self.pages_lincs_four):
            # for index, link in enumerate(self.pages_lincs_prod_four):
            if index >= len(self.expected_parts):
                break

            try:
                response = requests.get(link)
                if response.status_code == 404:
                    print(f"404 Error: {link}")
                    continue
                else:
                    print(f"Accessible: {link} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {link}: {e}")
                continue

            try:
                self.driver.get(link)
                self.accept_cookie_consent_four()
                current_url = self.driver.current_url
                translated_url = self.translate_url_four(current_url)

                expected_part = self.expected_parts[index].rstrip('/')
                translated_url_normalized = translated_url.rstrip('/')

                if translated_url_normalized.endswith(expected_part):
                    print(
                        f"Правильно: Ссылка {link} перенаправляет на {translated_url}, которая совпадает с '{expected_part}'.")
                else:
                    print(
                        f"Ошибка: Ссылка {link} перенаправляет на {translated_url}, но должна была содержать '{expected_part}'.")

                # Проверка на наличие секции 404
                self.driver.get(translated_url)
                if self.is_404_page():
                    print(f"Ошибка 404: Перенаправленный URL {translated_url} содержит ошибку 404.")

            except WebDriverException as e:
                print(f"Не удалось загрузить ссылку {link}: {e}")

    def accept_cookie_consent_four(self):
        try:
            accept_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-primary-modal__confirm'))
            )
            accept_button.click()
        except (WebDriverException, TimeoutException):
            pass

    def is_404_page(self):
        try:
            not_found_section = self.driver.find_element(By.CSS_SELECTOR, 'section.section.not-found-page')
            if not_found_section:
                return True
        except NoSuchElementException:
            return False
    def translate_url_four(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'xn--80aswg.xn--k1aahcehedi.xn--90ais':
            translated_domain = 'сайт.оллспортс.бел'
            translated_path = parsed_url.path.replace('//by', '')
            translated_url = urlunparse(('https', translated_domain, translated_path, '', '', ''))
            return translated_url
        else:
            return url







    def check_links_for_404(self):
        links = [
            "https://www.allsports.by/ru-by/affiliates-table/",
            "https://www.allsports.by/contact/",
            "http://www.allsports.by/objects",
            "http://allsports.by/affiliates",
            "https://www.allsports.by/политика-конфиденциальности",
            "https://www.allsports.by/program-rules-allsports-super",
            "https://www.allsports.by/holder-app-license-agreement/",
            "https://allsports.by/price/220418_price/",
            "https://allsports.by/holder-app-rules",
            "https://www.allsports.by/android-policy",
            "https://www.allsports.by/price/210615_price/"
        ]

        for link in links:
            try:
                response = requests.get(link)
                if response.status_code == 404:
                    print(f"404 Error: {link}")
                else:
                    print(f"Accessible: {link} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {link}: {e}")










    def translate_url_five(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'xn--80aswg.xn--k1aahcehedi.xn--90ais':
            translated_domain = 'сайт.оллспортс.бел'
            translated_path = parsed_url.path.replace('/by', '/ru-by')
            translated_url = urlunparse(('https', translated_domain, translated_path, '', '', ''))
            return translated_url
        elif parsed_url.netloc == 'xn--k1aahcehedi.xn--90ais':
            translated_domain = 'оллспортс.бел'
            translated_path = parsed_url.path
            translated_url = urlunparse(('https', translated_domain, translated_path, '', '', ''))
            return translated_url
        else:
            return url

    def check_links_five(self):
        input_url = "https://оллспортс.бел"
        expected_url = "https://сайт.оллспортс.бел/ru-by"

        try:
            r1 = requests.get('https://habr.com/ru/post/470938500/')
            print(f"Status code for https://habr.com/ru/post/470938500/: {r1.status_code}")

            r2 = requests.get('https://habr.com')
            print(f"Status code for https://habr.com: {r2.status_code}")
        except requests.RequestException as e:
            print(f"Произошла ошибка при проверке статусов: {e}")

        # Проверка редиректа
        self.driver.get(input_url)
        try:
            # Ожидание изменения URL
            WebDriverWait(self.driver, 300).until(EC.url_changes(input_url))

            # Ожидание полной загрузки страницы (например, можно проверять наличие какого-либо элемента на странице)
            WebDriverWait(self.driver, 300).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            current_url = self.driver.current_url
            translated_current_url = self.translate_url_five(current_url)

            if translated_current_url == expected_url:
                print(f"Успешно: ввели адрес {input_url}, открылся {translated_current_url}")
            else:
                print(
                    f"Неуспешно: ввели адрес {input_url}, открылся {translated_current_url}, должен открыться {expected_url}")
        except Exception as e:
            print(f"Произошла ошибка при проверке редиректа: {e}")





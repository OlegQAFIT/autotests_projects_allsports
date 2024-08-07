import time

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

    def __init__(self, driver, domain, domain_new=None, paths_and_redirects=None):
        super().__init__(driver)
        self.driver = driver
        self.domain = domain
        self.domain_new = domain_new
        self.paths_and_redirects = paths_and_redirects or []

    def check_links_one(self):
        for link in self.stay_links:
            full_url = self.domain + link

            try:
                response = requests.get(full_url)
                if response.status_code == 404:
                    print(f"404 Error: {full_url}")
                else:
                    print(f"Accessible: {full_url} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {full_url}: {e}")

        for link in self.stay_links:
            full_url = self.domain + link

            self.driver.get(full_url)

            try:
                WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                current_url = self.driver.current_url
                translated_current_url = self.translate_url(current_url, is_full_url=True)

                assert full_url == translated_current_url, f"URL mismatch: {full_url} != {translated_current_url}"
            except TimeoutException:
                print(f"TimeoutException: Page did not load for {full_url}")
            except AssertionError as e:
                print(f"\nAssertionError: {str(e)}")
            except Exception as e:
                print(f"Exception: {str(e)}")

    def translate_url(self, url, is_full_url=False):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'xn--k1aahcehedi.xn--90ais':
            translated_domain = 'оллспортс.бел'
        elif parsed_url.netloc == 'xn--80aswg.xn--k1aahcehedi.xn--90ais':
            translated_domain = 'сайт.оллспортс.бел'
        elif parsed_url.netloc == 'www.allsports.by':
            translated_domain = 'www.allsports.by'
        else:
            return url

        if is_full_url:
            translated_url = urlunparse((parsed_url.scheme, translated_domain, parsed_url.path, parsed_url.params,
                                         parsed_url.query, parsed_url.fragment))
        else:
            translated_path = parsed_url.path
            if parsed_url.netloc == 'xn--80aswg.xn--k1aahcehedi.xn--90ais':
                translated_path = translated_path.replace('//by', '/')
            elif parsed_url.netloc == 'xn--k1aahcehedi.xn--90ais':
                translated_path = translated_path.replace('/by', '/ru-by')
            elif parsed_url.netloc == 'www.allsports.by':
                translated_path = translated_path.replace('/by', '/ru-by')
            translated_url = urlunparse(('https', translated_domain, translated_path, '', '', ''))

        return translated_url

    def check_links_two(self):
        for page_link in self.pages_links:
            url = self.domain + page_link

            try:
                response = requests.get(url)
                if response.status_code == 404:
                    print(f"404 Error: {url}")
                else:
                    print(f"Accessible: {url} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {url}: {e}")

        for page_link in self.pages_links:
            url = self.domain + page_link
            self.driver.get(url)
            self.accept_cookie_consent()
            current_url = self.get_current_url()
            translated_url = self.translate_url(current_url)
            self.verify_domain_new(page_link, translated_url)

    def accept_cookie_consent(self):
        try:
            accept_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-primary-modal__confirm'))
            )
            accept_button.click()
        except (WebDriverException, TimeoutException):
            pass

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    def verify_domain_new(self, original_url, translated_url):
        expected_url = self.domain_new + original_url.replace(self.domain, '')

        if translated_url != expected_url:
            if translated_url.endswith('/'):
                translated_url = translated_url[:-1]
            if expected_url.endswith('/'):
                expected_url = expected_url[:-1]

            if translated_url != expected_url:
                print(f"\nURL {translated_url} does NOT match the expected URL {expected_url}")

    def check_links_three(self):
        for entry in self.paths_and_redirects:
            # Используем разные ожидаемые редиректы для доменов теста и продакшена
            expected_redirect_key = "expected_redirect_test" if "оллспортс.бел" in self.domain else "expected_redirect_prod"

            for domain, domain_new in [
                (self.domain, self.domain_new)
            ]:
                url = domain + entry["path"]
                expected_redirect = entry.get(expected_redirect_key)

                try:
                    response = requests.get(url)
                    if response.status_code == 404:
                        print(f"404 Error: {url}")
                    else:
                        print(f"Accessible: {url} (Status Code: {response.status_code})")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed for {url}: {e}")

                self.driver.get(url)
                self.accept_cookie_consent()
                current_url = self.get_current_url()
                self.check_redirects_to_pages(current_url, expected_redirect)

    def check_redirects_to_pages(self, current_url, expected_redirect):
        translated_current_url = self.translate_url(current_url)
        translated_expected_url = self.translate_url(expected_redirect)
        if translated_current_url != translated_expected_url:
            print(f"\nError: URL {translated_current_url} does NOT match the expected redirect: {translated_expected_url}")

    def get_expected_redirect(self, entry):
        if "allsports.fit" in self.domain:
            return entry["expected_redirect_prod"]
        else:
            return entry["expected_redirect_test"]

    def check_links_four(self):
        for index, path in enumerate(self.pages_lincs_four):
            if index >= len(self.expected_parts):
                break

            link = f"{self.domain}{path}"
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
                self.accept_cookie_consent()
                current_url = self.driver.current_url
                translated_url = self.translate_url(current_url, is_full_url=True)

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

    def is_404_page(self):
        try:
            not_found_section = self.driver.find_element(By.CSS_SELECTOR, 'section.section.not-found-page')
            if not_found_section:
                return True
        except NoSuchElementException:
            return False

    def check_links_five(self):
        input_url = "https://оллспортс.бел"
        expected_url = "https://сайт.оллспортс.бел/ru-by"
        self.driver.get(input_url)
        time.sleep(5)
        current_url = self.driver.current_url
        current_url_translated = self.translate_url(current_url, is_full_url=True)
        expected_url_translated = self.translate_url(expected_url, is_full_url=True)
        if current_url_translated == expected_url_translated:
            print(f"Redirection successful: {current_url_translated}")
        else:
            print(f"Redirection failed: {current_url_translated}. Expected: {expected_url_translated}")

    def check_links_for_404(self):
        for link in self.links:
            try:
                response = requests.get(link)
                if response.status_code == 404:
                    print(f"404 Error: {link}")
                else:
                    print(f"Accessible: {link} (Status Code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {link}: {e}")




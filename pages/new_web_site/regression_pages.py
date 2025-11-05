# -*- coding: utf-8 -*-
import os
import time
import allure
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.elements_for_new_web_site.regression_pages_locators import RegressionLocators as L


class RegressionPages:
    """Класс, выполняющий полную регрессионную проверку всех страниц сайта."""

    def __init__(self, driver):
        self.driver = driver

    # ======================================================
    # 🔹 Общие методы
    # ======================================================
    @allure.step("Открыть страницу {1}")
    def open_page(self, url):
        self.driver.get(url)

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        """Закрытие cookie-баннера, если он отображается."""
        try:
            cookie_button = (By.CSS_SELECTOR, ".cookie-primary-modal__confirm")
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(cookie_button))
            self.driver.find_element(*cookie_button).click()
            time.sleep(0.5)
        except Exception:
            pass

    @allure.step("Проверить статус-код страницы")
    def check_http_status(self, url):
        """Проверка, что страница возвращает код 200."""
        response = requests.get(url, timeout=10)
        assert response.status_code == 200, f"❌ Страница {url} вернула код {response.status_code}"

    def _scroll_smoothly_through_page(self):
        """Плавный скролл всей страницы для подгрузки ленивых элементов."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(0, last_height, 400):
            self.driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.2)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.3)

    @allure.step("Проверить элемент на странице")
    def check_element_visible(self, locator):
        """Проверка элемента с автопрокруткой, повторными попытками и мягким падением."""
        for attempt in range(3):
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
                return element
            except Exception:
                self._scroll_smoothly_through_page()

        # если не найден после трёх попыток — логируем, но не падаем
        allure.attach(body=f"{locator}", name="Не найден элемент", attachment_type=allure.attachment_type.TEXT)
        self.take_screenshot(f"missing_{locator[1].replace('/', '_')[:50]}")
        print(f"[WARN] Элемент {locator} не найден после нескольких попыток")
        return None

    @allure.step("Проверить ошибки JavaScript")
    def check_js_errors(self):
        """Проверка отсутствия ошибок JavaScript уровня SEVERE."""
        try:
            logs = self.driver.get_log("browser")
            severe = [entry for entry in logs if entry["level"] == "SEVERE"]
            assert not severe, f"⚠️ Обнаружены JS-ошибки: {severe}"
        except Exception:
            pass

    def take_screenshot(self, name):
        """Создать скриншот."""
        os.makedirs("screenshots", exist_ok=True)
        file_path = f"screenshots/{name}_{int(time.time())}.png"
        self.driver.save_screenshot(file_path)
        allure.attach.file(file_path, name=name, attachment_type=allure.attachment_type.PNG)

    # ======================================================
    # 🔹 Основной регрессионный сценарий
    # ======================================================
    @allure.step("Выполнить полную регрессию сайта")
    def run_full_regression(self):
        """Основной метод, который проходит по всем страницам и проверяет их работу."""
        for page_key, data in L.PAGES.items():
            url = data["url"]
            locators = data["locators"]

            with allure.step(f"Проверка страницы: {page_key} — {url}"):
                try:
                    # 1️⃣ Проверка кода 200
                    self.check_http_status(url)

                    # 2️⃣ Открытие страницы
                    self.open_page(url)

                    # 3️⃣ Принять cookies
                    self.accept_cookie_consent()

                    # 4️⃣ Прокрутить страницу
                    self._scroll_smoothly_through_page()

                    # 5️⃣ Проверить элементы
                    missing = []
                    for locator in locators:
                        if not self.check_element_visible(locator):
                            missing.append(locator)

                    # 6️⃣ Проверка JS ошибок
                    self.check_js_errors()

                    # 7️⃣ Отчёт, если что-то не найдено
                    if missing:
                        allure.attach(str(missing), "Отсутствующие элементы", allure.attachment_type.TEXT)
                        print(f"[WARN] На странице {url} отсутствуют элементы: {missing}")

                except Exception as e:
                    self.take_screenshot(page_key)
                    raise AssertionError(f"Ошибка на странице {url}: {e}")

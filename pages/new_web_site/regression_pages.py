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
    """Строгая регрессионная проверка всех страниц сайта с ленивой прокруткой."""

    def __init__(self, driver):
        self.driver = driver
        self.checks_total = 0
        self.checks_passed = 0
        self.checks_failed = 0

    # ==============================
    # 🔹 Общие методы
    # ==============================
    @allure.step("Открыть страницу {1}")
    def open_page(self, url):
        self.driver.get(url)

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        try:
            cookie_button = (By.CSS_SELECTOR, ".cookie-primary-modal__confirm")
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(cookie_button))
            self.driver.find_element(*cookie_button).click()
            time.sleep(0.5)
        except Exception:
            pass

    @allure.step("Проверить статус-код страницы")
    def check_http_status(self, url):
        response = requests.get(url, timeout=10)
        assert response.status_code == 200, f"❌ Страница {url} вернула код {response.status_code}"

    # ==============================
    # 🔹 Улучшенная прокрутка
    # ==============================
    def _lazy_scroll(self, step=400, delay=0.3, max_cycles=3):
        """Ленивая прокрутка всей страницы: 3 цикла вверх-вниз для гарантии подгрузки lazy-контента."""
        for cycle in range(max_cycles):
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            for pos in range(0, last_height, step):
                self.driver.execute_script(f"window.scrollTo(0, {pos});")
                time.sleep(delay)
            # Возвращаемся вверх — помогает подгрузить изображения и iframes
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(delay)
        time.sleep(1)

    @allure.step("Проверить элемент на странице")
    def check_element_visible(self, locator):
        """Мягкая проверка — НЕ прерывает тест, ошибки записываются."""

        self.checks_total += 1  # считаем проверку

        for attempt in range(3):
            try:
                element = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located(locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                WebDriverWait(self.driver, 6).until(EC.visibility_of_element_located(locator))

                self.checks_passed += 1
                print(f"CHECK_OK: {locator}")  # <-- важный print
                return element
            except Exception:
                self._lazy_scroll()

        # если не нашли
        self.checks_failed += 1
        print(f"❌ FAIL: {locator}")  # <-- важный print

        try:
            self.take_screenshot(f"missing_{locator[1].replace('/', '_')[:40]}")
        except:
            pass

        return None

    def take_screenshot(self, name):
        os.makedirs("screenshots", exist_ok=True)
        file_path = f"screenshots/{name}_{int(time.time())}.png"
        self.driver.save_screenshot(file_path)
        allure.attach.file(file_path, name=name, attachment_type=allure.attachment_type.PNG)

    # ==============================
    # 🔹 Основной регрессионный сценарий
    # ==============================
    @allure.step("Выполнить полную регрессию сайта")
    def run_full_regression(self):
        """Проходит по всем страницам, выполняет реальную ленивую прокрутку и проверку элементов."""

        # Инициализация счётчиков
        self.checks_total = 0
        self.checks_failed = 0

        # страницы без скролла
        no_scroll_pages = [
            "policy/251010_processing_personal_data",
            "license/241009_license",
            "individual_license/241009_license",
            "rule/250731_rule",
            "facilities-table",
        ]

        for page_key, data in L.PAGES.items():
            url = data["url"]
            locators = data["locators"]
            skip_scroll = any(skip in url for skip in no_scroll_pages)

            with allure.step(f"Проверка страницы: {page_key} — {url}"):
                try:
                    # 1️⃣ Проверяем код ответа
                    self.check_http_status(url)

                    # 2️⃣ Открываем страницу
                    self.open_page(url)

                    # 3️⃣ Принять cookies
                    self.accept_cookie_consent()

                    # 4️⃣ Ленивая прокрутка
                    if not skip_scroll:
                        self._lazy_scroll()
                    else:
                        print(f"[INFO] Пропускаем прокрутку для {url}")

                    # 5️⃣ Проверка элементов
                    for locator in locators:
                        self.checks_total += 1
                        try:
                            self.check_element_visible(locator)
                        except Exception as e:
                            print(f"❌ FAIL: {locator} — {e}")
                            self.checks_failed += 1
                            continue

                except Exception as e:
                    self.take_screenshot(page_key)
                    print(f"❌ FAIL_PAGE: {url} — {e}")
                    self.checks_failed += 1
                    continue

        # ==== Итоговые принты для bash =====
        checks_passed = self.checks_total - self.checks_failed

        print(f"CHECKS_TOTAL={self.checks_total}")
        print(f"CHECKS_PASSED={checks_passed}")
        print(f"CHECKS_FAILED={self.checks_failed}")


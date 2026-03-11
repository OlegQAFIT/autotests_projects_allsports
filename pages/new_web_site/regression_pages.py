# -*- coding: utf-8 -*-
import os
import time
import allure
import requests
from urllib.parse import urlparse, urlunparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.elements_for_new_web_site.regression_pages_locators import RegressionLocators as L


class RegressionPages:
    """Строгая регрессионная проверка всех страниц сайта с ленивой прокруткой."""

    def __init__(self, driver):
        self.driver = driver
        self.base_url = getattr(driver, 'base_url', '').rstrip('/')

    def _resolve_url(self, url: str) -> str:
        if not self.base_url:
            return url
        parsed_target = urlparse(url)
        parsed_base = urlparse(self.base_url)
        if parsed_target.scheme and parsed_target.netloc and parsed_base.scheme and parsed_base.netloc:
            return urlunparse(
                (
                    parsed_base.scheme,
                    parsed_base.netloc,
                    parsed_target.path,
                    parsed_target.params,
                    parsed_target.query,
                    parsed_target.fragment,
                )
            )
        return url

    def _record_failure(self, page_key, url, reason, locator='-'):
        self.failed_items.append(
            {
                "page": page_key,
                "url": self._resolve_url(url),
                "locator": str(locator),
                "reason": str(reason),
            }
        )

    # ==============================
    # 🔹 Общие методы
    # ==============================
    @allure.step("Открыть страницу {1}")
    def open_page(self, url):
        self.driver.get(self._resolve_url(url))

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
        resolved_url = self._resolve_url(url)
        response = requests.get(resolved_url, timeout=10)
        assert response.status_code == 200, f"❌ Страница {resolved_url} вернула код {response.status_code}"

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
        """Жёсткая проверка: если элемент не найден даже после ленивой прокрутки — тест падает."""
        for attempt in range(3):
            try:
                element = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located(locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                WebDriverWait(self.driver, 6).until(EC.visibility_of_element_located(locator))
                return element
            except Exception:
                self._lazy_scroll()
        self.take_screenshot(f"missing_{locator[1].replace('/', '_')[:40]}")
        raise AssertionError(f"❌ Элемент {locator} не найден после нескольких циклов прокрутки")

    @allure.step("Проверить ошибки JavaScript")
    def check_js_errors(self):
        try:
            logs = self.driver.get_log("browser")
            return [entry for entry in logs if entry.get("level") == "SEVERE"]
        except Exception:
            return []

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

        # ---- СЧЁТЧИКИ ----
        self.checks_total = 0
        self.checks_passed = 0
        self.checks_failed = 0
        self.failed_items = []

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

                    # 4️⃣ Прокрутка
                    if not skip_scroll:
                        self._lazy_scroll()

                    # 5️⃣ Проверка всех локаторов — БЕЗ остановки теста!
                    for locator in locators:
                        self.checks_total += 1
                        try:
                            self.check_element_visible(locator)
                            self.checks_passed += 1
                        except Exception as e:
                            self.checks_failed += 1
                            self._record_failure(page_key, url, e, locator=locator)

                    # 6️⃣ Проверка JS ошибок
                    severe_logs = self.check_js_errors()
                    if severe_logs:
                        self.checks_failed += 1
                        js_error = f"SEVERE console errors: {severe_logs[:3]}"
                        self._record_failure(page_key, url, js_error, locator='[JS_CONSOLE]')

                except Exception as e:
                    self.take_screenshot(page_key)
                    self.checks_failed += 1
                    self._record_failure(page_key, url, e, locator='[PAGE]')

        summary_lines = [
            "=== FINAL REGRESSION SUMMARY ===",
            f"CHECKS_TOTAL={self.checks_total}",
            f"CHECKS_PASSED={self.checks_passed}",
            f"CHECKS_FAILED={self.checks_failed}",
        ]

        if self.failed_items:
            summary_lines.append("FAILED_ITEMS:")
            for idx, item in enumerate(self.failed_items, 1):
                summary_lines.append(
                    f"{idx}. page={item['page']} | url={item['url']} | "
                    f"locator={item['locator']} | reason={item['reason']}"
                )
        else:
            summary_lines.append("FAILED_ITEMS: none")

        summary_text = "\n".join(summary_lines)
        print(summary_text)
        allure.attach(
            summary_text,
            name="regression-final-summary",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert self.checks_failed == 0, (
            f"Регрессия завершилась с ошибками: failed={self.checks_failed}, "
            f"passed={self.checks_passed}, total={self.checks_total}"
        )

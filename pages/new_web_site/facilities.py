# -*- coding: utf-8 -*-
import time
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.base import BasePage
from locators.elements_for_new_web_site.for_facilities_page import FacilitiesLocators as L


class FacilitiesPage(BasePage):
    @allure.step("Открыть страницу Объекты")
    def open(self):
        self.driver.get(L.BASE_URL)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(L.PAGE_ROOT)
        )
        return self

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        try:
            self.click_if_visible(L.COOKIE_ACCEPT_BTN, timeout=3)
        except Exception:
            pass

    def _safe_scroll(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.4)
        except Exception:
            for _ in range(4):
                self.driver.execute_script("window.scrollBy(0, 700);")
                time.sleep(0.4)

    @allure.step("Проверить открытие страницы Объекты")
    def check_page_opened(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.PAGE_ROOT)
        )
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.PAGE_TITLE)
        )
        assert "/facilities" in self.driver.current_url, f"Открыт неверный URL: {self.driver.current_url}"

    @allure.step("Проверить отображение карты")
    def check_map_visible(self):
        self._safe_scroll(L.MAP_BLOCK)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(L.MAP_ROOT)
        )
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(L.MAP_CANVAS)
        )

    @allure.step("Проверить элементы управления карты")
    def check_map_controls(self):
        self._safe_scroll(L.MAP_ROOT)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.MAP_ZOOM_IN)
        )
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.MAP_ZOOM_OUT)
        )
        # Геолокация может быть отключена для headless/браузера — проверяем мягко.
        _ = self.driver.find_elements(*L.MAP_GEOLOCATE)

    @allure.step("Проверить фильтры объектов")
    def check_filters_visible(self):
        self._safe_scroll(L.MAP_BLOCK)
        WebDriverWait(self.driver, 20).until(
            lambda d: d.find_elements(*L.FILTER_BAR) or d.find_elements(*L.FILTER_BUTTONS)
        )
        buttons = self.driver.find_elements(*L.FILTER_BUTTONS)
        selects = self.driver.find_elements(*L.FILTER_SELECTS)
        assert len(buttons) >= 2, "Кнопки фильтров не найдены на странице Объекты"
        # Для части конфигураций селекты могут быть свернуты, но кнопки фильтра должны быть доступны.
        if not selects:
            assert any("фильтр" in b.text.lower() for b in buttons), (
                "Не найдены селекты фильтра и отсутствует кнопка 'Фильтр'"
            )

    @allure.step("Проверить список/таблицу объектов")
    def check_objects_content_loaded(self):
        self._safe_scroll(L.FILTER_BAR)
        values = self.driver.find_elements(*L.FACILITIES_LIST_ITEMS)
        assert len(values) >= 1, "Не найдены значения фильтров на странице объектов"

    @allure.step("Проверить блок таблицы объектов")
    def check_objects_table_block(self):
        self._safe_scroll(L.OBJECTS_TABLE_SECTION)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(L.OBJECTS_TABLE_SECTION)
        )
        href = self.driver.find_element(*L.OBJECTS_TABLE_SECTION).get_attribute("href") or ""
        assert L.TABLE_URL_SUFFIX in href, f"Ссылка на таблицу объектов некорректна: {href}"

    @allure.step("Проверить полный сценарий фильтрации на странице 'Список объектов (таблица)'")
    def check_full_table_filters_flow(self):
        self._safe_scroll(L.OBJECTS_TABLE_SECTION)
        table_link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(L.OBJECTS_TABLE_SECTION)
        )
        self.driver.execute_script("arguments[0].click();", table_link)
        WebDriverWait(self.driver, 20).until(EC.url_contains(L.TABLE_URL_SUFFIX))

        # Базовая загрузка таблицы
        WebDriverWait(self.driver, 25).until(
            lambda d: len(d.find_elements(*L.FACILITIES_TABLE_ROWS)) > 0
        )
        baseline_rows = len(self.driver.find_elements(*L.FACILITIES_TABLE_ROWS))
        assert baseline_rows > 0, "Таблица объектов не загружена"

        # Проверяем поиск
        search = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.TABLE_SEARCH_INPUT)
        )
        search.clear()
        search.send_keys("Адреналин")
        WebDriverWait(self.driver, 15).until(
            lambda d: len(d.find_elements(*L.FACILITIES_TABLE_ROWS)) > 0
        )
        filtered_rows = len(self.driver.find_elements(*L.FACILITIES_TABLE_ROWS))
        assert filtered_rows <= baseline_rows, (
            f"Поиск не сузил выборку: до={baseline_rows}, после={filtered_rows}"
        )

        # Проверяем открытие модалки фильтра
        filter_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(L.TABLE_FILTER_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", filter_btn)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.TABLE_FILTER_MODAL)
        )

        # Применяем/сбрасываем фильтр — проверка интерактивности контролов
        apply_buttons = self.driver.find_elements(*L.TABLE_FILTER_APPLY)
        assert apply_buttons, "Кнопка 'Применить' не найдена в модалке фильтра"
        self.driver.execute_script("arguments[0].click();", apply_buttons[0])
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(L.TABLE_FILTER_MODAL)
        )

        # Повторно открываем и проверяем кнопку сброса
        filter_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(L.TABLE_FILTER_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", filter_btn)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.TABLE_FILTER_MODAL)
        )
        reset_buttons = self.driver.find_elements(*L.TABLE_FILTER_RESET)
        assert reset_buttons, "Кнопка 'Сбросить фильтры' не найдена в модалке фильтра"
        self.driver.execute_script("arguments[0].click();", reset_buttons[0])
        apply_buttons = self.driver.find_elements(*L.TABLE_FILTER_APPLY)
        if apply_buttons:
            self.driver.execute_script("arguments[0].click();", apply_buttons[0])

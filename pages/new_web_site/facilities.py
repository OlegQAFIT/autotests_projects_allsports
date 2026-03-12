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
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(L.MAP_GEOLOCATE)
        )

    @allure.step("Проверить фильтры объектов")
    def check_filters_visible(self):
        self._safe_scroll(L.FILTER_BAR)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.FILTER_BAR)
        )
        buttons = self.driver.find_elements(*L.FILTER_BUTTONS)
        assert len(buttons) >= 1, "Кнопки фильтров не найдены на странице Объекты"

    @allure.step("Проверить список/таблицу объектов")
    def check_objects_content_loaded(self):
        self._safe_scroll(L.FACILITIES_LIST)
        WebDriverWait(self.driver, 20).until(
            lambda d: len(d.find_elements(*L.FACILITIES_LIST_ITEMS)) > 0
            or len(d.find_elements(*L.FACILITIES_TABLE_ROWS)) > 0
        )
        list_items = self.driver.find_elements(*L.FACILITIES_LIST_ITEMS)
        table_rows = self.driver.find_elements(*L.FACILITIES_TABLE_ROWS)
        assert list_items or table_rows, "Не найдено ни одного объекта в списке или таблице"

    @allure.step("Проверить блок таблицы объектов")
    def check_objects_table_block(self):
        self._safe_scroll(L.OBJECTS_TABLE_SECTION)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(L.OBJECTS_TABLE_SECTION)
        )
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(L.FACILITIES_TABLE)
        )

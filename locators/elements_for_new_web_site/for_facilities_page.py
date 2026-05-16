# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class FacilitiesLocators:
    """Локаторы для страницы https://www.allsports.by/ru-by/facilities"""

    BASE_URL = "https://www.allsports.by/ru-by/facilities"

    # === COMMON ===
    COOKIE_ACCEPT_BTN = (By.CSS_SELECTOR, ".cookie-primary-modal__confirm")
    PAGE_ROOT = (By.CSS_SELECTOR, "section.facilities")
    PAGE_TITLE = (By.CSS_SELECTOR, "section.facilities .facilities-header, section.facilities .facilities-filter")

    # === MAP ===
    MAP_BLOCK = (By.CSS_SELECTOR, "section.facilities .facilities-map, #map")
    MAP_ROOT = (By.ID, "map")
    MAP_CANVAS = (By.CSS_SELECTOR, "#map .mapboxgl-canvas")
    MAP_ZOOM_IN = (By.CSS_SELECTOR, "#map .mapboxgl-ctrl-zoom-in")
    MAP_ZOOM_OUT = (By.CSS_SELECTOR, "#map .mapboxgl-ctrl-zoom-out")
    MAP_GEOLOCATE = (By.CSS_SELECTOR, "#map .mapboxgl-ctrl-geolocate")

    # === FILTERS ===
    FILTER_BAR = (By.CSS_SELECTOR, ".facilities-filter-bar")
    FILTER_BUTTONS = (By.CSS_SELECTOR, ".facilities-filter-buttons .facilities-filter__button")
    FILTER_SELECTS = (By.CSS_SELECTOR, ".facilities-filter-bar .select-field")

    # === CONTENT ===
    FACILITIES_LIST = (By.CSS_SELECTOR, ".facilities-filter-bar")
    FACILITIES_LIST_ITEMS = (By.CSS_SELECTOR, ".facilities-filter-bar .select-field__value")
    OBJECTS_TABLE_SECTION = (By.CSS_SELECTOR, "a.facilities__objects-table")
    FACILITIES_TABLE = (By.CSS_SELECTOR, ".facilities-table")
    FACILITIES_TABLE_ROWS = (By.CSS_SELECTOR, ".facilities-table .facilities-table__row")

    # === FACILITIES TABLE PAGE ===
    TABLE_URL_SUFFIX = "/facilities-table"
    TABLE_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Поиск']")
    TABLE_FILTER_BUTTON = (By.CSS_SELECTOR, "button.facilities-table-filter__button")
    TABLE_FILTER_MODAL = (By.CSS_SELECTOR, ".modal-container.map-filter-modal, .modal")
    TABLE_FILTER_APPLY = (By.XPATH, "//button[contains(.,'Применить')]")
    TABLE_FILTER_RESET = (By.XPATH, "//button[contains(.,'Сбросить фильтры')]")

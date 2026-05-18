# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class FacilitiesLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy/facilities"
    TABLE_URL = "https://www.sportbenefit.eu/en-cy/facilities-table"

    PAGE_ROOT = (By.CSS_SELECTOR, "section.facilities, main")
    MAP_ROOT = (By.ID, "map")
    MAP_CANVAS = (By.CSS_SELECTOR, "#map .mapboxgl-canvas")
    MAP_ZOOM_IN = (By.CSS_SELECTOR, "#map .mapboxgl-ctrl-zoom-in")
    MAP_ZOOM_OUT = (By.CSS_SELECTOR, "#map .mapboxgl-ctrl-zoom-out")

    SEARCH_BUTTON = (By.XPATH, "//button[contains(.,'Search') or .//span[contains(.,'Search')]]")
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter') or .//span[contains(.,'Filter')]]")

    TABLE_ROWS = (By.CSS_SELECTOR, ".facilities-table .facilities-table__row")
    TABLE_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search']")
    TABLE_FILTER_BUTTON = (By.CSS_SELECTOR, "button.facilities-table-filter__button")

    FILTER_MODAL_ROOT = (By.CSS_SELECTOR, ".modal-container.map-filter-modal")
    FILTER_APPLY_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'map-filter-modal')]//button[.//span[normalize-space()='Apply'] or normalize-space()='Apply']",
    )
    FILTER_RESET_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'map-filter-modal')]//button[.//span[normalize-space()='Reset filters'] or normalize-space()='Reset filters']",
    )

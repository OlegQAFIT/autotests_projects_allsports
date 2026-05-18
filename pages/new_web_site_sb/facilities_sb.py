# -*- coding: utf-8 -*-
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.for_facilities_page_sb import FacilitiesLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class FacilitiesPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        return self

    def open_table_page(self):
        self.open_url(L.TABLE_URL)
        self.wait_table_loaded()
        return self

    def wait_table_loaded(self):
        WebDriverWait(self.driver, 25).until(
            lambda d: len(d.find_elements(*L.TABLE_ROWS)) > 0
        )

    def table_rows_count(self):
        return len(self.driver.find_elements(*L.TABLE_ROWS))

    def check_page_opened(self):
        assert "/facilities" in self.driver.current_url, f"Unexpected facilities URL: {self.driver.current_url}"

    def check_map_visible(self):
        self.assert_element_present(L.MAP_ROOT)
        self.assert_element_present(L.MAP_CANVAS)

    def check_map_controls(self):
        self.assert_element_present(L.MAP_ZOOM_IN)
        self.assert_element_present(L.MAP_ZOOM_OUT)

    def check_filter_buttons_visible(self):
        self.assert_element_present(L.SEARCH_BUTTON)
        self.assert_element_present(L.FILTER_BUTTON)

    def check_table_basics(self):
        self.wait_table_loaded()
        assert self.table_rows_count() > 0, "Facilities table is empty"
        self.assert_element_present(L.TABLE_SEARCH_INPUT)
        self.assert_element_present(L.TABLE_FILTER_BUTTON)

    def check_table_search(self, query="yoga"):
        self.wait_table_loaded()
        baseline = self.table_rows_count()
        search = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.TABLE_SEARCH_INPUT))
        search.clear()
        search.send_keys(query)
        time.sleep(0.8)

        filtered = self.table_rows_count()
        assert 0 < filtered <= baseline, (
            f"Search results are out of range for '{query}': baseline={baseline}, filtered={filtered}"
        )

    def _open_filter_modal(self):
        btn = WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(L.TABLE_FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, 12).until(EC.visibility_of_element_located(L.FILTER_MODAL_ROOT))

    def _close_filter_modal_apply(self):
        apply_btn = WebDriverWait(self.driver, 12).until(EC.presence_of_element_located(L.FILTER_APPLY_BUTTON))
        self.driver.execute_script("arguments[0].click();", apply_btn)
        WebDriverWait(self.driver, 12).until(EC.invisibility_of_element_located(L.FILTER_MODAL_ROOT))
        time.sleep(0.9)

    @staticmethod
    def _option_xpath(section_title, option_text):
        return (
            "//div[contains(@class,'map-filter-modal')]"
            f"//p[normalize-space()='{section_title}']/following-sibling::ul[1]"
            f"//li[.//span[contains(normalize-space(),\"{option_text}\")]]"
        )

    @staticmethod
    def _show_all_xpath(section_title):
        return (
            "//div[contains(@class,'map-filter-modal')]"
            f"//p[normalize-space()='{section_title}']/following-sibling::ul[1]"
            "//li[contains(@class,'show-all')]"
        )

    def _is_option_checked(self, section_title, option_text):
        li = WebDriverWait(self.driver, 8).until(
            EC.presence_of_element_located((By.XPATH, self._option_xpath(section_title, option_text)))
        )
        label = li.find_element(By.CSS_SELECTOR, "label.circle-checkbox")
        classes = (label.get_attribute("class") or "").strip()
        return "circle-checkbox_checked" in classes

    def _select_filter_option(self, section_title, option_text, show_all=True):
        if show_all:
            show_all_items = self.driver.find_elements(By.XPATH, self._show_all_xpath(section_title))
            if show_all_items:
                self.driver.execute_script("arguments[0].click();", show_all_items[0])
                time.sleep(0.15)

        li = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self._option_xpath(section_title, option_text)))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", li)
        self.driver.execute_script("arguments[0].click();", li)
        WebDriverWait(self.driver, 8).until(
            lambda _: self._is_option_checked(section_title, option_text)
        )

    def check_table_single_filter_value(self, section_title, option_text):
        self.wait_table_loaded()
        baseline = self.table_rows_count()
        assert baseline > 0, "Baseline table rows count is zero"

        self._open_filter_modal()
        self._select_filter_option(section_title, option_text, show_all=True)
        self._close_filter_modal_apply()

        filtered = self.table_rows_count()
        assert 0 < filtered < baseline, (
            f"Single filter did not narrow results: baseline={baseline}, filtered={filtered}, "
            f"filter={section_title}:{option_text}"
        )

    def check_table_filter_combination(self, filters):
        self.wait_table_loaded()
        baseline = self.table_rows_count()
        assert baseline > 0, "Baseline table rows count is zero"

        self._open_filter_modal()
        for flt in filters:
            self._select_filter_option(
                flt["section"],
                flt["option"],
                show_all=flt.get("show_all", True),
            )
        self._close_filter_modal_apply()

        filtered = self.table_rows_count()
        assert 0 < filtered < baseline, (
            f"Filter combination did not narrow results: baseline={baseline}, filtered={filtered}"
        )

    def check_table_reset_returns_baseline(self, filters, attempts=2):
        self.wait_table_loaded()
        baseline = self.table_rows_count()
        assert baseline > 0, "Baseline table rows count is zero"

        self._open_filter_modal()
        for flt in filters:
            self._select_filter_option(
                flt["section"],
                flt["option"],
                show_all=flt.get("show_all", True),
            )
        self._close_filter_modal_apply()

        narrowed = self.table_rows_count()
        assert narrowed < baseline, f"Pre-reset check failed: baseline={baseline}, narrowed={narrowed}"

        restored = narrowed
        for _ in range(attempts):
            self._open_filter_modal()
            reset_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(L.FILTER_RESET_BUTTON))
            self.driver.execute_script("arguments[0].click();", reset_btn)
            time.sleep(0.2)
            self._close_filter_modal_apply()
            restored = self.table_rows_count()
            if restored == baseline:
                break

        assert restored == baseline, (
            f"Reset did not restore baseline: baseline={baseline}, restored={restored}"
        )

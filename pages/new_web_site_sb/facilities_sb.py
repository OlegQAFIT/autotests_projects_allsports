# -*- coding: utf-8 -*-
import re
import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
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
        WebDriverWait(self.driver, 30).until(lambda d: len(d.find_elements(*L.TABLE_ROWS)) > 0)

    def wait_table_settled(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: len(d.find_elements(*L.TABLE_ROWS)) > 0 or len(d.find_elements(*L.TABLE_NO_RESULT)) > 0
        )

    def table_rows_count(self):
        return len(self.driver.find_elements(*L.TABLE_ROWS))

    def _visible_table_rows_count(self, retries=6):
        for _ in range(retries):
            rows = self.driver.find_elements(*L.TABLE_ROWS)
            visible = 0
            stale = False
            for row in rows:
                try:
                    if row.is_displayed():
                        visible += 1
                except StaleElementReferenceException:
                    stale = True
                    break
            if not stale:
                return visible
            time.sleep(0.25)
        return 0

    @staticmethod
    def _normalize_text(value):
        return re.sub(r"\s+", " ", str(value or "")).strip().lower()

    @classmethod
    def _normalize_key(cls, value):
        normalized = cls._normalize_text(value)
        normalized = normalized.replace("&", " and ")
        normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
        return normalized.strip("_")

    def _table_row_names(self):
        names = []
        for element in self.driver.find_elements(*L.TABLE_ROW_NAME):
            text = (element.text or "").strip()
            if text:
                names.append(text)
        return names

    def _open_filter_modal(self, trigger_locator):
        button = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(trigger_locator))
        self.driver.execute_script("arguments[0].click();", button)
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.FILTER_MODAL_ROOT))

    def _close_filter_modal_apply(self):
        apply_btn = WebDriverWait(self.driver, 12).until(EC.presence_of_element_located(L.FILTER_APPLY_BUTTON))
        self.driver.execute_script("arguments[0].click();", apply_btn)
        WebDriverWait(self.driver, 12).until(EC.invisibility_of_element_located(L.FILTER_MODAL_ROOT))
        time.sleep(0.9)

    def _reset_filters_in_modal(self):
        reset_btn = WebDriverWait(self.driver, 12).until(EC.presence_of_element_located(L.FILTER_RESET_BUTTON))
        self.driver.execute_script("arguments[0].click();", reset_btn)
        time.sleep(0.25)

    def _open_search_list_modal(self):
        button = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(L.SEARCH_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.SEARCH_LIST_MODAL))
        WebDriverWait(self.driver, 20).until(
            lambda d: len(d.find_elements(*L.FACILITY_LIST_ITEMS)) > 0 or len(d.find_elements(*L.FACILITY_LIST_EMPTY)) > 0
        )

    def _close_search_list_modal(self):
        close_buttons = self.driver.find_elements(*L.SEARCH_LIST_CLOSE)
        if close_buttons:
            try:
                self.driver.execute_script("arguments[0].click();", close_buttons[0])
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(L.SEARCH_LIST_MODAL))
                return
            except Exception:
                pass

        search_buttons = self.driver.find_elements(*L.SEARCH_BUTTON)
        if search_buttons:
            self.driver.execute_script("arguments[0].click();", search_buttons[0])
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(L.SEARCH_LIST_MODAL))

    def _search_list_items_count(self):
        return len(self.driver.find_elements(*L.FACILITY_LIST_ITEMS))

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

        try:
            WebDriverWait(self.driver, 8).until(lambda _: self._is_option_checked(section_title, option_text))
        except TimeoutException:
            # Some options in "More" can update state without checkbox class transition.
            time.sleep(0.35)

    def _set_table_search(self, query):
        search = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.TABLE_SEARCH_INPUT))
        query = query or ""

        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            input.focus();
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            search,
            query,
        )

        time.sleep(1.0)
        self.wait_table_settled()

    def get_table_filter_state(self):
        return self.driver.execute_script(
            """
            const state = window.__NUXT__?.pinia?.tableFilter;
            if (!state) {
              return null;
            }

            const toText = (value) => {
              if (value == null) return '';
              if (typeof value === 'string') return value;
              if (typeof value === 'number' || typeof value === 'boolean') return String(value);
              if (Array.isArray(value)) return '';
              if (typeof value === 'object') {
                if (typeof value.value === 'string') return value.value;
                if (typeof value.id === 'string') return value.id;
                if (typeof value.name === 'string') return value.name;
              }
              return '';
            };

            const toTextList = (items) => Array.isArray(items)
              ? items.map(toText).filter(Boolean)
              : [];

            const groups = Array.isArray(state.facilities) ? state.facilities : [];
            const objects = [];

            groups.forEach((group) => {
              const groupCity = toText(group?.city);
              const groupObjects = Array.isArray(group?.objects) ? group.objects : [];
              groupObjects.forEach((obj) => {
                objects.push({
                  id: obj?.id ?? null,
                  name: toText(obj?.name),
                  city: toText(obj?.city || groupCity),
                  activities: toTextList(obj?.activities),
                  tags: toTextList(obj?.tags),
                  services: toTextList(obj?.services),
                  levels: toTextList(obj?.levels),
                });
              });
            });

            return {
              selectedLevels: toTextList(state.selectedLevels),
              selectedActivities: toTextList(state.selectedActivities),
              selectedCities: toTextList(state.selectedCities),
              selectedTags: toTextList(state.selectedTags),
              search: toText(state.search),
              objectsCount: objects.length,
              objects: objects,
            };
            """
        )

    def get_map_filter_state(self):
        return self.driver.execute_script(
            """
            const state = window.__NUXT__?.pinia?.mapFilter;
            if (!state) {
              return null;
            }

            const toText = (value) => {
              if (value == null) return '';
              if (typeof value === 'string') return value;
              if (typeof value === 'number' || typeof value === 'boolean') return String(value);
              if (typeof value === 'object') {
                if (typeof value.value === 'string') return value.value;
                if (typeof value.id === 'string') return value.id;
                if (typeof value.name === 'string') return value.name;
              }
              return '';
            };

            const toTextList = (items) => Array.isArray(items)
              ? items.map(toText).filter(Boolean)
              : [];

            return {
              city: toText(state.city),
              activities: toTextList(state.activities),
              tags: toTextList(state.tags),
              search: toText(state.search),
              searchActivities: toText(state.searchActivities),
              selectedLevel: toText(state.selectedLevel),
            };
            """
        )

    def _assert_table_rows_are_from_state(self, state):
        row_names = self._table_row_names()
        assert row_names, "Visible table row names are empty"

        state_names = {self._normalize_text(item.get("name")) for item in state["objects"] if item.get("name")}
        assert state_names, "State object names are empty"

        unknown_names = [name for name in row_names if self._normalize_text(name) not in state_names]
        assert not unknown_names, f"Rows not found in table state: {unknown_names[:5]}"

    def _assert_selected_contains_expected(self, selected_values, expected_value, kind):
        expected_norm = self._normalize_key(expected_value)
        selected_norm = {self._normalize_key(value) for value in selected_values if value}
        assert selected_norm, f"State has no selected values for {kind}"
        assert any(expected_norm in value or value in expected_norm for value in selected_norm), (
            f"Expected '{expected_value}' in selected {kind}, got {selected_values}"
        )

    def _assert_city_content_matches(self, state, expected_city):
        self._assert_selected_contains_expected(state["selectedCities"], expected_city, "city")
        expected_norm = self._normalize_key(expected_city)

        assert state["objectsCount"] > 0, "No objects after city filter"
        for item in state["objects"]:
            city_norm = self._normalize_key(item.get("city"))
            assert city_norm, f"Object without city in filtered state: {item}"
            assert expected_norm in city_norm or city_norm in expected_norm, (
                f"Filtered city mismatch: expected '{expected_city}', got '{item.get('city')}'"
            )

    def _assert_activity_content_matches(self, state, expected_activity):
        self._assert_selected_contains_expected(state["selectedActivities"], expected_activity, "activity")
        selected = {self._normalize_key(value) for value in state["selectedActivities"] if value}

        assert state["objectsCount"] > 0, "No objects after activity filter"
        for item in state["objects"]:
            object_activities = {self._normalize_key(value) for value in item.get("activities", []) if value}
            assert object_activities & selected, (
                f"Object does not match selected activity set: {item.get('name')} -> {item.get('activities')}"
            )

    def _assert_tag_content_matches(self, state, expected_tag):
        self._assert_selected_contains_expected(state["selectedTags"], expected_tag, "tag")
        selected = {self._normalize_key(value) for value in state["selectedTags"] if value}

        assert state["objectsCount"] > 0, "No objects after 'More' filter"
        for item in state["objects"]:
            object_tags = {self._normalize_key(value) for value in item.get("tags", []) if value}
            object_services = {self._normalize_key(value) for value in item.get("services", []) if value}
            merged = object_tags | object_services
            assert merged & selected, (
                f"Object does not match selected tag set: {item.get('name')} -> tags={item.get('tags')}, "
                f"services={item.get('services')}"
            )

    def _assert_level_content_matches(self, state, expected_level):
        expected_norm = self._normalize_key(expected_level)
        assert state["objectsCount"] > 0, "No objects after level filter"

        for item in state["objects"]:
            object_levels = {self._normalize_key(value) for value in item.get("levels", []) if value}
            assert any(
                expected_norm == level or expected_norm in level or level in expected_norm
                for level in object_levels
            ), f"Object does not match selected level '{expected_level}': {item.get('name')} -> {item.get('levels')}"

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
        baseline = self._visible_table_rows_count()
        self._set_table_search(query)

        filtered = self._visible_table_rows_count()
        assert 0 < filtered <= baseline, (
            f"Search results are out of range for '{query}': baseline={baseline}, filtered={filtered}"
        )

    def check_table_single_filter_value(self, section_title, option_text):
        self.wait_table_loaded()
        baseline = self._visible_table_rows_count()
        assert baseline > 0, "Baseline table rows count is zero"

        self._open_filter_modal(L.TABLE_FILTER_BUTTON)
        self._select_filter_option(section_title, option_text, show_all=True)
        self._close_filter_modal_apply()

        filtered = self._visible_table_rows_count()
        assert 0 < filtered < baseline, (
            f"Single filter did not narrow results: baseline={baseline}, filtered={filtered}, "
            f"filter={section_title}:{option_text}"
        )

    def check_table_filter_combination(self, filters):
        self.wait_table_loaded()
        baseline = self._visible_table_rows_count()
        assert baseline > 0, "Baseline table rows count is zero"

        self._open_filter_modal(L.TABLE_FILTER_BUTTON)
        for flt in filters:
            self._select_filter_option(
                flt["section"],
                flt["option"],
                show_all=flt.get("show_all", True),
            )
        self._close_filter_modal_apply()

        filtered = self._visible_table_rows_count()
        assert 0 < filtered < baseline, (
            f"Filter combination did not narrow results: baseline={baseline}, filtered={filtered}"
        )

    def check_table_reset_returns_baseline(self, filters, attempts=2):
        self.wait_table_loaded()
        baseline = self._visible_table_rows_count()
        assert baseline > 0, "Baseline table rows count is zero"

        self._open_filter_modal(L.TABLE_FILTER_BUTTON)
        for flt in filters:
            self._select_filter_option(
                flt["section"],
                flt["option"],
                show_all=flt.get("show_all", True),
            )
        self._close_filter_modal_apply()

        narrowed = self._visible_table_rows_count()
        assert narrowed < baseline, f"Pre-reset check failed: baseline={baseline}, narrowed={narrowed}"

        restored = narrowed
        for _ in range(attempts):
            self._open_filter_modal(L.TABLE_FILTER_BUTTON)
            self._reset_filters_in_modal()
            self._close_filter_modal_apply()
            restored = self._visible_table_rows_count()
            if restored == baseline:
                break

        assert restored == baseline, f"Reset did not restore baseline: baseline={baseline}, restored={restored}"

    def check_table_filter_content_matches(self, section_title, option_text, content_kind):
        self.wait_table_loaded()
        baseline = self._visible_table_rows_count()
        assert baseline > 0, "Baseline table rows count is zero"

        self._open_filter_modal(L.TABLE_FILTER_BUTTON)
        self._select_filter_option(section_title, option_text, show_all=True)
        self._close_filter_modal_apply()
        self.wait_table_settled()

        filtered = self._visible_table_rows_count()
        assert 0 < filtered <= baseline, (
            f"Filter returned invalid rows: baseline={baseline}, filtered={filtered}, "
            f"filter={section_title}:{option_text}"
        )
        if content_kind != "tag":
            assert filtered < baseline, (
                f"Filter did not narrow rows: baseline={baseline}, filtered={filtered}, "
                f"filter={section_title}:{option_text}"
            )

        state = self.get_table_filter_state()
        assert state, "tableFilter state is unavailable"
        self._assert_table_rows_are_from_state(state)

        if content_kind == "city":
            self._assert_city_content_matches(state, option_text)
        elif content_kind == "activity":
            self._assert_activity_content_matches(state, option_text)
        elif content_kind == "tag":
            self._assert_tag_content_matches(state, option_text)
        elif content_kind == "level":
            self._assert_level_content_matches(state, option_text)
        else:
            raise AssertionError(f"Unsupported content kind: {content_kind}")

    def check_table_search_filters_reset_empty_state(
        self,
        search_query="yoga",
        city="Limassol",
        activity="Aerial Yoga",
        empty_query="zzzzzzzzzz_not_found",
    ):
        self.wait_table_loaded()

        baseline_state = self.get_table_filter_state()
        assert baseline_state, "tableFilter state is unavailable at baseline"
        baseline_count = baseline_state["objectsCount"]
        assert baseline_count > 0, "Baseline object count is zero"

        self._set_table_search(search_query)
        search_state = self.get_table_filter_state()
        assert search_state and search_state["search"] == search_query, "Search state is not set"
        assert search_state["objectsCount"] > 0, "Search unexpectedly returned zero results"
        assert search_state["objectsCount"] <= baseline_count, "Search unexpectedly expanded dataset"

        self._open_filter_modal(L.TABLE_FILTER_BUTTON)
        self._select_filter_option("City", city, show_all=True)
        self._select_filter_option("Activities", activity, show_all=True)
        self._close_filter_modal_apply()
        self.wait_table_settled()

        combined_state = self.get_table_filter_state()
        assert combined_state, "tableFilter state unavailable after combined search+filters"
        assert combined_state["objectsCount"] > 0, "Combined search+filters returned empty unexpectedly"
        assert combined_state["objectsCount"] <= search_state["objectsCount"], (
            "Combined search+filters should not expand dataset"
        )
        self._assert_table_rows_are_from_state(combined_state)

        reset_state = None
        for _ in range(3):
            self._open_filter_modal(L.TABLE_FILTER_BUTTON)
            self._reset_filters_in_modal()
            self._close_filter_modal_apply()

            self._set_table_search("")
            reset_state = self.get_table_filter_state()
            assert reset_state, "tableFilter state unavailable after reset"

            no_active_filters = (
                len(reset_state["selectedCities"]) == 0
                and len(reset_state["selectedActivities"]) == 0
                and len(reset_state["selectedTags"]) == 0
                and len(reset_state["selectedLevels"]) == 0
            )
            if reset_state["search"] == "" and no_active_filters and reset_state["objectsCount"] == baseline_count:
                break

        assert reset_state["search"] == "", "Search query was not cleared"
        assert reset_state["objectsCount"] == baseline_count, (
            f"Baseline not restored after reset flow: baseline={baseline_count}, current={reset_state['objectsCount']}"
        )

        self._set_table_search(empty_query)
        empty_state = self.get_table_filter_state()
        assert empty_state is not None, "tableFilter state unavailable for empty-state check"

        no_result_visible = len(self.driver.find_elements(*L.TABLE_NO_RESULT)) > 0
        rows_visible = self._visible_table_rows_count()
        assert empty_state["objectsCount"] == 0, f"Empty-state search returned objects: {empty_state['objectsCount']}"
        assert no_result_visible or rows_visible == 0, (
            f"Expected table empty-state UI after impossible search; rows_visible={rows_visible}, "
            f"no_result_visible={no_result_visible}"
        )

    def check_map_marker_popup(self):
        self.check_map_visible()
        self.check_map_controls()
        self.check_filter_buttons_visible()

        self._open_search_list_modal()
        items = self.driver.find_elements(*L.FACILITY_LIST_ITEMS)
        assert items, "Facility search list is empty"

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", items[0])
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", items[0])

        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.FACILITY_POPUP))
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.FACILITY_OBJECT_MODAL))

        popup_text = self.driver.find_element(*L.FACILITY_POPUP).text.strip()
        assert popup_text, "Facility popup text is empty"

    def check_map_reacts_to_filters(self, section_title="City", option_text="Limassol"):
        self.check_map_visible()
        self.check_filter_buttons_visible()

        self._open_search_list_modal()
        baseline_list = self._search_list_items_count()
        assert baseline_list > 0, "Baseline facilities list count is zero"
        self._close_search_list_modal()

        self._open_filter_modal(L.FILTER_BUTTON)
        self._select_filter_option(section_title, option_text, show_all=True)
        self._close_filter_modal_apply()

        map_state = self.get_map_filter_state()
        assert map_state, "mapFilter state is unavailable"
        if section_title == "City":
            assert self._normalize_key(option_text) in self._normalize_key(map_state["city"]), (
                f"Map city state was not set to '{option_text}': got '{map_state['city']}'"
            )

        self._open_search_list_modal()
        filtered_list = self._search_list_items_count()
        empty_visible = len(self.driver.find_elements(*L.FACILITY_LIST_EMPTY)) > 0

        assert filtered_list <= baseline_list, (
            f"Filtered facilities list expanded unexpectedly: baseline={baseline_list}, filtered={filtered_list}"
        )
        assert filtered_list < baseline_list or empty_visible, (
            f"Facilities list did not react to filter '{section_title}:{option_text}': "
            f"baseline={baseline_list}, filtered={filtered_list}, empty_visible={empty_visible}"
        )

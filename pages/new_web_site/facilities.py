# -*- coding: utf-8 -*-
import re
import time

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.base import BasePage
from locators.elements_for_new_web_site.for_facilities_page import FacilitiesLocators as L


class FacilitiesPage(BasePage):
    VALUE_ALIASES = {
        "гомель": {"гомель", "gomel"},
        "аквааэробика": {"аквааэробика", "aqua_aerobic", "aqua_aerobics"},
        "аргентинское танго": {"аргентинское_танго", "argentina_tango", "argentine_tango"},
        "адреналин": {"адреналин", "adrenalin", "adrenalin"},
    }

    @allure.step("Открыть страницу Объекты")
    def open(self):
        self.driver.get(L.BASE_URL)
        WebDriverWait(self.driver, 25).until(EC.presence_of_element_located(L.PAGE_ROOT))
        return self

    @allure.step("Открыть страницу 'Список объектов (таблица)'")
    def open_table_page(self):
        base_url = getattr(self.driver, "base_url", "https://www.allsports.by/ru-by").rstrip("/")
        self.driver.get(f"{base_url}{L.TABLE_URL_SUFFIX}")
        WebDriverWait(self.driver, 20).until(EC.url_contains(L.TABLE_URL_SUFFIX))
        self.wait_table_loaded()
        return self

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        locators = [
            L.COOKIE_ACCEPT_BTN,
            (By.XPATH, "//button[normalize-space()='Принять' or .//span[normalize-space()='Принять']]"),
            (By.XPATH, "//button[normalize-space()='Подтвердить' or .//span[normalize-space()='Подтвердить']]"),
            (By.XPATH, "//button[normalize-space()='Accept' or .//span[normalize-space()='Accept']]"),
            (By.XPATH, "//button[normalize-space()='Confirm' or .//span[normalize-space()='Confirm']]"),
        ]

        end_at = time.time() + 6
        while time.time() < end_at:
            clicked = False
            found_any = False

            for locator in locators:
                elements = self.driver.find_elements(*locator)
                if elements:
                    found_any = True

                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            self.driver.execute_script("arguments[0].click();", element)
                            clicked = True
                            time.sleep(0.35)
                            break
                    except Exception:
                        continue

                if clicked:
                    break

            if clicked:
                continue

            if not found_any:
                break

            time.sleep(0.25)

    def _safe_scroll(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                element,
            )
            time.sleep(0.4)
        except Exception:
            for _ in range(4):
                self.driver.execute_script("window.scrollBy(0, 700);")
                time.sleep(0.4)

    @staticmethod
    def _normalize_text(value):
        return re.sub(r"\s+", " ", str(value or "")).strip().lower()

    @classmethod
    def _normalize_key(cls, value):
        normalized = cls._normalize_text(value)
        normalized = normalized.replace("&", " и ")
        normalized = normalized.replace("ё", "е")
        normalized = re.sub(r"[^a-zа-я0-9]+", "_", normalized)
        return normalized.strip("_")

    def wait_table_loaded(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: len(d.find_elements(*L.FACILITIES_TABLE_ROWS)) > 0
        )

    def wait_table_settled(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: len(d.find_elements(*L.FACILITIES_TABLE_ROWS)) > 0
            or len(d.find_elements(*L.FACILITIES_TABLE_NO_RESULT)) > 0
        )

    def _is_any_displayed(self, locator):
        for element in self.driver.find_elements(*locator):
            try:
                if element.is_displayed():
                    return True
            except StaleElementReferenceException:
                continue
        return False

    def _visible_table_rows_count(self, retries=6):
        for _ in range(retries):
            rows = self.driver.find_elements(*L.FACILITIES_TABLE_ROWS)
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

    def _table_row_names(self):
        for _ in range(6):
            names = []
            stale = False
            for element in self.driver.find_elements(*L.FACILITIES_TABLE_ROW_NAME):
                try:
                    text = (element.text or "").strip()
                except StaleElementReferenceException:
                    stale = True
                    break
                if text:
                    names.append(text)
            if not stale:
                return names
            time.sleep(0.25)
        return []

    def _open_table_filter_modal(self):
        buttons = self.driver.find_elements(*L.TABLE_FILTER_BUTTON)
        if not buttons:
            return
        self.driver.execute_script("arguments[0].click();", buttons[0])
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.TABLE_FILTER_MODAL_ROOT)
        )

    def _open_main_filter_modal(self):
        buttons = self.driver.find_elements(*L.FILTER_BUTTON)
        if not buttons:
            return
        self.driver.execute_script("arguments[0].click();", buttons[0])
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.FILTER_MODAL_ROOT)
        )

    def _close_main_filter_modal_apply(self):
        apply_btn = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(L.FILTER_APPLY)
        )
        self.driver.execute_script("arguments[0].click();", apply_btn)
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(L.FILTER_MODAL_ROOT)
        )
        time.sleep(0.9)

    def _reset_main_filters_in_modal(self):
        reset_btn = WebDriverWait(self.driver, 12).until(
            EC.presence_of_element_located(L.FILTER_RESET)
        )
        self.driver.execute_script("arguments[0].click();", reset_btn)
        time.sleep(0.25)

    def _open_search_list_modal(self):
        buttons = self.driver.find_elements(*L.SEARCH_BUTTON)
        if buttons:
            self.driver.execute_script("arguments[0].click();", buttons[0])
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: len(d.find_elements(*L.SEARCH_LIST_MODAL)) > 0
                    or len(d.find_elements(*L.FACILITY_LIST_ITEMS)) > 0
                    or len(d.find_elements(*L.FACILITY_LIST_EMPTY)) > 0
                )
                return
            except TimeoutException:
                pass

        if not buttons or not self.driver.find_elements(*L.SEARCH_LIST_MODAL):
            search_input = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(L.MAIN_SEARCH_INPUT)
            )
            query = "Фитнес"
            self.driver.execute_script(
                """
                const input = arguments[0];
                const value = arguments[1];
                input.focus();
                const setter = Object.getOwnPropertyDescriptor(
                  window.HTMLInputElement.prototype,
                  'value'
                ).set;
                setter.call(input, value);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true, key: 't' }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                """,
                search_input,
                query,
            )
            time.sleep(0.8)
            WebDriverWait(self.driver, 20).until(
                lambda d: len(d.find_elements(*L.SEARCH_LIST_MODAL)) > 0
                or len(d.find_elements(*L.FACILITY_LIST_ITEMS)) > 0
                or len(d.find_elements(*L.FACILITY_LIST_EMPTY)) > 0
            )

    def _close_search_list_modal(self):
        if not self._is_any_displayed(L.SEARCH_BUTTON):
            search_inputs = self.driver.find_elements(*L.MAIN_SEARCH_INPUT)
            if search_inputs:
                self.driver.execute_script(
                    """
                    const input = arguments[0];
                    input.value = '';
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.blur();
                    """,
                    search_inputs[0],
                )
                time.sleep(0.6)
            return

        close_buttons = self.driver.find_elements(*L.SEARCH_LIST_CLOSE)
        if close_buttons:
            try:
                self.driver.execute_script("arguments[0].click();", close_buttons[0])
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located(L.SEARCH_LIST_MODAL)
                )
                return
            except Exception:
                pass

        search_buttons = self.driver.find_elements(*L.SEARCH_BUTTON)
        if search_buttons:
            self.driver.execute_script("arguments[0].click();", search_buttons[0])
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(L.SEARCH_LIST_MODAL)
            )

    def _search_list_items_count(self):
        return len(self.driver.find_elements(*L.FACILITY_LIST_ITEMS))

    def _close_facility_object_modal(self):
        close_buttons = self.driver.find_elements(*L.FACILITY_OBJECT_MODAL_CLOSE)
        assert close_buttons, "Не найдена кнопка закрытия карточки поставщика"
        self.driver.execute_script("arguments[0].click();", close_buttons[0])
        WebDriverWait(self.driver, 12).until(
            EC.invisibility_of_element_located(L.FACILITY_OBJECT_MODAL)
        )

    def _desktop_select_option(self, section_kind, option_text):
        indices = {
            "city": 1,
            "activity": 2,
            "tag": 3,
        }
        select_index = indices[section_kind]
        script = """
            const selectIndex = arguments[0];
            const optionText = arguments[1];
            const root = document;
            const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim();
            const isVisible = (el) => !!(el && (el.offsetWidth || el.offsetHeight || el.getClientRects().length));

            const visibleSelects = Array.from(
              root.querySelectorAll('.facilities-table-section .select')
            ).filter(isVisible);
            const selectRoot = visibleSelects[selectIndex];
            if (!selectRoot) return false;

            selectRoot.click();
            const options = Array.from(selectRoot.querySelectorAll('li, span, div')).filter((el) => {
              if (!isVisible(el)) return false;
              return normalize(el.textContent) === optionText;
            });
            const option = options[0];
            if (!option) return false;
            option.click();
            document.body.click();
            return true;
        """
        success = self.driver.execute_script(script, select_index, option_text)
        assert success, f"Не удалось выбрать '{option_text}' в desktop-контроле '{section_kind}'"
        time.sleep(0.8)
        self.wait_table_settled()

    def _desktop_reset_filters(self):
        for section_kind in ("city", "activity", "tag"):
            reset_target = "Вся Беларусь" if section_kind == "city" else "Сбросить все"
            try:
                self._desktop_select_option(section_kind, reset_target)
            except AssertionError:
                if section_kind == "city":
                    raise

    def _close_table_filter_modal_apply(self):
        apply_btn = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(L.TABLE_FILTER_APPLY)
        )
        self.driver.execute_script("arguments[0].click();", apply_btn)
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(L.TABLE_FILTER_MODAL_ROOT)
        )
        time.sleep(0.8)
        self.wait_table_settled()

    def _reset_filters_in_modal(self):
        reset_btn = WebDriverWait(self.driver, 12).until(
            EC.presence_of_element_located(L.TABLE_FILTER_RESET)
        )
        self.driver.execute_script("arguments[0].click();", reset_btn)
        time.sleep(0.25)

    def _option_xpath(self, section_title, option_text):
        return (
            "//div[contains(@class,'map-filter-modal')]"
            f"//p[normalize-space()='{section_title}']/following-sibling::ul[1]"
            f"//li[.//span[contains(normalize-space(),\"{option_text}\")]]"
        )

    def _show_all_xpath(self, section_title):
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

    def _select_filter_option(self, section_title, option_text, show_all=False):
        if show_all:
            show_all_items = self.driver.find_elements(By.XPATH, self._show_all_xpath(section_title))
            if show_all_items:
                self.driver.execute_script("arguments[0].click();", show_all_items[0])
                time.sleep(0.15)

        option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self._option_xpath(section_title, option_text)))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        self.driver.execute_script("arguments[0].click();", option)

        try:
            WebDriverWait(self.driver, 8).until(
                lambda _: self._is_option_checked(section_title, option_text)
            )
        except TimeoutException:
            time.sleep(0.35)

    def _set_table_search(self, query):
        search = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.TABLE_SEARCH_INPUT)
        )
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
            if (!state) return null;

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
            if (!state) return null;

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

            const bounds = state.bounds && typeof state.bounds === 'object'
              ? {
                  south: Number(state.bounds._sw?.lat ?? state.bounds.south ?? 0),
                  west: Number(state.bounds._sw?.lng ?? state.bounds.west ?? 0),
                  north: Number(state.bounds._ne?.lat ?? state.bounds.north ?? 0),
                  east: Number(state.bounds._ne?.lng ?? state.bounds.east ?? 0),
                }
              : null;

            return {
              city: toText(state.city),
              activities: toTextList(state.activities),
              tags: toTextList(state.tags),
              search: toText(state.search),
              searchActivities: toText(state.searchActivities),
              selectedLevel: toText(state.selectedLevel),
              bounds: bounds,
            };
            """
        )

    def _get_modal_option_states(self, section_title):
        script = """
            const sectionTitle = arguments[0];
            const modal = document.querySelector('.modal-container.map-filter-modal');
            if (!modal) return [];

            const section = Array.from(modal.querySelectorAll('p')).find(
              (node) => node.textContent.trim() === sectionTitle
            );
            if (!section) return [];

            const list = section.nextElementSibling;
            if (!list) return [];

            return Array.from(list.querySelectorAll('li')).map((item) => {
              const label = item.querySelector('span');
              const checkbox = item.querySelector('label.circle-checkbox');
              const classes = item.className || '';
              return {
                text: (label?.textContent || item.textContent || '').trim(),
                unavailable: classes.includes('unavailable'),
                showAll: classes.includes('show-all'),
                checked: (checkbox?.className || '').includes('circle-checkbox_checked'),
              };
            });
        """
        return self.driver.execute_script(script, section_title) or []

    def _assert_table_rows_are_from_state(self, state):
        row_names = self._table_row_names()
        assert row_names, "Названия отображаемых строк таблицы пусты"

        state_names = {
            self._normalize_text(item.get("name"))
            for item in state["objects"]
            if item.get("name")
        }
        assert state_names, "В state таблицы нет названий объектов"

        unknown_names = [
            name for name in row_names
            if self._normalize_text(name) not in state_names
        ]
        assert not unknown_names, f"В таблице есть строки вне текущего state: {unknown_names[:5]}"

    def _assert_selected_contains_expected(self, selected_values, expected_value, kind):
        expected_aliases = self._aliases_for_value(expected_value)
        selected_norm = {self._normalize_key(value) for value in selected_values if value}
        assert selected_norm, f"В state нет выбранных значений для фильтра {kind}"
        assert any(
            any(
                expected_alias in value or value in expected_alias
                for expected_alias in expected_aliases
            )
            for value in selected_norm
        ), f"Ожидали '{expected_value}' в выбранных {kind}, получили {selected_values}"

    def _aliases_for_value(self, value):
        normalized = self._normalize_key(value)
        aliases = {normalized}
        raw_key = self._normalize_text(value).replace("ё", "е")
        aliases.update(self.VALUE_ALIASES.get(raw_key, set()))
        return {self._normalize_key(alias) for alias in aliases if alias}

    def _assert_city_content_matches(self, state, expected_city):
        self._assert_selected_contains_expected(state["selectedCities"], expected_city, "город")
        expected_aliases = self._aliases_for_value(expected_city)
        assert state["objectsCount"] > 0, "После фильтра по городу не осталось объектов"

        for item in state["objects"]:
            city_norm = self._normalize_key(item.get("city"))
            assert city_norm, f"Объект без города в отфильтрованном state: {item}"
            assert any(
                alias in city_norm or city_norm in alias
                for alias in expected_aliases
            ), (
                f"Город объекта не соответствует фильтру: ожидали '{expected_city}', "
                f"получили '{item.get('city')}'"
            )

    def _assert_activity_content_matches(self, state, expected_activity):
        self._assert_selected_contains_expected(
            state["selectedActivities"],
            expected_activity,
            "активности",
        )
        selected = self._aliases_for_value(expected_activity)
        assert state["objectsCount"] > 0, "После фильтра по активности не осталось объектов"

        for item in state["objects"]:
            object_activities = {
                self._normalize_key(value)
                for value in item.get("activities", [])
                if value
            }
            assert any(
                any(alias in activity or activity in alias for alias in selected)
                for activity in object_activities
            ), (
                f"Объект не соответствует выбранной активности: "
                f"{item.get('name')} -> {item.get('activities')}"
            )

    def _assert_level_content_matches(self, state, expected_level):
        expected_aliases = self._aliases_for_value(expected_level)
        assert state["objectsCount"] > 0, "После фильтра по уровню не осталось объектов"

        for item in state["objects"]:
            object_levels = {
                self._normalize_key(value)
                for value in item.get("levels", [])
                if value
            }
            assert any(
                any(alias == level or alias in level or level in alias for alias in expected_aliases)
                for level in object_levels
            ), (
                f"Объект не соответствует уровню '{expected_level}': "
                f"{item.get('name')} -> {item.get('levels')}"
            )

    def _assert_tag_content_matches(self, state, expected_tag, baseline_state=None):
        self._assert_selected_contains_expected(state["selectedTags"], expected_tag, "дополнительно")
        expected_aliases = self._aliases_for_value(expected_tag)
        assert state["objectsCount"] > 0, "После фильтра 'Дополнительно' не осталось объектов"

        matched_objects = 0
        for item in state["objects"]:
            merged = {
                self._normalize_key(value)
                for value in (item.get("tags", []) + item.get("services", []))
                if value
            }
            if any(
                any(alias == value or alias in value or value in alias for alias in expected_aliases)
                for value in merged
            ):
                matched_objects += 1

        if matched_objects > 0:
            return

        # Для части опций "Дополнительно" сайт не отдает в state явный признак,
        # по которому можно верифицировать каждый объект по полям tags/services.
        if baseline_state:
            baseline_names = {
                self._normalize_text(item.get("name"))
                for item in baseline_state["objects"]
                if item.get("name")
            }
            filtered_names = {
                self._normalize_text(item.get("name"))
                for item in state["objects"]
                if item.get("name")
            }
            assert filtered_names, "После фильтра 'Дополнительно' нет имен объектов для проверки"
            assert filtered_names != baseline_names, (
                f"Фильтр '{expected_tag}' выбран, но состав объектов не изменился"
            )

    @allure.step("Проверить открытие страницы Объекты")
    def check_page_opened(self):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.PAGE_ROOT))
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.PAGE_TITLE))
        assert "/facilities" in self.driver.current_url, (
            f"Открыт неверный URL: {self.driver.current_url}"
        )

    @allure.step("Проверить отображение карты")
    def check_map_visible(self):
        self._safe_scroll(L.MAP_BLOCK)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(L.MAP_ROOT))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(L.MAP_CANVAS))

    @allure.step("Проверить элементы управления карты")
    def check_map_controls(self):
        self._safe_scroll(L.MAP_ROOT)
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.MAP_ZOOM_IN))
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.MAP_ZOOM_OUT))
        _ = self.driver.find_elements(*L.MAP_GEOLOCATE)

    @allure.step("Проверить фильтры объектов на основной странице")
    def check_filters_visible(self):
        self._safe_scroll(L.MAP_BLOCK)
        WebDriverWait(self.driver, 20).until(
            lambda d: d.find_elements(*L.FILTER_BAR)
            or d.find_elements(*L.FILTER_BUTTONS)
            or d.find_elements(*L.SEARCH_BUTTON)
            or d.find_elements(*L.FILTER_BUTTON)
        )

        buttons = self.driver.find_elements(*L.FILTER_BUTTONS)
        search_buttons = self.driver.find_elements(*L.SEARCH_BUTTON)
        filter_buttons = self.driver.find_elements(*L.FILTER_BUTTON)
        selects = self.driver.find_elements(*L.FILTER_SELECTS)

        assert buttons or search_buttons or filter_buttons or selects, (
            "Не найдены фильтры или кнопки поиска/фильтра на странице Объекты"
        )

    @allure.step("Проверить загрузку контента объектов на основной странице")
    def check_objects_content_loaded(self):
        self._safe_scroll(L.FILTER_BAR)
        values = self.driver.find_elements(*L.FACILITIES_LIST_ITEMS)
        buttons = self.driver.find_elements(*L.FILTER_BUTTONS)
        assert values or buttons, "Не найдены элементы фильтров/контента на странице объектов"

    @allure.step("Проверить блок ссылки на таблицу объектов")
    def check_objects_table_block(self):
        self._safe_scroll(L.OBJECTS_TABLE_SECTION)
        link = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(L.OBJECTS_TABLE_SECTION)
        )
        href = link.get_attribute("href") or ""
        assert L.TABLE_URL_SUFFIX in href, f"Ссылка на таблицу объектов некорректна: {href}"

    @allure.step("Проверить, что поиск на карте открывает список поставщиков")
    def check_search_list_modal(self):
        self._safe_scroll(L.MAP_BLOCK)
        self._open_search_list_modal()
        items_count = self._search_list_items_count()
        empty_state = self.driver.find_elements(*L.FACILITY_LIST_EMPTY)
        assert items_count > 0 or empty_state, "Поиск не открыл ни список поставщиков, ни empty state"
        self._close_search_list_modal()

    @allure.step("Проверить, что из списка поставщиков открывается карточка объекта")
    def check_search_item_opens_provider_modal(self):
        self._safe_scroll(L.MAP_BLOCK)
        self._open_search_list_modal()
        items = WebDriverWait(self.driver, 15).until(
            lambda d: d.find_elements(*L.FACILITY_LIST_ITEMS)
        )
        self.driver.execute_script("arguments[0].click();", items[0])
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.FACILITY_OBJECT_MODAL)
        )
        title = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.FACILITY_OBJECT_MODAL_TITLE)
        )
        modal_items = self.driver.find_elements(*L.FACILITY_OBJECT_MODAL_LIST_ITEMS)
        assert (title.text or "").strip(), "Карточка поставщика открылась без заголовка"
        assert modal_items, "В карточке поставщика не найден список активностей/услуг"
        self._close_facility_object_modal()

    @allure.step("Проверить, что фильтр по городу на карте меняет результаты и положение карты")
    def check_map_city_filter_reacts(self, city="Гомель"):
        self._safe_scroll(L.MAP_BLOCK)
        baseline_state = self.get_map_filter_state()
        assert baseline_state, "mapFilter state недоступен до фильтрации"

        self._open_search_list_modal()
        baseline_count = self._search_list_items_count()
        self._close_search_list_modal()
        assert baseline_count > 0, "Базовый список поставщиков пуст"

        self._open_main_filter_modal()
        self._select_filter_option("Город", city, show_all=True)
        self._close_main_filter_modal_apply()

        filtered_state = self.get_map_filter_state()
        assert filtered_state, "mapFilter state недоступен после выбора города"
        self._assert_selected_contains_expected([filtered_state["city"]], city, "город карты")

        self._open_search_list_modal()
        filtered_count = self._search_list_items_count()
        self._close_search_list_modal()
        assert 0 < filtered_count <= baseline_count, (
            f"Фильтр по городу на карте дал некорректный набор: "
            f"baseline={baseline_count}, filtered={filtered_count}"
        )

        baseline_bounds = baseline_state.get("bounds") or {}
        filtered_bounds = filtered_state.get("bounds") or {}
        bounds_changed = baseline_bounds != filtered_bounds
        count_changed = filtered_count != baseline_count
        assert bounds_changed or count_changed, (
            "После выбора города не изменились ни границы карты, ни число поставщиков"
        )

    @allure.step("Проверить, что при выборе города часть активностей становится недоступной")
    def check_map_city_disables_some_activities(self, city="Гомель"):
        self._safe_scroll(L.MAP_BLOCK)
        self._open_main_filter_modal()
        before_options = self._get_modal_option_states("Активности")
        before_unavailable = {
            self._normalize_text(item["text"])
            for item in before_options
            if item.get("text") and item.get("unavailable") and not item.get("showAll")
        }
        self._select_filter_option("Город", city, show_all=True)
        time.sleep(0.8)
        after_options = self._get_modal_option_states("Активности")
        after_unavailable = {
            self._normalize_text(item["text"])
            for item in after_options
            if item.get("text") and item.get("unavailable") and not item.get("showAll")
        }
        self._close_main_filter_modal_apply()

        assert after_unavailable, (
            f"После выбора города '{city}' не появилось ни одной недоступной активности"
        )
        assert after_unavailable != before_unavailable or len(after_unavailable) > len(before_unavailable), (
            "Набор недоступных активностей не изменился после смены города"
        )

    @allure.step("Проверить базовую структуру таблицы объектов")
    def check_table_basics(self):
        self.wait_table_loaded()
        assert self._visible_table_rows_count() > 0, "Таблица объектов пустая"
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.TABLE_SEARCH_INPUT))
        assert self._is_any_displayed(L.TABLE_FILTER_BUTTON) or len(self.driver.find_elements(*L.TABLE_FILTER_SELECTS)) >= 3, (
            "Не найдены элементы фильтрации таблицы"
        )

    @allure.step("Проверить поиск в таблице объектов: {1}")
    def check_table_search(self, query="Адреналин"):
        self.wait_table_loaded()
        baseline_state = self.get_table_filter_state()
        assert baseline_state, "tableFilter state недоступен до поиска"
        baseline_count = baseline_state["objectsCount"]
        assert baseline_count > 0, "Базовый набор таблицы пуст"

        self._set_table_search(query)
        search_state = self.get_table_filter_state()
        assert search_state, "tableFilter state недоступен после поиска"
        assert search_state["search"] == query, (
            f"Строка поиска не сохранилась в state: ожидали '{query}', "
            f"получили '{search_state['search']}'"
        )
        assert 0 < search_state["objectsCount"] <= baseline_count, (
            f"Поиск вернул некорректный диапазон результатов: "
            f"baseline={baseline_count}, filtered={search_state['objectsCount']}"
        )
        self._assert_table_rows_are_from_state(search_state)

    @allure.step("Проверить одиночный фильтр таблицы: {1} -> {2}")
    def check_table_filter_content_matches(self, section_title, option_text, content_kind):
        self.wait_table_loaded()
        baseline_state = self.get_table_filter_state()
        assert baseline_state, "tableFilter state недоступен до фильтрации"
        baseline_count = baseline_state["objectsCount"]
        assert baseline_count > 0, "Базовый набор таблицы пуст"

        if self.driver.find_elements(*L.TABLE_FILTER_BUTTON):
            self._open_table_filter_modal()
            self._select_filter_option(section_title, option_text, show_all=True)
            self._close_table_filter_modal_apply()
        else:
            desktop_kind = {"Город": "city", "Активности": "activity", "Дополнительно": "tag"}[section_title]
            self._desktop_select_option(desktop_kind, option_text)

        filtered_state = self.get_table_filter_state()
        assert filtered_state, "tableFilter state недоступен после фильтрации"
        assert 0 < filtered_state["objectsCount"] <= baseline_count, (
            f"Фильтр вернул некорректный набор: baseline={baseline_count}, "
            f"filtered={filtered_state['objectsCount']}"
        )
        self._assert_table_rows_are_from_state(filtered_state)

        if content_kind == "city":
            self._assert_city_content_matches(filtered_state, option_text)
        elif content_kind == "activity":
            self._assert_activity_content_matches(filtered_state, option_text)
        elif content_kind == "tag":
            self._assert_tag_content_matches(filtered_state, option_text, baseline_state=baseline_state)
        elif content_kind == "level":
            self._assert_level_content_matches(filtered_state, option_text)
        else:
            raise AssertionError(f"Неподдерживаемый тип проверки контента: {content_kind}")

    @allure.step("Проверить, что строка таблицы открывает карточку поставщика")
    def check_table_row_opens_provider_modal(self):
        self.wait_table_loaded()
        buttons = WebDriverWait(self.driver, 15).until(
            lambda d: d.find_elements(*L.FACILITIES_TABLE_OBJECT_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", buttons[0])
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.FACILITY_OBJECT_MODAL)
        )
        title = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.FACILITY_OBJECT_MODAL_TITLE)
        )
        modal_items = self.driver.find_elements(*L.FACILITY_OBJECT_MODAL_LIST_ITEMS)
        assert (title.text or "").strip(), "Карточка объекта из таблицы открылась без заголовка"
        assert modal_items, "В карточке объекта из таблицы нет активностей/услуг"
        self._close_facility_object_modal()

    @allure.step("Проверить комбинацию фильтров таблицы ({1})")
    def check_table_filter_combination(self, filters):
        self.wait_table_loaded()
        baseline_state = self.get_table_filter_state()
        assert baseline_state, "tableFilter state недоступен до комбинированной фильтрации"
        baseline_count = baseline_state["objectsCount"]
        assert baseline_count > 0, "Базовый набор таблицы пуст"

        if self.driver.find_elements(*L.TABLE_FILTER_BUTTON):
            self._open_table_filter_modal()
            for flt in filters:
                self._select_filter_option(
                    flt["section"],
                    flt["option"],
                    show_all=flt.get("show_all", False),
                )
            self._close_table_filter_modal_apply()
        else:
            kind_map = {"Город": "city", "Активности": "activity", "Дополнительно": "tag"}
            for flt in filters:
                self._desktop_select_option(kind_map[flt["section"]], flt["option"])

        filtered_state = self.get_table_filter_state()
        assert filtered_state, "tableFilter state недоступен после комбинации фильтров"
        assert 0 < filtered_state["objectsCount"] <= baseline_count, (
            f"Комбинация фильтров вернула некорректный набор: "
            f"baseline={baseline_count}, filtered={filtered_state['objectsCount']}"
        )
        self._assert_table_rows_are_from_state(filtered_state)

    @allure.step("Сбросить фильтры и вернуть baseline набор")
    def check_table_reset_returns_baseline(self, filters, max_attempts=2):
        self.wait_table_loaded()
        baseline_state = self.get_table_filter_state()
        assert baseline_state, "tableFilter state недоступен в baseline"
        baseline_count = baseline_state["objectsCount"]
        assert baseline_count > 0, "Базовый набор таблицы пуст"

        if self.driver.find_elements(*L.TABLE_FILTER_BUTTON):
            self._open_table_filter_modal()
            for flt in filters:
                self._select_filter_option(
                    flt["section"],
                    flt["option"],
                    show_all=flt.get("show_all", False),
                )
            self._close_table_filter_modal_apply()
        else:
            kind_map = {"Город": "city", "Активности": "activity", "Дополнительно": "tag"}
            for flt in filters:
                self._desktop_select_option(kind_map[flt["section"]], flt["option"])

        filtered_state = self.get_table_filter_state()
        assert filtered_state, "tableFilter state недоступен после фильтрации"
        assert 0 < filtered_state["objectsCount"] <= baseline_count, (
            f"Фильтрация перед reset дала некорректный набор: "
            f"baseline={baseline_count}, filtered={filtered_state['objectsCount']}"
        )

        restored_state = filtered_state
        for _ in range(max_attempts):
            if self.driver.find_elements(*L.TABLE_FILTER_BUTTON):
                self._open_table_filter_modal()
                self._reset_filters_in_modal()
                self._close_table_filter_modal_apply()
            else:
                self._desktop_reset_filters()
            restored_state = self.get_table_filter_state()
            assert restored_state, "tableFilter state недоступен после reset"

            no_active_filters = (
                len(restored_state["selectedCities"]) == 0
                and len(restored_state["selectedActivities"]) == 0
                and len(restored_state["selectedTags"]) == 0
                and len(restored_state["selectedLevels"]) == 0
            )
            if no_active_filters and restored_state["objectsCount"] == baseline_count:
                break

        assert restored_state["objectsCount"] == baseline_count, (
            f"После reset baseline не восстановлен: baseline={baseline_count}, "
            f"current={restored_state['objectsCount']}"
        )

    @allure.step("Проверить полный сценарий поиска, фильтров и reset на таблице объектов")
    def check_table_search_filters_reset_flow(
        self,
        search_query="Адреналин",
        city="Гомель",
        activity="Аквааэробика",
        empty_query="zzzzzzzzzz_not_found",
    ):
        self.wait_table_loaded()

        baseline_state = self.get_table_filter_state()
        assert baseline_state, "tableFilter state недоступен в baseline"
        baseline_count = baseline_state["objectsCount"]
        assert baseline_count > 0, "Базовый набор таблицы пуст"

        self._set_table_search(search_query)
        search_state = self.get_table_filter_state()
        assert search_state, "tableFilter state недоступен после поиска"
        assert search_state["search"] == search_query, "Запрос поиска не сохранился в state"
        assert 0 < search_state["objectsCount"] <= baseline_count, (
            "Поиск дал пустой или расширенный набор результатов"
        )

        if self.driver.find_elements(*L.TABLE_FILTER_BUTTON):
            self._open_table_filter_modal()
            self._select_filter_option("Город", city, show_all=True)
            self._select_filter_option("Активности", activity, show_all=True)
            self._close_table_filter_modal_apply()
        else:
            self._desktop_select_option("city", city)
            self._desktop_select_option("activity", activity)

        combined_state = self.get_table_filter_state()
        assert combined_state, "tableFilter state недоступен после связки search+filters"
        current_search = combined_state["search"]
        assert current_search in ("", search_query), (
            f"После применения фильтров search перешел в неожиданное состояние: '{current_search}'"
        )
        if combined_state["objectsCount"] == 0:
            assert self.driver.find_elements(*L.FACILITIES_TABLE_NO_RESULT), (
                "Комбинация search+filters вернула пустой набор без отображения empty state"
            )
        else:
            self._assert_table_rows_are_from_state(combined_state)
            self._assert_city_content_matches(combined_state, city)
            self._assert_activity_content_matches(combined_state, activity)

        reset_state = None
        for _ in range(3):
            if self.driver.find_elements(*L.TABLE_FILTER_BUTTON):
                self._open_table_filter_modal()
                self._reset_filters_in_modal()
                self._close_table_filter_modal_apply()
            else:
                self._desktop_reset_filters()
            self._set_table_search("")
            reset_state = self.get_table_filter_state()
            assert reset_state, "tableFilter state недоступен после reset"

            no_active_filters = (
                len(reset_state["selectedCities"]) == 0
                and len(reset_state["selectedActivities"]) == 0
                and len(reset_state["selectedTags"]) == 0
                and len(reset_state["selectedLevels"]) == 0
            )
            if reset_state["search"] == "" and no_active_filters and reset_state["objectsCount"] == baseline_count:
                break

        assert reset_state["search"] == "", "Поле поиска не очистилось после reset"
        assert reset_state["objectsCount"] == baseline_count, (
            f"После полного reset baseline не восстановлен: "
            f"baseline={baseline_count}, current={reset_state['objectsCount']}"
        )

        self._set_table_search(empty_query)
        empty_state = self.get_table_filter_state()
        assert empty_state, "tableFilter state недоступен для empty state"
        assert empty_state["search"] == empty_query, "Запрос для empty state не сохранился"
        assert empty_state["objectsCount"] == 0, (
            f"Empty state не наступил для запроса '{empty_query}': "
            f"current={empty_state['objectsCount']}"
        )
        assert self.driver.find_elements(*L.FACILITIES_TABLE_NO_RESULT), (
            "После запроса без совпадений не показан empty state в UI"
        )

    @allure.step("Проверить полный сценарий фильтрации на странице 'Список объектов (таблица)'")
    def check_full_table_filters_flow(self):
        self.check_objects_table_block()
        self._safe_scroll(L.OBJECTS_TABLE_SECTION)
        table_link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(L.OBJECTS_TABLE_SECTION)
        )
        self.driver.execute_script("arguments[0].click();", table_link)
        WebDriverWait(self.driver, 20).until(EC.url_contains(L.TABLE_URL_SUFFIX))
        self.check_table_basics()
        self.check_table_search_filters_reset_flow()

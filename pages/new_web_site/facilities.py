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
        filter_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(L.TABLE_FILTER_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", filter_btn)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.TABLE_FILTER_MODAL_ROOT)
        )

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

    @allure.step("Проверить базовую структуру таблицы объектов")
    def check_table_basics(self):
        self.wait_table_loaded()
        assert self._visible_table_rows_count() > 0, "Таблица объектов пустая"
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.TABLE_SEARCH_INPUT))
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.TABLE_FILTER_BUTTON))

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

        self._open_table_filter_modal()
        self._select_filter_option(section_title, option_text, show_all=True)
        self._close_table_filter_modal_apply()

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
        elif content_kind == "level":
            self._assert_level_content_matches(filtered_state, option_text)
        else:
            raise AssertionError(f"Неподдерживаемый тип проверки контента: {content_kind}")

    @allure.step("Проверить комбинацию фильтров таблицы ({1})")
    def check_table_filter_combination(self, filters):
        self.wait_table_loaded()
        baseline_state = self.get_table_filter_state()
        assert baseline_state, "tableFilter state недоступен до комбинированной фильтрации"
        baseline_count = baseline_state["objectsCount"]
        assert baseline_count > 0, "Базовый набор таблицы пуст"

        self._open_table_filter_modal()
        for flt in filters:
            self._select_filter_option(
                flt["section"],
                flt["option"],
                show_all=flt.get("show_all", False),
            )
        self._close_table_filter_modal_apply()

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

        self._open_table_filter_modal()
        for flt in filters:
            self._select_filter_option(
                flt["section"],
                flt["option"],
                show_all=flt.get("show_all", False),
            )
        self._close_table_filter_modal_apply()

        filtered_state = self.get_table_filter_state()
        assert filtered_state, "tableFilter state недоступен после фильтрации"
        assert 0 < filtered_state["objectsCount"] <= baseline_count, (
            f"Фильтрация перед reset дала некорректный набор: "
            f"baseline={baseline_count}, filtered={filtered_state['objectsCount']}"
        )

        restored_state = filtered_state
        for _ in range(max_attempts):
            self._open_table_filter_modal()
            self._reset_filters_in_modal()
            self._close_table_filter_modal_apply()
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

        self._open_table_filter_modal()
        self._select_filter_option("Город", city, show_all=True)
        self._select_filter_option("Активности", activity, show_all=True)
        self._close_table_filter_modal_apply()

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
            self._open_table_filter_modal()
            self._reset_filters_in_modal()
            self._close_table_filter_modal_apply()
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

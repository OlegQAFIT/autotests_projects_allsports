# -*- coding: utf-8 -*-
import allure
import pytest
from pages.new_web_site.facilities import FacilitiesPage


@allure.feature('Facilities Page')
@allure.severity('Blocker')
@allure.story('Открытие страницы Объекты')
def test_open_facilities_page(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('Проверка карты на странице Объекты')
def test_facilities_map_visible(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_visible()


@allure.feature('Facilities Page')
@allure.severity('Normal')
@allure.story('Проверка элементов управления карты')
def test_facilities_map_controls(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_controls()


@allure.feature('Facilities Page')
@allure.severity('Normal')
@allure.story('Проверка фильтров объектов')
def test_facilities_filters_visible(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_filters_visible()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('Проверка загрузки объектов')
def test_facilities_objects_content_loaded(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_objects_content_loaded()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('Поиск на карте открывает список поставщиков')
def test_facilities_search_list_modal(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_search_list_modal()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('Из списка поставщиков открывается карточка объекта')
def test_facilities_search_item_opens_provider_card(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_search_item_opens_provider_modal()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('Выбор города на карте меняет выдачу и положение карты')
@pytest.mark.release_gate
def test_facilities_map_city_filter_reacts(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_city_filter_reacts("Гомель")


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('После выбора города часть активностей становится недоступной')
@pytest.mark.release_gate
def test_facilities_map_city_disables_some_activities(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_city_disables_some_activities("Гомель")


@allure.feature('Facilities Page')
@allure.severity('Normal')
@allure.story('Проверка блока таблицы объектов')
def test_facilities_objects_table_block(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_objects_table_block()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('Полный базовый сценарий страницы Объекты')
@pytest.mark.release_gate
def test_facilities_full_flow(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()
    page.check_map_visible()
    page.check_map_controls()
    page.check_filters_visible()
    page.check_objects_content_loaded()
    page.check_objects_table_block()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story('Полная проверка фильтров и поиска в таблице объектов')
@pytest.mark.release_gate
def test_facilities_table_filters_full_flow(driver):
    page = FacilitiesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()
    page.check_full_table_filters_flow()


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — базовая структура и поиск")
@pytest.mark.release_gate
def test_facilities_table_basics_and_search(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_basics()
    page.check_table_search("Адреналин")


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — отдельный фильтр: Город = Гомель")
@pytest.mark.release_gate
def test_facilities_table_single_filter_city_gomel(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_content_matches("Город", "Гомель", content_kind="city")


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — отдельный фильтр: Активность = Аквааэробика")
@pytest.mark.release_gate
def test_facilities_table_single_filter_activity_aqua(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_content_matches("Активности", "Аквааэробика", content_kind="activity")


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — отдельный фильтр: Активность = Аргентинское танго")
@pytest.mark.release_gate
def test_facilities_table_single_filter_activity_tango(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_content_matches("Активности", "Аргентинское танго", content_kind="activity")


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — отдельный фильтр: Дополнительно = Объекты с Plus услугами")
@pytest.mark.release_gate
def test_facilities_table_single_filter_additional_plus_services(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_content_matches(
        "Дополнительно",
        "Объекты с Plus услугами",
        content_kind="tag",
    )


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — комбинация 2 фильтров (Город + Активность)")
@pytest.mark.release_gate
def test_facilities_table_filters_combination_two(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_combination(
        [
            {"section": "Город", "option": "Гомель", "show_all": True},
            {"section": "Активности", "option": "Аквааэробика", "show_all": True},
        ]
    )


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — комбинация 3 фильтров (Город + 2 активности)")
@pytest.mark.release_gate
def test_facilities_table_filters_combination_three(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_combination(
        [
            {"section": "Город", "option": "Гомель", "show_all": True},
            {"section": "Активности", "option": "Аквааэробика", "show_all": True},
            {"section": "Активности", "option": "Аргентинское танго", "show_all": True},
        ]
    )


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — reset фильтров возвращает baseline набор")
@pytest.mark.release_gate
def test_facilities_table_reset_returns_baseline(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_reset_returns_baseline(
        [
            {"section": "Город", "option": "Гомель", "show_all": True},
            {"section": "Активности", "option": "Аквааэробика", "show_all": True},
        ],
        max_attempts=2,
    )


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — связка search + filters + reset + empty state")
@pytest.mark.release_gate
def test_facilities_table_search_filters_reset_empty_state(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_search_filters_reset_flow(
        search_query="Адреналин",
        city="Гомель",
        activity="Аквааэробика",
        empty_query="zzzzzzzzzz_not_found",
    )


@allure.feature('Facilities Page')
@allure.severity('Critical')
@allure.story("Таблица объектов — строка поставщика открывает карточку с активностями")
@pytest.mark.release_gate
def test_facilities_table_row_opens_provider_modal(driver):
    page = FacilitiesPage(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_row_opens_provider_modal()

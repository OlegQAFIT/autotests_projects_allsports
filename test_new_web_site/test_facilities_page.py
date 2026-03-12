# -*- coding: utf-8 -*-
import allure
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

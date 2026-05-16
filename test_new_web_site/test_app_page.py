# -*- coding: utf-8 -*-
import allure
import pytest
import requests

from pages.new_web_site.app_page import AppPage


pytestmark = [pytest.mark.release_gate]


@allure.feature("App Page")
@allure.severity("Blocker")
@allure.story("Открытие и базовая структура страницы /app")
def test_app_page_open_and_structure(driver):
    page = AppPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()


@allure.feature("App Page")
@allure.severity("Critical")
@allure.story("Ссылки на магазины приложений присутствуют и корректны")
def test_app_page_store_links(driver):
    page = AppPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_store_links()


@allure.feature("App Page")
@allure.severity("Normal")
@allure.story("Проверка canonical и meta тегов")
def test_app_page_canonical_and_meta(driver):
    page = AppPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_meta()
    page.check_canonical()


@allure.feature("App Page")
@allure.severity("Normal")
@allure.story("Проверка отсутствия критичных ошибок в консоли")
def test_app_page_console_errors(driver):
    page = AppPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_no_severe_console_errors()


@allure.feature("App Page")
@allure.severity("Critical")
@allure.story("Проверка HTTP статуса страницы /app")
def test_app_page_http_status_200():
    response = requests.get("https://www.allsports.by/ru-by/app", timeout=20, allow_redirects=True)
    assert response.status_code == 200, f"/ru-by/app returned {response.status_code}"

# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.app_page_sb import AppPageSb


pytestmark = [pytest.mark.release_gate]


@allure.feature("App SB")
@allure.severity("Blocker")
def test_app_page_open_and_structure_sb(driver):
    """Проверка открытия страницы приложения и наличия базовой структуры контента."""
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()


@allure.feature("App SB")
@allure.severity("Critical")
def test_app_page_store_links_sb(driver):
    """Проверка ссылок на App Store, Google Play, Huawei и APK на странице приложения."""
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_store_links()


@allure.feature("App SB")
@allure.severity("Normal")
def test_app_page_canonical_and_meta_sb(driver):
    """Проверка canonical и meta-атрибутов страницы приложения."""
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_meta()
    page.check_canonical()


@allure.feature("App SB")
@allure.severity("Normal")
def test_app_page_console_errors_sb(driver):
    """Проверка отсутствия критических ошибок в консоли на странице приложения."""
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_no_severe_console_errors()


@allure.feature("App SB")
@allure.severity("Critical")
def test_app_page_http_status_sb(driver):
    """Проверка, что страница /app отвечает со статусом HTTP 200."""
    page = AppPageSb(driver)
    page.check_http_status()

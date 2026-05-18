# -*- coding: utf-8 -*-
import allure
import pytest
import requests

from pages.new_web_site_sb.app_page_sb import AppPageSb


pytestmark = [pytest.mark.release_gate]


@allure.feature("App SB")
@allure.severity("Blocker")
def test_app_page_open_and_structure_sb(driver):
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()


@allure.feature("App SB")
@allure.severity("Critical")
def test_app_page_store_links_sb(driver):
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_store_links()


@allure.feature("App SB")
@allure.severity("Normal")
def test_app_page_canonical_and_meta_sb(driver):
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_meta()
    page.check_canonical()


@allure.feature("App SB")
@allure.severity("Normal")
def test_app_page_console_errors_sb(driver):
    page = AppPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_no_severe_console_errors()


@allure.feature("App SB")
@allure.severity("Critical")
def test_app_page_http_status_sb():
    response = requests.get("https://www.sportbenefit.eu/en-cy/app", timeout=20, allow_redirects=True)
    assert response.status_code == 200, f"/en-cy/app returned {response.status_code}"

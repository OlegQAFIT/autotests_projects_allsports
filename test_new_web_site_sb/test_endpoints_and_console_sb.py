# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.site_health_sb import SiteHealthSb


pytestmark = [pytest.mark.release_gate]


@allure.feature("Endpoints SB")
@allure.severity("Critical")
@pytest.mark.parametrize("url", SiteHealthSb.PUBLIC_ENDPOINTS)
def test_public_endpoints_status_200_sb(driver, url):
    page = SiteHealthSb(driver)
    page.check_public_endpoint_status_200(url)


@allure.feature("Endpoints SB")
@allure.severity("Critical")
@pytest.mark.parametrize("url", SiteHealthSb.API_ENDPOINTS)
def test_contact_api_options_sb(driver, url):
    page = SiteHealthSb(driver)
    page.check_options_endpoint_status_200(url)


@allure.feature("Endpoints SB")
@allure.severity("Normal")
@pytest.mark.parametrize("url", SiteHealthSb.API_ENDPOINTS)
def test_contact_api_get_method_guard_sb(driver, url):
    page = SiteHealthSb(driver)
    page.check_get_method_guard(url)


@allure.feature("Console SB")
@allure.severity("Normal")
@pytest.mark.parametrize("url", SiteHealthSb.UI_PAGES_FOR_CONSOLE)
def test_pages_have_no_severe_console_errors_sb(driver, url):
    page = SiteHealthSb(driver)
    page.check_page_has_no_severe_console_errors(url)

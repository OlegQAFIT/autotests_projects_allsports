# -*- coding: utf-8 -*-
import allure
import pytest
from pages.new_web_site.site_health import SiteHealthPage


pytestmark = [pytest.mark.release_gate]


PUBLIC_ENDPOINTS = [
    "https://www.allsports.fit/by/",
    "https://www.allsports.by/ru-by/",
    "https://www.allsports.by/ru-by/facilities",
    "https://www.allsports.by/ru-by/facilities-table",
    "https://www.allsports.by/ru-by/levels",
    "https://www.allsports.by/ru-by/companies",
    "https://www.allsports.by/ru-by/partners",
    "https://www.allsports.by/ru-by/contacts",
    "https://www.allsports.by/ru-by/license",
    "https://www.allsports.by/ru-by/user-agreements",
    "https://www.allsports.by/ru-by/providing-payment-service-rules",
    "https://www.allsports.by/ru-by/policy/251010_processing_personal_data",
    "https://www.allsports.by/ru-by/license/241009_license",
    "https://www.allsports.by/ru-by/individual_license/241009_license",
    "https://www.allsports.by/ru-by/rule/250731_rule",
    "https://www.allsports.by/ru-by/cookie/cookie-policy",
]

API_ENDPOINTS = [
    "https://www.allsports.by/api/www/2.0.0/contact/get_offer",
    "https://www.allsports.by/api/www/2.0.0/contact/become_partner",
]

UI_PAGES_FOR_CONSOLE = [
    "https://www.allsports.by/ru-by/",
    "https://www.allsports.by/ru-by/facilities",
    "https://www.allsports.by/ru-by/facilities-table",
    "https://www.allsports.by/ru-by/levels",
    "https://www.allsports.by/ru-by/companies",
    "https://www.allsports.by/ru-by/partners",
    "https://www.allsports.by/ru-by/contacts",
]

@allure.feature("Endpoints")
@allure.severity("Critical")
@pytest.mark.parametrize("url", PUBLIC_ENDPOINTS)
def test_public_endpoints_status_200(url):
    page = SiteHealthPage(None)
    page.check_public_endpoint_status_200(url)


@allure.feature("Endpoints")
@allure.severity("Critical")
@pytest.mark.parametrize("url", API_ENDPOINTS)
def test_contact_api_options(url):
    page = SiteHealthPage(None)
    page.check_options_endpoint_status_200(url)


@allure.feature("Endpoints")
@allure.severity("Normal")
@pytest.mark.parametrize("url", API_ENDPOINTS)
def test_contact_api_get_method_guard(url):
    page = SiteHealthPage(None)
    page.check_get_method_guard(url)


@allure.feature("Console")
@allure.severity("Normal")
@pytest.mark.parametrize("url", UI_PAGES_FOR_CONSOLE)
def test_pages_have_no_severe_console_errors(driver, url):
    page = SiteHealthPage(driver)
    page.check_page_has_no_severe_console_errors(url)

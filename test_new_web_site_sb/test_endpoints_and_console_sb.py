# -*- coding: utf-8 -*-
import allure
import pytest
import requests

from pages.new_web_site_sb.base_page_sb import BasePageSb


pytestmark = [pytest.mark.release_gate]


PUBLIC_ENDPOINTS_SB = [
    "https://www.sportbenefit.eu/en-cy",
    "https://www.sportbenefit.eu/en-cy/facilities",
    "https://www.sportbenefit.eu/en-cy/facilities-table",
    "https://www.sportbenefit.eu/en-cy/levels",
    "https://www.sportbenefit.eu/en-cy/companies",
    "https://www.sportbenefit.eu/en-cy/partners",
    "https://www.sportbenefit.eu/en-cy/contacts",
    "https://www.sportbenefit.eu/en-cy/app",
    "https://www.sportbenefit.eu/en-cy/license",
    "https://www.sportbenefit.eu/en-cy/user-agreements",
    "https://www.sportbenefit.eu/en-cy/policy/260407_processing_personal_data",
    "https://www.sportbenefit.eu/en-cy/rule/250811_rule",
    "https://www.sportbenefit.eu/en-cy/cookie/cookie-policy",
    "https://www.sportbenefit.eu/en-cy/license/260407_license",
    "https://www.sportbenefit.eu/en-cy/individual_license/260407_license",
    "https://sportbenefit.eu/media/sportbenefiteu-release.apk",
]

API_ENDPOINTS_SB = [
    "https://www.sportbenefit.eu/api/www/2.0.0/contact/get_offer",
    "https://www.sportbenefit.eu/api/www/2.0.0/contact/become_partner",
    "https://www.sportbenefit.eu/api/www/2.0.0/contact/ask_question",
]

UI_PAGES_FOR_CONSOLE_SB = [
    "https://www.sportbenefit.eu/en-cy",
    "https://www.sportbenefit.eu/en-cy/facilities",
    "https://www.sportbenefit.eu/en-cy/facilities-table",
    "https://www.sportbenefit.eu/en-cy/levels",
    "https://www.sportbenefit.eu/en-cy/companies",
    "https://www.sportbenefit.eu/en-cy/partners",
    "https://www.sportbenefit.eu/en-cy/contacts",
    "https://www.sportbenefit.eu/en-cy/app",
]


@allure.feature("Endpoints SB")
@allure.severity("Critical")
@pytest.mark.parametrize("url", PUBLIC_ENDPOINTS_SB)
def test_public_endpoints_status_200_sb(url):
    response = requests.get(url, timeout=25, allow_redirects=True)
    assert response.status_code == 200, f"{url} returned {response.status_code}"


@allure.feature("Endpoints SB")
@allure.severity("Critical")
@pytest.mark.parametrize("url", API_ENDPOINTS_SB)
def test_contact_api_options_sb(url):
    response = requests.options(url, timeout=20)
    assert response.status_code == 200, f"OPTIONS {url} returned {response.status_code}"


@allure.feature("Endpoints SB")
@allure.severity("Normal")
@pytest.mark.parametrize("url", API_ENDPOINTS_SB)
def test_contact_api_get_method_guard_sb(url):
    response = requests.get(url, timeout=20)
    assert response.status_code == 405, f"GET {url} should return 405, got {response.status_code}"


@allure.feature("Console SB")
@allure.severity("Normal")
@pytest.mark.parametrize("url", UI_PAGES_FOR_CONSOLE_SB)
def test_pages_have_no_severe_console_errors_sb(driver, url):
    page = BasePageSb(driver)
    page.open_url(url)
    page.accept_cookie_consent()

    logs = driver.get_log("browser")
    filtered = page.filtered_console_errors(logs)
    assert not filtered, f"Console SEVERE errors on {url}: {filtered}"

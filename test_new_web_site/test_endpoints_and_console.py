# -*- coding: utf-8 -*-
import allure
import pytest
import requests

from selenium.webdriver.common.by import By


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


def _filtered_console_errors(raw_logs):
    severe = [entry for entry in raw_logs if entry.get("level") == "SEVERE"]
    filtered = []
    for entry in severe:
        msg = (entry.get("message") or "").lower()
        source = (entry.get("source") or "").lower()
        if "sentry" in msg:
            continue
        if "content security policy" in msg or "csp" in msg:
            continue
        if source in ("security", "network"):
            continue
        filtered.append(entry)
    return filtered


@allure.feature("Endpoints")
@allure.severity("Critical")
@pytest.mark.parametrize("url", PUBLIC_ENDPOINTS)
def test_public_endpoints_status_200(url):
    response = requests.get(url, timeout=20, allow_redirects=True)
    assert response.status_code == 200, f"{url} returned {response.status_code}"


@allure.feature("Endpoints")
@allure.severity("Critical")
@pytest.mark.parametrize("url", API_ENDPOINTS)
def test_contact_api_options(url):
    response = requests.options(url, timeout=20)
    assert response.status_code == 200, f"OPTIONS {url} returned {response.status_code}"


@allure.feature("Endpoints")
@allure.severity("Normal")
@pytest.mark.parametrize("url", API_ENDPOINTS)
def test_contact_api_get_method_guard(url):
    response = requests.get(url, timeout=20)
    assert response.status_code == 405, f"GET {url} should be method-guarded (405), got {response.status_code}"


@allure.feature("Console")
@allure.severity("Normal")
@pytest.mark.parametrize("url", UI_PAGES_FOR_CONSOLE)
def test_pages_have_no_severe_console_errors(driver, url):
    driver.get(url)
    try:
        cookie = driver.find_element(By.CSS_SELECTOR, ".cookie-primary-modal__confirm")
        cookie.click()
    except Exception:
        pass

    logs = driver.get_log("browser")
    filtered = _filtered_console_errors(logs)
    assert not filtered, f"Console SEVERE errors on {url}: {filtered}"

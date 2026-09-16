"""Smoke-проверка доступности и базовой работоспособности ключевых сервисов."""

import json
import os
import time
from urllib.parse import urlparse

import allure
import pytest
import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


LOGIN_PAGE_SELECTOR = (
    "form input:not([type='hidden']):not([type='checkbox']), "
    "form button[type='submit']"
)
PUBLIC_PAGE_SELECTOR = "header, main, [role='main']"
APPLICATION_PAGE_SELECTOR = (
    "main, [role='main'], form, input, button, #root > *, #app > *"
)

PAGES_TO_CHECK = (
    ("Journal BY", "https://journal.allsports.by/login", LOGIN_PAGE_SELECTOR),
    ("Journal EU", "https://journal.sportbenefit.eu/", LOGIN_PAGE_SELECTOR),
    ("SportBenefit EU website", "https://www.sportbenefit.eu/en-cy", PUBLIC_PAGE_SELECTOR),
    ("Allsports BY website", "https://www.allsports.by/ru-by/", PUBLIC_PAGE_SELECTOR),
    ("HR portal", "https://hr.sportbenefit.eu/login", LOGIN_PAGE_SELECTOR),
    ("Allsports portal", "https://portal.allsports.by/login", LOGIN_PAGE_SELECTOR),
    (
        "SportBenefit member page",
        "https://member.sportbenefit.eu/c2b1a2f3-3c36-48f0-9d03-4d8e4e9859c9",
        APPLICATION_PAGE_SELECTOR,
    ),
    (
        "Allsports member page",
        "https://member.allsports.by/26792355-85af-43fb-932d-6419d7b10f12",
        APPLICATION_PAGE_SELECTOR,
    ),
    ("Allsports partner portal", "https://partner.allsports.fit/login", LOGIN_PAGE_SELECTOR),
    ("SportBenefit partner portal", "https://partner.sportbenefit.eu/login", LOGIN_PAGE_SELECTOR),
)

REQUEST_TIMEOUT_SECONDS = 30
PAGE_LOAD_TIMEOUT_SECONDS = 30
CONTINUE_BUTTON_XPATH = (
    "//button[not(@disabled) and ("
    "normalize-space()='Продолжить' or normalize-space()='Continue' or "
    ".//*[normalize-space()='Продолжить'] or .//*[normalize-space()='Continue']"
    ")]"
)
ERROR_PAGE_MARKERS = (
    "404 not found",
    "page not found",
    "internal server error",
    "bad gateway",
    "gateway timeout",
    "service unavailable",
    "temporarily unavailable",
)

SUPPLIER_PANELS_TO_CHECK = (
    (
        "Allsports supplier panel",
        "https://partner.allsports.fit/login",
        "ALLSPORTS_PARTNER_SMOKE_LOGIN",
        "ALLSPORTS_PARTNER_SMOKE_PASSWORD",
    ),
    (
        "SportBenefit supplier panel",
        "https://partner.sportbenefit.eu/login",
        "SPORTBENEFIT_PARTNER_SMOKE_LOGIN",
        "SPORTBENEFIT_PARTNER_SMOKE_PASSWORD",
    ),
)


def _assert_http_response_is_healthy(url: str) -> None:
    """Проверяет TLS/соединение, HTTP-ответ и наличие HTML-контента."""
    response = requests.get(
        url,
        allow_redirects=True,
        timeout=REQUEST_TIMEOUT_SECONDS,
        headers={"User-Agent": "Allsports-Availability-Monitor/1.0"},
    )

    assert response.status_code < 400, (
        f"HTTP check failed: {url} returned {response.status_code}; "
        f"final URL: {response.url}"
    )
    assert response.content, f"HTTP check failed: {url} returned an empty response"
    content_type = response.headers.get("content-type", "").lower()
    assert "html" in content_type, (
        f"HTTP check failed: {url} returned unexpected content-type "
        f"{content_type!r}; final URL: {response.url}"
    )


def _clear_performance_log(driver) -> None:
    """Очищает события предыдущей страницы перед проверкой следующей."""
    try:
        driver.get_log("performance")
    except WebDriverException:
        pass


def _get_critical_network_errors(driver) -> list[str]:
    """Возвращает ошибки главного документа и серверные сбои XHR/fetch."""
    try:
        raw_entries = driver.get_log("performance")
    except WebDriverException:
        return []

    errors = []
    for entry in raw_entries:
        message = json.loads(entry["message"])["message"]
        method = message.get("method")
        params = message.get("params", {})
        resource_type = params.get("type")

        if method == "Network.responseReceived":
            response = params.get("response", {})
            status = response.get("status", 0)
            is_failed_document = resource_type == "Document" and status >= 400
            is_failed_api = resource_type in {"XHR", "Fetch"} and status >= 500
            if is_failed_document or is_failed_api:
                errors.append(
                    f"{resource_type} returned HTTP {status}: {response.get('url')}"
                )

        if method == "Network.loadingFailed" and not params.get("canceled"):
            if resource_type in {"Document", "XHR", "Fetch"}:
                errors.append(
                    f"{resource_type} failed to load: {params.get('errorText', 'unknown error')}"
                )

    return errors


def _get_authenticated_panel_network_errors(driver) -> list[str]:
    """Returns failed document/API requests made after supplier-panel login."""
    try:
        raw_entries = driver.get_log("performance")
    except WebDriverException:
        return []

    errors = []
    for entry in raw_entries:
        message = json.loads(entry["message"])["message"]
        method = message.get("method")
        params = message.get("params", {})
        resource_type = params.get("type")

        if method == "Network.responseReceived" and resource_type in {"Document", "XHR", "Fetch"}:
            response = params.get("response", {})
            status = response.get("status", 0)
            if status >= 400:
                errors.append(
                    f"{resource_type} returned HTTP {status}: {response.get('url')}"
                )

        if method == "Network.loadingFailed" and not params.get("canceled"):
            if resource_type in {"Document", "XHR", "Fetch"}:
                errors.append(
                    f"{resource_type} failed to load: {params.get('errorText', 'unknown error')}"
                )

    return errors


def _assert_supplier_panel_login_is_healthy(driver, service_name, url, login_env, password_env):
    """Logs in and checks that the registration page and its API requests are healthy."""
    login = os.getenv(login_env, "").strip()
    password = os.getenv(password_env, "").strip()
    assert login and password, (
        f"Для {service_name} укажите {login_env} и {password_env} в .env."
    )

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT_SECONDS)
    driver.get(url)
    login_field = WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input:not([type='hidden']):not([type='password'])")
        ),
        f"{service_name}: поле логина не появилось на {driver.current_url}",
    )
    _clear_performance_log(driver)

    login_field.clear()
    login_field.send_keys(login)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        EC.element_to_be_clickable((By.XPATH, CONTINUE_BUTTON_XPATH)),
        f"{service_name}: кнопка 'Продолжить' для логина недоступна",
    ).click()

    password_field = WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")),
        f"{service_name}: поле пароля не появилось после отправки логина",
    )
    password_field.clear()
    password_field.send_keys(password)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        EC.element_to_be_clickable((By.XPATH, CONTINUE_BUTTON_XPATH)),
        f"{service_name}: кнопка 'Продолжить' для пароля недоступна",
    ).click()

    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        lambda browser: "/login" not in browser.current_url,
        f"{service_name}: после отправки пароля осталась страница login ({driver.current_url})",
    )
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        lambda browser: browser.execute_script(
            "return document.readyState === 'complete' && "
            "Boolean(document.body && document.body.innerHTML.trim())"
        ),
        f"{service_name}: после входа не загрузился DOM страницы регистрации визитов "
        f"({driver.current_url})",
    )
    time.sleep(2)

    network_errors = _get_authenticated_panel_network_errors(driver)
    assert not network_errors, (
        f"{service_name}: after login the supplier panel has failed network requests: "
        + "; ".join(network_errors)
    )


def _assert_page_is_rendered(driver, url: str, expected_selector: str) -> None:
    """Проверяет, что браузер закончил загрузку и отрисовал содержимое страницы."""
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT_SECONDS)
    _clear_performance_log(driver)
    driver.get(url)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        lambda current_driver: current_driver.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    body_html = driver.execute_script("return document.body.innerHTML").strip()
    assert body_html, f"Browser check failed: {url} rendered an empty DOM"

    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        EC.visibility_of_element_located(("css selector", expected_selector))
    )

    # Некоторые login-страницы отрисовывают только поля/иконки и не содержат текста.
    # Поэтому проверяем DOM, а не видимый текст страницы.
    page_text = driver.find_element("tag name", "body").text.lower()
    found_markers = [marker for marker in ERROR_PAGE_MARKERS if marker in page_text]
    assert not found_markers, (
        f"Browser check failed: {url} displays an error page ({found_markers}); "
        f"final URL: {driver.current_url}"
    )

    final_host = urlparse(driver.current_url).hostname
    expected_host = urlparse(url).hostname
    assert final_host == expected_host, (
        f"Browser check failed: {url} redirected to unexpected host "
        f"{final_host!r}"
    )

    network_errors = _get_critical_network_errors(driver)
    assert not network_errors, (
        f"Browser check failed: critical network errors for {url}: "
        + "; ".join(network_errors)
    )


@allure.feature("Service availability")
@allure.story("Hourly check of public entry points")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.schedule
@pytest.mark.smoke
def test_main_urls_are_available_and_rendered(driver):
    """Проверяет HTTP-доступность и загрузку ключевых страниц в реальном браузере."""
    failures = []

    for service_name, url, expected_selector in PAGES_TO_CHECK:
        with allure.step(f"Check {service_name}: {url}"):
            try:
                _assert_http_response_is_healthy(url)
                _assert_page_is_rendered(driver, url, expected_selector)
            except Exception as error:
                failures.append(f"{service_name} ({url}): {type(error).__name__}: {error}")

    assert not failures, "\n\n".join(failures)


@allure.feature("Service availability")
@allure.story("Scheduled login check for supplier panels")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.schedule
@pytest.mark.smoke
def test_supplier_panels_login_and_load_without_network_errors(driver):
    """Checks production supplier panels after authentication, including initial API calls."""
    failures = []

    for service_name, url, login_env, password_env in SUPPLIER_PANELS_TO_CHECK:
        with allure.step(f"Log in to {service_name} and check registration-page requests"):
            try:
                _assert_supplier_panel_login_is_healthy(
                    driver, service_name, url, login_env, password_env
                )
            except Exception as error:
                failures.append(f"{service_name} ({url}): {type(error).__name__}: {error}")

    assert not failures, "\n\n".join(failures)

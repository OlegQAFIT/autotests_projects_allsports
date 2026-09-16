"""Comprehensive smoke checks for the Allsports test website.

Run the read-only/UI suite:
  pytest test_new_web_site/test_smoke_as.py --headless

To also submit an intentionally synthetic form, set
TEST_WEBSITE_FORM_SUBMIT=1.  This is deliberately opt-in because it creates a
test lead in the target environment.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import allure
import pytest
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass(frozen=True)
class SiteProfile:
    name: str
    base_url: str
    locale: str
    country: str
    subscriptions: tuple[str, ...]
    expected_phone_prefix: str

    @property
    def host(self) -> str:
        return urlparse(self.base_url).netloc


AS = SiteProfile(
    "Allsports BY",
    os.getenv("AS_TEST_BASE_URL", "https://xn--80aswg.xn--k1aahcehedi.xn--90ais/ru-by"),
    "ru",
    "Беларус",
    ("region", "lite", "classic", "premium", "vip"),
    "+375",
)

COMMON_PATHS = (
    "",
    "/facilities",
    "/facilities-table",
    "/levels",
    "/companies",
    "/partners",
    "/contacts",
    "/license",
    "/user-agreements",
)
LEGAL_TOKENS = ("/license", "/user-agreements", "/policy/", "/rule/", "/cookie/")
STORE_HOSTS = ("apps.apple.com", "play.google.com", "appgallery.huawei.com")
WAIT = 20


def _url(profile: SiteProfile, path: str) -> str:
    return f"{profile.base_url.rstrip('/')}{path}"


def _wait_ready(driver) -> None:
    WebDriverWait(driver, WAIT).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    WebDriverWait(driver, WAIT).until(
        lambda d: d.find_element(By.TAG_NAME, "body").text.strip()
    )


def _open(driver, url: str) -> None:
    driver.get(url)
    _wait_ready(driver)
    _accept_cookies(driver)


def _accept_cookies(driver) -> None:
    for selector in (".cookie-primary-modal__confirm", "button[id*='cookie']"):
        for button in driver.find_elements(By.CSS_SELECTOR, selector):
            if button.is_displayed() and button.is_enabled():
                driver.execute_script("arguments[0].click()", button)
                return


def _http_get(url: str, **kwargs) -> requests.Response:
    return requests.get(url, timeout=30, allow_redirects=True, **kwargs)


def _same_site(profile: SiteProfile, href: str) -> bool:
    return urlparse(href).netloc == profile.host


def _links(driver) -> list[str]:
    return driver.execute_script(
        "return [...document.querySelectorAll('a[href]')].map(a => a.href).filter(Boolean)"
    )


def _check_no_failed_network_requests(driver) -> None:
    try:
        entries = driver.get_log("performance")
    except Exception:
        pytest.skip("Performance log is unavailable in the selected browser")

    failures = []
    for entry in entries:
        try:
            message = json.loads(entry["message"])["message"]
        except (KeyError, TypeError, json.JSONDecodeError):
            continue
        params = message.get("params", {})
        resource_type = params.get("type")
        if message.get("method") == "Network.responseReceived" and resource_type in {"Document", "XHR", "Fetch"}:
            response = params.get("response", {})
            if response.get("status", 0) >= 400:
                failures.append(f"{resource_type} {response.get('status')}: {response.get('url')}")
        if message.get("method") == "Network.loadingFailed" and not params.get("canceled"):
            if resource_type in {"Document", "XHR", "Fetch"}:
                failures.append(f"{resource_type} loading failed: {params.get('errorText')}")
    assert not failures, "Failed UI network requests:\n" + "\n".join(failures)


def _visible_text(driver) -> str:
    return driver.find_element(By.TAG_NAME, "body").text


def _legal_links(profile: SiteProfile, driver) -> list[str]:
    return sorted({
        href for href in _links(driver)
        if _same_site(profile, href) and any(token in urlparse(href).path for token in LEGAL_TOKENS)
    })


def _form_inputs(driver):
    return driver.find_elements(By.CSS_SELECTOR, "form input")


def _fill_input(element, value: str) -> None:
    element.clear()
    element.send_keys(value)


def _form_button(driver):
    return driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")


def _test_public_routes(profile: SiteProfile) -> None:
    for path in COMMON_PATHS:
        url = _url(profile, path)
        response = _http_get(url)
        assert response.status_code == 200, f"{url} returned {response.status_code}"
        assert "text/html" in response.headers.get("content-type", "").lower(), url
        assert len(response.text) > 500, f"Unexpectedly short HTML: {url}"


def _test_rendering_and_media(driver, profile: SiteProfile) -> None:
    for path in COMMON_PATHS:
        _open(driver, _url(profile, path))
        assert profile.locale in driver.find_element(By.TAG_NAME, "html").get_attribute("lang").lower()
        broken = driver.execute_script(
            "return [...document.images].filter(i => i.complete && !i.naturalWidth).map(i => i.currentSrc || i.src)"
        )
        assert not broken, f"Broken images on {driver.current_url}: {broken}"
        for source in driver.execute_script(
            "return [...document.querySelectorAll('video source, video[src]')].map(v => v.src).filter(Boolean)"
        ):
            assert _http_get(source).status_code < 400, f"Broken video resource: {source}"
        _check_no_failed_network_requests(driver)

    _open(driver, profile.base_url)
    assert profile.country.lower() in _visible_text(driver).lower(), (
        f"Homepage copy does not mention its target country: {profile.country}"
    )


def _test_all_links_and_documents(driver, profile: SiteProfile) -> None:
    discovered = set()
    for path in COMMON_PATHS:
        _open(driver, _url(profile, path))
        discovered.update(_links(driver))

    internal = sorted(href for href in discovered if _same_site(profile, href))
    for href in internal:
        response = _http_get(href)
        assert response.status_code == 200, f"Internal link is broken: {href} -> {response.status_code}"

    legal = set()
    for landing in ("/license", "/user-agreements"):
        _open(driver, _url(profile, landing))
        legal.update(_legal_links(profile, driver))
    assert legal, "Legal document links were not found"
    for href in sorted(legal):
        response = _http_get(href)
        assert response.status_code == 200, f"Legal document is unavailable: {href}"
        assert len(response.text) > 800, f"Legal document is unexpectedly short: {href}"
        assert re.search(r"<html[^>]+lang=", response.text, re.I), f"Missing lang in {href}"

    # Some legal pages expose a date/version selector.  Its options must render
    # when the control exists; older document layouts legitimately have none.
    for landing in ("/license", "/user-agreements"):
        _open(driver, _url(profile, landing))
        selectors = driver.find_elements(
            By.CSS_SELECTOR,
            "select, input[readonly][class*='select'], button[class*='select']",
        )
        for selector in selectors:
            if selector.is_displayed() and selector.is_enabled():
                driver.execute_script("arguments[0].click()", selector)
                options = driver.find_elements(By.CSS_SELECTOR, "option, [role='option'], li")
                assert any(option.text.strip() for option in options), (
                    f"Document date/version dropdown opened without options on {driver.current_url}"
                )

    stores = [href for href in discovered if urlparse(href).netloc in STORE_HOSTS]
    assert stores, "No application-store links found"
    for href in stores:
        assert urlparse(href).scheme == "https", f"Store link must use HTTPS: {href}"


def _test_levels_navigation(driver, profile: SiteProfile) -> None:
    _open(driver, _url(profile, "/levels"))
    links = _links(driver)
    for level in profile.subscriptions:
        matching = [href for href in links if "/facilities?" in href and f"level={level}" in href]
        assert matching, f"No map link for {level} subscription"
        _open(driver, matching[0])
        assert f"level={level}" in driver.current_url, f"Level filter lost for {level}"
        assert "mapbox" in driver.page_source.lower() or driver.find_elements(By.CSS_SELECTOR, "canvas"), "Map is not rendered"

    table_links = [href for href in links if "/facilities-table" in href]
    assert table_links, "Levels page has no transition to facilities table"
    _open(driver, table_links[0])
    assert "/facilities-table" in driver.current_url
    assert _visible_text(driver).strip(), "Facilities table has no visible content"


def _test_map_filters_and_supplier_cards(driver, profile: SiteProfile) -> None:
    _open(driver, _url(profile, "/facilities"))
    assert driver.find_elements(By.CSS_SELECTOR, ".mapboxgl-map, canvas"), "Map canvas is absent"
    controls = driver.find_elements(By.CSS_SELECTOR, ".mapboxgl-ctrl-zoom-in, .mapboxgl-ctrl-zoom-out")
    assert len(controls) >= 2, "Map zoom controls are absent"

    # The test checks all visible filter controls and opens the filter modal when present.
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[readonly], input[placeholder*='Поиск'], input[placeholder*='Search']")
    assert inputs, "Map filter/search controls are absent"
    filter_buttons = [button for button in driver.find_elements(By.TAG_NAME, "button") if button.text.strip() in {"Фильтр", "Filter", "More", "Дополнительно"}]
    if filter_buttons:
        driver.execute_script("arguments[0].click()", filter_buttons[0])
        WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "li, [role='option']")) > 0)
        options = [item.text.strip() for item in driver.find_elements(By.CSS_SELECTOR, "li, [role='option']") if item.text.strip()]
        assert options, "Filter opened without translated options"
        clickable = driver.find_elements(By.CSS_SELECTOR, "li label, [role='option']")
        if clickable:
            driver.execute_script("arguments[0].click()", clickable[0])
            apply = [b for b in driver.find_elements(By.TAG_NAME, "button") if b.text.strip() in {"Применить", "Apply"}]
            if apply:
                driver.execute_script("arguments[0].click()", apply[0])
                WebDriverWait(driver, 10).until(lambda d: _visible_text(d).strip())

    cards = driver.find_elements(By.CSS_SELECTOR, "[class*='marker'], [class*='facility-card'], [class*='object-card']")
    if cards:
        driver.execute_script("arguments[0].click()", cards[0])
        WebDriverWait(driver, 10).until(lambda d: _visible_text(d).strip())


def _test_form_validation_and_optional_submission(driver, profile: SiteProfile) -> None:
    _open(driver, _url(profile, "/contacts"))
    inputs = _form_inputs(driver)
    assert len(inputs) >= 4, "Contact form fields are absent"
    button = _form_button(driver)
    assert not button.is_enabled(), "Submit button must be disabled on an empty form"

    policy_links = [href for href in _links(driver) if "processing-personal-data" in href]
    assert policy_links, "Personal data policy link is absent from the form"
    for href in policy_links:
        assert _http_get(href).status_code == 200, f"Broken policy link: {href}"

    _fill_input(inputs[0], "QA Test")
    _fill_input(inputs[1], "invalid")
    _fill_input(inputs[2], "invalid-email")
    _fill_input(inputs[3], "QA Test Company")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "form input[type='checkbox']")
    if checkboxes:
        driver.execute_script("arguments[0].click()", checkboxes[0])
    WebDriverWait(driver, 10).until(lambda d: any("email" in e.text.lower() or "почт" in e.text.lower() for e in d.find_elements(By.CSS_SELECTOR, ".input-error")) or not _form_button(d).is_enabled())

    if os.getenv("TEST_WEBSITE_FORM_SUBMIT") != "1":
        return

    # A real test lead is created only when this explicit CI/local switch is set.
    _open(driver, _url(profile, "/contacts"))
    inputs = _form_inputs(driver)
    _fill_input(inputs[0], "QA Test")
    _fill_input(inputs[1], f"{profile.expected_phone_prefix} 00 000 00 00")
    _fill_input(inputs[2], "qa-smoke@example.test")
    _fill_input(inputs[3], "QA Smoke Test Company")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "form input[type='checkbox']")
    if checkboxes:
        driver.execute_script("arguments[0].click()", checkboxes[0])
    submit = _form_button(driver)
    assert submit.is_enabled(), "Valid test form did not enable Submit"
    driver.execute_script("arguments[0].click()", submit)
    WebDriverWait(driver, 20).until(
        lambda d: any(token in _visible_text(d).lower() for token in ("thank", "success", "успеш", "спасибо", "oops", "error"))
    )
    text = _visible_text(driver).lower()
    assert not any(token in text for token in ("oops!", "something went wrong", "ошибка")), text


def run_site_suite(driver, profile: SiteProfile) -> None:
    with allure.step("HTTP availability of all key public routes"):
        _test_public_routes(profile)
    with allure.step("Rendering, media and failed UI network requests"):
        _test_rendering_and_media(driver, profile)
    with allure.step("All discovered internal links, policy links and legal documents"):
        _test_all_links_and_documents(driver, profile)
    with allure.step("Subscription cards, preselected map levels and facilities table"):
        _test_levels_navigation(driver, profile)
    with allure.step("Map, filter controls, translated options and supplier cards"):
        _test_map_filters_and_supplier_cards(driver, profile)
    with allure.step("Contact form, validation, policy link and optional submission"):
        _test_form_validation_and_optional_submission(driver, profile)


@allure.feature("Test website smoke")
@allure.story("Allsports BY: full public-site journey")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.release_gate
@pytest.mark.form_submission
def test_smoke_as_full_public_site(driver):
    run_site_suite(driver, AS)

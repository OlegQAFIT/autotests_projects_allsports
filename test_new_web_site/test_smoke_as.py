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
from selenium.webdriver.support.ui import Select, WebDriverWait


@dataclass(frozen=True)
class SiteProfile:
    name: str
    base_url: str
    locale: str
    country: str
    subscriptions: tuple[str, ...]
    expected_phone_prefix: str
    expected_email_placeholder: str

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
    "qwerty@allsports.by",
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


def _check_no_browser_errors(driver) -> None:
    """Fail on actual JavaScript runtime errors, not harmless console warnings."""
    try:
        entries = driver.get_log("browser")
    except Exception:
        pytest.skip("Browser console log is unavailable in the selected browser")
    errors = [
        entry["message"] for entry in entries
        if entry.get("level") == "SEVERE"
        and not any(allowed in entry["message"].lower() for allowed in (
            "favicon.ico", "third-party cookie", "maps.googleapis.com",
            "[nuxt-gtag] missing google tag id",
        ))
    ]
    assert not errors, "Browser JavaScript errors:\n" + "\n".join(errors)


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


def _visible_forms(driver):
    return [
        form for form in driver.find_elements(By.CSS_SELECTOR, "form")
        if form.is_displayed() and form.find_elements(By.CSS_SELECTOR, "button[type='submit']")
    ]


def _buttons_with_text(driver, *labels: str):
    expected = {label.casefold() for label in labels}
    return [
        button for button in driver.find_elements(By.TAG_NAME, "button")
        if button.is_displayed() and button.text.strip().casefold() in expected
    ]


def _install_network_probe(driver) -> None:
    """Record application Fetch/XHR results without changing the requests."""
    driver.execute_script(
        """
        if (window.__qaNetworkProbeInstalled) return;
        window.__qaNetworkProbeInstalled = true;
        window.__qaNetworkEvents = [];
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
          const response = await originalFetch(...args);
          window.__qaNetworkEvents.push({
            kind: 'fetch', url: String(args[0]), status: response.status, ok: response.ok
          });
          return response;
        };
        const open = XMLHttpRequest.prototype.open;
        const send = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.open = function(method, url, ...rest) {
          this.__qaMethod = method; this.__qaUrl = url;
          return open.call(this, method, url, ...rest);
        };
        XMLHttpRequest.prototype.send = function(...args) {
          this.addEventListener('loadend', () => window.__qaNetworkEvents.push({
            kind: 'xhr', method: this.__qaMethod, url: this.__qaUrl,
            status: this.status, ok: this.status >= 200 && this.status < 400
          }));
          return send.apply(this, args);
        };
        """
    )


def _submission_events(driver):
    return driver.execute_script("return window.__qaNetworkEvents || []")


def _form_label(form) -> str:
    return re.sub(r"\s+", " ", form.text).strip()[:160]


def _form_submit(form):
    return form.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")


def _fill_synthetic_form(form, profile: SiteProfile, valid: bool) -> None:
    """Fill every editable field without relying on translated placeholders."""
    for index, field in enumerate(form.find_elements(By.CSS_SELECTOR, "input, textarea, select")):
        if not field.is_displayed() or field.get_attribute("type") in {"hidden", "submit", "button"}:
            continue
        kind = (field.get_attribute("type") or "").lower()
        if kind in {"checkbox", "radio"}:
            if valid and not field.is_selected():
                field.click()
            continue
        if field.tag_name.lower() == "select":
            options = field.find_elements(By.CSS_SELECTOR, "option:not([disabled])")
            if len(options) > 1:
                driver = form.parent
                driver.execute_script("arguments[0].selectedIndex=1; arguments[0].dispatchEvent(new Event('change',{bubbles:true}))", field)
            continue
        name = " ".join((
            field.get_attribute("name") or "",
            field.get_attribute("placeholder") or "",
            field.get_attribute("autocomplete") or "",
        )).lower()
        if "mail" in name or kind == "email":
            value = "qa.matrix@example.test" if valid else "broken-email"
        elif "phone" in name or "tel" in name or kind == "tel":
            value = f"{profile.expected_phone_prefix} 99 123 45 67" if valid else "123"
        elif field.tag_name.lower() == "textarea":
            value = "QA synthetic question for test environment"
        elif "company" in name or "facility" in name:
            value = "QA Synthetic Company"
        elif "city" in name:
            value = "QA City"
        else:
            value = "QA Synthetic Name"
        field.clear()
        field.send_keys(value)


def _assert_form_validation_contract(driver, form, profile: SiteProfile) -> None:
    """Negative form cases must show feedback and must never create a request."""
    _install_network_probe(driver)
    before = len(_submission_events(driver))
    _fill_synthetic_form(form, profile, valid=False)
    submit = _form_submit(form)
    driver.execute_script("arguments[0].click()", submit)
    WebDriverWait(driver, 10).until(
        lambda d: not submit.is_enabled()
        or bool(form.find_elements(By.CSS_SELECTOR, ".input-error, [aria-invalid='true'], .error"))
    )
    after = _submission_events(driver)[before:]
    assert not [event for event in after if event.get("method", "POST").upper() == "POST"], (
        f"Invalid form sent a POST instead of blocking client-side validation: {_form_label(form)}"
    )


def _assert_live_form_submission(driver, form, profile: SiteProfile) -> None:
    """Post a synthetic lead and require a precise successful network outcome."""
    if os.getenv("TEST_WEBSITE_FORM_SUBMIT") != "1":
        return
    _install_network_probe(driver)
    before = len(_submission_events(driver))
    _fill_synthetic_form(form, profile, valid=True)
    submit = _form_submit(form)
    assert submit.is_enabled(), f"Valid form remains disabled: {_form_label(form)}"
    driver.execute_script("arguments[0].click()", submit)
    WebDriverWait(driver, 20).until(
        lambda d: any(
            event.get("method", "POST").upper() == "POST"
            for event in _submission_events(d)[before:]
        )
    )
    posts = [
        event for event in _submission_events(driver)[before:]
        if event.get("method", "POST").upper() == "POST"
    ]
    assert posts and all(200 <= int(event["status"]) < 300 for event in posts), (
        f"Form HTTP response is not 2xx: {_form_label(form)}; {posts}"
    )


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
        _check_no_browser_errors(driver)

    _open(driver, profile.base_url)
    assert profile.country.lower() in _visible_text(driver).lower(), (
        f"Homepage copy does not mention its target country: {profile.country}"
    )


def _test_copy_and_page_semantics(driver, profile: SiteProfile) -> None:
    """Catch empty templates, untranslated placeholders and inaccessible pages."""
    for path in COMMON_PATHS:
        _open(driver, _url(profile, path))
        body = _visible_text(driver)
        assert driver.find_elements(By.CSS_SELECTOR, "h1"), f"Page has no H1: {driver.current_url}"
        assert not re.search(r"\{\{[^}]+\}\}|\[object Object\]|lorem ipsum", body, re.I), (
            f"Template placeholder leaked into visible copy: {driver.current_url}"
        )
        title = driver.title.strip()
        assert title and len(title) > 3, f"Page has an empty/placeholder title: {driver.current_url}"
def _assert_form_placeholders(form, profile: SiteProfile) -> int:
    """Check a single inline or CTA-modal form against its site profile."""
    checked_email_fields = 0
    for field in form.find_elements(By.CSS_SELECTOR, "input"):
        if not field.is_displayed():
            continue
        placeholder = (field.get_attribute("placeholder") or "").strip()
        kind = (field.get_attribute("type") or "").casefold()
        if kind == "email" or "@" in placeholder:
            assert placeholder == profile.expected_email_placeholder, (
                f"Wrong e-mail placeholder on {form.parent.current_url}: "
                f"expected '{profile.expected_email_placeholder}', got '{placeholder}'"
            )
            checked_email_fields += 1
        if kind == "tel" or "phone" in (field.get_attribute("name") or "").casefold():
            assert profile.expected_phone_prefix in placeholder, (
                f"Wrong phone placeholder on {form.parent.current_url}: "
                f"expected prefix {profile.expected_phone_prefix}, got '{placeholder}'"
            )
    return checked_email_fields


def _test_form_placeholders(driver, profile: SiteProfile) -> None:
    """Protect brand/country-specific form hints from cross-site leakage."""
    checked_email_fields = 0
    for path in ("", "/levels", "/companies", "/partners", "/contacts"):
        _open(driver, _url(profile, path))
        for form in _visible_forms(driver):
            checked_email_fields += _assert_form_placeholders(form, profile)
    assert checked_email_fields, f"No e-mail placeholders found for {profile.name}"


def _test_all_links_and_documents(driver, profile: SiteProfile) -> None:
    discovered = set()
    for path in COMMON_PATHS:
        _open(driver, _url(profile, path))
        discovered.update(_links(driver))

    # Crawl every first-party URL reachable from the public templates and legal
    # documents. It catches broken links that are not present in the footer.
    pending = [href for href in discovered if _same_site(profile, href)]
    checked: set[str] = set()
    while pending:
        href = pending.pop(0).split("#", 1)[0]
        if not href or href in checked:
            continue
        checked.add(href)
        response = _http_get(href)
        assert response.status_code == 200, f"Internal link is broken: {href} -> {response.status_code}"
        for raw_href in re.findall(r'''href=["']([^"']+)["']''', response.text, flags=re.I):
            absolute = urljoin(response.url, raw_href)
            if _same_site(profile, absolute) and absolute.split("#", 1)[0] not in checked:
                pending.append(absolute)

    legal = set()
    document_external = set()
    for landing in ("/license", "/user-agreements"):
        _open(driver, _url(profile, landing))
        legal.update(_legal_links(profile, driver))
    assert legal, "Legal document links were not found"
    for href in sorted(legal):
        response = _http_get(href)
        assert response.status_code == 200, f"Legal document is unavailable: {href}"
        assert len(response.text) > 800, f"Legal document is unexpectedly short: {href}"
        assert re.search(r"<html[^>]+lang=", response.text, re.I), f"Missing lang in {href}"
        # Follow every document hyperlink as well, including version-history and
        # footer references that are not present on marketing pages.
        for raw_href in re.findall(r'''href=["']([^"']+)["']''', response.text, flags=re.I):
            absolute = urljoin(response.url, raw_href)
            if _same_site(profile, absolute):
                nested = _http_get(absolute.split("#", 1)[0])
                assert nested.status_code == 200, (
                    f"Broken link inside legal document: {absolute} -> {nested.status_code}"
                )
            elif urlparse(absolute).scheme == "https":
                document_external.add(absolute)

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
        # Native version/date selects must render every option and retain the
        # chosen value. This is intentionally separate from the generic custom
        # dropdown check above.
        for select_element in driver.find_elements(By.CSS_SELECTOR, "select"):
            if not select_element.is_displayed() or not select_element.is_enabled():
                continue
            select = Select(select_element)
            values = [option.get_attribute("value") for option in select.options if option.text.strip()]
            assert values, f"Document select has no versions/dates: {driver.current_url}"
            for value in values:
                select.select_by_value(value)
                assert select.first_selected_option.get_attribute("value") == value, (
                    f"Document select did not retain version/date '{value}'"
                )
        custom_triggers = [
            element for element in driver.find_elements(
                By.CSS_SELECTOR, "input[readonly][class*='select'], button[class*='select']"
            )
            if element.is_displayed() and element.is_enabled()
        ]
        for trigger_index, trigger in enumerate(custom_triggers):
            driver.execute_script("arguments[0].click()", trigger)
            labels = [
                option.text.strip() for option in driver.find_elements(
                    By.CSS_SELECTOR, "[role='option'], .select__option, .dropdown-item"
                )
                if option.is_displayed() and option.text.strip()
            ]
            assert labels, f"Custom document dropdown has no options: {driver.current_url}"
            for label in labels:
                _open(driver, _url(profile, landing))
                triggers = [
                    element for element in driver.find_elements(
                        By.CSS_SELECTOR, "input[readonly][class*='select'], button[class*='select']"
                    )
                    if element.is_displayed() and element.is_enabled()
                ]
                assert trigger_index < len(triggers), "Document dropdown changed after reload"
                driver.execute_script("arguments[0].click()", triggers[trigger_index])
                option = next(
                    (element for element in driver.find_elements(
                        By.CSS_SELECTOR, "[role='option'], .select__option, .dropdown-item"
                    ) if element.is_displayed() and element.text.strip() == label),
                    None,
                )
                assert option is not None, f"Document version/date disappeared: {label}"
                driver.execute_script("arguments[0].click()", option)
                assert label in _visible_text(driver), (
                    f"Selecting document version/date did not render '{label}'"
                )

    stores = [href for href in discovered if urlparse(href).netloc in STORE_HOSTS]
    assert stores, "No application-store links found"
    for href in stores:
        assert urlparse(href).scheme == "https", f"Store link must use HTTPS: {href}"

    external = sorted({
        href for href in discovered
        if urlparse(href).scheme == "https" and not _same_site(profile, href)
    } | document_external)
    for href in external:
        response = _http_get(href)
        assert 200 <= response.status_code < 400, (
            f"External link does not resolve successfully: {href} -> {response.status_code}"
        )


def _test_internal_clickthrough(driver, profile: SiteProfile) -> None:
    """Follow every distinct first-party anchor through the browser UI itself."""
    destinations: dict[str, str] = {}
    for path in COMMON_PATHS:
        _open(driver, _url(profile, path))
        for href in _links(driver):
            canonical = href.split("#", 1)[0]
            if _same_site(profile, canonical):
                destinations.setdefault(canonical, driver.current_url)
    assert destinations, "No first-party UI links were found"

    for destination, source in destinations.items():
        _open(driver, source)
        anchors = [
            anchor for anchor in driver.find_elements(By.CSS_SELECTOR, "a[href]")
            if anchor.get_attribute("href").split("#", 1)[0] == destination
            and anchor.is_displayed()
        ]
        if not anchors:
            # The link may be in a desktop/mobile variant; it was already
            # checked by HTTP crawl, so do not misreport a hidden duplicate.
            continue
        driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", anchors[0])
        _wait_ready(driver)
        assert driver.current_url.split("#", 1)[0] == destination, (
            f"UI navigation failed: {source} -> {destination}; got {driver.current_url}"
        )
        assert _visible_text(driver).strip(), f"Blank destination after clicking {destination}"


def _test_visual_layout_at_key_viewports(driver, profile: SiteProfile) -> None:
    """Provide reviewable key-screen snapshots and reject horizontal overflow."""
    original = driver.get_window_size()
    try:
        for width, height in ((390, 844), (1440, 1000)):
            driver.set_window_size(width, height)
            for path in ("", "/levels", "/facilities", "/facilities-table", "/contacts"):
                _open(driver, _url(profile, path))
                overflow = driver.execute_script(
                    "return Math.max(0, document.documentElement.scrollWidth - window.innerWidth)"
                )
                assert overflow <= 2, f"Horizontal overflow ({overflow}px) at {width}px: {driver.current_url}"
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"{profile.name}_{path.strip('/') or 'home'}_{width}px",
                    attachment_type=allure.attachment_type.PNG,
                )
    finally:
        driver.set_window_size(original["width"], original["height"])


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


def _test_facilities_table_and_supplier_transitions(driver, profile: SiteProfile) -> None:
    """Covers search, filter reset and the table/card-to-supplier journey."""
    _open(driver, _url(profile, "/facilities-table"))
    tables = driver.find_elements(By.CSS_SELECTOR, "table")
    assert tables, "Facilities table is absent"
    rows = [
        row for row in driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        if row.is_displayed() and row.text.strip()
    ]
    assert rows, "Facilities table has no data rows"

    search_fields = [
        item for item in driver.find_elements(By.CSS_SELECTOR, "input")
        if item.is_displayed() and ("search" in (item.get_attribute("placeholder") or "").lower()
                               or "поиск" in (item.get_attribute("placeholder") or "").lower())
    ]
    if search_fields:
        original = rows[0].text.split()[0]
        _fill_input(search_fields[0], original)
        WebDriverWait(driver, 10).until(
            lambda d: any(original.casefold() in row.text.casefold()
                          for row in d.find_elements(By.CSS_SELECTOR, "tbody tr"))
        )
        search_fields[0].clear()

    # A row must lead to the same provider details instead of a dead click.
    first_row = next(row for row in driver.find_elements(By.CSS_SELECTOR, "tbody tr") if row.is_displayed())
    provider_name = first_row.text.splitlines()[0].strip()
    driver.execute_script("arguments[0].click()", first_row)
    WebDriverWait(driver, 10).until(
        lambda d: provider_name.casefold() in _visible_text(d).casefold()
        or bool(d.find_elements(By.CSS_SELECTOR, "[role='dialog'], [class*='modal']"))
    )

    close_buttons = _buttons_with_text(driver, "Close", "Закрыть")
    if close_buttons:
        driver.execute_script("arguments[0].click()", close_buttons[0])
    _open(driver, _url(profile, "/facilities"))
    table_links = [href for href in _links(driver) if "/facilities-table" in href]
    assert table_links, "Map has no transition to the facilities table"
    _open(driver, table_links[0])
    assert driver.find_elements(By.CSS_SELECTOR, "tbody tr"), "Map-to-table transition lost facilities"


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
    assert cards, "No map marker or provider card is available to open"
    driver.execute_script("arguments[0].click()", cards[0])
    WebDriverWait(driver, 10).until(
        lambda d: bool(d.find_elements(By.CSS_SELECTOR, "[role='dialog'], [class*='modal'], [class*='popup']"))
        or len(_visible_text(d).strip()) > 50
    )


def _test_map_all_filter_values(driver, profile: SiteProfile) -> None:
    """Opens every map-filter group and verifies its data and selection state."""
    _open(driver, _url(profile, "/facilities"))
    buttons = [
        button for button in driver.find_elements(By.TAG_NAME, "button")
        if button.text.strip() in {"Фильтр", "Filter"}
    ]
    assert buttons, "Map filter button is absent"
    driver.execute_script("arguments[0].click()", buttons[0])
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, ".map-filter-modal li")) > 0
    )
    groups = driver.find_elements(By.CSS_SELECTOR, ".map-filter-modal ul")
    assert groups, "Map filters have no option groups"
    for group in groups:
        options = [item for item in group.find_elements(By.CSS_SELECTOR, ":scope > li") if item.text.strip()]
        selectable = [
            item for item in options
            if "show all" not in item.text.lower() and "показать все" not in item.text.lower()
        ]
        assert selectable, "A map-filter group has no real values"
        # Every visible value is checked for readable localized content.
        assert all(item.text.strip() for item in selectable), "Empty filter option text"
        driver.execute_script("arguments[0].click()", selectable[0])

    apply = [
        button for button in driver.find_elements(By.TAG_NAME, "button")
        if button.text.strip() in {"Применить", "Apply"}
    ]
    if apply:
        driver.execute_script("arguments[0].click()", apply[0])
    WebDriverWait(driver, 15).until(lambda d: _visible_text(d).strip())
    state = driver.execute_script(
        "return window.__NUXT__?.pinia?.mapFilter || window.__NUXT__?.pinia?.tableFilter || null"
    )
    assert state is not None, "Filter application did not expose a map/table state"


def _test_each_map_filter_value(driver, profile: SiteProfile) -> None:
    """Apply each offered value independently and ensure results remain usable.

    The options are read from the UI, so this test automatically expands when
    cities, activities or subscription types are added to the catalogue.
    """
    _open(driver, _url(profile, "/facilities"))
    filter_button = _buttons_with_text(driver, "Filter", "Фильтр")
    assert filter_button, "Map filter button is absent"
    driver.execute_script("arguments[0].click()", filter_button[0])
    WebDriverWait(driver, 10).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, ".map-filter-modal ul")
    )
    # Snapshot labels first: clicking closes/re-renders the Vue modal.
    groups = []
    for index, group in enumerate(driver.find_elements(By.CSS_SELECTOR, ".map-filter-modal ul")):
        labels = [
            option.text.strip() for option in group.find_elements(By.CSS_SELECTOR, ":scope > li")
            if option.text.strip()
            and "show all" not in option.text.lower()
            and "показать все" not in option.text.lower()
        ]
        groups.append((index, labels))

    for group_index, labels in groups:
        for label in labels:
            # Start from clean filters for every value to prove it is individually
            # selectable and does not produce a broken map/table UI.
            _open(driver, _url(profile, "/facilities"))
            button = _buttons_with_text(driver, "Filter", "Фильтр")[0]
            driver.execute_script("arguments[0].click()", button)
            modal_groups = driver.find_elements(By.CSS_SELECTOR, ".map-filter-modal ul")
            assert group_index < len(modal_groups), "Filter group order unexpectedly changed"
            option = next(
                (item for item in modal_groups[group_index].find_elements(By.CSS_SELECTOR, ":scope > li")
                 if item.text.strip() == label),
                None,
            )
            assert option is not None, f"Filter option disappeared: {label}"
            driver.execute_script("arguments[0].click()", option)
            apply = _buttons_with_text(driver, "Apply", "Применить")
            if apply:
                driver.execute_script("arguments[0].click()", apply[0])
            WebDriverWait(driver, 10).until(lambda d: _visible_text(d).strip())
            state = driver.execute_script(
                "return window.__NUXT__?.pinia?.mapFilter || window.__NUXT__?.pinia?.tableFilter || null"
            )
            assert state is not None, f"Applying '{label}' did not update filter state"
            normalized_label = re.sub(r"[^a-zа-я0-9]+", "", label.casefold())
            serialized_state = re.sub(
                r"[^a-zа-я0-9]+", "", json.dumps(state, ensure_ascii=False).casefold()
            )
            assert normalized_label in serialized_state, (
                f"Selected filter value is absent from the applied state: {label}"
            )
            results = driver.find_elements(
                By.CSS_SELECTOR, "tbody tr, [class*='facility-card'], [class*='object-card'], [class*='marker']"
            )
            empty_state = driver.find_elements(
                By.CSS_SELECTOR, "[class*='empty'], [class*='no-result'], [class*='not-found']"
            )
            assert results or empty_state, (
                f"Filter '{label}' leaves neither suppliers nor an explicit empty-result state"
            )
            assert not driver.find_elements(By.CSS_SELECTOR, ".error-page, [class*='error-page']"), (
                f"Applying '{label}' opened an error page"
            )
            _check_no_failed_network_requests(driver)


def _test_every_supplier_card(driver, profile: SiteProfile) -> None:
    """Open every currently available supplier entry from the map/list UI."""
    _open(driver, _url(profile, "/facilities"))
    selector = "[class*='facility-card'], [class*='object-card'], [class*='marker']"
    cards = [card for card in driver.find_elements(By.CSS_SELECTOR, selector) if card.is_displayed()]
    assert cards, "Map exposes no supplier cards/markers"
    # Reopen the page before each click because opening a card can replace the
    # map DOM. This intentionally covers each current provider/marker type.
    total = len(cards)
    for index in range(total):
        _open(driver, _url(profile, "/facilities"))
        current = [card for card in driver.find_elements(By.CSS_SELECTOR, selector) if card.is_displayed()]
        assert index < len(current), "Supplier list changed while opening cards"
        card = current[index]
        label = card.get_attribute("aria-label") or card.text.strip() or f"card #{index + 1}"
        driver.execute_script("arguments[0].click()", card)
        WebDriverWait(driver, 10).until(
            lambda d: bool(d.find_elements(By.CSS_SELECTOR, "[role='dialog'], [class*='modal'], [class*='popup']"))
            or label.casefold() in _visible_text(d).casefold()
        )


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
    WebDriverWait(driver, 10).until(
        lambda d: any("email" in e.text.lower() or "почт" in e.text.lower()
                      for e in d.find_elements(By.CSS_SELECTOR, ".input-error"))
        or not _form_button(d).is_enabled()
    )
    assert not _form_button(driver).is_enabled(), (
        "Submit became enabled despite invalid phone/e-mail; validation must block a request"
    )

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
    _install_network_probe(driver)
    driver.execute_script("arguments[0].click()", submit)
    WebDriverWait(driver, 20).until(
        lambda d: any(token in _visible_text(d).lower() for token in ("thank", "success", "успеш", "спасибо", "oops", "error"))
    )
    text = _visible_text(driver).lower()
    assert not any(token in text for token in ("oops!", "something went wrong", "ошибка")), text
    events = _submission_events(driver)
    assert events, "Form click emitted no Fetch/XHR request"
    assert all(event["ok"] for event in events), f"Form request failed: {events}"


def _test_all_visible_form_ctas(driver, profile: SiteProfile) -> None:
    """Checks each public-page form's consent link and initial submit state.

    Modal forms are deliberately opened but not posted here; their submission
    is covered by the explicitly enabled synthetic-lead scenario above.
    """
    checked = 0
    ctas_checked = 0
    for path in ("", "/levels", "/companies", "/partners", "/contacts"):
        _open(driver, _url(profile, path))
        forms = _visible_forms(driver)
        for form in forms:
            button = _form_submit(form)
            assert not button.is_enabled(), (
                f"Empty form has an active submit button on {driver.current_url}"
            )
            policy = form.find_elements(
                By.CSS_SELECTOR,
                "a[href*='processing-personal-data'], a[href*='policy']",
            )
            assert policy, f"Form has no personal-data policy link on {driver.current_url}"
            for link in policy:
                assert _http_get(link.get_attribute("href")).status_code == 200
            checked += 1

        # Run negative and (when explicitly allowed) positive submission paths
        # for every inline form. Reloading isolates one form from another.
        for form_index in range(len(forms)):
            _open(driver, _url(profile, path))
            current_forms = _visible_forms(driver)
            assert form_index < len(current_forms), "Inline form disappeared after reload"
            _assert_form_validation_contract(driver, current_forms[form_index], profile)
            _open(driver, _url(profile, path))
            current_forms = _visible_forms(driver)
            assert form_index < len(current_forms), "Inline form disappeared before live submission"
            _assert_live_form_submission(driver, current_forms[form_index], profile)

        # Cover each semantic CTA separately. Modal dialogs are re-found after
        # every click, which handles Vue re-rendering and identical labels.
        cta_buttons = [
            button for button in driver.find_elements(By.TAG_NAME, "button")
            if button.is_displayed()
            and button.get_attribute("type") != "submit"
            and any(token in button.text.casefold() for token in (
                "offer", "предлож", "partner", "партнер", "question", "вопрос", "contact", "связ",
            ))
        ]
        for index in range(len(cta_buttons)):
            _open(driver, _url(profile, path))
            buttons = [
                button for button in driver.find_elements(By.TAG_NAME, "button")
                if button.is_displayed()
                and button.get_attribute("type") != "submit"
                and any(token in button.text.casefold() for token in (
                    "offer", "предлож", "partner", "партнер", "question", "вопрос", "contact", "связ",
                ))
            ]
            assert index < len(buttons), "CTA disappeared while opening modal"
            driver.execute_script("arguments[0].click()", buttons[index])
            modal_forms = _visible_forms(driver)
            assert modal_forms, f"CTA did not open a form: {buttons[index].text}"
            form = modal_forms[-1]
            assert _assert_form_placeholders(form, profile), (
                f"CTA form has no e-mail placeholder: {buttons[index].text}"
            )
            _assert_form_validation_contract(driver, form, profile)
            _assert_live_form_submission(driver, form, profile)
            ctas_checked += 1
    assert checked, "No public forms were discovered"
    assert ctas_checked, "No offer/partner/question/contact CTAs were discovered"


def _test_question_cta_placeholder(driver, profile: SiteProfile) -> None:
    """Focused regression helper for the Ask Us a Question CTA."""
    _open(driver, profile.base_url)
    questions = [
        button for button in driver.find_elements(By.TAG_NAME, "button")
        if button.is_displayed() and any(
            token in button.text.casefold() for token in ("question", "вопрос")
        )
    ]
    assert questions, f"Ask Us a Question CTA is absent for {profile.name}"
    driver.execute_script("arguments[0].click()", questions[0])
    forms = _visible_forms(driver)
    assert forms, "Ask Us a Question CTA did not open its form"
    assert _assert_form_placeholders(forms[-1], profile), (
        "Ask Us a Question form has no e-mail placeholder"
    )


def run_site_suite(driver, profile: SiteProfile) -> None:
    with allure.step("HTTP availability of all key public routes"):
        _test_public_routes(profile)
    with allure.step("Rendering, media and failed UI network requests"):
        _test_rendering_and_media(driver, profile)
    with allure.step("Visible copy, page headings, titles and template placeholders"):
        _test_copy_and_page_semantics(driver, profile)
    with allure.step("Brand and country-specific e-mail/phone form placeholders"):
        _test_form_placeholders(driver, profile)
    with allure.step("All discovered internal links, policy links and legal documents"):
        _test_all_links_and_documents(driver, profile)
    with allure.step("Browser click-through for every visible internal link"):
        _test_internal_clickthrough(driver, profile)
    with allure.step("Mobile and desktop visual layout snapshots"):
        _test_visual_layout_at_key_viewports(driver, profile)
    with allure.step("Subscription cards, preselected map levels and facilities table"):
        _test_levels_navigation(driver, profile)
    with allure.step("Facilities table, search and provider-card transitions"):
        _test_facilities_table_and_supplier_transitions(driver, profile)
    with allure.step("Map, filter controls, translated options and supplier cards"):
        _test_map_filters_and_supplier_cards(driver, profile)
    with allure.step("Every visible map-filter group and selected-result state"):
        _test_map_all_filter_values(driver, profile)
    with allure.step("Each available map-filter value"):
        _test_each_map_filter_value(driver, profile)
    with allure.step("Contact form, validation, policy link and optional submission"):
        _test_form_validation_and_optional_submission(driver, profile)
    with allure.step("All visible public forms and consent links"):
        _test_all_visible_form_ctas(driver, profile)


@allure.feature("Test website smoke")
@allure.story("Allsports BY: full public-site journey")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.release_gate
@pytest.mark.form_submission
def test_smoke_as_full_public_site(driver):
    run_site_suite(driver, AS)


@allure.feature("Test website smoke")
@allure.story("Allsports BY: dynamic homepage counter and Russian copy")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_smoke_as_homepage_counter_is_rendered(driver):
    _open(driver, AS.base_url)
    text = _visible_text(driver).lower()
    counter = re.search(r"(\d+)\s+объект", text)
    assert counter, "Homepage facility counter is missing"
    assert int(counter.group(1)) >= 0, f"Homepage counter is invalid: {counter.group(1)}"


@allure.feature("Test website regressions")
@allure.story("Allsports BY: invalid contact data cannot submit")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_smoke_as_invalid_contact_data_keeps_submit_disabled(driver):
    """Regression for an enabled submit button with invalid contact values."""
    _test_form_validation_and_optional_submission(driver, AS)


@allure.feature("Jira regressions")
@allure.story("AL-892: AS rejects a Cyprus phone number")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_regression_al_892_as_invalid_cyprus_phone_keeps_offer_disabled(driver):
    """The exact invalid-phone case reported in AL-892 must not enable Send."""
    _open(driver, AS.base_url)
    offer_ctas = [
        button for button in driver.find_elements(By.TAG_NAME, "button")
        if button.is_displayed() and "получить предложение" in button.text.casefold()
    ]
    assert offer_ctas, "AL-892: Get an Offer CTA is absent on AS homepage"
    driver.execute_script("arguments[0].click()", offer_ctas[0])
    WebDriverWait(driver, 10).until(
        lambda d: bool(d.find_elements(By.CSS_SELECTOR, ".modal form, [role='dialog'] form"))
    )
    forms = [
        form for form in driver.find_elements(By.CSS_SELECTOR, ".modal form, [role='dialog'] form")
        if form.is_displayed()
    ]
    assert forms, "AL-892: Get an Offer CTA did not open its form"
    form = forms[-1]
    _fill_synthetic_form(form, AS, valid=True)
    phone = next(
        (field for field in form.find_elements(By.CSS_SELECTOR, "input")
         if (field.get_attribute("type") or "").casefold() == "tel"
         or "phone" in (field.get_attribute("name") or "").casefold()),
        None,
    )
    assert phone is not None, "Offer form has no phone input"
    _fill_input(phone, "+75796276351")
    submit = _form_submit(form)
    WebDriverWait(driver, 10).until(
        lambda d: not submit.is_enabled()
        or bool(form.find_elements(By.CSS_SELECTOR, ".input-error, [aria-invalid='true']"))
    )
    assert not submit.is_enabled(), "AL-892: Cyprus phone enabled AS offer submission"


@allure.feature("Jira regressions")
@allure.story("AL-891: AS uses hard sign in object copy")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_regression_al_891_as_has_no_soft_sign_object_typos(driver):
    """Regression for 'обьект*'; Russian copy must use 'объект*'."""
    for path in ("", "/levels", "/facilities", "/facilities-table"):
        _open(driver, _url(AS, path))
        text = _visible_text(driver).casefold()
        assert "обьект" not in text, f"AL-891 soft-sign typo found: {driver.current_url}"

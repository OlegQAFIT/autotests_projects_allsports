"""Production-only website checks executed by the scheduled smoke workflow."""

import allure
import pytest
import requests
from urllib.parse import urljoin

from conftest import create_chrome
from test_journal_main_flow.test_www_check import (
    CRITICAL_PAGE_PATHS,
    REDIRECT_STATUS_CODES,
    ROUTES_TO_CHECK,
    VISUAL_PAGE_PATHS,
    Website,
    _accept_cookie_consent,
    _assert_app_links_are_available,
    _assert_header_links,
    _assert_http_page_is_available,
    _assert_images_are_loaded,
    _assert_map_is_rendered,
    _discover_published_localized_paths,
    _expected_localized_url,
    _localized_url,
    _normalize_url,
    _open_rendered_page,
    _run_check,
    _url_without_locale,
)


PRODUCTION_WEBSITES = (
    Website("Allsports production", "https://www.allsports.by/ru-by"),
    Website("SportBenefit Cyprus production", "https://www.sportbenefit.eu/en-cy"),
    Website("SportBenefit Lithuania production", "https://www.sportbenefit.eu/en-lt"),
)
PRODUCTION_REDIRECT_WEBSITES = PRODUCTION_WEBSITES[:2]


@pytest.fixture(scope="module")
def production_paths() -> dict[str, tuple[set[str], list[str]]]:
    """Discover links from production itself; test environments are not accessed."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Production-Route-Monitor/1.0"})
    return {
        website.localized_base_url: _discover_published_localized_paths(session, website)
        for website in PRODUCTION_WEBSITES
    }


@pytest.fixture(scope="module")
def driver(pytestconfig):
    browser = create_chrome(pytestconfig.getoption("--headless"))
    browser.implicitly_wait(2)
    yield browser
    browser.quit()


@allure.feature("Production public websites")
@allure.story("Published production pages availability")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("website", PRODUCTION_WEBSITES, ids=lambda site: site.name)
def test_production_published_pages_open_directly(website, production_paths) -> None:
    """Every published production link discovered by the crawler must return HTTP 200."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Production-Route-Monitor/1.0"})
    paths, discovery_failures = production_paths[website.localized_base_url]
    failures = list(discovery_failures)

    for path in sorted(paths):
        try:
            _assert_http_page_is_available(session, _localized_url(website, path))
        except (AssertionError, requests.RequestException) as error:
            failures.append(f"{path}: {error}")

    assert not failures, "Production localized pages are unavailable:\n" + "\n".join(failures)


@allure.feature("Production public websites")
@allure.story("Production locale redirects")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "website", PRODUCTION_REDIRECT_WEBSITES, ids=lambda site: site.name
)
def test_production_routes_redirect_to_locale(website) -> None:
    """Checks production redirects to the correct localized public URL."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Production-Route-Monitor/1.0"})
    failures = []

    for route in ROUTES_TO_CHECK:
        source_url = _url_without_locale(website, route)
        expected_url = _expected_localized_url(website, route)
        try:
            response = session.get(source_url, allow_redirects=False, timeout=15)
            assert response.status_code in REDIRECT_STATUS_CODES, (
                f"HTTP {response.status_code}; expected redirect"
            )
            location = response.headers.get("location")
            assert location, "Redirect response does not contain Location header"
            actual_url = _normalize_url(urljoin(source_url, location))
            assert actual_url == _normalize_url(expected_url), (
                f"Expected {expected_url}, got {actual_url}"
            )
        except (AssertionError, requests.RequestException) as error:
            failures.append(f"{route}: {error}")

    assert not failures, "Production locale redirects failed:\n" + "\n".join(failures)


@allure.feature("Production public websites")
@allure.story("Production website key UI health")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("website", PRODUCTION_WEBSITES, ids=lambda site: site.name)
def test_production_key_website_ui_health(driver, website) -> None:
    """Checks key production pages, the facilities map, header, images, and app links."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Production-Website-Health-Monitor/1.0"})
    failures = []

    for path in CRITICAL_PAGE_PATHS:
        _run_check(
            failures,
            website,
            f"HTTP 200 {path}",
            lambda path=path: _assert_http_page_is_available(session, _localized_url(website, path)),
        )

    _run_check(
        failures,
        website,
        "homepage renders",
        lambda: _open_rendered_page(driver, _localized_url(website, "/")),
    )
    _accept_cookie_consent(driver)
    _run_check(failures, website, "header links", lambda: _assert_header_links(driver, website))
    _run_check(failures, website, "homepage images", lambda: _assert_images_are_loaded(driver))

    for path in VISUAL_PAGE_PATHS[1:]:
        _run_check(
            failures,
            website,
            f"{path} renders and images load",
            lambda path=path: (
                _open_rendered_page(driver, _localized_url(website, path)),
                _accept_cookie_consent(driver),
                _assert_images_are_loaded(driver),
            ),
        )
        if path == "/facilities":
            _run_check(failures, website, "facilities map renders", lambda: _assert_map_is_rendered(driver))
        if path == "/app":
            _run_check(failures, website, "application links", lambda: _assert_app_links_are_available(driver))

    assert not failures, f"Production website health check failed for {website.name}:\n" + "\n".join(failures)

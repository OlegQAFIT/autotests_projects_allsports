"""Ежечасовые smoke-проверки доступности и ключевых флоу публичных сайтов."""

from collections import deque
from dataclasses import dataclass
from html.parser import HTMLParser
import time
from urllib.parse import urljoin, urlsplit, urlunsplit

import allure
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from conftest import create_chrome


REQUEST_TIMEOUT_SECONDS = 15
REDIRECT_STATUS_CODES = {301, 302, 307, 308}
PAGE_LOAD_TIMEOUT_SECONDS = 15


@dataclass(frozen=True)
class Website:
    name: str
    localized_base_url: str
    route_source_base_url: str | None = None

    @property
    def origin(self) -> str:
        parsed_url = urlsplit(self.localized_base_url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"


WEBSITES = (
    Website(
        "Allsports test",
        "https://xn--80aswg.xn--k1aahcehedi.xn--90ais/ru-by",
    ),
    Website(
        "SportBenefit Cyprus test",
        "https://xn--h1adqe.xn--k1aahcehedi.xn--90ais/en-cy",
    ),
    Website("Allsports production", "https://www.allsports.by/ru-by"),
    Website("SportBenefit Cyprus production", "https://www.sportbenefit.eu/en-cy"),
)

HEALTH_WEBSITES = (
    *WEBSITES,
    Website("SportBenefit Lithuania production", "https://www.sportbenefit.eu/en-lt"),
)

# Для production список опубликованных страниц берётся с соответствующего
# тестового сайта. Поэтому новая страница или новая версия документа попадает
# в проверку автоматически, а production обязан повторить это поведение.
TEST_ALLSPORTS_BY = "https://xn--80aswg.xn--k1aahcehedi.xn--90ais/ru-by"
TEST_SPORTBENEFIT_CY = "https://xn--h1adqe.xn--k1aahcehedi.xn--90ais/en-cy"
TEST_SPORTBENEFIT_LT = "https://xn--h1adqe.xn--k1aahcehedi.xn--90ais/en-lt"

REDIRECT_WEBSITES = (
    Website("Allsports test", TEST_ALLSPORTS_BY, TEST_ALLSPORTS_BY),
    Website("SportBenefit Cyprus test", TEST_SPORTBENEFIT_CY, TEST_SPORTBENEFIT_CY),
    Website("Allsports production", "https://www.allsports.by/ru-by", TEST_ALLSPORTS_BY),
    Website(
        "SportBenefit Cyprus production",
        "https://www.sportbenefit.eu/en-cy",
        TEST_SPORTBENEFIT_CY,
    ),
)

# У домена sportbenefit.eu locale по умолчанию — en-cy. Поэтому путь без
# locale нельзя корректно редиректить в en-lt: Lithuania проверяем прямым
# открытием всех /en-lt/... страниц и переключением locale в UI-smoke.
LITHUANIAN_WEBSITES = (
    Website("SportBenefit Lithuania test", TEST_SPORTBENEFIT_LT, TEST_SPORTBENEFIT_LT),
    Website(
        "SportBenefit Lithuania production",
        "https://www.sportbenefit.eu/en-lt",
        TEST_SPORTBENEFIT_LT,
    ),
)

CRITICAL_PAGE_PATHS = (
    "/", "/facilities", "/facilities-table", "/contacts", "/app",
    "/license", "/user-agreements",
)
HEADER_PAGE_PATHS = ("/", "/facilities", "/levels", "/companies", "/partners", "/contacts")
VISUAL_PAGE_PATHS = ("/", "/facilities", "/app")
ERROR_PAGE_MARKERS = (
    "internal server error", "bad gateway", "gateway timeout", "service unavailable",
    "temporarily unavailable",
)

# Известные legacy/статические пути. Для каждого из них удаление locale
# должно вернуть пользователя на тот же путь с locale. Документы не хардкодим:
# они находятся автоматически на тестовом сайте, потому что их версия меняется.
ROUTES_TO_CHECK = (
    "/",
    "/ru",
    "/facilities",
    "/companies",
    "/contacts",
    "/partners",
    "/rules",
    "/levels",
    "/blog",
    "/app",
    "/processing-personal-data",
    "/providing-payment-service-rules",
    "/license",
    "/user-agreements",
    "/facilities-table",
    "/cookie/cookie-policy",
    # Контрольные catch-all адреса: это не страницы сайта, но они защищают
    # от возврата старого поведения с 404 на несуществующих legacy URL.
    "/some-random-page-123456",
    "/definitely-not-a-real-allsports-route",
)


class _InternalLinkParser(HTMLParser):
    """Собирает href из HTML без дополнительной зависимости BeautifulSoup."""

    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.hrefs.append(href)


def _url_without_locale(website: Website, route: str) -> str:
    return f"{website.origin}{route}"


def _expected_localized_url(website: Website, route: str) -> str:
    suffix = "" if route == "/" else route
    return f"{website.localized_base_url}{suffix}"


def _localized_url(website: Website, path: str) -> str:
    return _expected_localized_url(website, path)


def _normalize_url(url: str) -> str:
    return url.rstrip("/")


def _localized_path(website: Website, url: str) -> str:
    """Возвращает путь страницы относительно locale-префикса, например /policy/123."""
    localized_prefix = urlsplit(website.localized_base_url).path.rstrip("/")
    path = urlsplit(url).path.rstrip("/") or "/"
    if path == localized_prefix:
        return "/"
    return path.removeprefix(localized_prefix)


def _discover_published_localized_paths(
    session: requests.Session,
    website: Website,
) -> tuple[set[str], list[str]]:
    """Рекурсивно обходит опубликованные внутренние ссылки одной locale-версии."""
    parsed_base = urlsplit(website.localized_base_url)
    localized_prefix = parsed_base.path.rstrip("/")
    pending_urls = deque([website.localized_base_url])
    visited_urls: set[str] = set()
    paths: set[str] = set()
    failures: list[str] = []

    while pending_urls and len(visited_urls) < 100:
        current_url = pending_urls.popleft()
        parsed_current = urlsplit(current_url)
        canonical_url = urlunsplit(
            (
                parsed_current.scheme,
                parsed_current.netloc,
                parsed_current.path.rstrip("/") or "/",
                "",
                "",
            )
        )
        if canonical_url in visited_urls:
            continue
        visited_urls.add(canonical_url)

        try:
            response = session.get(
                current_url,
                allow_redirects=False,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as error:
            failures.append(f"{current_url}: {type(error).__name__}: {error}")
            continue

        if response.status_code != 200:
            failures.append(f"{current_url}: expected HTTP 200, got {response.status_code}")
            continue
        if "html" not in response.headers.get("content-type", "").lower():
            failures.append(f"{current_url}: unexpected content type")
            continue

        paths.add(_localized_path(website, current_url))
        parser = _InternalLinkParser()
        parser.feed(response.text)
        for href in parser.hrefs:
            absolute_url = urljoin(current_url, href)
            parsed_link = urlsplit(absolute_url)
            normalized_path = parsed_link.path.rstrip("/") or "/"
            is_same_locale = normalized_path == localized_prefix or normalized_path.startswith(
                f"{localized_prefix}/"
            )
            if (
                parsed_link.scheme not in {"http", "https"}
                or parsed_link.netloc != parsed_base.netloc
                or not is_same_locale
            ):
                continue
            pending_urls.append(
                urlunsplit(
                    (parsed_link.scheme, parsed_link.netloc, normalized_path, "", "")
                )
            )

    if pending_urls:
        failures.append("Reached safety limit of 100 localized pages during link crawl")
    return paths, failures


@pytest.fixture(scope="module")
def published_paths_by_test_locale() -> dict[str, tuple[set[str], list[str]]]:
    """Кэширует маршруты test BY/CY/LT, чтобы production проверял те же данные."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Route-Parity-Monitor/1.0"})
    source_websites = (
        Website("Allsports test source", TEST_ALLSPORTS_BY),
        Website("SportBenefit Cyprus test source", TEST_SPORTBENEFIT_CY),
        Website("SportBenefit Lithuania test source", TEST_SPORTBENEFIT_LT),
    )
    return {
        source.localized_base_url: _discover_published_localized_paths(session, source)
        for source in source_websites
    }


def _assert_http_page_is_available(session: requests.Session, url: str) -> None:
    response = session.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT_SECONDS)
    assert response.status_code == 200, f"HTTP {response.status_code}; final URL: {response.url}"
    assert response.content, "Empty response body"
    assert "html" in response.headers.get("content-type", "").lower(), (
        f"Unexpected content type: {response.headers.get('content-type')!r}"
    )


def _open_rendered_page(driver, url: str) -> None:
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT_SECONDS)
    driver.get(url)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        lambda current_driver: current_driver.execute_script("return document.readyState") == "complete"
    )
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        lambda current_driver: current_driver.find_element(By.TAG_NAME, "body")
    )
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    found_markers = [marker for marker in ERROR_PAGE_MARKERS if marker in body_text]
    assert not found_markers, f"Error page markers found: {found_markers}"


def _assert_header_links(driver, website: Website) -> None:
    hrefs = {
        (link.get_attribute("href") or "").rstrip("/")
        for link in driver.find_elements(By.CSS_SELECTOR, "header a[href]")
    }
    expected_hrefs = {_normalize_url(_localized_url(website, path)) for path in HEADER_PAGE_PATHS}
    missing_hrefs = sorted(expected_hrefs - hrefs)
    assert not missing_hrefs, f"Header links are missing: {missing_hrefs}"


def _assert_images_are_loaded(driver) -> None:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.7)
    broken_images = driver.execute_script(
        "return Array.from(document.images).filter((image) => image.currentSrc && image.complete && image.naturalWidth === 0).map((image) => image.currentSrc);"
    )
    assert not broken_images, f"Broken images: {broken_images}"


def _assert_map_is_rendered(driver) -> None:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.65);")
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT_SECONDS).until(
        lambda current_driver: current_driver.find_elements(
            By.CSS_SELECTOR, "#map .mapboxgl-canvas, .contacts-map .mapboxgl-canvas"
        )
    )


def _assert_app_links_are_available(driver) -> None:
    app_links = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='play.google'], a[href*='apps.apple'], a[href*='appgallery'], a[download]",
    )
    assert app_links, "Application download links are missing"
    assert all(link.get_attribute("href") for link in app_links), "Empty application download link found"


@pytest.fixture(scope="module")
def _website_browser(pytestconfig):
    """Один Chrome только для UI-smoke этого модуля."""
    web_driver = create_chrome(pytestconfig.getoption("--headless"))
    web_driver.implicitly_wait(2)
    yield web_driver
    web_driver.quit()


@pytest.fixture
def driver(request):
    """Не запускает браузер для HTTP-редиректов; UI-проверки используют общий Chrome."""
    if request.node.name.startswith("test_www_hourly_key_functionality_health"):
        return request.getfixturevalue("_website_browser")
    return None


@allure.feature("Public websites")
@allure.story("Redirect to localized URL")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.schedule
@pytest.mark.smoke
@pytest.mark.parametrize("website", REDIRECT_WEBSITES, ids=lambda site: site.name)
def test_www_routes_redirect_to_localized_url(
    website: Website,
    published_paths_by_test_locale: dict[str, tuple[set[str], list[str]]],
) -> None:
    """Проверяет одинаковый redirect-сценарий на test и соответствующем production."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Route-Parity-Monitor/1.0"})
    failures = []
    passed_routes = []
    discovered_paths, discovery_failures = published_paths_by_test_locale[
        website.route_source_base_url or website.localized_base_url
    ]
    routes_to_check = tuple(sorted(set(ROUTES_TO_CHECK) | discovered_paths))

    for failure in discovery_failures:
        failures.append(f"Не удалось собрать опубликованные маршруты: {failure}")

    for route in routes_to_check:
        source_url = _url_without_locale(website, route)
        expected_url = _expected_localized_url(website, route)
        response: requests.Response | None = None

        with allure.step(f"{source_url} redirects to {expected_url}"):
            try:
                response = session.get(
                    source_url,
                    allow_redirects=False,
                    timeout=REQUEST_TIMEOUT_SECONDS,
                )
                assert response.status_code in REDIRECT_STATUS_CODES, (
                    f"HTTP {response.status_code}; expected 301 or 302 redirect"
                )
                location = response.headers.get("location")
                assert location, "Redirect response does not contain Location header"
                actual_target_url = _normalize_url(urljoin(source_url, location))
                assert actual_target_url == _normalize_url(expected_url), (
                    f"Expected redirect target {expected_url}, got {actual_target_url}"
                )
                passed_routes.append(route)
                print(
                    f"ПРОШЕЛ | {website.name} | {route} | "
                    f"{source_url} -> {actual_target_url} | HTTP {response.status_code}"
                )
            except (AssertionError, requests.RequestException) as error:
                failures.append(f"{route}: {error}")
                final_url = response.headers.get("location", "нет ответа") if response is not None else "нет ответа"
                print(
                    f"НЕ ПРОШЕЛ | {website.name} | {route} | "
                    f"{source_url} -> {final_url} | {error}"
                )

    print(
        f"ИТОГ | {website.name} | прошло: {len(passed_routes)} из "
        f"{len(routes_to_check)} | не прошло: {len(failures)}"
    )

    assert not failures, (
        f"Localized redirects failed for {website.name}:\n" + "\n".join(failures)
    )


@allure.feature("Public websites")
@allure.story("Localized pages availability")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.schedule
@pytest.mark.smoke
@pytest.mark.parametrize(
    "website",
    (*REDIRECT_WEBSITES, *LITHUANIAN_WEBSITES),
    ids=lambda site: site.name,
)
def test_www_published_localized_pages_open_directly(
    website: Website,
    published_paths_by_test_locale: dict[str, tuple[set[str], list[str]]],
) -> None:
    """Проверяет, что опубликованные locale URL открываются напрямую с HTTP 200."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Route-Parity-Monitor/1.0"})
    published_paths, discovery_failures = published_paths_by_test_locale[
        website.route_source_base_url or website.localized_base_url
    ]
    failures = list(discovery_failures)

    for path in sorted(published_paths):
        url = _localized_url(website, path)
        try:
            response = session.get(url, allow_redirects=False, timeout=REQUEST_TIMEOUT_SECONDS)
            assert response.status_code == 200, f"HTTP {response.status_code}"
            print(f"ПРОШЕЛ | {website.name} | прямое открытие {path} | HTTP 200")
        except (AssertionError, requests.RequestException) as error:
            failures.append(f"{path}: {error}")
            print(f"НЕ ПРОШЕЛ | {website.name} | прямое открытие {path} | {error}")

    print(
        f"ИТОГ DIRECT | {website.name} | проверено: {len(published_paths)} | "
        f"не прошло: {len(failures)}"
    )
    assert not failures, "Localized pages are unavailable:\n" + "\n".join(failures)


def _accept_cookie_consent(driver) -> None:
    for selector in (
        ".cookie-primary-modal__confirm",
        "button[aria-label*='Accept']",
        "button[aria-label*='Confirm']",
    ):
        for button in driver.find_elements(By.CSS_SELECTOR, selector):
            if button.is_displayed() and button.is_enabled():
                driver.execute_script("arguments[0].click();", button)
                return


def _run_check(failures: list[str], website: Website, check_name: str, callback) -> None:
    try:
        callback()
        print(f"ПРОШЕЛ | {website.name} | {check_name}")
    except Exception as error:
        failures.append(f"{check_name}: {type(error).__name__}: {error}")
        print(f"НЕ ПРОШЕЛ | {website.name} | {check_name} | {error}")


@allure.feature("Public websites")
@allure.story("Hourly website health check")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.schedule
@pytest.mark.smoke
@pytest.mark.parametrize("website", HEALTH_WEBSITES, ids=lambda site: site.name)
def test_www_hourly_key_functionality_health(driver, website: Website) -> None:
    """Быстрая проверка доступности и ключевых элементов без отправки форм."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Allsports-Website-Health-Monitor/1.0"})
    failures: list[str] = []

    for path in CRITICAL_PAGE_PATHS:
        url = _localized_url(website, path)
        _run_check(
            failures,
            website,
            f"HTTP 200 {path}",
            lambda url=url: _assert_http_page_is_available(session, url),
        )

    homepage_url = _localized_url(website, "/")
    _run_check(
        failures,
        website,
        "главная страница рендерится",
        lambda: _open_rendered_page(driver, homepage_url),
    )
    _accept_cookie_consent(driver)
    _run_check(failures, website, "header содержит ключевые ссылки", lambda: _assert_header_links(driver, website))
    _run_check(failures, website, "изображения главной загружены", lambda: _assert_images_are_loaded(driver))

    for path in VISUAL_PAGE_PATHS[1:]:
        url = _localized_url(website, path)
        _run_check(
            failures,
            website,
            f"{path} рендерится и изображения загружены",
            lambda url=url: (_open_rendered_page(driver, url), _accept_cookie_consent(driver), _assert_images_are_loaded(driver)),
        )

        if path == "/facilities":
            _run_check(failures, website, f"карта на {path} отображается", lambda: _assert_map_is_rendered(driver))
        if path == "/app":
            _run_check(failures, website, "ссылки на приложение доступны", lambda: _assert_app_links_are_available(driver))

    print(f"ИТОГ HEALTH | {website.name} | прошло: проверяйте строки выше | не прошло: {len(failures)}")
    assert not failures, f"Website health check failed for {website.name}:\n" + "\n".join(failures)

import os
from urllib.parse import urlparse, urlunparse

import pytest
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOption
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOption
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from helpers.base import BasePage


def pytest_addoption(parser):
    parser.addoption(
        '--headless',
        action='store_true',
        default=False,
        help='run browsers in headless mode',
    )
    parser.addoption(
        '--b',
        default='chrome',
        help='browser: chrome | ff | edge',
    )
    parser.addoption(
        '--base-url',
        default=os.getenv('BASE_URL', 'https://www.allsports.by/ru-by'),
        help='base URL for UI tests, e.g. https://staging.example.com/ru-by',
    )
    parser.addoption(
        '--live-api',
        action='store_true',
        default=False,
        help='enable real API POST checks (disabled by default)',
    )


def _rewrite_url(url: str, base_url: str) -> str:
    parsed_target = urlparse(url)
    parsed_base = urlparse(base_url)
    if parsed_target.scheme and parsed_target.netloc:
        return urlunparse(
            (
                parsed_base.scheme,
                parsed_base.netloc,
                parsed_target.path,
                parsed_target.params,
                parsed_target.query,
                parsed_target.fragment,
            )
        )
    if url.startswith('/'):
        return f"{base_url}{url}"
    return url


def _patch_driver_get(web_driver, base_url: str):
    original_get = web_driver.get

    def _wrapped_get(url):
        return original_get(_rewrite_url(url, base_url))

    web_driver.get = _wrapped_get


def _patch_http_requests(base_url: str, live_api: bool):
    original_get = requests.get
    original_post = requests.post

    def _wrapped_get(url, *args, **kwargs):
        return original_get(_rewrite_url(url, base_url), *args, **kwargs)

    def _wrapped_post(url, *args, **kwargs):
        if not live_api:
            pytest.skip('Live API checks are disabled. Use --live-api to enable real POST checks.')
        return original_post(_rewrite_url(url, base_url), *args, **kwargs)

    requests.get = _wrapped_get
    requests.post = _wrapped_post
    return original_get, original_post


def _patch_base_assertions():
    def _strict_assert_element_not_present(self, locator, timeout=3):
        if isinstance(locator, tuple):
            by, value = locator
        else:
            by, value = By.XPATH, locator

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            return

        raise AssertionError(f'Элемент {locator} присутствует на странице')

    BasePage.assert_element_not_present = _strict_assert_element_not_present


def create_chrome(headless: bool = False):
    chrome_options = ChromeOption()
    if headless:
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('window-size=1900x1600')

    chrome_options.add_argument('--disable-notifications')
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def create_firefox(headless: bool = False):
    firefox_options = FirefoxOption()
    if headless:
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--width=1900')
        firefox_options.add_argument('--height=1600')

    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=firefox_options)


def create_edge(headless: bool = False):
    edge_option = EdgeOption()
    if headless:
        edge_option.add_argument('--headless')
        edge_option.add_argument('window-size=1900x1600')

    return webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager().install()),
        options=edge_option,
    )


@pytest.fixture(autouse=True)
def driver(request):
    browser = request.config.getoption('--b')
    headless = request.config.getoption('--headless')
    base_url = request.config.getoption('--base-url').rstrip('/')
    live_api = request.config.getoption('--live-api')

    if browser == 'chrome':
        web_driver = create_chrome(headless)
    elif browser == 'ff':
        web_driver = create_firefox(headless)
    elif browser == 'edge':
        web_driver = create_edge(headless)
    else:
        raise ValueError(f'Unsupported browser: {browser}')

    web_driver.base_url = base_url
    web_driver.live_api = live_api
    _patch_driver_get(web_driver, base_url)
    _patch_base_assertions()
    original_get, original_post = _patch_http_requests(base_url, live_api)

    try:
        web_driver.implicitly_wait(5)
        web_driver.maximize_window()
        yield web_driver
    finally:
        requests.get = original_get
        requests.post = original_post
        web_driver.quit()

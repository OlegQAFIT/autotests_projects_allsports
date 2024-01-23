from selenium.webdriver.edge.options import Options as EdgeOption
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOption
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService


def pytest_addoption(parser):
    parser.addoption('--headless',
                     default='False',
                     help='headless options: "yes" or "no"')
    parser.addoption('--b',
                     default='chrome',
                     help='option to define type of browser')


def create_chrome(headless=True):
    chrome_option = ChromeOption()
    if headless == 'True':
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('window-size=1900x1600')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_option)
    return driver


def create_firefox(headless=True):
    ff_option = FirefoxOption()
    if headless == 'True':
        ff_option.add_argument('--headless')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=ff_option)
    return driver


def create_edge(headless=True):
    edge_option = EdgeOption()
    if headless == 'True':
        edge_option.add_argument('--headless')
        edge_option.add_argument('window-size=1900x1600')
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_option)
    return driver


# def create_opera(headless=True):
#     opera_option = OperaOption()
#     if headless == 'True':
#         opera_option.add_argument('--headless')
#         opera_option.add_argument('window-size=1900x1600')
#     driver = webdriver.Opera(service=OperaService(OperaDriverManager().install()), options=opera_option)
#     return driver


@pytest.fixture(autouse=True)
def driver(request):
    driver = None
    browser = request.config.getoption('--b')
    headless = request.config.getoption('--headless')

    if browser == 'chrome':
        driver = create_chrome(headless)
    elif browser == 'ff':
        driver = create_firefox(headless)
    elif browser == 'edge':
        driver = create_edge(headless)
    # elif browser == 'opera':
    #     driver = create_opera(headless)

    driver.implicitly_wait(5)
    driver.maximize_window()

    yield driver
    driver.quit()

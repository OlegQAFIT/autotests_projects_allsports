from selenium.webdriver.edge.options import Options as EdgeOption
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
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
    chrome_options = ChromeOption()
    if headless == 'True':
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=1900x1600')
    chrome_options.add_argument('--disable-notifications')  # Отключить уведомления

    # Указание пути к уже установленному драйверу
    driver_path = "C:/Users/test/.wdm/drivers/chromedriver/win64/126.0.6478.182/chromedriver-win32/chromedriver.exe"
    driver = webdriver.Chrome(service=ChromeService(driver_path), options=chrome_options)
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

    driver.implicitly_wait(5)
    driver.maximize_window()

    yield driver
    driver.quit()
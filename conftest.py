import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOption
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOption
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def pytest_addoption(parser):
    parser.addoption('--headless',
                     default='False',
                     help='headless options: "True" or "False"')
    parser.addoption('--b',
                     default='chrome',
                     help='option to define type of browser')


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def create_chrome(headless=True):
    chrome_options = ChromeOption()
    if headless == 'True':
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('window-size=1900x1600')

    chrome_options.add_argument('--disable-notifications')

    # ✅ Современный способ добавить capabilities
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
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
    browser = request.config.getoption('--b')
    headless = request.config.getoption('--headless')

    if browser == 'chrome':
        driver = create_chrome(headless)
    elif browser == 'ff':
        driver = create_firefox(headless)
    elif browser == 'edge':
        driver = create_edge(headless)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.quit()
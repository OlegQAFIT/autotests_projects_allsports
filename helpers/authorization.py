import allure
from helpers import BasePage

class LoginLocators:
    LOGIN_FIELD = "//input[@id='email']"
    PASSWORD_FIELD = "//input[@id='password']"
    SIGNIN_BUTTON = "//button[text()='Signin']"

    LOGIN_TEXT = "oleg.fit@gmail.com"
    PASSWORD_TEXT = "9efbee942864"



    LOGIN_FIELD_SUPPLER_PANEL = "//div[@class='input-container']/input[@type='text']"
    PASSWORD_FIELD_SUPPLER_PANEL = "//div[@class='input-container']/input[@type='password']"
    SIGNIN_BUTTON_SUPPLER_PANEL = "//button[contains(@class, 'btn__primary') and contains(@class, 'btn-base') and contains(@class, 'w-50')]"

    LOGIN_TEXT_SUPPLER_PANEL = "test@allsports.by"
    PASSWORD_TEXT_SUPPLER_PANEL = "secret"

    ALLOW_NOTIFICATIONS_BUTTON = "//div[@class='btn-content_slot' and text()='Запросить разрешения']"


class LoginPage(BasePage, LoginLocators):

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Login with credentials")
    def login(self):
        self.fill(self.LOGIN_FIELD, self.LOGIN_TEXT)
        self.fill(self.PASSWORD_FIELD, self.PASSWORD_TEXT)
        self.hard_click(self.SIGNIN_BUTTON)


class LoginPageSupplierPanel(BasePage, LoginLocators):

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Login with credentials")
    def login_supplier_panel(self):
        self.fill(self.LOGIN_FIELD_SUPPLER_PANEL, self.LOGIN_TEXT_SUPPLER_PANEL)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)
        self.fill(self.PASSWORD_FIELD_SUPPLER_PANEL, self.PASSWORD_TEXT_SUPPLER_PANEL)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)


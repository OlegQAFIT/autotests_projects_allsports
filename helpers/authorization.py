import allure
from helpers import BasePage

class LoginLocators:
    LOGIN_FIELD = "//input[@id='email']"
    PASSWORD_FIELD = "//input[@id='password']"
    SIGNIN_BUTTON = "//button[text()='Signin']"

    LOGIN_TEXT = "alex@allsports.by"
    PASSWORD_TEXT = "30ba637a-b76c-4155-9da4-09204af0ce79"


class LoginPage(BasePage, LoginLocators):

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Login with credentials")
    def login(self):
        self.fill(self.LOGIN_FIELD, self.LOGIN_TEXT)
        self.fill(self.PASSWORD_FIELD, self.PASSWORD_TEXT)
        self.hard_click(self.SIGNIN_BUTTON)
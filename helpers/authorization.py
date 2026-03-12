import allure
from helpers import BasePage
from helpers.supplier_panel_data import get_role_credentials

class LoginLocators:
    LOGIN_FIELD = "//input[@id='email']"
    PASSWORD_FIELD = "//input[@id='password']"
    SIGNIN_BUTTON = "//button[text()='Signin']"

    LOGIN_TEXT = "auttest@gmail.com"
    PASSWORD_TEXT = "secret"



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

    def _remove_notification_modal_if_present(self):
        self.driver.execute_script(
            "const m=document.querySelector('.modal-container'); if (m) m.remove();"
        )

    @allure.step("Login with credentials")
    def login_supplier_panel(self, role="reception", login=None, password=None):
        if login is None or password is None:
            role_login, role_password = get_role_credentials(role)
            login = login or role_login
            password = password or role_password

        self._remove_notification_modal_if_present()
        self.fill(self.LOGIN_FIELD_SUPPLER_PANEL, login)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)
        self.fill(self.PASSWORD_FIELD_SUPPLER_PANEL, password)
        self.hard_click(self.SIGNIN_BUTTON_SUPPLER_PANEL)

    def login_supplier_panel_reception(self):
        self.login_supplier_panel(role="reception")

    def login_supplier_panel_finance(self):
        self.login_supplier_panel(role="finance")

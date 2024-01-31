class LoginPageLocators():
    CONTACT_NUMBER = "//a[@href='tel:375291294950' and contains(@class, 'header-support_phone')]"

    FORGET_PASSWORD_BUTTON = "//a[@class='col-12 pb-4 link link_additional' and @href='#']"

    LOGO = "//div[@class='header-logo']"

    LOG_IN = "//a[@href='/login' and @aria-current='page']"
    CONTACTS = "//a[@class='nav_link' and @href='/contacts']"

    TEXT_LOGIN = "//div[@class='header-title_text']"

    CHANGE_LANGUAGE_DROPDOWN = "//select[@class='language-switcher_list']"
    DROPDOWN_LANGUAGE_EN = "//div[@class='language-switcher']//span[text()='en']"
    DROPDOWN_LANGUAGE_RU = "//select[@class='language-switcher_list']/option[@value='ru']"

    SIGNIN_BUTTON_SUPPLER_PANEL = "//button[contains(@class, 'btn__primary') and contains(@class, 'btn-base') and contains(@class, 'w-50')]"

    LOGIN_TEXT_SUPPLER_PANEL = "test@allsports.by"
    WRONG_LOGIN_TEXT_SUPPLER_PANEL = "atrohov199206@gmail.com"
    WRONG_PASSWORD_TEXT_SUPPLER_PANEL = "secret"
    WRONG_PASSWORD_FORMAT_TEXT_SUPPLER_PANEL = "secret12"
    LOCATOR_TEXT_ERRORE_WRONG_EMAIL = "//p[text()='Выбранное значение для email не найдено в списке.']"
    LOCATOR_TEXT_ERRORE_WRONG_PASSWORD = "//p[@class='info-banner_message' and text()='Неверный пароль']"
    LOCATOR_TEXT_ERRORE_WRONG_PASSWORD_EN = "//p[@class='info-banner_message' and text()='Invalid password']"

    LOCATOR_TEXT_ERRORE_WRONG_USER = "//p[@data-v-fe06182b and contains(@class, 'info-banner_message')]"
    LOCATOR_TEXT_ERRORE_WRONG_PASSWORD = "//p[@class='info-banner_message' and text()='Неверный пароль']"



    WRONG_TEXT_SUPPLER_PANEL = "test@allsports@gmail.com"
    LOCATOR_TEXT_ERRORE_WRONG_FORMAT = "//span[@class='input_error' and @title='Check that the entered data is correct.']"

    LOCATOR_TEXT_ERRORE_WRONG_FORMAT_EN = "//span[@class='input_error' and @title='Check that the entered data is correct.']"
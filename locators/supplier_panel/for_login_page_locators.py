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
    NOTIFICATION_MODAL_TITLE_RU = "//h2[text()='Пожалуйста, предоставьте доступ для отправки уведомлений.']"
    NOTIFICATION_MODAL_TITLE_EN = "//h2[text()='Please, provide access for sending notifications.']"
    ALLOW_NOTIFICATIONS_BUTTON_RU = "//button[normalize-space()='Запросить разрешения']"
    ALLOW_NOTIFICATIONS_BUTTON_EN = "//button[normalize-space()='Request permissions']"

    SIGNIN_BUTTON_SUPPLER_PANEL = "//button[contains(@class, 'btn__primary') and contains(@class, 'btn-base') and contains(@class, 'w-50')]"

    WRONG_LOGIN_TEXT_SUPPLER_PANEL = "atrohov199206@gmail.com"
    WRONG_PASSWORD_TEXT_SUPPLER_PANEL = "secret"
    WRONG_PASSWORD_FORMAT_TEXT_SUPPLER_PANEL = "secret12"
    LOCATOR_TEXT_ERRORE_WRONG_EMAIL = "//p[text()='Выбранное значение для email не найдено в списке.']"
    LOCATOR_TEXT_ERRORE_WRONG_PASSWORD = (
        "//*[contains(@class,'info-banner_message') and "
        "(contains(normalize-space(),'Неверный пароль') or contains(normalize-space(),'Invalid password'))]"
    )
    LOCATOR_TEXT_ERRORE_WRONG_PASSWORD_EN = LOCATOR_TEXT_ERRORE_WRONG_PASSWORD

    LOCATOR_TEXT_ERRORE_WRONG_USER = "//p[@data-v-fe06182b and contains(@class, 'info-banner_message')]"
    WRONG_TEXT_SUPPLER_PANEL = "test@allsports@gmail.com"
    LOCATOR_TEXT_ERRORE_WRONG_FORMAT = "//span[@class='input_error' and @title='Check that the entered data is correct.']"

    LOCATOR_TEXT_ERRORE_WRONG_FORMAT_EN = "//span[@class='input_error' and @title='Check that the entered data is correct.']"

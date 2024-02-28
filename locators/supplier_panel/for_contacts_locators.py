class ContactsLocators():
    # Sidebar история визитов вкладка
    FACILITY_DETAILS_RU = "//a[text()='Контакты']"
    FACILITY_DETAILS_EN = "//a[text()='Contacts']"
    LANGUAGE_DROPDOWN_LOCATOR = "//select[@class='language-switcher_list']"

    # Заголовки
    HEADER_CONTACTS_LOCATOR_RU = "//div[@class='header-title_text'][text()='Контакты']"
    HEADER_CONTACTS_LOCATOR_EN = "//div[@class='header-title_text'][text()='Contacts']"

    # Названия блоков
    PHONE_LOCATOR_RU = "//h3[text()='Телефон']"
    PHONE_LOCATOR_EN = "//h3[text()='Phone']"
    EMAIL_LOCATOR_RU = "//h3[text()='Электронная почта']"
    EMAIL_LOCATOR_EN = "//h3[text()='E-mail']"
    HOURS_LOCATOR_RU = "//h3[text()='Режим работы']"
    HOURS_LOCATOR_EN = "//h3[text()='Support availability hours']"

    # Текст блоков
    TEXT_PHONE_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div/div[2]/div[1]/a'
    TEXT2_PHONE_LOCATOR = '//*[@id="app"]/div/div/main/div[1]/header/div[2]/a'
    TEXT_EMAIL_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div/div[2]/div[2]/a'
    TEXT_HOURS_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div/div[2]/div[3]'

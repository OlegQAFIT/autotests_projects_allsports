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
    TEXT_PHONE_LOCATOR = "//h3[text()='Телефон' or text()='Phone']/following-sibling::a[1]"
    TEXT2_PHONE_LOCATOR = "(//a[contains(@class,'header-support_phone')])[1]"
    TEXT_EMAIL_LOCATOR = "//h3[text()='Электронная почта' or text()='E-mail']/following-sibling::a[1]"
    TEXT_HOURS_LOCATOR = "//h3[text()='Режим работы' or text()='Support availability hours']/following-sibling::*[1]"

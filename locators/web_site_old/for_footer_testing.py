class FooterLocators():
    CONTACT_NUMBER = '//*[@href="tel:+375-44-525-38-92"]'
    CONTACT_EMAIL = '//*[@href="mailto:contact@allsports.by"]'
    INSTAGRAM = '//a[@href="https://www.instagram.com/allsports.fit/"]'
    LINKEDIN = '//a[@href="https://www.linkedin.com/company/allsportsby"]'
    BUTTON_EMPLOYEE = '//ul[@class="links"]/li[1]/a'
    BUTTON_FOR_PARTNERS = '//li/a[text()="Партнерам"]'
    BUTTON_CONTACTS = '//ul[@class="links"]/li[5]/a'
    BUTTON_DOCUMENTS_FOR_LEGAL_ENTITIES = '//li/a[text()="Документы для юр.лиц"]'
    BUTTON_COMPANY = '//li/a[text()="Компаниям"]'
    BUTTON_OBJECTS = '//ul[@class="links"]/li[4]/a'
    BUTTON_BLOG = '//li/a[text()="Блог"]'
    USER_AGREEMENTS = '//li/a[text()="Пользовательские соглашения"]'
    SUBSCRIPTION_TYPES = '//h1[text()="Типы подписки"]'
    FOUND_ELEMENTS_DELETE = '//button[@class="reset" and @title="Очистить фильтр"]'
    PARTNER = "//h3[text()='Что Allsports дает вашему фитнес-клубу?']"
    ELEMENT_IN_BLOG_PAGE = '//div[h1[text()="Оллспортс Статьи"]]/article'
    ACT_RESULT = '//div/div/main/section[1]/p[7]/a'
    COMPANIES_PAGE = '//h1[@class="top_title"]'
    DOCUMENTS_FOR_LEGAL_ENTITIES = "//a[contains(text(), 'Документы для юр.лиц')]"
    EXPECTED_RESULT_TEXT = '+375 (44) 502-36-13'
    FILE_NAME = "Индивидуальные лицензии"
    PHONE_NUMBER = '+375 (44) 525-38-92'
    EXPECTED_ALERT_TEXT = "Открыть приложение 'Выбор приложения'"

    READ_FILE_1 = "//div[@class='license'][1]//a[text()='Читать документ']"
    READ_FILE_2 = "//div[@class='license'][2]//a[text()='Читать документ']"
    READ_FILE_3 = "//div[@class='license'][3]//a[text()='Читать документ']"
    ELEMENT_IN_LICENSES_DOC = "//h1[text()='ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ держателей Карт Allsports']"
    ELEMENT_IN_PERSONAL_INFORMATION = "//h2[text()='Политика в отношении обработки персональных данных']"

    ELEMENT_IN_PERSONAL_INFORMATION_DOC_FOR_TEXT = "//h2[text()='Политика в отношении обработки персональных данных']"
    TEXT = "Политика в отношении обработки персональных данных"

    CHECK_DATE = "//small[text()='18.02.2022']"
    TEXT_DATE = "18.02.2022"

    DATE_2 = "//a[contains(@href, '220127_processing_personal_data')]"
    CHECK_DATE_2 = "//small[text()='27.01.2022']"
    TEXT_DATE_2 = "27.01.2022"

    DATE_3 = "//a[contains(@href, '211115_policy')]"
    CHECK_DATE_3 = "//small[text()='15.11.2021']"
    TEXT_DATE_3 = "15.11.2021"

    ELEMENT_IN_ACCESS_RULES = '//h1[text()="Правила доступа в спортивные объекты с помощью Электронной платформы Allsports"]'

    READ_FILE_ACCESS_RULES_1 = "//div[@class='license'][1]//a[text()='Читать документ']"
    READ_FILE_ACCESS_RULES_2 = "//div[@class='license'][2]//a[text()='Читать документ']"

    DOCUMENTS_FOR_LEGAL = "//a[contains(text(), 'Документы для юр.лиц')]"

    DATE_ACCESS_2 = "//a[contains(@href, '220127_processing_personal_data')]"
    DATE_ACCESS_3 = "//a[contains(@href, '211115_policy')]"

    ELEMENT_IN_ACCESS_RULES_2 = "//h2[text()='Документы для юридических лиц']"
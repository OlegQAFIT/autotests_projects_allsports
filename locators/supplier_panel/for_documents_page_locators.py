class DocumentsPageLocators:
    DOCUMENTS_TAB_RU = "//a[@href='/documents' and contains(@class, 'nav_link') and normalize-space()='Документы']"
    DOCUMENTS_TAB_EN = "//a[@href='/documents' and contains(@class, 'nav_link') and normalize-space()='Documents']"

    HEADER_RU = "//div[@class='header-title_text' and normalize-space()='Документы']"
    HEADER_EN = "//div[@class='header-title_text' and normalize-space()='Documents']"

    DATE_LABEL_RU = "//span[@class='datepicker_label' and normalize-space()='Дата:']"
    DATE_LABEL_EN = "//span[@class='datepicker_label' and normalize-space()='Date:']"
    DATE_INPUT = "//input[contains(@class, 'dp__input')]"

    FOR_ALL_TIME_BUTTON_RU = "//button[normalize-space()='За всё время' or .//*[normalize-space()='За всё время']]"
    FOR_ALL_TIME_BUTTON_EN = "//button[normalize-space()='For all time' or .//*[normalize-space()='For all time']]"

    TABLE_HEADER_NUMBER = "//table//thead//td[normalize-space()='№']"
    TABLE_HEADER_SUPPLIER_RU = "//table//thead//td[normalize-space()='Поставщик']"
    TABLE_HEADER_SUPPLIER_EN = "//table//thead//td[normalize-space()='Supplier']"
    TABLE_HEADER_NAME_RU = "//table//thead//td[normalize-space()='ФИО']"
    TABLE_HEADER_NAME_EN = "//table//thead//td[normalize-space()='Name']"
    TABLE_HEADER_FROM_RU = "//table//thead//td[normalize-space()='Начало периода']"
    TABLE_HEADER_FROM_EN = "//table//thead//td[normalize-space()='From']"
    TABLE_HEADER_TILL_RU = "//table//thead//td[normalize-space()='Конец периода']"
    TABLE_HEADER_TILL_EN = "//table//thead//td[normalize-space()='Till']"
    TABLE_HEADER_CREATED_RU = "//table//thead//td[normalize-space()='Дата создания']"
    TABLE_HEADER_CREATED_EN = "//table//thead//td[normalize-space()='Created']"

    TABLE_ROWS = "//table//tbody//tr"

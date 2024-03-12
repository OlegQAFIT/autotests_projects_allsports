class VisitUnderCorrectionLocators():
    # Sidebar история визитов вкладка
    VISITS_UNDER_CORRECTION_RU = '//a[@href="/visits/corrections" and @class="nav_link"]'
    LANGUAGE_DROPDOWN_LOCATOR = "//select[@class='language-switcher_list']"

    # Header нформация
    VISITS_UNDER_CORRECTION_TEXT_LOCATOR_EN = "//div[@class='header-title_text' and text()='Visits under correction']"
    VISITS_UNDER_CORRECTION_TEXT_LOCATOR_RU = "//div[@class='header-title_text' and text()='Визиты на исправлении']"

    # Календарь
    DATE_NAME_TEXT_CALENDAR_LOCATOR_RU = '//span[@class="datepicker_label" and text()="Дата:"]'
    DATE_NAME_TEXT_CALENDAR_LOCATOR_EN = "//span[@class='datepicker_label' and text()='Date:']"
    CALENDAR_BUTTON_LOCATOR = "//div[@class='dp__input_wrap']"

    # Период
    PERIOD_NAME_TEXT_LOCATOR_RU = '//span[text()="Период:"]'
    PERIOD_NAME_TEXT_LOCATOR_EN = '//span[text()="Period:"]'
    PERIOD_BUTTON_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/label/div[2]'
    PERIOD_MONTH_LOCATOR_EN = "//p[@class='select_option selected']/span[@title='Month']"
    PERIOD_MONTH_LOCATOR_RU = "//p[@class='select_option selected']/span[@title='Месяц']"
    PERIOD_WEEK_LOCATOR_EN = "//p[@class='select_option']/span[@title='Week']"
    PERIOD_WEEK_LOCATOR_RU = "//p[@class='select_option']/span[@title='Неделя']"
    PERIOD_DAY_LOCATOR_EN = "//p[@class='select_option']/span[@title='Day']"
    PERIOD_DAY_LOCATOR_RU = "//p[@class='select_option']/span[@title='День']"
    PERIOD_INTERVAL_LOCATOR_EN = "//p[@class='select_option']/span[@title='Interval']"
    PERIOD_INTERVAL_LOCATOR_RU = "//p[@class='select_option']/span[@title='Интервал']"

    PERIOD_EN = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/label/div[2]/div[1]'
    PERIOD_RU = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/label/div[2]/div[1]'

    # Таблица
    DATE_RU = "//a[contains(text(), 'Дата ')]"
    DATE_EN = "//a[contains(text(), 'Date')]"
    NUMBER_RU = '//*[@id="app"]/div/div/main/div[2]/div/div[2]/div/div/table/thead/tr/td[2]'
    NUMBER_EN = '//*[@id="app"]/div/div/main/div[2]/div/div[2]/div/div/table/thead/tr/td[2]'
    VISIT_INFO_RU = "//td[div[contains(@class, 'cell-content-wrapper') and contains(span, 'Данные визита ')]]"
    VISIT_INFO_EN = "//td[div[contains(@class, 'cell-content-wrapper') and contains(span, 'Visit info')]]"
    CORRECTION_REQUEST_RU = "//td[div[contains(@class, 'cell-content-wrapper') and contains(span, 'Запрос на корректировку ')]]"
    CORRECTION_REQUEST_EN = "//td[div[contains(@class, 'cell-content-wrapper') and contains(span, 'Correction request')]]"
    DECISION_RU = "//td[div[contains(@class, 'cell-content-wrapper') and contains(a, 'Решение ')]]"
    DECISION_EN = "//td[div[contains(@class, 'cell-content-wrapper') and contains(a, 'Decision')]]"

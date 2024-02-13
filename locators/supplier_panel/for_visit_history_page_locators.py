class VisitHistoryLocators():

    # Sidebar история визитов вкладка
    VISIT_HISTORY_RU = "//a[@href='/visits/all' and contains(@class, 'nav_link')]"
    VISIT_HISTORY_EN = "//a[@href='/visits/all' and @class='nav_link' and @previewlistener='true']"
    LANGUAGE_DROPDOWN_LOCATOR = "//select[@class='language-switcher_list']"

    # Header нформация
    VISIT_HISTORY_TEXT_LOCATOR_RU = '//div[@class="header-title_text" and text()="История визитов"]'
    VISIT_HISTORY_TEXT_LOCATOR_EN = '//div[@class="header-title_text" and text()="Visit history"]'
    TOTAL_VISITS_TEXT_LOCATOR_RU = '//h3[@class="d-none d-sm-block" and text()="Всего посещений:"]'
    TOTAL_VISITS_TEXT_LOCATOR_EN = '//h3[@class="d-none d-sm-block" and text()="Total visits:"]'
    TOTAL_SUMMERY_VISITS_LOCATOR = "//span[@class='total-visits_number ms-2']"
    TOTAL_PRICE_TEXT_LOCATOR_RU = '//h3[@class="d-none d-sm-block" and text()="Общая стоимость:"]'
    TOTAL_PRICE_TEXT_LOCATOR_EN = '//h3[@class="d-none d-sm-block" and text()="Total price:"]'

    # Календарь
    DATE_NAME_TEXT_CALENDAR_LOCATOR_RU = '//span[@class="datepicker_label" and text()="Дата:"]'
    DATE_NAME_TEXT_CALENDAR_LOCATOR_EN = '//span[@class="datepicker_label" and text()="Date:"]'
    CALENDAR_BUTTON_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div'

    # Период
    PERIOD_NAME_TEXT_LOCATOR_RU = '//span[text()="Период:"]'
    PERIOD_NAME_TEXT_LOCATOR_EN = '//span[text()="Period:"]'
    PERIOD_BUTTON_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/div[2]/label/div[2]/div[1]'
    PERIOD_MONTH_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/div[2]/label/div[2]/div[2]/p[1]'
    PERIOD_WEEK_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/div[2]/label/div[2]/div[2]/p[2]'
    PERIOD_DAY_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div[1]/div[2]/div[2]/label/div[2]/div[2]/p[3]'


    # Визиты
    ALL_VISITS_BUTTON_RU = "//a[@id='Все']"
    ALL_VISITS_BUTTON_EN = "//a[@id='all']"
    ACCEPTED_VISITS_BUTTON_RU = "//a[@id='Принятые']"
    ACCEPTED_VISITS_BUTTON_EN = "//a[@id='accepted']"
    DECLINED_VISITS_BUTTON_RU = "//a[@id='Отклоненные']"
    DECLINED_VISITS_BUTTON_EN = "//a[@id='declined']"
    TIMEOUT_VISITS_BUTTON_RU = "//a[@id='Тайм-аут']"
    TIMEOUT_VISITS_BUTTON_EN = "//a[@id='timeout']"

    # Модалка корректирования визита
    EDIT_BUTTON_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div[3]/div/div/table/tbody/tr[1]/td[6]/svg'

    DATE_TEXT_MODAL_RU = "//p[@class='item_title'][text()='Дата:']"
    DATE_TEXT_MODAL_EN = "//p[@class='item_title'][text()='Date:']"
    ATTRACTION_TEXT_MODAL_RU = "//p[@class='item_title'][text()='Услуга:']"
    ATTRACTION_TEXT_MODAL_EN = "//p[@class='item_title'][text()='Attraction:']"
    STATUS_TEXT_MODAL_RU = "//p[@class='item_title'][text()='Статус:']"
    STATUS_TEXT_MODAL_EN = "//p[@class='item_title'][text()='Status:']"
    CORRECTION_REASON_TEXT_MODAL_RU = "//p[@class='item_title'][text()='Причина корректировки:']"
    CORRECTION_REASON_TEXT_MODAL_EN = "//p[@class='item_title'][text()='Correction reason:']"
    TEXT_FOR_CORRECTION_REASON = "ОШИБКА"
    CEMPOYEE_REASON_TEXT_MODAL_RU = "//p[@class='item_title'][text()='Сотрудник']"
    CEMPOYEE_REASON_TEXT_MODAL_EN = "//p[@class='item_title'][text()='Employee:']"

    CANCEL_BUTTON_MODAL_LOCATOR_RU = "//button[contains(@class, 'btn') and contains(@class, 'btn__primary') and contains(@class, 'btn-outline')]//div[@class='btn-content_slot' and text()='Отменить']"
    CANCEL_BUTTON_MODAL_LOCATOR_EN = "//button[contains(@class, 'btn') and contains(@class, 'btn__primary') and contains(@class, 'btn-outline')]//div[@class='btn-content_slot' and text()='Cancel']"
    CORRECT_VISIT_BUTTON_MODAL_LOCATOR_RU = "//button[contains(@class, 'btn') and contains(@class, 'btn__primary') and contains(@class, 'btn-base')]//div[@class='btn-content_slot' and text()='Исправить']"
    CORRECT_VISIT_BUTTON_MODAL_LOCATOR_EN = "//button[contains(@class, 'btn') and contains(@class, 'btn__primary') and contains(@class, 'btn-base')]//div[@class='btn-content_slot' and text()='Correct visit']"

    SELECT_STATUS_MODAL_LOCATOR_RU = "//p[@class='item_title' and text()='Статус:']/following-sibling::label[contains(@class, 'inline_select')]/p/select"
    SELECT_STATUS_MODAL_LOCATOR_EN = "//p[@class='item_title' and text()='Status:']/following-sibling::label[contains(@class, 'inline_select')]/p/select"
    ACCEPTED_SELECT = '//*[@id="modal-container"]/form/div[2]/label[2]/label/p/select/option[1]'
    DECLINED_SELECT = '//*[@id="modal-container"]/form/div[2]/label[2]/label/p/select/option[2]'
    TIMEOUT_SELECT = '//*[@id="modal-container"]/form/div[2]/label[2]/label/p/select/option[3]'



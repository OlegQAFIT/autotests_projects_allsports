class FacilityDetailsLocators():
    # Sidebar история визитов вкладка
    FACILITY_DETAILS_RU = "//a[text()='Описание обьекта']"
    FACILITY_DETAILS_EN = "//a[text()='Facility details']"
    LANGUAGE_DROPDOWN_LOCATOR = "//select[@class='language-switcher_list']"

    # Заголовки
    HEADER_FACILITY_DETAILS_LOCATOR_EN = "//div[@class='header-title_text' and text()='Facility details']"
    HEADER_FACILITY_DETAILS_LOCATOR_RU = "//div[@class='header-title_text' and text()='Описание обьекта']"

    FACILITY_NAME_LOCATOR_EN = "//h2[text()='Facility name:']"
    FACILITY_NAME_LOCATOR_RU = "//h2[text()='Название объекта:']"
    DESCRIPTION_LOCATOR_EN = "//h2[text()='Description:']"
    DESCRIPTION_LOCATOR_RU = "//h2[text()='Описание:']"
    VISITING_RULES_LOCATOR_EN = "//h2[text()='Visiting rules:']"
    VISITING_RULES_LOCATOR_RU = "//h2[text()='Правила посещения:']"
    ADDRESS_LOCATOR_EN = "//h2[text()='Address:']"
    ADDRESS_LOCATOR_RU = "//h2[text()='Адрес:']"
    CONTACT_PHONE_LOCATOR_EN = "//h2[text()='Contact phone:']"
    CONTACT_PHONE_LOCATOR_RU = "//h2[text()='Контактный телефон:']"
    WEBSITE_LOCATOR_EN = "//h2[text()='Website:']"
    WEBSITE_LOCATOR_RU = "//h2[text()='Веб-сайт:']"
    WORKING_HOURS_LOCATOR_EN = "//h2[text()='Working hours:']"
    WORKING_HOURS_LOCATOR_RU = "//h2[text()='Режим работы:']"
    KINDS_OF_SERVICE_LOCATOR_EN = "//h2[text()='Kinds of service:']"
    KINDS_OF_SERVICE_LOCATOR_RU = "//h2[text()='Виды услуг:']"


    # Текста в блоках
    TEXT_FACILITY_NAME_LOCATOR = "//p[text()='Gym1']"
    # TEXT_DESCRIPTION_LOCATOR = "//span[contains(@style, 'font-family: Calibri, sans-serif; font-size: 18px;') and text()='Some text hereSome text hereSome text hereSome text hereSome text hereSome text hereSome text hereSome text hereSome text here ']"
    # TEXT_VISITING_RULES_LOCATOR = "//h2[text()='Visiting rules:']"
    TEXT_ADDRESS_LOCATOR = "//p[text()='есенина 73']"
    TEXT_CONTACT_PHONE_LOCATOR = "//p[text()='+375000000000;+375123456789']"
    # TEXT_WEBSITE_LOCATOR = "//h2[text()='Website:']"
    # TEXT_WORKING_HOURS_LOCATOR = "//h2[text()='Working hours:']"
    TEXT_KINDS_OF_SERVICE_LOCATOR = "//p[text()='Теннис SG, Посещение SGP, Посещение SGP D']"



    # Кнопки
    BUTTON_REFRESH_INFO_LOCATOR_EN = "//button[@class='btn btn__primary btn-outline']//div[@class='btn-content_slot' and text()='Refresh info']"
    BUTTON_REFRESH_INFO_LOCATOR_RU = "//button[@class='btn btn__primary btn-outline']//div[@class='btn-content_slot' and text()='Обновить информацию']"
    BUTTON_CHANGE_DATA_LOCATOR_EN = "//button[@class='btn btn__primary btn-base']//div[@class='btn-content_slot' and text()='Change data']"
    BUTTON_CHANGE_DATA_LOCATOR_RU = "//button[@class='btn btn__primary btn-base']//div[@class='btn-content_slot' and text()='Изменить данные']"

    # Модалка
    CHANGE_DATA_LOCATOR_EN = "//h2[text()='Change data']"
    CHANGE_DATA_LOCATOR_RU = "//h2[text()='Изменить данные']"
    TEXT_INFO_LOCATOR_EN = "//p[@class='contact-support_hint' and text()='In order to change the data you need to contact technical support:']"
    TEXT_INFO_LOCATOR_RU = "//p[@class='contact-support_hint' and text()='Для того, чтобы изменить данные вам необходимо связаться с тех. поддержкой:']"
    PHONE_NUMBER_LOCATOR = "//div[@class='contacts-item'][1]/a[@class='header-support_phone']"
    EMAIL_LOCATOR = "//div[@class='contacts-item'][2]/a[@class='header-support_phone']"



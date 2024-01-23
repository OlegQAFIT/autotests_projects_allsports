class SubscriptionTypesLocators():
    BUTTON_SUBSCRIPTION_TYPES_TAB = '//li/a[@href="/by/prices/"]'
    ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE = '//h1[text()="Типы подписки"]'
    ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_1 = '//h3[text()="Gold"]'
    ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_2 = '//h3[@class="title hide-mobile"][text()="Количество объектов"]'
    ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_3 = '//button[@class="btn btn-order hide-mobile"]/p[text()="Заказать"]'
    ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_4 = '//h3[@class="title" and text()="Активности"]'
    ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_5 = '//h3[@class="title hide-mobile" and text()="Количество посещений в месяц"]'
    ELEMENT_ON_SUBSCRIPTION_TYPES_PAGE_6 = '//h3[@class="title" and text()="Период отмены"]'

    REGIONAL_LEVEL = '//h3[text()="Regional"]'
    SILVER_LEVEL = '//h3[text()="Silver"]'
    GOLD_LEVEL = '//h3[text()="Gold"]'
    PLATINUM_LEVEL = '//h3[text()="Platinum"]'
    BACK_BUTTON = '//button[@class="left" and @aria-label="decrease"]'

    VIEW_OBJECTS_SILVER = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[3]/div[1]/div'
    VIEW_OBJECTS_GOLD = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[3]/div[2]/div'
    VIEW_OBJECTS_PLATINUM = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[3]/div[3]/div'

    VIEW_ACTIVITY_SILVER = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[4]/div[1]/div'
    VIEW_ACTIVITY_GOLD = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[4]/div[2]/div'
    VIEW_ACTIVITY_PLATINUM = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[4]/div[3]/div'

    CHECKING_ELEMENT_FOR_ALL_OBJECT = '//span[@class="selected" and contains(text(), "Объекты")]'
    CHECKING_ELEMENT_FOR_ALL_ACTIVITY = '//span[@aria-hidden="true" and contains(text(), "Активности")]'
    ELEMENT_MINSK = '//h3[@class="title" and text()="Минск"]'
    SUPPLIER_MINSK = "//p[.='Тренажерный зал “Zona 531”']"
    WEB_SUPPLIER = "//a[contains(@href, 'rgolympic.by')]"

    SUPPLIER = '//p[text()="РЦОП по художественной гимнастике"]'
    SUPPLIER_ELEMENTS = '//h1[text()="РЦОП по художественной гимнастике"]'

    BUTTON_ORDER_1 = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[9]/button[2]'
    BUTTON_ORDER_2 = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[9]/button[4]'
    BUTTON_ORDER_3 = '//*[@id="gatsby-focus-wrapper"]/main/div/div/main/section[1]/div[9]/button[6]'
    GET_OFFER_BUTTON = '//button[contains(text(), "Получить предложение")]'

    FORM = '//h3[text()="Обратитесь к вашему работодателю!"]'

    NAME_COMPANY = '//input[@name="company" and @placeholder="Название организации"]'
    NUMBER_EMPLOYEES_BUTTON = '//button[text()="Количество сотрудников"]'
    NUMBER_EMPLOYEES = '//button[text()="более 1000"]'
    PHONE_NUMBER = '//input[@name="phone"]'
    CITY_LOCATOR = '//input[@name="city"]'
    NAME_EMPLOY = '//input[@name="name" and @placeholder="Имя представителя"]'
    EMAIL_LOCATOR = '//input[@name="email"]'

    EXPECTED_FRAGMENT = 'rgolympic'
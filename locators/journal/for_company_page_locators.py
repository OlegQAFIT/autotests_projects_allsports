class CompanyPageLocators():
    FOOTER_COMPANY = "//a[text()='Companies']"

    CREATE_COMPANY = "//button[contains(@class, 'btn-primary') and contains(., 'Create Company')]"

    LOCATION_DROP_DOWN = "//span[contains(text(), 'Location:')]/parent::p/following-sibling::div[contains(@class, 'select_body')]/div[@class='select_placeholder']"
    MINSK_VALUE = '//div[@class="select_option"]/span[text()="Minsk"]'
    # MOGILEV_VALUE = "//select[@class='']/option[@value='Mogilev']"
    # BREST_VALUE = "//select[@class='']/option[@value='Brest']"
    # GRODNO_VALUE = "//select[@class='']/option[@value='Grodno']"
    # GOMEL_VALUE = "//select[@class='']/option[@value='Gomel']"
    # VITEBSK_VALUE = "//select[@class='']/option[@value='Vitebsk']"

    LOCALE_DROP_DOWN = "//span[contains(text(), 'Locale:')]/parent::p/following-sibling::div[contains(@class, 'select_body')]/div[@class='select_placeholder']"
    RU_VALUE = '//div[@class="select_option"]/span[text()="ru"]'
    AM_VALUE = '//div[@class="select_option"]/span[text()="am"]'
    EN_VALUE = '//div[@class="select_option"]/span[text()="en"]'
    EN_LT_VALUE = '//div[@class="select_option"]/span[text()="en_LT"]'
    LT_LT_VALUE = '//div[@class="select_option"]/span[text()="lt_LT"]'
    UK_VALUE = '//div[@class="select_option"]/span[text()="uk"]'

    TIMEZONE_DROP_DOWN = '/html/body/div/div/div[2]/form/section[1]/div[3]/label/div'
    MINSK_VALUE_TIMEZONE = "/html/body/div/div/div[2]/form/section[1]/div[3]/ul/li[342]/a"

    SELL_STRATEGY_DROP_DOWN = '//span[text()="Sell Strategy"]/parent::p/following-sibling::div[contains(@class, "select_body")]/div[@class="select_placeholder"]'
    BY3_VALUE = '//div[@class="select_option"]/span[text()="ООО” ОЛЛСПОРТС“ ПЕРЕХОД"]'

    REGISTRATION_TYPE_STANDARD = '//p[./span[text()="Registration type"]]/following-sibling::div[@class="select_body"]/div[@class="select_placeholder"]'
    REGISTRATION_TYPE_FORM = '//div[@class="select_option"]/span[text()="REGISTRATION_FORM"]'

    # dropdown = "/html/body/div/div/div[2]/form/section[1]/div[2]/label/div/select"

    default_subscription = "/html/body/div/div/div[2]/form/section[1]/div[5]/div[2]/div"

    compensation_type = "/html/body/div/div/div[2]/form/section[1]/div[5]/div[3]/div"

    ID = "/html/body/div/div/div[2]/form/section[1]/label[1]/div/input"
    compensation_amount = "/html/body/div/div/div[2]/form/section[1]/div[5]/label/div/input"

    COMPANY_INPUT = "/html/body/div/div/div[2]/form/section[1]/label[2]/div/input"

    MANAGER_DROP_DOWN = "//div[@class='select_placeholder' and contains(span, 'Select a manager')]"
    MANAGER_VALUE = "//div[@class='select_option' and contains(span, 'QA-Oleg-A')]"
    # MANAGER_FILIP_WOLEK = "//select[@class='quiet']/option[@value='2']"
    # MANAGER_AUTOTEST_ADMIN_FILIP = "//select[@class='quiet']/option[@value='18']"
    # MANAGER_AUTOTEST_ADMIN_ALEX = "//select[@class='quiet']/option[@value='19']"
    # MANAGER_NADEZHDA_SADOVSKAYA = "//select[@class='quiet']/option[@value='231']"
    # MANAGER_SUPPORT = "//select[@class='quiet']/option[@value='238']"
    # MANAGER_AUTOTEST_ALVINA_MCDERMOTT_II = "//select[@class='quiet']/option[@value='245']"
    # MANAGER_AUTOTEST_GRANVILLE_GREENHOLT = "//select[@class='quiet']/option[@value='246']"
    # MANAGER_QA_YULIA_B = "//select[@class='quiet']/option[@value='252']"
    # MANAGER_QA_BAKURIN_A = "//select[@class='quiet']/option[@value='253']"
    # MANAGER_QA_RYZHKO_A = "//select[@class='quiet']/option[@value='254']"
    # MANAGER_QA_KAHADOUSKAYA_N = "//select[@class='quiet']/option[@value='255']"
    # MANAGER_QA_NOVOGRAN_V = "//select[@class='quiet']/option[@value='256']"
    # MANAGER_QA_PAVEL_L = "//select[@class='quiet']/option[@value='258']"
    # MANAGER_QA_YAN_S = "//select[@class='quiet']/option[@value='259']"
    # MANAGER_QA_ANDREY_L = "//select[@class='quiet']/option[@value='260']"
    # MANAGER_QA_DARIA_S = "//select[@class='quiet']/option[@value='261']"
    # MANAGER_QA_OLEG_A = "//select[@class='quiet']/option[@value='262']"
    # MANAGER_TEST1 = "//select[@class='quiet']/option[@value='265']"
    # MANAGER_ALEX_DEV_TEST = "//select[@class='quiet']/option[@value='269']"
    # MANAGER_ALEX = "//select[@class='quiet']/option[@value='270']"

    DATE = "/html/body/div/div/div[2]/form/section[2]/label[1]/div/input"
    # DATE_INPUT = "(//div[@data-v-3e74a67c]//input[@type='text'])[1]"
    DATE_TEXT = "0130"

    MIN_ORDER_ITEMS = "//input[@data-v-8a5e45de and @type='text' and @disabled='disabled']"
    MIN_ORDER_ITEMS_INPUT = "/html/body/div/div/div[2]/form/section[2]/label[2]/div/input"

    VAT_NUMBER_INPUT = "/html/body/div/div/div[2]/form/section[3]/label[1]/div/input"
    VAT_NUMBER_TEXT = "193190172"
    VAT_NUMBER_TEXT_MIN = "1931901"

    LEGAL_NAME_INPUT = "/html/body/div/div/div[2]/form/section[3]/label[2]/div/input"

    LEGAL_ADDRESS_INPUT = "/html/body/div/div/div[2]/form/section[4]/label[1]/div/input"
    LEGAL_ADDRESS_TEXT = "220030 г. Минск, ул. Интернациональная, 36-2, офисы 2-20, 1-21"

    CONTACT_PHONE_INPUT = "/html/body/div/div/div[2]/form/section[4]/label[2]/div/input"
    CONTACT_PHONE_TEXT = "+375 (44) 502-36-13"

    MAX_COMPANY_NAME_TEXT = "222838, Республика Беларусь, Минская область, Пуховичский р-н, Новосёлковский с/с, д. 35, " \
                            "район улицы Зорный Шлях г. Марьина Горка Почтовый адрес: 220089, Республика Беларусь, г. " \
                            "Минск, ул. Железнодорожная, д. 33222838, Республика Беларусь, Минская область, Пуховичский" \
                            " р-н, Новосёлковский с/с, д. 35, район улицы Зорный Шлях г. Марьина Горка Почтовый адрес: " \
                            "220089, Республика Беларусь, г. Минск, ул. Железнодорожная, д. 33"

    MIN_COMPANY_NAME_TEXT = "Бел"

    ERRORE_TEXT = "//div[@class='info-banner info-banner__visible']//p[@class='info-banner_message' and @data-v-32f372a4]"

    ERRORE_TEXT_MIN = "/html/body/div/div/div[2]/form/div[2]/p"

    ERRORE_TEXT_MIN_UNN = "/html/body/div/div/div[2]/form/section[3]/label[1]/div/span"

    ERRORE_TEXT_legal_name = "/html/body/div/div/div[2]/form/section[3]/label[2]/div/span"

    ERRORE_TEXT_LEGAL_NAME = "//p[@class='info-banner_message' and text()='Такое значение поля legal name уже существует.']"


    SWIFT_INPUT = "/html/body/div/div/div[2]/form/section[4]/label[4]/div/input"

    ACCOUNT_INPUT = "//html/body/div/div/div[2]/form/section[4]/label[5]/div/input"

    SAVE_AND_CONTINUE_BUTTON = "//html/body/div/div/div[2]/form/button"
# ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????

    EDIT_COMPANY = "/html/body/div/div/div[2]/form/div[1]/h1"

    ADD_COMPANY = "/html/body/div/div/div[2]/form/div[1]/h1"
    HR_SETTINGS = "/html/body/div/div/div[2]/form/h2[1]"
    DATA_FOR_THE_CONTRACT = "/html/body/div/div/div[2]/form/h2[2]"
    BENEFIARY = "/html/body/div/div/div[2]/form/h2[3]"
    OPTIONAL = "/html/body/div/div/div[2]/form/h2[4]"

    LEGAL_NAME_SEARCH = "/html/body/div/div/div[2]/form/section[3]/label[2]/div"

    Locale_required_fields = "/html/body/div/div/div[2]/form/section[1]/div[2]/span"
    Timezone_required_fields = "/html/body/div/div/div[2]/form/section[1]/div[3]/div"
    Sell_Strategy_required_fields = "/html/body/div/div/div[2]/form/section[1]/div[4]/span"
    Company_Name_required_fields = "/html/body/div/div/div[2]/form/section[1]/label[2]/div/span"
    VAT_NUMBER_required_fields = "/html/body/div/div/div[2]/form/section[3]/label[1]/div/span"
    Legal_Name_required_fields = "/html/body/div/div/div[2]/form/section[3]/label[2]/div/span"
    Legal_Address_required_fields = "/html/body/div/div/div[2]/form/section[4]/label[1]/div/span"
    Contact_Phone_required_fields = "/html/body/div/div/div[2]/form/section[4]/label[2]/div/span"

    MANAGER_SELECT = "/html/body/div/div/div[2]/div[3]/div[1]/div/div"
    COMPANY_WITH_SELECT_MANAGER = "/html/body/div/div/div[2]/div[3]/div[2]/table/tbody/tr/td[2]"

    SEARCH_FIELDS = "//input[@placeholder='Search']"
    SEARCH_COMPANY = "CompanyA"
    FOUND_COMPANY = "//td[text()='CompanyA']"

    BUTTON_DELETE = "//span[text()='Удалить']"
    BUTTON_PORTAL_USER  = "//span[text()='Portal Users']"






    HEADLINE_HR_EMPLOYEES = "//h1[@data-v-4cc5be50]"
    PHONE_LOCATOR = "/html/body/div/div/div[2]/div[3]/table/thead/tr/td[1]/span"
    NAME_LOCATOR = "/html/body/div/div/div[2]/div[3]/table/thead/tr/td[2]/span"
    POSITION_LOCATOR = "/html/body/div/div/div[2]/div[3]/table/thead/tr/td[3]/span"
    EMAIL_LOCATOR = "/html/body/div/div/div[2]/div[3]/table/thead/tr/td[4]/span"
    SEARCH_LOCATOR = "//div[@data-v-d1b72270 and @data-v-4cc5be50 and @class='local-search']"
    BUTTON_ADD_LOCATOR = "//button[@data-v-51670868 and @data-v-4cc5be50 and @type='button' and @class='btn btn-primary btn__auto-width']"

    ADD_EMPLOYEE_LOCATOR = "//div[@class='modal_row header']//h3[@data-v-a9a67602]"

    MODAL_PHONE_LOCATOR = "/html/body/div/div/div[1]/form/label[1]/span"
    INPUT_MODAL_PHONE_LOCATOR = "/html/body/div/div/div[1]/form/label[1]/label/div/input"
    MODAL_NAME_LOCATOR = "/html/body/div/div/div[1]/form/label[2]/span"
    INPUT_MODAL_NAME_LOCATOR = "/html/body/div/div/div[1]/form/label[2]/label/div/input"
    MODAL_POSITION_LOCATOR = "/html/body/div/div/div[1]/form/label[3]/span"
    INPUT_MODAL_POSITION_LOCATOR = "/html/body/div/div/div[1]/form/label[3]/label/div/input"
    MODAL_EMAIL_LOCATOR = "/html/body/div/div/div[1]/form/label[4]/span"
    INPUT_MODAL_EMAIL_LOCATOR = "/html/body/div/div/div[1]/form/label[4]/label/div/input"
    MODAL_LOCAL_LOCATOR = "/html/body/div/div/div[1]/form/label[5]/span"
    DROP_MODAL_LOCAL_LOCATOR = "/html/body/div/div/div[1]/form/label[5]/div/div"
    EN = "/html/body/div/div/div[1]/form/label[5]/div/div/div[2]/div[2]"
    MODAL_TIMEZONE_LOCATOR = "/html/body/div/div/div[1]/form/label[6]/span"
    DROP_MODAL_TIMEZONE_LOCATOR = "/html/body/div/div/div[1]/form/label[6]/div/label/div"
    INPUT_TIMEZONE = "/html/body/div/div/div[1]/form/label[6]/div/label/div/input"

    MODAL_BUTTON_CANCEL_LOCATOR = "/html/body/div/div/div[1]/form/div[3]/button[1]"
    MODAL_BUTTON_ADD_LOCATOR = "/html/body/div/div/div[1]/form/div[3]/button[2]"

    MODAL_NAME_TEXT = "AQA OLEG"
    MODAL_NAME_TEXT_CHANGE = "AQA OLEG CHANGE"
    MODAL_POSITION_TEXT = "hr"
    MODAL_TIMEZONE_TEXT = "Europe/Minsk"
    SELECT_TIMEZONE_MINSK = "/html/body/div/div/div[1]/form/label[6]/div/ul/li/a"

    PORTAL_USER_PHONE = "375441234578"
    PORTAL_USER_PHONE_BY_CY = "35796348952"
    PORTAL_USER_EMAIL = "forAtest@gmail.com"
    NAME_PORTAL_USER = "Oleg for test"
    SEARCH_PORTAL_USER = "/html/body/div/div/div[2]/div[3]/table/tbody/tr/td[4]"

    WRONG_EMAIL_ERRORE = "привет"
    WRONG_EMAIL_ERRORE_LOCATOR = "/html/body/div/div/div[1]/form/label[4]/label/div/span"

    ADDED_PORTAL_USER_PHONE = "375441234578"
    WRONG_PORTAL_USER_ERRORE_LOCATOR = "/html/body/div/div/div[1]/form/label[1]/label/div/span"
    WRONG_PORTAL_USER_ERRORE_TEXT = "Phone already used by another Portal User"



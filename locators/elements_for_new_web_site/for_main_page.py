class MainPageLocators():
    BUTTON_GET_OFFER = "//div[contains(@class, 'suggestion-text')]//button[contains(@class, 'btn') and .//span[text()='Получить предложение']]"

    CONNECT_COMPANY = "(//ul[contains(@class, 'select-tab')]//li[@id='getOffer' and text()='Подключить компанию'])[2]"
    BECOME_PARTNER = "(//ul[@class='select-tab']//li[@id='becomePartner'])[1]"

    INPUT_NAME = "/html/body/div[1]/div/div[2]/form/div[1]/label[1]/div[2]/input"
    INPUT_PHONE = "/html/body/div[1]/div/div[2]/form/div[1]/label[2]/div[2]/input"
    INPUT_EMAIL = "/html/body/div[1]/div/div[2]/form/div[1]/label[3]/div[2]/input"
    INPUT_NAME_COMPANY = "/html/body/div[1]/div/div[2]/form/div[1]/label[4]/div[2]/input"

    CHECKBOX = "/html/body/div[1]/div/div[2]/form/div[1]/div/div/label"

    BUTTON_SEND = "/html/body/div[1]/div/div[2]/form/div[2]/button"

    text_modal_send = "/html/body/div[1]/div/div[2]/div[1]"
    expected_text = "Спасибо за ваш запрос! Ваш запрос очень важен для нас. Ожидайте звонка от нашего менеджера, который в ближайшее время соберет все необходимые данные, чтобы составить индивидуальное предложение для уникальных потребностей вашей компании."


    ASK_QUESTION = '//*[@id="defaultView"]/main/section[2]/div/div[2]/div/div[2]/div/button'

    COMPANY = "//div[@class='advantages-select-tab']//li[@id='companies']"
    BUTTON_GET_OFFER_COMPANY = '//*[@id="defaultView"]/main/section[2]/div/div[3]/div/div[2]/div/button'

    PARTNERS = "//div[@class='advantages-select-tab']//li[@id='partners']"
    BUTTON_GET_OFFER_PARTNERS = '//*[@id="defaultView"]/main/section[2]/div/div[4]/div/div[2]/div/button'

    #########################################################################################################################################################################################
    ASK_QUESTION_USER = '//*[@id="defaultView"]/main/section[5]/div/div[2]/div[2]/button'


    ASK_QUESTION_COMPANY = "//ul[@class='select-tab faq__select-tab']//li[@id='companies']"
    ASK_QUESTION_GET_OFFER_COMPANY = '//*[@id="defaultView"]/main/section[5]/div/div[2]/div[2]/button/div'

    ASK_QUESTION_PARTNERS = "//ul[@class='select-tab faq__select-tab']//li[@id='partners']"
    ASK_QUESTION_GET_OFFER_PARTNERS = '//*[@id="defaultView"]/main/section[5]/div/div[2]/div[2]/button'


    INPUT_NAME_MAIN = '//*[@id="defaultView"]/main/section[7]/div/div[1]/div/form/label[1]/div[2]/input'
    INPUT_PHONE_MAIN = '//*[@id="defaultView"]/main/section[7]/div/div[1]/div/form/label[2]/div[2]/input'
    INPUT_EMAIL_MAIN = '//*[@id="defaultView"]/main/section[7]/div/div[1]/div/form/label[3]/div[2]/input'
    INPUT_NAME_COMPANY_MAIN = '//*[@id="defaultView"]/main/section[7]/div/div[1]/div/form/label[4]/div[2]/input'

    CHECKBOX_MAIN = '//*[@id="defaultView"]/main/section[7]/div/div[1]/div/form/div/div/label'
    BUTTON_SEND_MAIN = '//*[@id="defaultView"]/main/section[7]/div/div[1]/div/form/button'

    JOIN_COMPANY = '//*[@id="becomePartner"]'



    LOGO_TEXT = '//*[@id="defaultView"]/main/section[1]/div[1]/p[1]'
    ADVANTAGES_TEXT = '//*[@id="defaultView"]/main/section[2]/h2'
    SUBSCRIPTION_TYPES_TEXT = '//*[@id="defaultView"]/main/section[3]/h2'
    REVIEWS_TEXT = '//*[@id="defaultView"]/main/section[4]/h2'
    QUESTION_TEXT = '//*[@id="defaultView"]/main/section[5]/h2'
    CONTACTS_TEXT = '//*[@id="defaultView"]/main/section[8]/h2'

    LIST_OBJECTS = '//*[@id="defaultView"]/main/section[2]/div/div[2]/div/div[2]/div/a'
    FOR_COMPANY = '//*[@id="defaultView"]/main/section[2]/div/div[3]/div/div[2]/div/a'
    FOR_PARTNERS = '//*[@id="defaultView"]/main/section[2]/div/div[4]/div/div[2]/div/a'


    PLATINUM_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[1]/p[2]'
    GOLD = "//li[@id='gold']"
    GOLD_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[1]/p[2]'
    REGIN = "//li[@id='region']"
    REGIN_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[1]/p[2]'
    SILVER = "//li[@id='silver']"
    SILVER_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[1]/p[2]'

    PLATINUM_VID_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[2]/p[2]'
    GOLD_VID_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[2]/p[2]'
    REGIN_VID_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[2]/p[2]'
    SILVER_VID_TEXT = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[2]/p[2]'


    LIST_OBJECTS_OLD_SITE = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[1]/div[2]/a'


    SUBSCRIPTION_OBJECTS = '//*[@id="defaultView"]/main/section[3]/div[2]/div[1]/div/ul/li[1]/div[1]/a'
    SELECT_SUBSCRIPTION = '//*[@id="defaultView"]/main/section/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/span'
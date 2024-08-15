class HeaderLocators():
    BUTTON_GET_OFFER_HEADER = '//*[@id="offer-btn"]'

    INPUT_QUESTION_NAME = "/html/body/div[1]/div/div[2]/form/div[1]/label[1]/div[2]/input"
    INPUT_QUESTION_PHONE = "/html/body/div[1]/div/div[2]/form/div[1]/label[2]/div[2]/input"
    INPUT_QUESTION = "/html/body/div[1]/div/div[2]/form/div[1]/label[3]/textarea"

    CHECKBOX_QUESTION = "/html/body/div[1]/div/div[2]/form/div[1]/div/div/label"

    BUTTON_SEND_QUESTION = "/html/body/div[1]/div/div[2]/form/div[2]/button"


    OBJECTS = "//header[@class='header']//a[@href='/ru-by/facilities' and contains(@class, 'navbar-list__link')]"
    SUBSCRIPTION_TYPES = "//header[@class='header']//a[@href='/ru-by/levels' and contains(@class, 'navbar-list__link')]"
    COMPANIES = "//header[@class='header']//a[@href='/ru-by/companies' and contains(@class, 'navbar-list__link')]"
    PARTNERS = "//header[@class='header']//a[@href='/ru-by/partners' and contains(@class, 'navbar-list__link')]"
    CONTACTS = "//header[@class='header']//a[@href='/ru-by/contacts' and contains(@class, 'navbar-list__link')]"


    LINK_PERSONAL_DATE_HEADER = "//div[@class='agreement-link']//a[contains(@href, '/ru-by/policy/231109_processing_personal_data')]"
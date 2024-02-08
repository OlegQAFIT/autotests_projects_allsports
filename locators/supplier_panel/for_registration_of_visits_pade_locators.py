class RegistrationVisitsLocators():

    HELPDESK_MOBILE_LOCATOR = '//a[@href="/helpdesk/mobile"]'
    HOLDER_BUTTON = '//form[@id="search"]//a[text()="Holder"]'
    SEARCH_INPUT = '//input[@id="up_holder1_phone" and @placeholder="Search by Phone Number"]'
    PHONE = "375000000088"
    HOLDER_USER = '//td[@data-v-00e8e599]/a[text()="Oleg Atr[CompanyA]"]'
    RESET_BUTTON = '(//button[@data-v-2a492a77 and text()="Reset"])[last()]'


    # SIDEBAR сайдбар с вкладками
    SIDEBAR_REGISTRATION_VISITS_LOCATOR_EN = '//a[@href="/visits/registration" and @class="router-link-active router-link-exact-active nav_link" and text()="Registration of visits"]'
    SIDEBAR_VISITS_HISTORY_LOCATOR_EN = '//a[@href="/visits/all" and @class="nav_link" and text()="Visit history"]'
    SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR_EN = '//a[@href="/visits/corrections" and @class="nav_link" and text()="Visits under correction"]'
    SIDEBAR_FACILITY_DETAILS_LOCATOR_EN = '//a[@href="/supplier/about" and @class="nav_link" and text()="Facility details"]'
    SIDEBAR_CONTACTS_LOCATOR_EN = '//a[@href="/contacts" and @class="nav_link" and text()="Contacts"]'
    SIDEBAR_DOCUMENTS_LOCATOR_EN = '//a[@href="/documents" and @class="nav_link" and text()="Documents"]'

    SIDEBAR_REGISTRATION_VISITS_LOCATOR = '//a[@href="/visits/registration" and @class="router-link-active router-link-exact-active nav_link" and text()="Регистрация визитов"]'
    SIDEBAR_VISITS_HISTORY_LOCATOR = '//a[@href="/visits/all" and @class="nav_link" and text()="История визитов"]'
    SIDEBAR_VISITS_UNDER_CORRECTION_LOCATOR = '//a[@href="/visits/corrections" and @class="nav_link" and text()="Визиты на исправлении"]'
    SIDEBAR_FACILITY_DETAILS_LOCATOR = '//a[@href="/supplier/about" and @class="nav_link" and text()="Описание обьекта"]'
    SIDEBAR_CONTACTS_LOCATOR = '//a[@href="/contacts" and @class="nav_link" and text()="Контакты"]'
    SIDEBAR_DOCUMENTS_LOCATOR = '//a[@href="/documents" and @class="nav_link" and text()="Документы"]'

    BUTTON_LOGOUT_LOCATOR = '//div[@class="footer-controls"]/a[text()="Выйти"]'
    BUTTON_LOGOUT_LOCATOR_EN = '//div[@class="footer-controls"]/a[text()="Logout"]'

    CHANGE_LANGUAGE_DROPDOWN_LOCATOR = "//select[@class='language-switcher_list']"
    DROPDOWN_LANGUAGE_EN = "//div[@class='language-switcher']//span[text()='en']"
    DROPDOWN_LANGUAGE_RU = "//select[@class='language-switcher_list']/option[@value='ru']"

    # REGISTRATION OF VISITS PAGE страница регистрации визитов без визита
    LOGO_REGISTRATION_VISITS_LOCATOR = '//div[@class="header-title_text" and text()="Регистрация визитов"]'
    LOGO_REGISTRATION_VISITS_LOCATOR_EN = '//div[@class="header-title_text" and text()="Registration of visits"]'
    TEXT_ADMINISTRATOR_LOCATOR = '//div[@class="row"]/label/div[@class="input_title"]/span[text()="Администратор"]'
    TEXT_ADMINISTRATOR_LOCATOR_EN = '//div[@class="row"]/label/div[@class="input_title"]/span[text()="Administrator"]'
    SELECT_ADMIN_LOCATOR = '//div[@class="input-container"]/div[@class="select fullfilled hide_placeholder"]'
    SHORT_INSTRUCTION_LOCATOR = '//h3[@class="mb-4" and text()="Краткая инструкция:"]'
    SHORT_INSTRUCTION_LOCATOR_EN = '//h3[@class="mb-4" and text()="Short instruction:"]'
    FIRST_INSTRUCTION_LOCATOR = '//ol[@class="ps-4"]/li[1]'
    SECOND_INSTRUCTION_LOCATOR = '//ol[@class="ps-4"]/li[2]'
    THIRD_INSTRUCTION_LOCATOR = '//ol[@class="ps-4"]/li[3]'
    BUTTON_NEW_VISITS_LOCATOR = "//button[contains(@class, 'btn__primary') and contains(@class, 'btn-base') and .//div[contains(@class, 'btn-content_slot') and text()='Новые визиты']]"
    BUTTON_NEW_VISITS_LOCATOR_EN = "//button[contains(@class, 'btn__primary') and contains(@class, 'btn-base') and .//div[contains(@class, 'btn-content_slot') and text()='New visits']]"

    # REGISTRATION OF VISITS PAGE когда пришел визит
    SUPPLIER_NAME_LOCATOR = '//div[@class="row pb-3 pb-sm-4"]/h2[text()="Gym1"]'
    NAME_USER_LOCATOR = '//div[@class="row visit-info-item"][1]/p[@class="col-6 visit-info-item_body"]'
    LEVEL_USER_LOCATOR = '//div[@class="row visit-info-item"][2]/p[@class="col-6 visit-info-item_body"]'
    ATTRACTION_USER_LOCATOR = '//div[@class="row visit-info-item"][3]/p[@class="col-6 visit-info-item_body"]'

    # REJECT VISIT шаги когда отклоняем визит
    DECLINE_BUTTON_LOCATOR = "//div[@class='btn-content']/div[@class='btn-content_slot' and text()='Отклонить']"
    DECLINE_BUTTON_LOCATOR_EN = "//div[@class='btn-content']/div[@class='btn-content_slot' and text()='Decline']"
    REJECT_VISIT_TEXT_LOCATOR = "//h2[@class='d-none d-sm-block' and text()='Отклонить визит']"
    REJECT_VISIT_TEXT_LOCATOR_EN = "//h2[@class='d-none d-sm-block' and text()='Reject the visit']"
    REASON_TEXT_LOCATOR = "//span[text()='Причина']"
    REASON_TEXT_LOCATOR_EN = "//span[text()='Reason']"
    INPUT_REASON_REJECT_LOCATOR = "//div[@class='input-container']//input[@class='item_body']"
    INPUT_REASON_REJECT_TEXT_LOCATOR = "неправильно"
    BUTTON_SAVE_LOCATOR = "//button[@class='btn btn__primary btn-base modal-controls_control' and @disabled]/div[@class='btn-content']/div[@class='btn-content_slot' and text()='Сохранить']"
    BUTTON_SAVE_LOCATOR_EN = "//button[@class='btn btn__primary btn-base modal-controls_control' and @disabled]/div[@class='btn-content']/div[@class='btn-content_slot' and text()='Save']"
    CLICK_BUTTON_SAVE = "//button[contains(@class, 'btn__primary') and contains(@class, 'btn-base') and contains(@class, 'modal-controls_control') and .//div[contains(@class, 'btn-content_slot') and text()='Сохранить']]"
    CLICK_BUTTON_SAVE_EN = "//button[contains(@class, 'btn__primary') and contains(@class, 'btn-base') and contains(@class, 'modal-controls_control') and .//div[contains(@class, 'btn-content_slot') and text()='Save']]"
    BUTTON_CLOSE_MODAL_REJECT = "//a[@class='icon-container' and @href='#']/*[@id='close-icon']"
    #  CONFIRM VISIT шаги когда подтверждаем визиты
    ACCEPT_BUTTON_LOCATOR = '//*[@id="app"]/div/div/main/div[2]/div/div/div/div/div[2]/div[1]/div[4]/div/button[2]'
    ACCEPT_BUTTON_LOCATOR_EN = '//*[@id="app"]/div/div/main/div[2]/div/div/div/div/div[2]/div[1]/div[4]/div/button[2]/div/div'
    TEXT_QUESTION_ACCEPT_LOCATOR = "//div[@class='modal-header_title']/h2[text()='Является ли клиент человеком на фото?']"
    TEXT_QUESTION_ACCEPT_LOCATOR_EN = "//div[@class='modal-header_title']/h2[text()='Is the visitor the person in the photo?']"
    BUTTON_LOOKS_LIKE_LOCATOR = "//div[@class='modal-controls']//button[@class='btn btn__primary btn-base modal-controls_control']/div[@class='btn-content']/div[@class='btn-content_slot' and text()='Похож']"
    BUTTON_LOOKS_LIKE_LOCATOR_EN = "//div[@class='modal-controls']//button[@class='btn btn__primary btn-base modal-controls_control']/div[@class='btn-content']/div[@class='btn-content_slot' and text()='Looks like']"
    BUTTON_NOT_SURE_LOCATOR = "//div[@class='modal-controls']//button[@class='btn btn__primary btn-outline modal-controls_control']/div[@class='btn-content']/div[@class='btn-content_slot' and text()='Не уверен']"
    BUTTON_NOT_SURE_LOCATOR_EN = "//div[@class='modal-controls']//button[@class='btn btn__primary btn-outline modal-controls_control']/div[@class='btn-content']/div[@class='btn-content_slot' and text()='Not sure']"
    BUTTON_CLOSE_MODAL_CONFIRM = "//a[@class='icon-container']/*[@id='close-icon']"

    FOTO_LOCATOR = "//div[@class='my-2 my-sm-0 visit-photo']"
    FOTO_LOCATOR_MODAL = "//div[@class='my-2 my-sm-0 visit-photo']"

    #  ADD ADMINISTRATION

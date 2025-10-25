class ContactsPageLocators:
    # ==== Header ====
    PAGE_TITLE = '//*[@id="defaultView"]/main/section[1]/h2'

    # ==== Contacts Info ====
    ADDRESS_BLOCK = (
        "//*[contains(@class, 'contacts') and "
        "(contains(., 'Минск') or contains(., 'Республика') or contains(., 'Адрес') or contains(., 'address'))]"
    )
    PHONE_LINKS = "//a[starts-with(@href, 'tel:')]"
    EMAIL_LINKS = "//a[starts-with(@href, 'mailto:')]"
    SOCIAL_LINKS = ("//a[contains(@class, 'contacts') or contains(@href, 't.me') or contains(@href, 'telegram') "
                    "or contains(@href, 'instagram') or contains(@href, 'facebook') or contains(@href, 'vk.com')]")

    # ==== Map ====
    MAP_IFRAME = (
        "//div[@id='map' or contains(@class, 'mapboxgl-map') or contains(@class, 'contacts-map')]"
    )

    # ==== Tabs ====
    TAB_GET_OFFER = "//li[@id='get-offer' or contains(., 'Подключить компанию')]"
    TAB_BECOME_PARTNER = ("//li[@id='become-partner' or contains(., 'Стать партнером') "
                          "or contains(., 'Стать партёром')]")

    # ==== Feedback form (унифицировано под текущую вёрстку) ====
    INPUT_NAME = ("//label[contains(., 'Ваше имя') or contains(., 'Имя') or .//input[@type='text']]"
                  "//input[@type='text' and not(@name='email')]")
    INPUT_PHONE = "//input[@name='phone' or (contains(@placeholder,'+375') and @type='tel')]"
    INPUT_EMAIL = "//input[@name='email' or (contains(@placeholder,'@') and @type='text')]"

    # На старых версиях могла быть textarea message — поддержим оба варианта.
    INPUT_MESSAGE = ("//textarea[@name='message' or contains(@placeholder, 'Сообщение') or @id='message']"
                     " | //input[contains(@placeholder,'Компания') or contains(@placeholder,'компания')]")

    CHECKBOX_AGREE = ("//div[contains(@class,'agreement')]//input[@type='checkbox' and "
                      "(contains(@name,'agree') or contains(@id,'agree') or contains(@aria-label,'соглас') "
                      "or contains(@aria-label,'agree') or not(@name))]")

    # Кнопка отправки (три состояния)
    BUTTON_SEND_ANY = "//form[contains(@class,'get-details__form')]//button[contains(@class,'get-details__button')]"
    BUTTON_SEND_ENABLED = f"{BUTTON_SEND_ANY}[not(@disabled)]"
    BUTTON_SEND_DISABLED = f"{BUTTON_SEND_ANY}[@disabled]"

    ERROR_MESSAGE = ("//*[contains(@class, 'input-error') and string-length(normalize-space())>0] "
                     "| //*[contains(@class,'error') or contains(@class,'invalid') "
                     "or contains(text(), 'некоррект') or contains(text(), 'обязат')]")

    MODAL_SUCCESS = ("//*[contains(text(), 'Спасибо за ваш запрос') or "
                     "contains(text(), 'Ваш запрос очень важен для нас')]")

    # ==== Footer ====
    FOOTER_COMPANY_INFO = ("//footer//*[contains(@class, 'official') or contains(., 'ООО') or "
                           "contains(., 'УНП') or contains(., 'ALLSPORTS') or contains(., 'ОЛЛСПОРТС')]")
    FOOTER_COPYRIGHT = ("//footer//*[contains(., 'Все права защищены') or contains(., 'All rights reserved') "
                        "or contains(@class,'copyright')]")
    FOOTER_RULES_LINK = ("//footer//a[contains(@href, '/providing-payment-service-rules') "
                         "or contains(., 'Правила оказания услуг')]")

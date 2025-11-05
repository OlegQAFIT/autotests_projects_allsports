# === Блок: Весь спорт в одном приложении ===

from selenium.webdriver.common.by import By


class MainPageLocators:
    BASE_URL = "https://www.allsports.by/ru-by"
    # === Блок: Весь спорт в одном приложении ===

    SUGGESTION_TITLE = (By.CSS_SELECTOR, ".suggestion-text .text-h1")
    SUGGESTION_STATISTICS = (By.CSS_SELECTOR, ".suggestion-text .suggestion__statistics")
    SUGGESTION_DESCRIPTION = (By.CSS_SELECTOR, ".suggestion-text .suggestion__description")
    SUGGESTION_BTN_GET_OFFER = (By.XPATH, "//div[contains(@class,'suggestion-text')]//button[contains(@class,'btn') and not(contains(@class,'btn_text'))]//span[normalize-space()='Получить предложение']")
    SUGGESTION_BTN_ASK_QUESTION = (By.XPATH, "//div[contains(@class,'suggestion-text')]//button[contains(@class,'btn_text')]//span[normalize-space()='Задать вопрос']")
    PROMO_SECTION = (By.CSS_SELECTOR, '//*[@id="defaultView"]/main/section/div[1]')

    # === Блок: Изображение телефона в секции предложения ===
    SUGGESTION_IMAGE_PHONE = (By.CSS_SELECTOR, "img[src*='suggestionSection/phone.png']")

    # === Блок: Преимущества Allsports ===

    # ===================== Пользователям ============================================================
    ADVANTAGES_TITLE = (By.CSS_SELECTOR, "section.advantages h2")
    ADVANTAGES_TAB_USERS = (By.ID, "members")
    ADVANTAGES_TAB_COMPANIES = (By.ID, "companies")
    ADVANTAGES_TAB_PARTNERS = (By.ID, "partners")
    ADVANTAGES_TAB_ACTIVE = (By.CSS_SELECTOR, ".select-tab__option_selected")
    ADVANTAGES_SUBTITLE = (By.CSS_SELECTOR, ".advantages-tab:not(.advantages-tab_hidden) h3")
    ADVANTAGES_LIST_ITEMS = (By.CSS_SELECTOR, ".advantages-tab:not(.advantages-tab_hidden) .advantages-text ul li span")
    ADVANTAGES_BTN_LIST = (By.XPATH, "//a[.//span[contains(text(),'Список объектов') or contains(text(),'Компаниям') or contains(text(),'Партнерам')]]")
    ADVANTAGES_BTN_ASK_OR_GET = (By.XPATH, "//button[.//span[contains(text(),'Задать вопрос') or contains(text(),'Получить предложение')]]")
    ADVANTAGES_SLIDER_IMAGES = (By.CSS_SELECTOR, ".advantages-tab-user .advantages-images img[src*='advantagesSection/']")
    ADVANTAGES_SLIDER_PREV = (By.CSS_SELECTOR, ".scroll-slider-control__prev")
    ADVANTAGES_SLIDER_NEXT = (By.CSS_SELECTOR, ".scroll-slider-control__next")

    # === Модалка: Задать вопрос (вкладка "Пользователям") ===
    MODAL_ASK_QUESTION_TITLE = (By.XPATH, "//div[@class='modal-header']//div[text()='Задать вопрос']")
    MODAL_ASK_QUESTION_CLOSE_BTN = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    MODAL_INPUT_NAME = (By.XPATH, "//label[@class='input']//div[text()='Ваше имя']/following-sibling::div//input")
    MODAL_INPUT_PHONE = (By.XPATH, "//label[@class='input']//div[text()='Телефон']/following-sibling::div//input[@type='tel']")
    MODAL_PHONE_HELP_TEXT = (By.CSS_SELECTOR, ".input__help-text")
    MODAL_INPUT_EMAIL = (By.XPATH, "//label[@class='input']//div[text()='Email']/following-sibling::div//input[@type='email']")
    MODAL_TEXTAREA_QUESTION = (By.CSS_SELECTOR, ".modal-form textarea")
    MODAL_AGREEMENT_CHECKBOX = (By.CSS_SELECTOR, ".agreement input[type='checkbox']")
    MODAL_AGREEMENT_LINK = (By.CSS_SELECTOR, ".agreement a[href*='processing_personal_data']")
    MODAL_BTN_SUBMIT = (By.XPATH, "//button[.//span[text()='Отправить']]")
    MODAL_SEPARATOR_TEXT = (By.XPATH, "//div[@class='modal-body__separator']//span[text()='или']")
    MODAL_PHONE_LINK = (By.CSS_SELECTOR, ".modal-body__phone[href^='tel:']")
    MODAL_PHONE_NUMBER = (By.CSS_SELECTOR, ".modal-body__phone span")

    # ===================== Компаниям ================================================================
    ADVANTAGES_COMPANY_TITLE = (By.CSS_SELECTOR, ".advantages-tab-company h3")
    ADVANTAGES_COMPANY_IMAGE = (By.CSS_SELECTOR, ".advantages-tab-company .advantages-images img")
    ADVANTAGES_COMPANY_LIST = (By.CSS_SELECTOR, ".advantages-tab-company .advantages-text ul li span")
    ADVANTAGES_COMPANY_LINK = (By.XPATH, "//a[.//span[text()='Компаниям']]")
    ADVANTAGES_COMPANY_BTN_GET_OFFER = (By.XPATH, "//button[.//span[contains(text(),'Получить предложение')]]")

    # === Модалка: Получить предложение (Компаниям) ===
    MODAL_GET_OFFER_TITLE = (By.XPATH, "//div[@class='modal-header']//div[text()='Получить предложение']")
    MODAL_GET_OFFER_CLOSE_BTN = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    MODAL_GET_OFFER_INPUT_NAME = (By.XPATH, "//label[@class='input']//div[contains(text(),'Ваше имя')]/following-sibling::div//input")
    MODAL_GET_OFFER_INPUT_PHONE = (By.XPATH, "//label[@class='input']//div[text()='Телефон']/following-sibling::div//input[@type='tel']")
    MODAL_GET_OFFER_PHONE_HELP_TEXT = (By.CSS_SELECTOR, ".input__help-text")
    MODAL_GET_OFFER_INPUT_EMAIL = (By.XPATH, "//label[@class='input']//div[contains(text(),'Email')]/following-sibling::div//input")
    MODAL_GET_OFFER_INPUT_COMPANY = (By.XPATH, "//label[@class='input']//div[contains(text(),'Название компании')]/following-sibling::div//input")
    MODAL_GET_OFFER_INPUT_CITY = (By.XPATH, "//label[@class='input']//div[text()='Город']/following-sibling::div//input")
    MODAL_GET_OFFER_CHECKBOX = (
        By.XPATH,
        "//div[contains(@class,'agreement-body')]//label[contains(@class,'checkbox')]"
    )

    MODAL_GET_OFFER_POLICY_LINK = (By.CSS_SELECTOR, ".agreement a[href*='processing_personal_data']")
    MODAL_GET_OFFER_BTN_SUBMIT = (
        By.XPATH,
        "//div[contains(@class,'modal-form-control')]//button[@type='submit']"
    )

    MODAL_GET_OFFER_SEPARATOR_TEXT = (By.XPATH, "//div[@class='modal-body__separator']//span[text()='или']")
    MODAL_GET_OFFER_PHONE_LINK = (By.CSS_SELECTOR, ".modal-body__phone[href^='tel:']")
    MODAL_GET_OFFER_PHONE_NUMBER = (By.CSS_SELECTOR, ".modal-body__phone span")

    # ===================== Партнерам ================================================================
    ADVANTAGES_PARTNER_TITLE = (By.CSS_SELECTOR, ".advantages-tab-partner h3")
    ADVANTAGES_PARTNER_IMAGE = (By.CSS_SELECTOR, ".advantages-tab-partner .advantages-images img[src*='partner']")
    ADVANTAGES_PARTNER_LIST = (By.CSS_SELECTOR, ".advantages-tab-partner .advantages-text ul li span")
    ADVANTAGES_PARTNER_LINK = (By.XPATH, "//a[.//span[text()='Партнерам']]")
    ADVANTAGES_PARTNER_BTN_GET_OFFER = (By.XPATH, "//button[.//span[contains(text(),'Получить предложение')]]")

    # === Модалка: Стать партнёром ===
    MODAL_BECOME_PARTNER_TITLE = (By.XPATH, "//div[@class='modal-header']//div[text()='Стать партнером']")
    MODAL_BECOME_PARTNER_CLOSE_BTN = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    MODAL_BECOME_PARTNER_INPUT_NAME = (By.XPATH, "//label[@class='input']//div[contains(text(),'Ваше имя')]/following-sibling::div//input")
    MODAL_BECOME_PARTNER_INPUT_PHONE = (By.XPATH, "//label[@class='input']//div[text()='Телефон']/following-sibling::div//input[@type='tel']")
    MODAL_BECOME_PARTNER_PHONE_HELP_TEXT = (By.CSS_SELECTOR, ".input__help-text")
    MODAL_BECOME_PARTNER_INPUT_EMAIL = (By.XPATH, "//label[@class='input']//div[contains(text(),'Email')]/following-sibling::div//input")
    MODAL_BECOME_PARTNER_INPUT_OBJECT_NAME = (By.XPATH, "//label[@class='input']//div[contains(text(),'Название объекта')]/following-sibling::div//input")
    MODAL_BECOME_PARTNER_INPUT_CITY = (By.XPATH, "//label[@class='input']//div[text()='Город']/following-sibling::div//input")
    MODAL_BECOME_PARTNER_CHECKBOX = (By.CSS_SELECTOR, ".agreement input[type='checkbox']")
    MODAL_BECOME_PARTNER_POLICY_LINK = (By.CSS_SELECTOR, ".agreement a[href*='processing_personal_data']")
    MODAL_BECOME_PARTNER_BTN_SUBMIT = (By.XPATH, "//button[.//span[text()='Отправить']]")
    MODAL_BECOME_PARTNER_SEPARATOR_TEXT = (By.XPATH, "//div[@class='modal-body__separator']//span[text()='или']")
    MODAL_BECOME_PARTNER_PHONE_LINK = (By.CSS_SELECTOR, ".modal-body__phone[href^='tel:']")
    MODAL_BECOME_PARTNER_PHONE_NUMBER = (By.CSS_SELECTOR, ".modal-body__phone span")

    # =============== Видео (YouTube) ================================================================
    VIDEO_SECTION = (By.CSS_SELECTOR, "#videoSection")
    VIDEO_IFRAME = (By.CSS_SELECTOR, "#videoSection iframe")
    VIDEO_IFRAME_SRC = (By.XPATH, "//iframe[contains(@src, 'youtube.com/embed')]")
    VIDEO_IFRAME_TITLE = (By.XPATH, "//iframe[@title='YouTube video player']")
    VIDEO_IFRAME_VISIBLE = (By.XPATH, "//iframe[contains(@src, 'youtube.com') and @loading='lazy']")
    VIDEO_IFRAME_ALLOWFULLSCREEN = (By.XPATH, "//iframe[@allowfullscreen]")
    VIDEO_IFRAME_CONTROLS_PARAM = (By.XPATH, "//iframe[contains(@src, 'controls=0')]")
    VIDEO_IFRAME_NO_RELATED = (By.XPATH, "//iframe[contains(@src, 'rel=0')]")
    VIDEO_IFRAME_MODEST_BRANDING = (By.XPATH, "//iframe[contains(@src, 'modestbranding=1')]")
    VIDEO_IFRAME_NO_INFO = (By.XPATH, "//iframe[contains(@src, 'showinfo=0')]")

    # =============== Присоединяйтесь к Allsports — Подключить компанию ===============================
    JOIN_SECTION = (By.CSS_SELECTOR, "#getDetailsSection")
    JOIN_SECTION_TITLE = (By.XPATH, "//h2[text()='Присоединяйтесь к Allsports']")
    JOIN_TABS = (By.CSS_SELECTOR, ".get-details__form-container .select-tab .select-tab__option")
    JOIN_TAB_CONNECT_COMPANY = (By.CSS_SELECTOR, ".select-tab__option#get-offer")
    JOIN_TAB_BECOME_PARTNER = (By.CSS_SELECTOR, ".select-tab__option#become-partner")
    JOIN_TAB_SELECTED = (By.CSS_SELECTOR, ".select-tab__option.select-tab__option_selected")
    JOIN_FORM = (By.CSS_SELECTOR, ".get-details__form")
    JOIN_INPUT_NAME = (By.XPATH, "//label[.//div[text()='Ваше имя']]//input")
    JOIN_INPUT_PHONE = (By.XPATH, "//label[.//div[text()='Телефон']]//input[@type='tel']")
    JOIN_INPUT_EMAIL = (By.XPATH, "//label[.//div[text()='Email']]//input[@name='email']")
    JOIN_INPUT_COMPANY = (By.XPATH, "//label[.//div[text()='Название компании']]//input")
    JOIN_CHECKBOX = (By.CSS_SELECTOR, ".agreement input[type='checkbox']")
    JOIN_POLICY_LINK = (By.XPATH, "//a[contains(@href, '/policy') and text()='Политикой обработки персональных данных']")
    JOIN_SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']//span[text()='Получить предложение']")
    JOIN_SECTION_IMAGE = (By.CSS_SELECTOR, ".get-details__image img")

    # =============== Присоединяйтесь к Allsports — Стать партнёром ================================
    JOIN_PARTNER_SECTION = (By.CSS_SELECTOR, "#getDetailsSection")
    JOIN_PARTNER_SECTION_TITLE = (By.XPATH, "//h2[text()='Присоединяйтесь к Allsports']")
    JOIN_PARTNER_TABS = (By.CSS_SELECTOR, ".get-details__form-container .select-tab .select-tab__option")
    JOIN_PARTNER_TAB_COMPANY = (By.XPATH, "//li[@id='get-offer' and text()='Подключить компанию']")
    JOIN_PARTNER_TAB_SELECTED = (By.XPATH, "//li[@id='become-partner' and contains(@class,'select-tab__option_selected')]")
    JOIN_PARTNER_FORM = (By.CSS_SELECTOR, ".get-details__form")
    JOIN_PARTNER_INPUT_NAME = (By.XPATH, "//label[.//div[text()='Ваше имя']]//input")
    JOIN_PARTNER_INPUT_PHONE = (By.XPATH, "//label[.//div[text()='Телефон']]//input[@type='tel']")
    JOIN_PARTNER_INPUT_EMAIL = (By.XPATH, "//label[.//div[text()='Email']]//input[@name='email']")
    JOIN_PARTNER_INPUT_OBJECT = (By.XPATH, "//label[.//div[text()='Название объекта']]//input")
    JOIN_PARTNER_CHECKBOX = (By.CSS_SELECTOR, ".agreement input[type='checkbox']")
    JOIN_PARTNER_POLICY_LINK = (By.XPATH, "//a[contains(@href, '/policy') and text()='Политикой обработки персональных данных']")
    JOIN_PARTNER_SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']//span[text()='Получить предложение']")
    JOIN_PARTNER_SECTION_IMAGE = (By.CSS_SELECTOR, ".get-details__image img")

    MODAL = (By.CSS_SELECTOR, "div.modal")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    MODAL_PHONE_ERROR = (By.CSS_SELECTOR, "label.input div.input-error")
    MODAL_EMAIL_ERROR = (By.CSS_SELECTOR, "label.input div.input-error")
    SUCCESS_MODAL = (By.CSS_SELECTOR, "div.modal-success, div.modal-successfully")
    SUCCESS_TEXT = (By.XPATH, "//div[contains(text(),'Спасибо') or contains(text(),'запрос')]")
    SUCCESS_CLOSE_BTN = (By.CSS_SELECTOR, "div.modal-success button.icon-btn")
    MODAL_POLICY_LINK = (By.CSS_SELECTOR, ".agreement a[href*='processing_personal_data']")

    # === БЛОК: Типы подписок ===

    SUBSCRIPTION_SECTION = (By.XPATH, "//h2[contains(normalize-space(),'Типы подписок')]")
    SUBSCRIPTION_CARDS = (By.CSS_SELECTOR, ".level-card-wrapper")
    SUBSCRIPTION_CARD_TITLE = (By.CSS_SELECTOR, ".level-card__main h2")
    SUBSCRIPTION_CARD_TEXTS = (By.CSS_SELECTOR, ".level-card__main p")

    # === Ссылки внутри карточки ===
    SUBSCRIPTION_LINK_OBJECTS = (By.XPATH, ".//span[contains(normalize-space(),'Объекты подписки')]")
    SUBSCRIPTION_LINK_TABLE = (By.XPATH, ".//span[contains(normalize-space(),'Список объектов')]")

    # === Вспомогательные элементы в карточке ===
    SUBSCRIPTION_CARD_DESCRIPTIONS = (By.CSS_SELECTOR, ".level-card__main-description-text p")
    SUBSCRIPTION_CARD_MISC_TEXT = (By.CSS_SELECTOR, ".level-card__misc p")

    # === Кнопки скроллера (стрелки) ===
    SUBSCRIPTION_SLIDER_NEXT = (By.CSS_SELECTOR, ".scroll-slider-control__next")
    SUBSCRIPTION_SLIDER_PREV = (By.CSS_SELECTOR, ".scroll-slider-control__prev")

    # === Кнопка открытия модалки “Архивные типы подписок” ===
    SUBSCRIPTIONS_ARCHIVE_BTN = (By.XPATH, "//button[.//span[normalize-space()='Архивные типы подписок']]")

    # === Модалка “Архивные типы подписок” ===
    SUBSCRIPTIONS_ARCHIVE_MODAL = (By.CSS_SELECTOR, "div.modal")
    SUBSCRIPTIONS_ARCHIVE_CLOSE = (By.CSS_SELECTOR, "div.modal button.icon-btn")
    SUBSCRIPTIONS_ARCHIVE_CARDS = (By.CSS_SELECTOR, ".modal .level-card-wrapper")
    SUBSCRIPTIONS_ARCHIVE_CARD_TITLE = (By.CSS_SELECTOR, ".modal .level-card__main h2")
    SUBSCRIPTIONS_ARCHIVE_CARD_TEXTS = (By.CSS_SELECTOR, ".modal .level-card__main p")
    SUBSCRIPTIONS_ARCHIVE_LINK_OBJECTS = (By.XPATH, ".//span[contains(normalize-space(),'Объекты подписки')]")
    SUBSCRIPTIONS_ARCHIVE_LINK_TABLE = (By.XPATH, ".//span[contains(normalize-space(),'Список объектов')]")



# === Нам доверяют ===
    # === Заголовок и секция ===
    TRUST_SECTION = (By.XPATH, "//h2[normalize-space()='Нам доверяют']")
    TRUST_SECTION_WRAPPER = (By.CSS_SELECTOR, "#feedbackSection.section-wrapper")

    # === Карточки компаний ===
    TRUST_COMPANY_ITEMS = (By.CSS_SELECTOR, ".partner-companies ul li.item")
    TRUST_COMPANY_LOGOS = (By.CSS_SELECTOR, ".partner-companies__scroll-item img")
    TRUST_COMPANY_TEXTS = (By.CSS_SELECTOR, ".partner-companies ul li.item p")
    TRUST_COMPANY_LINKS = (By.XPATH, ".//a[normalize-space()='Читать отзыв']")

    # === Слайдер ===
    TRUST_SLIDER_CONTAINER = (By.CSS_SELECTOR, ".partner-companies__scroll-slider")
    TRUST_SLIDER_NEXT = (By.CSS_SELECTOR, ".scroll-slider-control__next")
    TRUST_SLIDER_PREV = (By.CSS_SELECTOR, ".scroll-slider-control__prev")

    # === Дополнительно (если тестируется скролл или lazy-load логотипов) ===
    TRUST_VISIBLE_LOGO = (By.CSS_SELECTOR, ".partner-companies__scroll-item img[loading='lazy']")
    TRUST_SECTION_IN_VIEW = (By.XPATH, "//section[contains(@class,'partner-companies')]")


# === FAQ ===
    # === Основной блок FAQ ===
    FAQ_SECTION = (By.CSS_SELECTOR, "#faqSection.section-wrapper")
    FAQ_TITLE = (By.XPATH, "//h2[normalize-space()='Часто задаваемые вопросы']")
    FAQ_WRAPPER = (By.CSS_SELECTOR, ".faq-wrapper")
    FAQ_CONTAINER = (By.CSS_SELECTOR, ".faq-container")
    FAQ_LIST = (By.CSS_SELECTOR, ".faq-list")
    FAQ_ITEMS = (By.CSS_SELECTOR, ".faq-list .expansion-item")

    # === Заголовки и стрелки ===
    FAQ_QUESTION_TITLES = (By.CSS_SELECTOR, ".expansion-item-title h5.text-h5-new")
    FAQ_QUESTION_ARROWS = (By.CSS_SELECTOR, ".expansion-item__arrow")
    FAQ_QUESTION_OPEN = (By.CSS_SELECTOR, ".expansion-item__arrow .expansion-item_open")

    # === Ответы ===
    FAQ_ANSWER_BLOCKS = (By.CSS_SELECTOR, ".expansion-item .expansion-item-text")
    FAQ_ANSWER_VISIBLE = (By.XPATH,
                          "//div[contains(@class,'expansion-item-text') and not(contains(@style,'display: none'))]")
    FAQ_ANSWER_LINKS = (By.CSS_SELECTOR, ".expansion-item-text a")

    # === Табы ===
    FAQ_TAB_BAR = (By.CSS_SELECTOR, ".faq__select-tab")
    FAQ_TAB_ITEMS = (By.CSS_SELECTOR, ".faq__select-tab li.select-tab__option")
    FAQ_TAB_SELECTED = (By.CSS_SELECTOR, ".faq__select-tab li.select-tab__option_selected")
    FAQ_TAB_MEMBERS = (By.ID, "members")
    FAQ_TAB_PARTNERS = (By.ID, "partners")
    FAQ_TAB_COMPANIES = (By.ID, "companies")

    # === Мобильный селект ===
    FAQ_DROPDOWN = (By.CSS_SELECTOR, ".faq__select")
    FAQ_DROPDOWN_VALUE = (By.CSS_SELECTOR, ".faq__select .select-field__value")
    FAQ_DROPDOWN_ARROW = (By.CSS_SELECTOR, ".faq__select .select-field__arrow")
    FAQ_DROPDOWN_INPUT = (By.CSS_SELECTOR, ".faq__select .select-field__input")

    # === Блоки "Информация для ..." ===
    FAQ_INFO_BLOCK = (By.CSS_SELECTOR, ".faq-links")
    FAQ_INFO_TITLE = (By.CSS_SELECTOR, ".faq-links span.text-h5-new")
    FAQ_INFO_LINK = (By.CSS_SELECTOR, ".faq-links a")

    # === Форма "Не нашли ответ?" ===
    FAQ_FORM = (By.CSS_SELECTOR, ".faq-form")
    FAQ_FORM_TITLE = (By.XPATH, "//h5[normalize-space()='Не нашли ответ на вопрос?']")
    FAQ_FORM_BTN_ASK = (By.XPATH, "//button[contains(@class,'btn_text')]//span[normalize-space()='Задать вопрос']")

    # === Модальное окно "Задать вопрос" ===
    MODAL_FAQ = (By.CSS_SELECTOR, ".modal")
    MODAL_TITLE = (By.CSS_SELECTOR, ".modal-header div")
    MODAL_CLOSE_BTN = (By.CSS_SELECTOR, ".modal-header button")

    # Поля формы
    MODAL_INPUT_NAME_FAQ = (By.XPATH, "//input[@type='text' and @placeholder='Ваше имя']")
    MODAL_INPUT_PHONE_FAQ = (By.XPATH, "//input[@type='tel']")
    MODAL_INPUT_EMAIL_FAQ = (By.XPATH, "//input[@type='email']")
    MODAL_TEXTAREA = (By.CSS_SELECTOR, ".modal textarea.text-body")

    # Чекбокс и кнопка
    MODAL_AGREE = (By.CSS_SELECTOR, ".modal .agreement-body input[type='checkbox']")
    MODAL_SUBMIT = (By.XPATH, "//button[.//span[normalize-space()='Отправить']]")

    # Телефон под кнопкой
    MODAL_PHONE_LINK_FAQ = (By.CSS_SELECTOR, ".modal-body__phone")
    MODAL_PHONE_TEXT = (By.XPATH, "//a[contains(@href,'tel:')]//span[contains(text(),'+375')]")




    # === КОНТАКТЫ (Наши контакты) =====================================================================

    # Основной блок
    CONTACTS_SECTION = (By.CSS_SELECTOR, "#contactsSection.section-wrapper")
    CONTACTS_TITLE = (By.XPATH, "//h2[normalize-space()='Наши контакты']")
    CONTACTS_CONTAINER = (By.CSS_SELECTOR, ".contacts-container")
    CONTACTS_INFO = (By.CSS_SELECTOR, ".contacts-info")

    # Блоки информации (каждый из 4: клиенты, партнёры, техподдержка, адрес)
    CONTACTS_INFO_BLOCKS = (By.CSS_SELECTOR, ".contacts-info > div")
    CONTACTS_INFO_TITLES = (By.CSS_SELECTOR, ".contacts-info p.text-h4")
    CONTACTS_INFO_PARAGRAPHS = (By.CSS_SELECTOR, ".contacts-info p:not(.text-h4)")

    # Телефоны и email
    CONTACTS_PHONES = (By.CSS_SELECTOR, ".contacts-info a[href^='tel:']")
    CONTACTS_EMAILS = (By.CSS_SELECTOR, ".contacts-info a[href^='mailto:']")

    # Адрес
    CONTACTS_ADDRESS_TEXT = (By.XPATH, "//p[contains(text(),'г. Минск') or contains(text(),'ул. Интернациональная')]")

    # Карта
    CONTACTS_MAP = (By.CSS_SELECTOR, ".contacts-map")
    CONTACTS_MAP_CANVAS = (By.CSS_SELECTOR, ".contacts-map canvas.mapboxgl-canvas")
    CONTACTS_MARKER = (By.CSS_SELECTOR, ".contacts-map .marker.mapboxgl-marker")

    # Элементы управления картой (для отладки, если нужно)
    CONTACTS_MAP_ZOOM_IN = (By.CSS_SELECTOR, ".mapboxgl-ctrl-zoom-in")
    CONTACTS_MAP_ZOOM_OUT = (By.CSS_SELECTOR, ".mapboxgl-ctrl-zoom-out")
    CONTACTS_MAP_ATTRIBUTION = (By.CSS_SELECTOR, ".mapboxgl-ctrl-attrib-inner a")



    # === INLINE-ФОРМА: Присоединяйтесь к Allsports (общая проверка формы) ===========================

    JOIN_INLINE_SECTION = (By.CSS_SELECTOR, "#getDetailsSection.section-wrapper")
    JOIN_INLINE_TITLE = (By.XPATH, "//h2[normalize-space()='Присоединяйтесь к Allsports']")
    JOIN_INLINE_FORM = (By.CSS_SELECTOR, "form.get-details__form")
    JOIN_INLINE_TABS = (By.CSS_SELECTOR, ".get-details__form-container .select-tab .select-tab__option")
    JOIN_INLINE_TAB_SELECTED = (By.CSS_SELECTOR, ".select-tab__option.select-tab__option_selected")

    # Поля формы
    JOIN_INLINE_NAME_INPUT = (By.XPATH, "//label[.//div[text()='Ваше имя']]//input[@type='text']")
    JOIN_INLINE_PHONE_INPUT = (By.XPATH, "//label[.//div[text()='Телефон']]//input[@type='tel']")
    JOIN_INLINE_EMAIL_INPUT = (By.XPATH, "//label[.//div[text()='Email']]//input[@name='email']")
    JOIN_INLINE_COMPANY_INPUT = (By.XPATH, "//label[.//div[text()='Название компании']]//input[@type='text']")

    # Подсказка под телефоном
    JOIN_INLINE_PHONE_HELP_TEXT = (By.CSS_SELECTOR, ".input__help-text")

    # Чекбокс и политика
    JOIN_INLINE_AGREE_LABEL = (By.CSS_SELECTOR, ".agreement-body label.checkbox")
    JOIN_INLINE_CHECKBOX = (By.CSS_SELECTOR, ".agreement-body input[type='checkbox']")
    JOIN_INLINE_POLICY_LINK = (By.CSS_SELECTOR, ".agreement-body a[href*='processing_personal_data']")

    # Кнопка отправки
    JOIN_INLINE_SUBMIT_BTN = (
        By.XPATH,
        "//button[@type='submit' and .//span[normalize-space()='Получить предложение']]"
    )

    # Изображение справа
    JOIN_INLINE_IMAGE = (By.CSS_SELECTOR, ".get-details__image img[loading='lazy']")

    # === Блок: Преимущества Allsports ============================================================================================================

    # === Общая секция ===
    ADV_BLOCK_SECTION = (By.CSS_SELECTOR, "section.advantages")
    ADV_BLOCK_TITLE = (By.XPATH, "//h2[normalize-space()='Преимущества Allsports']")
    ADV_BLOCK_TABS = (By.CSS_SELECTOR, "section.advantages .select-tab__option")
    ADV_BLOCK_TAB_SELECTED = (By.CSS_SELECTOR, "section.advantages .select-tab__option_selected")

    # === Список преимуществ ===
    ADV_BLOCK_LIST_ITEMS = (By.CSS_SELECTOR, ".advantages-tab:not(.advantages-tab_hidden) .advantages-text ul li span")

    # === Кнопка перехода "Список объектов" ===
    ADV_BLOCK_FACILITIES_LINK = (By.XPATH, "//a[.//span[contains(text(),'Список объектов')]]")

    # === Вкладка "Пользователям" ===
    ADVQ_TAB_USERS = (By.ID, "members")
    ADVQ_BTN_ASK = (By.XPATH,
                    "//section[contains(@class,'advantages')]//button//span[normalize-space()='Задать вопрос']")

    # --- Модалка: Задать вопрос ---
    ADVQ_MODAL = (By.CSS_SELECTOR, "div.modal")
    ADVQ_TITLE = (By.XPATH, "//div[@class='modal-header']//div[normalize-space()='Задать вопрос']")
    ADVQ_CLOSE_BTN = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    ADVQ_INPUT_NAME = (By.XPATH, "//input[@type='text' and @placeholder='Ваше имя']")
    ADVQ_INPUT_PHONE = (By.XPATH, "//input[@type='tel']")
    ADVQ_INPUT_EMAIL = (By.XPATH, "//input[@type='email']")
    ADVQ_TEXTAREA = (By.CSS_SELECTOR, ".modal textarea.text-body")
    ADVQ_CHECKBOX = (By.CSS_SELECTOR, ".modal .agreement input[type='checkbox']")
    ADVQ_POLICY_LINK = (By.CSS_SELECTOR, ".modal .agreement a[href*='policy']")
    ADVQ_SUBMIT = (By.XPATH, "//button[@type='submit']//span[normalize-space()='Отправить']")
    ADVQ_ERRORS = (By.CSS_SELECTOR, "label.input div.input-error")

    # === Вкладка "Компаниям" ===
    ADVC_TAB_COMPANIES = (By.ID, "companies")
    ADVC_BTN_GET_OFFER = (By.XPATH,
                          "//section[contains(@class,'advantages')]//button//span[normalize-space()='Получить предложение']")

    # --- Модалка: Получить предложение ---
    ADVC_MODAL = (By.CSS_SELECTOR, "div.modal")
    ADVC_TITLE_MODAL = (By.XPATH, "//div[@class='modal-header']//div[normalize-space()='Получить предложение']")
    ADVC_CLOSE_BTN = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    ADVC_INPUT_NAME = (By.XPATH, "//label[.//div[text()='Ваше имя']]//input")
    ADVC_INPUT_PHONE = (By.XPATH, "//label[.//div[text()='Телефон']]//input[@type='tel']")
    ADVC_INPUT_EMAIL = (By.XPATH, "//label[.//div[text()='Email']]//input")
    ADVC_INPUT_COMPANY = (By.XPATH, "//label[.//div[contains(text(),'Название компании')]]//input")
    ADVC_CHECKBOX = (By.CSS_SELECTOR, ".modal .agreement input[type='checkbox']")
    ADVC_POLICY_LINK = (By.CSS_SELECTOR, ".modal .agreement a[href*='policy']")
    ADVC_SUBMIT = (By.XPATH, "//button[@type='submit']//span[normalize-space()='Отправить']")

    # === Вкладка "Партнёрам" ===
    ADVP_TAB_PARTNERS = (By.ID, "partners")
    ADVP_BTN_BECOME_PARTNER = (By.XPATH,
                               "//section[contains(@class,'advantages')]//button//span[normalize-space()='Получить предложение']")

    # --- Модалка: Стать партнёром ---
    ADVP_MODAL = (By.CSS_SELECTOR, "div.modal")
    ADVP_TITLE_MODAL = (By.XPATH, "//div[@class='modal-header']//div[normalize-space()='Стать партнером']")
    ADVP_CLOSE_BTN = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    ADVP_INPUT_NAME = (By.XPATH, "//label[.//div[text()='Ваше имя']]//input")
    ADVP_INPUT_PHONE = (By.XPATH, "//label[.//div[text()='Телефон']]//input[@type='tel']")
    ADVP_INPUT_EMAIL = (By.XPATH, "//label[.//div[text()='Email']]//input")
    ADVP_INPUT_OBJECT = (By.XPATH, "//label[.//div[contains(text(),'Название объекта')]]//input")
    ADVP_CHECKBOX = (By.CSS_SELECTOR, ".modal .agreement input[type='checkbox']")
    ADVP_POLICY_LINK = (By.CSS_SELECTOR, ".modal .agreement a[href*='policy']")
    ADVP_SUBMIT = (By.XPATH, "//button[@type='submit']//span[normalize-space()='Отправить']")

    # === Блок "Преимущества Allsports" — вкладка "Компаниям" ===
    ADV_TAB_COMPANIES = (By.ID, "companies")
    ADV_COMPANY_SECTION = (By.CSS_SELECTOR, ".advantages-tab-company")
    ADV_COMPANY_TITLE = (By.CSS_SELECTOR, ".advantages-tab-company h3")
    ADV_COMPANY_LIST_ITEMS = (By.CSS_SELECTOR, ".advantages-tab-company ul li")
    ADV_COMPANY_LINK = (By.CSS_SELECTOR, ".advantages-tab-company a[href*='/companies']")

    ADV_TAB_PARTNERS = (By.CSS_SELECTOR, ".select-tab__option#partners")
    ADV_PARTNER_SECTION = (By.CSS_SELECTOR, ".advantages-tab-partner")
    ADV_PARTNER_TITLE = (By.CSS_SELECTOR, ".advantages-tab-partner h3")
    ADV_PARTNER_LINK = (By.CSS_SELECTOR, ".advantages-tab-partner .advantages-links a[href*='/partners']")








# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class CompaniesLocators:
    BASE_URL = "https://www.allsports.by/ru-by/companies"

    # === HEADER ===
    HEADER = (By.CSS_SELECTOR, "header.header")
    HEADER_LOGO = (By.CSS_SELECTOR, ".header-navbar__logo img[alt='allsports']")
    HEADER_BTN_OFFER = (By.ID, "offer-btn")
    HEADER_BTN_QUESTION = (By.XPATH, "//button//span[contains(text(),'Задать вопрос')]")

    # === PROMO BLOCK ===
    PROMO_SECTION = (By.CSS_SELECTOR, "section.suggestion")
    PROMO_TITLE = (By.XPATH, "//h1[normalize-space()='Allsports']")
    PROMO_IMG = (By.CSS_SELECTOR, ".suggestion-images picture img")
    BTN_GET_OFFER = (By.XPATH, "//button//span[contains(text(),'Получить предложение')]")
    BTN_ASK_QUESTION = (By.XPATH, "//button//span[contains(text(),'Задать вопрос')]")

    # === MODAL FORMS ===
    MODAL = (By.CSS_SELECTOR, "div.modal")
    MODAL_HEADER = (By.CSS_SELECTOR, ".modal-header div")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".modal-header button.icon-btn")
    MODAL_INPUT_NAME = (By.XPATH, "//input[@placeholder='Ваше имя' or @placeholder='Ваше имя*']")
    MODAL_INPUT_PHONE = (By.XPATH, "//input[@type='tel']")
    MODAL_INPUT_EMAIL = (By.XPATH, "//input[@type='email' or @name='email']")
    MODAL_INPUT_COMPANY = (By.XPATH, "//input[@placeholder='Компания' or @placeholder='Название компании*']")
    MODAL_INPUT_CITY = (By.XPATH, "//input[@placeholder='Введите город']")
    MODAL_TEXTAREA = (By.TAG_NAME, "textarea")
    MODAL_CHECKBOX = (By.CSS_SELECTOR, ".agreement label.checkbox input")
    MODAL_BTN_SUBMIT = (By.XPATH, "//button[@type='submit']")
    MODAL_POLICY_LINK = (By.XPATH, "//a[contains(@href,'policy')]")
    MODAL_PHONE_LINK = (By.XPATH, "//a[contains(@href,'tel:')]")

    # === BENEFITS SECTION ===
    BENEFIT_SECTION = (By.ID, "benefitSection")
    BENEFIT_TITLE = (By.XPATH, "//*[@id='benefitSection']//h2[normalize-space()='Преимущества']")
    BENEFIT_ITEMS = (By.CSS_SELECTOR, "#benefitSection li.item")
    BENEFIT_TEXTS = (By.CSS_SELECTOR, "#benefitSection li.item p:not(:has(svg))")
    BENEFIT_NEXT = (By.CSS_SELECTOR, "#benefitSection .scroll-slider-control__next")
    BENEFIT_PREV = (By.CSS_SELECTOR, "#benefitSection .scroll-slider-control__prev")

    # === COOPERATION SECTION ===
    COOP_SECTION = (By.ID, "cooperationSection")
    COOP_TITLE = (By.XPATH, "//*[@id='cooperationSection']//h2[contains(.,'Сотрудничать')]")
    COOP_ITEMS = (By.CSS_SELECTOR, "#cooperationSection li.item")
    COOP_TEXTS = (By.CSS_SELECTOR, "#cooperationSection li.item p")
    COOP_NEXT = (By.CSS_SELECTOR, "#cooperationSection .scroll-slider-control__next")
    COOP_PREV = (By.CSS_SELECTOR, "#cooperationSection .scroll-slider-control__prev")

    # === FEEDBACK SECTION ===
    FEEDBACK_SECTION = (By.XPATH, "//*[@id='partnersLogoSection']")
    FEEDBACK_TITLE = (By.XPATH, "//*[@id='feedbackSection']//h2[normalize-space()='Нам доверяют']")
    FEEDBACK_ITEMS = (By.CSS_SELECTOR, "#feedbackSection li.item")
    FEEDBACK_COMPANY_LOGOS = (By.CSS_SELECTOR, "#feedbackSection li.item picture img")
    FEEDBACK_TEXTS = (By.CSS_SELECTOR, "#feedbackSection li.item p")
    FEEDBACK_LINKS = (By.XPATH, "//a[contains(text(),'Читать отзыв')]")
    FEEDBACK_MODAL = (By.CSS_SELECTOR, "div.modal")
    FEEDBACK_MODAL_TITLE = (By.CSS_SELECTOR, ".modal-header div")
    FEEDBACK_MODAL_BODY = (By.CSS_SELECTOR, ".modal-body span")

    # === FOOTER ===
    FOOTER = (By.CSS_SELECTOR, "footer.footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a")
    FOOTER_COMPANY_INFO = (By.XPATH, "//div[contains(text(),'ООО') or contains(text(),'Allsports')]")

    # === VALID DATA (для форм) ===
    VALID_NAME = "Олег"
    VALID_PHONE = "375297000000"
    VALID_EMAIL = "oleg@example.com"
    VALID_COMPANY = "ООО Автотест"
    VALID_CITY = "Минск"

    """Локаторы элементов блока FAQ (Часто задаваемые вопросы)."""

    # === БАЗОВЫЕ ЭЛЕМЕНТЫ ===
    FAQ_SECTION = (By.CSS_SELECTOR, "section.faq")
    FAQ_TITLE = (By.XPATH, "//h2[normalize-space()='Часто задаваемые вопросы']")
    FAQ_CONTAINER = (By.CSS_SELECTOR, ".faq-container")
    FAQ_LIST = (By.CSS_SELECTOR, ".faq-list")
    FAQ_ITEMS = (By.CSS_SELECTOR, ".faq-list .expansion-item")
    FAQ_QUESTIONS = (By.CSS_SELECTOR, ".expansion-item-title h5")
    FAQ_ANSWERS = (By.CSS_SELECTOR, ".expansion-item-text")
    FAQ_ARROWS = (By.CSS_SELECTOR, ".expansion-item__arrow svg")

    # === ССЫЛКА ДЛЯ ПАРТНЁРОВ ===
    FAQ_PARTNERS_BLOCK = (By.CSS_SELECTOR, ".faq-links")
    FAQ_PARTNERS_LINK = (By.XPATH, "//a[contains(@href,'/partners')]")

    # === ФОРМА "Не нашли ответ?" ===
    FAQ_FORM = (By.CSS_SELECTOR, ".faq-form")
    FAQ_FORM_TITLE = (By.XPATH, "//h5[contains(text(),'Не нашли ответ')]")
    FAQ_FORM_BUTTON = (By.XPATH, "//button//span[contains(text(),'Задать вопрос')]")

    # === ТЕКСТОВЫЕ ЭТАЛОНЫ ДЛЯ СРАВНЕНИЙ ===
    EXPECTED_QUESTIONS = [
        "Что такое Allsports и как он работает?",
        "Как подключить сотрудников компании к сервису Allsports?",
        "Как поменять список сотрудников?",
        "Чем отличаются типы подписок?",
        "Какие преимущества для компаний предоставляет Allsports?",
        "На какой срок можно оформить подписку и какие условия оплаты?",
        "Облагаются ли компенсации за спорт дополнительными налогами?",
        "Как узнать цены подписок?",
        "Можно поменять тип подписки для сотрудника?",
        "Мы забыли оплатить сервис. Что произойдёт?",
        "Что такое архивные подписки и как их подключить?",
    ]

    # =====================
    # CONTACTS
    # =====================
    CONTACTS_SECTION = (By.ID, "contactsSection")
    CONTACTS_CONTAINER = (By.CSS_SELECTOR, "#contactsSection .contacts-container")
    CONTACTS_INFO = (By.CSS_SELECTOR, "#contactsSection .contacts-info")
    CONTACTS_INFO_BLOCKS = (By.CSS_SELECTOR, "#contactsSection .contacts-info > div")
    CONTACTS_MAP = (By.CSS_SELECTOR, "#contactsSection .contacts-map")
    CONTACTS_MAP_CANVAS = (By.CSS_SELECTOR, "#contactsSection canvas.mapboxgl-canvas")
    CONTACTS_MARKER = (By.CSS_SELECTOR, "#contactsSection .mapboxgl-marker")

    # =====================
    # FORM
    # =====================

    # ====== HEADER ======
    HEADER_OFFER_BTN = (By.ID, "offer-btn")  # "Получить предложение"
    HEADER_ASK_BTN = (By.XPATH,
                      "//button[contains(@class,'header-controls__offer')][.//span[contains(.,'Задать вопрос')]]")

    # ====== PROMO (кнопки в первом экране) ======
    PROMO_OFFER_BTN = (By.XPATH,
                       "//section[contains(@class,'section')][.//span[contains(.,'Получить предложение')]]//button[.//span[contains(.,'Получить предложение')]]")
    PROMO_ASK_BTN = (By.XPATH,
                     "//section[contains(@class,'section')][.//span[contains(.,'Задать вопрос')]]//button[.//span[contains(.,'Задать вопрос')]]")

    # ====== FAQ (кнопка внизу FAQ) ======
    FAQ_ASK_BTN = (By.XPATH, "//button[.//span[contains(.,'Задать вопрос')]]")

    # --- INLINE JOIN FORM ("Присоединяйтесь к Allsports") ---
    JOIN_SECTION = (By.ID, "getDetailsSection")
    JOIN_FORM = (By.CSS_SELECTOR, "#getDetailsSection form.get-details__form")
    JOIN_POLICY_LINK = (By.CSS_SELECTOR, "#getDetailsSection .agreement a")
    JOIN_SUBMIT_BTN = (By.CSS_SELECTOR, "#getDetailsSection button.get-details__button")  # ✅ Исправленный вариант

    JOIN_NAME_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[placeholder='Ваше имя']")
    JOIN_PHONE_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[name='phone']")
    JOIN_EMAIL_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[name='email']")
    JOIN_COMPANY_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[placeholder='Компания']")
    JOIN_AGREE_LABEL = (By.CSS_SELECTOR, "#getDetailsSection label.checkbox")

    # ====== COMMON MODAL ======
    MODAL = (By.CSS_SELECTOR, "div.modal")
    MODAL_TITLE = (By.CSS_SELECTOR, "div.modal .modal-header > div")
    MODAL_CLOSE = (By.CSS_SELECTOR, "div.modal .modal-header .icon-btn")
    MODAL_FORM = (By.CSS_SELECTOR, "div.modal form.modal-form")
    MODAL_SUBMIT_BTN = (By.CSS_SELECTOR, "div.modal .modal-form-control button.btn")
    MODAL_POLICY_LINK = (By.CSS_SELECTOR, "div.modal .agreement a[href*='policy']")
    MODAL_AGREE_INPUT = (By.CSS_SELECTOR, "div.modal .agreement label.checkbox > input")
    MODAL_AGREE_LABEL = (By.CSS_SELECTOR, "div.modal .agreement label.checkbox")
    MODAL_PHONE_LINK = (By.CSS_SELECTOR, "div.modal a.modal-body__phone")

    # Поля ввода в модалках (универсальные локаторы по заголовкам плейсхолдеров)
    MODAL_NAME_INPUT = (By.XPATH, "//div[contains(@class,'modal')]//label[.//div[contains(.,'Ваше имя')]]//input")
    MODAL_PHONE_INPUT = (By.XPATH,
                         "//div[contains(@class,'modal')]//label[.//div[contains(.,'Телефон')]]//input[@name='phone']")
    MODAL_EMAIL_INPUT = (By.XPATH,
                         "//div[contains(@class,'modal')]//label[.//div[contains(.,'Email')]]//input[@name='email' or @type='text']")
    MODAL_COMPANY_INPUT = (By.XPATH,
                           "//div[contains(@class,'modal')]//label[.//div[contains(.,'Название компании')]]//input")
    MODAL_OBJECT_INPUT = (By.XPATH,
                          "//div[contains(@class,'modal')]//label[.//div[contains(.,'Название объекта')]]//input")
    MODAL_CITY_INPUT = (By.XPATH, "//div[contains(@class,'modal')]//label[.//div[contains(.,'Город')]]//input")
    MODAL_TEXTAREA_QUESTION = (By.XPATH,
                               "//div[contains(@class,'modal')]//label[contains(@class,'textarea')]//textarea")

    # Ошибки под полями в модалках (браузер показывает их после потери фокуса)
    MODAL_PHONE_ERROR = (By.CSS_SELECTOR, ".input-error__text")
    MODAL_EMAIL_ERROR = (By.CSS_SELECTOR, ".input-error__text")

    # === SUCCESS MODAL (после отправки формы) ===
    SUCCESS_MODAL = (By.CSS_SELECTOR, "div.modal")
    SUCCESS_TEXT = (By.XPATH, "//div[contains(text(),'Спасибо за ваш запрос')]")
    SUCCESS_CLOSE_BTN = (By.XPATH, "//button//span[text()='Закрыть']")

    # === COMMON ===
    COOKIE_ACCEPT_BTN = (By.CSS_SELECTOR, "button.cookie-accept, button[data-test='cookie-accept']")
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(),'Компаниям')]")

    # ===================== SUBSCRIPTION BLOCK =====================

    # Основные карточки (обычные)
    SUBSCRIPTION_CARDS = (By.CSS_SELECTOR, ".scroll-slider-card__carousel--item")
    SUBSCRIPTION_CARD_TITLE = (By.CSS_SELECTOR, ".level-card__main h2.text-20-600")
    SUBSCRIPTION_CARD_TEXTS = (By.CSS_SELECTOR, ".level-card__main-description-text p.text-body")
    SUBSCRIPTION_CARD_MISC = (By.CSS_SELECTOR, ".level-card__misc p.text-body")
    SUBSCRIPTION_LINK_OBJECTS = (By.XPATH, ".//span[contains(text(),'Объекты подписки')]")
    SUBSCRIPTION_LINK_TABLE = (By.XPATH, ".//span[contains(text(),'Список объектов (таблица)')]")

    # Кнопка и модалка архивных типов подписок
    SUBSCRIPTIONS_ARCHIVE_BTN = (By.XPATH, "//button[.//span[contains(text(),'Архивные типы подписок')]]")
    SUBSCRIPTIONS_ARCHIVE_MODAL = (By.CSS_SELECTOR, "div.modal")
    SUBSCRIPTIONS_ARCHIVE_CLOSE = (By.CSS_SELECTOR, "div.modal button.icon-btn")

    # Карточки в модалке "Архивные подписки"
    SUBSCRIPTIONS_ARCHIVE_CARDS = (By.CSS_SELECTOR, "div.modal .level-card-wrapper")
    SUBSCRIPTIONS_ARCHIVE_CARD_TITLE = (By.CSS_SELECTOR, "div.modal .level-card__main h2.text-20-600")
    SUBSCRIPTIONS_ARCHIVE_CARD_TEXTS = (By.CSS_SELECTOR, "div.modal .level-card__main-description-text p.text-body")
    SUBSCRIPTIONS_ARCHIVE_CARD_MISC = (By.CSS_SELECTOR, "div.modal .level-card__misc p.text-body")
    SUBSCRIPTIONS_ARCHIVE_LINK_OBJECTS = (By.XPATH, ".//span[contains(text(),'Объекты подписки')]")
    SUBSCRIPTIONS_ARCHIVE_LINK_TABLE = (By.XPATH, ".//span[contains(text(),'Список объектов (таблица)')]")

    # Страница "Объекты подписки" (проверка фильтра)
    FACILITIES_SELECT_VALUE = (By.CSS_SELECTOR, ".select__value-container .select__single-value")

    # Страница "Список объектов (таблица)"
    FACILITIES_TABLE_TITLE = (By.CSS_SELECTOR, "h1.text-h3, h2.text-h3")
    FACILITIES_TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")


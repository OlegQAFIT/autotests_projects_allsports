# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

class LevelsLocators:
    """Локаторы для страницы https://www.allsports.by/ru-by/levels"""

    BASE_URL = "https://www.allsports.by/ru-by/levels"

    # === HEADER ===
    HEADER = (By.CSS_SELECTOR, "header.header")
    HEADER_LOGO = (By.CSS_SELECTOR, ".header-navbar__logo img[alt='allsports']")
    HEADER_BTN_OFFER = (By.ID, "offer-btn")
    HEADER_BTN_QUESTION = (By.XPATH, "//button//span[contains(text(),'Задать вопрос')]")

    # === SUBSCRIPTION LEVELS SECTION ===
    LEVELS_SECTION = (By.CSS_SELECTOR, "section.level-section-wrapper h2.level-section-title")
    SUBSCRIPTION_CARDS = (By.CSS_SELECTOR, ".scroll-slider-card__carousel--item, .level-card-wrapper")
    SUBSCRIPTION_CARD_TITLE = (By.CSS_SELECTOR, ".level-card__main h2.text-20-600")
    SUBSCRIPTION_CARD_TEXTS = (By.CSS_SELECTOR, ".level-card__main-description-text p.text-body")
    SUBSCRIPTION_CARD_MISC = (By.CSS_SELECTOR, ".level-card__misc p.text-body")
    SUBSCRIPTION_LINK_OBJECTS = (By.XPATH, ".//span[contains(text(),'Объекты подписки')]/ancestor::a")
    SUBSCRIPTION_LINK_TABLE = (By.XPATH, ".//span[contains(text(),'Список объектов (таблица)')]/ancestor::a")

    # === ARCHIVE LEVELS ===
    ARCHIVE_BTN = (By.XPATH, "//button//span[contains(text(),'Архивные типы подписок')]/ancestor::button")
    ARCHIVE_MODAL = (By.CSS_SELECTOR, "div.modal")
    ARCHIVE_CLOSE = (By.CSS_SELECTOR, "div.modal button.icon-btn")
    SUBSCRIPTIONS_ARCHIVE_CARDS = (By.CSS_SELECTOR, "div.modal .level-card-wrapper")
    SUBSCRIPTIONS_ARCHIVE_CARD_TITLE = (By.CSS_SELECTOR, "div.modal .level-card__main h2.text-20-600")
    SUBSCRIPTIONS_ARCHIVE_CARD_TEXTS = (By.CSS_SELECTOR, "div.modal .level-card__main-description-text p.text-body")
    SUBSCRIPTIONS_ARCHIVE_CARD_MISC = (By.CSS_SELECTOR, "div.modal .level-card__misc p.text-body")
    SUBSCRIPTIONS_ARCHIVE_LINK_OBJECTS = (By.XPATH, ".//span[contains(text(),'Объекты подписки')]/ancestor::a")
    SUBSCRIPTIONS_ARCHIVE_LINK_TABLE = (By.XPATH, ".//span[contains(text(),'Список объектов (таблица)')]/ancestor::a")

    # === FACILITIES PAGES ===
    FACILITIES_SELECT_VALUE = (By.CSS_SELECTOR, "span.select-field__value, .select__value-container .select__single-value")
    FACILITIES_TABLE_TITLE = (By.CSS_SELECTOR, "h1.text-h3, h2.text-h3")
    FACILITIES_TABLE_ROWS = (By.CSS_SELECTOR, "div.facilities-table__row, table tbody tr")

    # === INLINE JOIN FORM (Присоединяйтесь к Allsports) ===
    JOIN_SECTION = (By.ID, "getDetailsSection")
    JOIN_FORM = (By.CSS_SELECTOR, "#getDetailsSection form.get-details__form")
    JOIN_NAME_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[placeholder='Ваше имя']")
    JOIN_PHONE_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[name='phone']")
    JOIN_EMAIL_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[name='email']")
    JOIN_COMPANY_INPUT = (By.CSS_SELECTOR, "#getDetailsSection input[placeholder='Компания']")
    JOIN_AGREE_LABEL = (By.CSS_SELECTOR, "#getDetailsSection label.checkbox")
    JOIN_POLICY_LINK = (By.CSS_SELECTOR, "#getDetailsSection .agreement a")
    JOIN_SUBMIT_BTN = (By.CSS_SELECTOR, "#getDetailsSection button.get-details__button")
    JOIN_PHONE_ERROR = (By.CSS_SELECTOR, "#getDetailsSection .input-error")
    JOIN_EMAIL_ERROR = (By.CSS_SELECTOR, "#getDetailsSection .input-error")

    # === SUCCESS MODAL ===
    SUCCESS_MODAL = (By.CSS_SELECTOR, "div.modal")
    SUCCESS_TEXT = (By.XPATH, "//div[contains(text(),'Спасибо за ваш запрос')]")
    SUCCESS_CLOSE_BTN = (By.XPATH, "//button//span[text()='Закрыть']")

    # === COMMON ===
    COOKIE_ACCEPT_BTN = (By.CSS_SELECTOR, "button.cookie-accept, button[data-test='cookie-accept']")

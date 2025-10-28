# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class PartnersLocators:
    BASE_URL = "https://www.allsports.by/ru-by/partners"

    # --- PROMO ---
    PROMO_BLOCK = (By.CSS_SELECTOR, ".suggestion-text")
    PROMO_TITLE = (By.XPATH, "//p[contains(@class,'text-h1') and normalize-space()='Allsports']")
    PROMO_SUBTITLE = (By.XPATH, "//p[contains(@class,'text-h1') and contains(.,'Для партнеров')]")
    PROMO_DESC = (By.CSS_SELECTOR, ".suggestion__description")
    BTN_BECOME_PARTNER = (By.XPATH, "//button[.//span[text()='Стать партнером']]")
    BTN_ASK_QUESTION = (By.XPATH, "(//div[@class='suggestion-text']//button)[2]")


    # --- BENEFITS ---
    BENEFITS_SECTION = (By.ID, "benefitSection")
    BENEFITS_TITLE = (By.XPATH, "//*[@id='benefitSection']//h2[normalize-space()='Преимущества']")
    BENEFITS_ITEMS = (By.CSS_SELECTOR, "#benefitSection li.item")
    BENEFITS_NEXT = (By.CSS_SELECTOR, "#benefitSection .scroll-slider-control__next")
    BENEFITS_PREV = (By.CSS_SELECTOR, "#benefitSection .scroll-slider-control__prev")

    # --- COOPERATION ---
    COOP_SECTION = (By.CSS_SELECTOR, "section.cooperation")
    COOP_TITLE = (By.XPATH, "//h2[contains(.,'Сотрудничать')]")
    COOP_ITEMS = (By.CSS_SELECTOR, "section.cooperation ul li.item")
    COOP_NEXT = (By.CSS_SELECTOR, "section.cooperation .scroll-slider-control__next")
    COOP_PREV = (By.CSS_SELECTOR, "section.cooperation .scroll-slider-control__prev")

    # --- VIDEO ---
    VIDEO_IFRAME = (By.CSS_SELECTOR, "#videoSection iframe")
    VIDEO_SECTION = (By.ID, "videoSection")

    # --- JOIN FORM ---
    JOIN_SECTION = (By.ID, "getDetailsSection")
    JOIN_TITLE = (By.XPATH, "//h2[contains(.,'Присоединяйтесь')]")
    JOIN_INPUT_NAME = (By.XPATH, "//input[@placeholder='Ваше имя']")
    JOIN_INPUT_PHONE = (By.XPATH, "//input[@type='tel']")
    JOIN_INPUT_EMAIL = (By.XPATH, "//input[@name='email']")
    JOIN_INPUT_COMPANY = (By.XPATH, "//input[@placeholder='Название объекта']")
    JOIN_CHECKBOX = (By.CSS_SELECTOR, "#getDetailsSection label.checkbox")
    JOIN_BUTTON = (By.CSS_SELECTOR, "button.get-details__button[type='submit']")
    JOIN_POLICY_LINK = (By.XPATH, "//a[contains(@href,'policy')]")

    # --- FAQ ---
    FAQ_SECTION = (By.CSS_SELECTOR, "#faqSection")
    FAQ_TITLE = (By.XPATH, "//h2[normalize-space()='Часто задаваемые вопросы']")
    FAQ_ITEMS = (By.CSS_SELECTOR, ".faq .expansion-item")
    FAQ_QUESTIONS = (By.CSS_SELECTOR, "section.faq .expansion-item-title h5")
    FAQ_BUTTON = (By.XPATH, "//button[.//span[text()='Задать вопрос']]")

    # --- CONTACTS ---
    CONTACTS_SECTION = (By.CSS_SELECTOR, "#contactsSection")
    CONTACTS_TITLE = (By.XPATH, "//h2[normalize-space()='Наши контакты']")
    CONTACTS_PHONE = (By.XPATH, "//a[starts-with(@href,'tel:')]")
    CONTACTS_EMAIL = (By.XPATH, "//a[starts-with(@href,'mailto:')]")
    CONTACTS_ADDRESS = (By.XPATH, "//p[contains(.,'Минск')]")
    MAP_CANVAS = (By.CSS_SELECTOR, ".mapboxgl-canvas")
    MAP_ZOOM_IN = (By.CSS_SELECTOR, ".mapboxgl-ctrl-zoom-in")
    MAP_ZOOM_OUT = (By.CSS_SELECTOR, ".mapboxgl-ctrl-zoom-out")

    # --- VALID DATA ---
    VALID_NAME = "Олег"
    VALID_PHONE = "375297000000"
    VALID_EMAIL = "oleg@example.com"
    VALID_COMPANY = "ООО Автотест"

# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By



class HeaderLocators:
    BASE_URL = "https://www.allsports.by/ru-by"

    # --- Основные элементы ---
    LOGO = (By.XPATH, "//header//a[contains(@class,'header-navbar__logo')]")
    LOGO_IMG = (By.XPATH, "//header//a[contains(@class,'header-navbar__logo')]//img")

    # --- Навигационные ссылки ---
    FACILITIES = (By.XPATH, "//header//a[@href='/ru-by/facilities']")
    LEVELS = (By.XPATH, "//header//a[@href='/ru-by/levels']")
    COMPANIES = (By.XPATH, "//header//a[@href='/ru-by/companies']")
    PARTNERS = (By.XPATH, "//header//a[@href='/ru-by/partners']")
    CONTACTS = (By.XPATH, "//header//a[@href='/ru-by/contacts']")

    # --- URL и тексты для проверок ---
    URL_FACILITIES = "https://www.allsports.by/ru-by/facilities"
    URL_LEVELS = "https://www.allsports.by/ru-by/levels"
    URL_COMPANIES = "https://www.allsports.by/ru-by/companies"
    URL_PARTNERS = "https://www.allsports.by/ru-by/partners"
    URL_CONTACTS = "https://www.allsports.by/ru-by/contacts"

    TEXT_FACILITIES = "Объекты"
    TEXT_LEVELS = "Типы подписок"
    TEXT_COMPANIES_H1 = "Компаниям"
    TEXT_PARTNERS_H1 = "Партнерам"
    TEXT_CONTACTS = "Контакты"

    # --- Кнопки Header ---
    BUTTON_GET_OFFER_HEADER = (By.XPATH, "//button[@id='offer-btn']")
    BUTTON_ASK_QUESTION = (By.XPATH, "//button[contains(.,'Задать вопрос')]")

    # --- Модалка «Получить предложение» ---
    MODAL_HEADER = (By.XPATH, "//div[contains(@class,'modal-header')]//div[contains(text(),'Получить предложение')]")
    TAB_CONNECT_COMPANY = (By.XPATH, "//li[@id='get-offer' or @id='getOffer']")
    TAB_BECOME_PARTNER = (By.XPATH, "//li[@id='become-partner' or @id='becomePartner']")

    INPUT_NAME = (By.XPATH, "//label//input[@type='text' and @placeholder='Ваше имя']")
    INPUT_PHONE = (By.XPATH, "//label//input[@type='tel']")
    INPUT_EMAIL = (By.XPATH, "//label//input[@type='text' and contains(@placeholder,'@')]")
    INPUT_COMPANY = (By.XPATH, "//label//input[@placeholder='Компания' or @placeholder='Название объекта']")
    INPUT_CITY = (By.XPATH, "//label//input[@placeholder='Введите город']")

    CHECKBOX_POLICY = (By.XPATH, "//label[contains(@class, 'checkbox')]")
    LINK_POLICY = (By.XPATH, "//a[contains(@href,'/policy/251010_processing_personal_data')]")
    BUTTON_SEND = (By.XPATH, "//form[contains(@class,'modal-form')]//button[contains(@class,'btn') and .//span[text()='Отправить']]")
    BUTTON_CLOSE = (By.XPATH, "//button[contains(@class,'icon-btn')]")
    BUTTON_SEND_1 = (By.XPATH, "//button[@type='submit']")

    # --- Модалка «Задать вопрос» ---
    INPUT_QUESTION_NAME = (By.XPATH, "//form//input[@type='text' and @placeholder='Ваше имя']")
    INPUT_QUESTION_PHONE = (By.XPATH, "//form//input[@type='tel']")
    INPUT_QUESTION_TEXT = (By.XPATH, "//form//textarea")
    CHECKBOX_QUESTION = (By.XPATH, "//form//label[contains(@class,'checkbox')]//input")
    BUTTON_SEND_QUESTION = (By.XPATH, "//form//button[contains(.,'Отправить')]")

    ERROR_NAME = "//div[contains(@class, 'input-error') and contains(text(), 'Введите имя')]"
    ERROR_EMAIL = "//label[contains(@class, 'input')]//div[@class='input-error']/span"
    ERROR_PHONE = (By.XPATH, "//label[contains(., 'Телефон')]//span[contains(text(),'Неверный формат номера')]")


# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class FooterLocators:
    BASE_URL = "https://www.allsports.by/"

    # --- Контактная информация ---
    PHONE = (By.XPATH, "//footer//a[contains(@href, 'tel') and contains(translate(., '  ', ' '), '+375')]")
    EMAIL = (By.XPATH, "//footer//a[contains(@href, 'mailto') and contains(., 'contact@allsports.by')]")

    # --- Соцсети ---
    INSTAGRAM = (By.XPATH, "//footer//a[contains(@href, 'instagram.com')]")
    LINKEDIN = (By.XPATH, "//footer//a[contains(@href, 'linkedin.com')]")

    # --- Магазины приложений ---
    APPSTORE = (By.XPATH, "//footer//a[contains(@href, 'apps.apple.com')]")
    GOOGLEPLAY = (By.XPATH, "//footer//a[contains(@href, 'play.google.com')]")
    APPGALLERY = (By.XPATH, "//footer//a[contains(@href, 'appgallery.huawei.com')]")

    # --- Навигация футера ---
    NAV_COMPANIES = (By.XPATH, "//footer//a[contains(@href, '/companies')]")
    NAV_PARTNERS = (By.XPATH, "//footer//a[contains(@href, '/partners')]")
    NAV_FACILITIES = (By.XPATH, "//footer//a[contains(@href, '/facilities')]")
    NAV_LEVELS = (By.XPATH, "//footer//a[contains(@href, '/levels')]")
    NAV_CONTACTS = (By.XPATH, "//footer//a[contains(@href, '/contacts')]")

    # --- Дополнительные ссылки футера ---
    NAV_LICENSE = (By.XPATH, "//footer//a[contains(@href, '/license')]")
    NAV_USER_AGR = (By.XPATH, "//footer//a[contains(@href, '/user-agreements')]")

    # --- Тексты и URL-адреса ---
    COMPANIES_URL = "https://www.allsports.by/ru-by/companies"
    PARTNERS_URL = "https://www.allsports.by/ru-by/partners"
    FACILITIES_URL = "https://www.allsports.by/ru-by/facilities"
    LEVELS_URL = "https://www.allsports.by/ru-by/levels"
    CONTACTS_URL = "https://www.allsports.by/ru-by/contacts"

    TEXT_COMPANIES_H1 = "Компаниям"
    TEXT_PARTNERS_H1 = "Партнерам"
    TEXT_FACILITIES = "Объекты"
    TEXT_LEVELS = "Типы подписок"
    TEXT_CONTACTS = "Контакты"

    # --- Копирайт и реквизиты ---
    COPYRIGHT = (By.XPATH, "//footer//*[contains(text(), '©')]")
    PROVIDER_NUMBER = (By.XPATH, "//footer//a[contains(@href, '/providing-payment-service-rules')]")


    # --- Документы ---
    POLICY_PD = "https://www.allsports.by/ru-by/policy/251010_processing_personal_data"
    LICENSE_INTERMEDIARY = "https://www.allsports.by/ru-by/license/241009_license"
    USER_AGREEMENTS = "https://www.allsports.by/ru-by/user-agreements"
    INDIVIDUAL_LICENSE = "https://www.allsports.by/ru-by/individual_license/241009_license"
    RULE_ACCESS = "https://www.allsports.by/ru-by/rule/250731_rule"
    COOKIE_POLICY = "https://www.allsports.by/ru-by/cookie/cookie-policy"

    TEXT_DOC_PD = "Политика компании в отношении обработки персональных данных"
    TEXT_DOC_INTERMEDIARY = "Договор возмездного оказания посреднических услуг"
    TEXT_INDIVIDUAL_AGR = "Пользовательское соглашение держателей Карт Allsports"
    TEXT_RULE_ACCESS = "Правила доступа в спортивные объекты"
    TEXT_COOKIE_POLICY = "Политика в отношении обработки cookie"

# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class AppPageLocators:
    BASE_URL = "https://www.allsports.by/ru-by/app"

    COOKIE_ACCEPT_BTN = (By.CSS_SELECTOR, ".cookie-primary-modal__confirm")
    PAGE_ROOT = (By.CSS_SELECTOR, "main, #defaultView")
    DOWNLOAD_HEADING = (By.XPATH, "//h2[contains(normalize-space(),'Скачать приложение Allsports')]")

    APPLE_LINKS = (By.XPATH, "//a[contains(@href,'apps.apple.com')]")
    GOOGLE_LINKS = (By.XPATH, "//a[contains(@href,'play.google.com')]")
    HUAWEI_LINKS = (By.XPATH, "//a[contains(@href,'appgallery.huawei.com')]")

    CANONICAL_LINK = (By.CSS_SELECTOR, "link[rel='canonical']")

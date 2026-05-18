# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class AppPageLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy/app"

    PAGE_ROOT = (By.CSS_SELECTOR, "main, #defaultView")
    DOWNLOAD_HEADING = (By.XPATH, "//h2[contains(normalize-space(),'Download the Sportbenefit App')]")

    APPLE_LINKS = (By.XPATH, "//a[contains(@href,'apps.apple.com')]")
    GOOGLE_LINKS = (By.XPATH, "//a[contains(@href,'play.google.com')]")
    HUAWEI_LINKS = (By.XPATH, "//a[contains(@href,'appgallery.huawei.com')]")
    APK_LINKS = (By.XPATH, "//a[contains(@href,'.apk')]")

    CANONICAL_LINK = (By.CSS_SELECTOR, "link[rel='canonical']")

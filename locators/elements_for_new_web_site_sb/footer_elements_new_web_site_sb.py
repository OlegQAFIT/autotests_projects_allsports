# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class FooterLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy"

    FOOTER_ROOT = (By.CSS_SELECTOR, "footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a[href]")

    PHONE = (By.CSS_SELECTOR, "footer a[href^='tel:']")
    EMAIL = (By.CSS_SELECTOR, "footer a[href^='mailto:']")

    LINKEDIN = (By.CSS_SELECTOR, "footer a[href*='linkedin.com']")
    INSTAGRAM = (By.CSS_SELECTOR, "footer a[href*='instagram.com']")
    FACEBOOK = (By.CSS_SELECTOR, "footer a[href*='facebook.com']")

    APPLE = (By.CSS_SELECTOR, "footer a[href*='apps.apple.com']")
    GOOGLE = (By.CSS_SELECTOR, "footer a[href*='play.google.com']")
    HUAWEI = (By.CSS_SELECTOR, "footer a[href*='appgallery.huawei.com']")

    NAV_COMPANIES = (By.CSS_SELECTOR, "footer a[href*='/en-cy/companies']")
    NAV_PARTNERS = (By.CSS_SELECTOR, "footer a[href*='/en-cy/partners']")
    NAV_FACILITIES = (By.CSS_SELECTOR, "footer a[href*='/en-cy/facilities']")
    NAV_LEVELS = (By.CSS_SELECTOR, "footer a[href*='/en-cy/levels']")
    NAV_CONTACTS = (By.CSS_SELECTOR, "footer a[href*='/en-cy/contacts']")

    LEGAL_LICENSE = (By.CSS_SELECTOR, "footer a[href*='/en-cy/license']")
    LEGAL_USER_AGREEMENTS = (By.CSS_SELECTOR, "footer a[href*='/en-cy/user-agreements']")

# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class HeaderLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy"

    HEADER_LINKS = (By.CSS_SELECTOR, "header a[href]")

    LINK_HOME = (By.CSS_SELECTOR, "header a[href='/en-cy'], header a[href='/en-cy/'], header a[href='https://www.sportbenefit.eu/en-cy']")
    LINK_FACILITIES = (By.CSS_SELECTOR, "header a[href*='/en-cy/facilities']")
    LINK_LEVELS = (By.CSS_SELECTOR, "header a[href*='/en-cy/levels']")
    LINK_COMPANIES = (By.CSS_SELECTOR, "header a[href*='/en-cy/companies']")
    LINK_PARTNERS = (By.CSS_SELECTOR, "header a[href*='/en-cy/partners']")
    LINK_CONTACTS = (By.CSS_SELECTOR, "header a[href*='/en-cy/contacts']")

    CTA_GET_OFFER = (
        By.XPATH,
        "//button[.//span[contains(normalize-space(),'Get an Offer')] or contains(normalize-space(),'Get an Offer')]",
    )

    MODAL = (By.CSS_SELECTOR, "div.modal")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    MODAL_TABS = (By.CSS_SELECTOR, ".modal .select-tab__option")
    MODAL_INPUTS = (By.CSS_SELECTOR, ".modal input, .modal textarea")
    MODAL_SEND_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal')]//button[.//span[normalize-space()='Send'] or normalize-space()='Send']",
    )

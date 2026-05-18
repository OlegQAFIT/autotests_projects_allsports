# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class MainPageLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy"

    PAGE_ROOT = (By.TAG_NAME, "body")
    HEADER = (By.CSS_SELECTOR, "header")
    FOOTER = (By.CSS_SELECTOR, "footer")

    CTA_GET_OFFER = (
        By.XPATH,
        "//button[.//span[contains(normalize-space(),'Get an Offer')] or contains(normalize-space(),'Get an Offer')]",
    )
    CTA_ASK_QUESTION = (
        By.XPATH,
        "//button[.//span[contains(normalize-space(),'Ask Us a Question')] or contains(normalize-space(),'Ask Us a Question')]",
    )

    MODAL = (By.CSS_SELECTOR, "div.modal")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".modal-header .icon-btn")
    MODAL_TABS = (By.CSS_SELECTOR, ".modal .select-tab__option")
    MODAL_INPUTS = (By.CSS_SELECTOR, ".modal input, .modal textarea")
    MODAL_SEND_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal')]//button[.//span[normalize-space()='Send'] or normalize-space()='Send']",
    )

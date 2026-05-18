# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class CompaniesLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy/companies"

    PAGE_ROOT = (By.TAG_NAME, "body")
    CTA_GET_OFFER = (
        By.XPATH,
        "//button[.//span[contains(normalize-space(),'Get an Offer')] or contains(normalize-space(),'Get an Offer')]",
    )
    MODAL_INPUTS = (By.CSS_SELECTOR, ".modal input, .modal textarea")
    MODAL_TABS = (By.CSS_SELECTOR, ".modal .select-tab__option")

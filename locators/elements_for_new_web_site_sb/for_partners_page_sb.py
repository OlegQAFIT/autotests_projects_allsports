# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class PartnersLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy/partners"

    PAGE_ROOT = (By.TAG_NAME, "body")
    CTA_BECOME_PARTNER = (
        By.XPATH,
        "//button[.//span[contains(normalize-space(),'Become a Partner')] or contains(normalize-space(),'Become a Partner')]",
    )
    MODAL_INPUTS = (By.CSS_SELECTOR, ".modal input, .modal textarea")

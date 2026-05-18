# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class LevelsLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy/levels"

    PAGE_ROOT = (By.TAG_NAME, "body")
    LEVEL_CARDS = (By.CSS_SELECTOR, ".level-card-wrapper")
    LEVEL_CARD_TITLE = (By.CSS_SELECTOR, ".level-card__main h2")
    LEVEL_CARD_LINKS = (By.CSS_SELECTOR, "a[href]")

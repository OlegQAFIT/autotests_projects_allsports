# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class SmokePagesLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy"

    UI_PAGES = [
        "https://www.sportbenefit.eu/en-cy",
        "https://www.sportbenefit.eu/en-cy/facilities",
        "https://www.sportbenefit.eu/en-cy/facilities-table",
        "https://www.sportbenefit.eu/en-cy/levels",
        "https://www.sportbenefit.eu/en-cy/companies",
        "https://www.sportbenefit.eu/en-cy/partners",
        "https://www.sportbenefit.eu/en-cy/contacts",
        "https://www.sportbenefit.eu/en-cy/app",
    ]

    HTTP_PAGES = UI_PAGES + [
        "https://www.sportbenefit.eu/en-cy/license",
        "https://www.sportbenefit.eu/en-cy/user-agreements",
        "https://www.sportbenefit.eu/en-cy/policy/260407_processing_personal_data",
        "https://www.sportbenefit.eu/en-cy/rule/250811_rule",
        "https://www.sportbenefit.eu/en-cy/cookie/cookie-policy",
        "https://www.sportbenefit.eu/en-cy/license/260407_license",
        "https://www.sportbenefit.eu/en-cy/individual_license/260407_license",
    ]

    PAGE_ROOT = (By.TAG_NAME, "body")

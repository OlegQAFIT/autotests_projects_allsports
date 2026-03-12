# -*- coding: utf-8 -*-
from locators.elements_for_new_web_site.regression_pages_locators import RegressionLocators as RL


class SmokeLocators:
    """Набор страниц для smoke-проверок после релиза."""

    UI_PAGE_KEYS = (
        'main',
        'facilities',
        'levels',
        'companies',
        'partners',
        'contacts',
    )

    HTTP_PAGE_KEYS = (
        'license',
        'user_agreement',
        'policy',
        'license_doc',
        'individual_license',
        'rule',
        'cookie_policy',
        'facilities_table',
    )

    @staticmethod
    def get_page_data(page_key):
        return RL.PAGES[page_key]

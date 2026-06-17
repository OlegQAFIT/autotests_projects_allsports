# -*- coding: utf-8 -*-
import requests

from pages.new_web_site_sb.base_page_sb import BasePageSb


class SiteHealthSb(BasePageSb):
    LEGAL_ENDPOINTS = [
        "https://www.sportbenefit.eu/en-cy/license",
        "https://www.sportbenefit.eu/en-cy/user-agreements",
        "https://www.sportbenefit.eu/en-cy/policy/260407_processing_personal_data",
        "https://www.sportbenefit.eu/en-cy/rule/250811_rule",
        "https://www.sportbenefit.eu/en-cy/cookie/cookie-policy",
        "https://www.sportbenefit.eu/en-cy/license/260407_license",
        "https://www.sportbenefit.eu/en-cy/individual_license/260407_license",
    ]

    PUBLIC_ENDPOINTS = [
        "https://www.sportbenefit.eu/en-cy",
        "https://www.sportbenefit.eu/en-cy/facilities",
        "https://www.sportbenefit.eu/en-cy/facilities-table",
        "https://www.sportbenefit.eu/en-cy/levels",
        "https://www.sportbenefit.eu/en-cy/companies",
        "https://www.sportbenefit.eu/en-cy/partners",
        "https://www.sportbenefit.eu/en-cy/contacts",
        "https://www.sportbenefit.eu/en-cy/app",
        *LEGAL_ENDPOINTS,
        "https://sportbenefit.eu/media/sportbenefiteu-release.apk",
    ]

    API_ENDPOINTS = [
        "https://www.sportbenefit.eu/api/www/2.0.0/contact/get_offer",
        "https://www.sportbenefit.eu/api/www/2.0.0/contact/become_partner",
        "https://www.sportbenefit.eu/api/www/2.0.0/contact/ask_question",
    ]

    UI_PAGES_FOR_CONSOLE = [
        "https://www.sportbenefit.eu/en-cy",
        "https://www.sportbenefit.eu/en-cy/facilities",
        "https://www.sportbenefit.eu/en-cy/facilities-table",
        "https://www.sportbenefit.eu/en-cy/levels",
        "https://www.sportbenefit.eu/en-cy/companies",
        "https://www.sportbenefit.eu/en-cy/partners",
        "https://www.sportbenefit.eu/en-cy/contacts",
        "https://www.sportbenefit.eu/en-cy/app",
    ]

    def check_public_endpoint_status_200(self, url, timeout=25):
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        assert response.status_code == 200, f"{url} returned {response.status_code}"

    def check_options_endpoint_status_200(self, url, timeout=20):
        response = requests.options(url, timeout=timeout)
        assert response.status_code == 200, f"OPTIONS {url} returned {response.status_code}"

    def check_get_method_guard(self, url, timeout=20, expected_status=405):
        response = requests.get(url, timeout=timeout)
        assert response.status_code == expected_status, (
            f"GET {url} should return {expected_status}, got {response.status_code}"
        )

    def check_page_has_no_severe_console_errors(self, url):
        self.open_url(url)
        self.accept_cookie_consent()
        logs = self.driver.get_log("browser")
        filtered = self.filtered_console_errors(logs)
        assert not filtered, f"Console SEVERE errors on {url}: {filtered}"

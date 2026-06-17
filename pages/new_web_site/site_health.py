# -*- coding: utf-8 -*-
import requests
from selenium.webdriver.common.by import By

from helpers.base import BasePage


class SiteHealthPage(BasePage):
    @staticmethod
    def filtered_console_errors(raw_logs):
        severe = [entry for entry in raw_logs if entry.get("level") == "SEVERE"]
        filtered = []
        for entry in severe:
            msg = (entry.get("message") or "").lower()
            source = (entry.get("source") or "").lower()
            if "sentry" in msg:
                continue
            if "content security policy" in msg or "csp" in msg:
                continue
            if source in ("security", "network"):
                continue
            filtered.append(entry)
        return filtered

    def check_public_endpoint_status_200(self, url, timeout=20):
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        assert response.status_code == 200, f"{url} returned {response.status_code}"

    def check_options_endpoint_status_200(self, url, timeout=20):
        response = requests.options(url, timeout=timeout)
        assert response.status_code == 200, f"OPTIONS {url} returned {response.status_code}"

    def check_get_method_guard(self, url, timeout=20, expected_status=405):
        response = requests.get(url, timeout=timeout)
        assert response.status_code == expected_status, (
            f"GET {url} should be method-guarded ({expected_status}), got {response.status_code}"
        )

    def check_page_has_no_severe_console_errors(self, url):
        self.driver.get(url)
        self.click_if_visible((By.CSS_SELECTOR, ".cookie-primary-modal__confirm"), timeout=3)
        logs = self.driver.get_log("browser")
        filtered = self.filtered_console_errors(logs)
        assert not filtered, f"Console SEVERE errors on {url}: {filtered}"

# -*- coding: utf-8 -*-
import time
from urllib.parse import urlparse, urlunparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.base import BasePage


class BasePageSb(BasePage):
    @staticmethod
    def normalize_url(url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path or "/"
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))

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

    @staticmethod
    def strict_console_issues(raw_logs):
        issues = []
        for entry in raw_logs:
            level = str(entry.get("level") or "").upper()
            message = str(entry.get("message") or "")
            source = str(entry.get("source") or "")
            if level in ("SEVERE", "ERROR"):
                issues.append(
                    {
                        "level": level,
                        "source": source,
                        "message": message,
                    }
                )
                continue

            # In strict mode warnings that contain explicit error/failure keywords
            # are also treated as blockers.
            if level in ("WARNING", "WARN"):
                lowered = message.lower()
                if any(token in lowered for token in ("error", "failed", "exception", "uncaught")):
                    issues.append(
                        {
                            "level": level,
                            "source": source,
                            "message": message,
                        }
                    )
        return issues

    def open_url(self, url: str):
        self.driver.get(url)
        self.wait_page_ready()
        return self

    def wait_page_ready(self):
        WebDriverWait(self.driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def set_viewport(self, width: int, height: int):
        self.driver.set_window_size(width, height)
        return self

    def accept_cookie_consent(self):
        # Cookie popup can appear lazily after initial interaction on Sportbenefit.
        locators = [
            (By.CSS_SELECTOR, ".cookie-primary-modal__confirm"),
            (By.XPATH, "//button[normalize-space()='Confirm' or .//span[normalize-space()='Confirm']]"),
            (By.XPATH, "//button[normalize-space()='Accept' or .//span[normalize-space()='Accept']]"),
            (By.XPATH, "//button[normalize-space()='Reject' or .//span[normalize-space()='Reject']]"),
        ]

        end_at = time.time() + 6
        while time.time() < end_at:
            clicked = False
            found_any = False

            for locator in locators:
                elements = self.driver.find_elements(*locator)
                if elements:
                    found_any = True

                for el in elements:
                    try:
                        if el.is_displayed() and el.is_enabled():
                            self.driver.execute_script("arguments[0].click();", el)
                            clicked = True
                            time.sleep(0.35)
                            break
                    except Exception:
                        continue

                if clicked:
                    break

            if clicked:
                continue

            if not found_any:
                break

            time.sleep(0.25)

    def assert_canonical_matches_current(self):
        canonical = self.driver.execute_script(
            "const e=document.querySelector(\"link[rel='canonical']\"); return e ? e.href : '';"
        )
        assert canonical, "Canonical link not found"

        current = self.normalize_url(self.driver.current_url)
        canonical_normalized = self.normalize_url(canonical)
        assert current == canonical_normalized, (
            f"Canonical mismatch: current={current}, canonical={canonical_normalized}"
        )

    def assert_no_severe_console_errors(self):
        time.sleep(0.3)
        logs = self.driver.get_log("browser")
        filtered = self.filtered_console_errors(logs)
        assert not filtered, f"Console SEVERE errors found: {filtered}"

    def assert_no_console_issues_strict(self):
        time.sleep(0.3)
        logs = self.driver.get_log("browser")
        issues = self.strict_console_issues(logs)
        assert not issues, f"Console strict issues found: {issues}"

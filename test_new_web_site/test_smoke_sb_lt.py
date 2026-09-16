"""Comprehensive smoke checks for the SportBenefit Lithuania test website."""

import os

import allure
import pytest
from selenium.webdriver.common.by import By

from test_new_web_site.test_smoke_as import SiteProfile, run_site_suite


SB_LT = SiteProfile(
    "SportBenefit Lithuania",
    os.getenv("SB_LT_TEST_BASE_URL", "https://xn--h1adqe.xn--k1aahcehedi.xn--90ais/en-lt"),
    "en",
    "Lithuania",
    ("gold", "platinum", "vip"),
    "+370",
)


@allure.feature("Test website smoke")
@allure.story("SportBenefit Lithuania: full public-site journey")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.release_gate
@pytest.mark.form_submission
def test_smoke_sb_lt_full_public_site(driver):
    run_site_suite(driver, SB_LT)


@allure.feature("Test website smoke")
@allure.story("SportBenefit Lithuania: locale-specific copy")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_smoke_sb_lt_copy_uses_lithuania_not_cyprus(driver):
    """Protects LT membership cards from Cyprus copy/phone-format leakage."""
    for path in ("", "/levels", "/companies", "/partners", "/contacts"):
        driver.get(f"{SB_LT.base_url.rstrip('/')}{path}")
        text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "across cyprus" not in text, f"Cyprus copy leaked into LT page: {driver.current_url}"
        placeholders = [
            item.get_attribute("placeholder") or ""
            for item in driver.find_elements(By.CSS_SELECTOR, "input[type='tel'], input[placeholder]")
        ]
        assert not any("+357" in placeholder for placeholder in placeholders), (
            f"Cyprus phone placeholder leaked into LT page: {driver.current_url}; {placeholders}"
        )
        phone_placeholders = [placeholder for placeholder in placeholders if "+" in placeholder]
        if phone_placeholders:
            assert any("+370" in placeholder for placeholder in phone_placeholders), (
                f"Lithuanian phone prefix +370 is missing: {driver.current_url}; {phone_placeholders}"
            )

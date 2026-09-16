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
    for path in ("", "/levels", "/contacts"):
        driver.get(f"{SB_LT.base_url.rstrip('/')}{path}")
        text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "across cyprus" not in text, f"Cyprus copy leaked into LT page: {driver.current_url}"
    assert "+357 00 00 00 00" not in text, "Cyprus phone placeholder leaked into LT contacts"

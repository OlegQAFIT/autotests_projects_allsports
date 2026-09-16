"""Comprehensive smoke checks for the SportBenefit Cyprus test website."""

import os

import allure
import pytest

from test_new_web_site.test_smoke_as import SiteProfile, run_site_suite


SB_CY = SiteProfile(
    "SportBenefit Cyprus",
    os.getenv("SB_CY_TEST_BASE_URL", "https://xn--h1adqe.xn--k1aahcehedi.xn--90ais/en-cy"),
    "en",
    "Cyprus",
    ("silver", "gold", "platinum", "vip"),
    "+357",
)


@allure.feature("Test website smoke")
@allure.story("SportBenefit Cyprus: full public-site journey")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.release_gate
@pytest.mark.form_submission
def test_smoke_sb_full_public_site(driver):
    run_site_suite(driver, SB_CY)

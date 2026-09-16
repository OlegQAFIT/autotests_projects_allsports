"""Comprehensive smoke checks for the SportBenefit Cyprus test website."""

import os

import allure
import pytest
from selenium.webdriver.common.by import By

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


@allure.feature("Test website smoke")
@allure.story("SportBenefit Cyprus: homepage counters and copy")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_smoke_sb_homepage_does_not_overstate_facility_count(driver):
    driver.get(SB_CY.base_url)
    text = driver.find_element(By.TAG_NAME, "body").text.lower()
    import re
    counter = re.search(r"(\d+)\s+facilit", text)
    claim = re.search(r"(\d+)\+\s+(?:venue|facilit)", text)
    assert counter and claim, "Homepage counter or marketing claim is missing"
    assert int(claim.group(1)) <= int(counter.group(1)), (
        f"Homepage says {claim.group(1)}+ venues but counter is {counter.group(1)}"
    )

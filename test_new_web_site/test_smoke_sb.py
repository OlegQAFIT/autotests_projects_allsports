"""Comprehensive smoke checks for the SportBenefit Cyprus test website."""

import os
import re

import allure
import pytest
from selenium.webdriver.common.by import By

from test_new_web_site.test_smoke_as import (
    SiteProfile,
    _test_question_cta_placeholder,
    _test_form_validation_and_optional_submission,
    run_site_suite,
)


SB_CY = SiteProfile(
    "SportBenefit Cyprus",
    os.getenv("SB_CY_TEST_BASE_URL", "https://xn--h1adqe.xn--k1aahcehedi.xn--90ais/en-cy"),
    "en",
    "Cyprus",
    ("silver", "gold", "platinum", "vip"),
    "+357",
    "qwerty@sportbenefit.eu",
    350,
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
    counter = re.search(r"(\d+)\s+facilit", text)
    claim = re.search(r"(\d+)\+\s+(?:venue|facilit)", text)
    assert counter and claim, "Homepage counter or marketing claim is missing"
    assert int(claim.group(1)) <= int(counter.group(1)), (
        f"Homepage says {claim.group(1)}+ venues but counter is {counter.group(1)}"
    )


@allure.feature("Test website regressions")
@allure.story("SportBenefit Cyprus: invalid contact data cannot submit")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_smoke_sb_invalid_contact_data_keeps_submit_disabled(driver):
    """Regression for the previously observed active button with invalid e-mail."""
    _test_form_validation_and_optional_submission(driver, SB_CY)


@allure.feature("Jira regressions")
@allure.story("AL-891: Cyprus contact address names the fourth floor")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_regression_al_891_sb_cy_contact_address_has_fourth_floor(driver):
    driver.get(f"{SB_CY.base_url.rstrip('/')}/contacts")
    text = driver.find_element(By.TAG_NAME, "body").text.casefold()
    assert "4th floor" in text, "AL-891: Cyprus contact address must specify '4th floor'"


@allure.feature("Jira regressions")
@allure.story("AL-883: Ask Us a Question uses SportBenefit e-mail placeholder")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_regression_al_883_sb_cy_question_form_has_no_allsports_placeholder(driver):
    _test_question_cta_placeholder(driver, SB_CY)

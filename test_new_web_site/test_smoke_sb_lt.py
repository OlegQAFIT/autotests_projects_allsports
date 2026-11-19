"""Comprehensive smoke checks for the SportBenefit Lithuania test website."""

import os

import allure
import pytest
from selenium.webdriver.common.by import By

from test_new_web_site.test_smoke_as import (
    SiteProfile,
    _test_question_cta_placeholder,
    run_site_suite,
)


SB_LT = SiteProfile(
    "SportBenefit Lithuania",
    os.getenv("SB_LT_TEST_BASE_URL", "https://xn--h1adqe.xn--k1aahcehedi.xn--90ais/en-lt"),
    "en",
    "Lithuania",
    ("gold", "platinum", "vip"),
    "+370",
    "qwerty@sportbenefit.eu",
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


@allure.feature("Jira regressions")
@allure.story("AL-891: LT contacts contain the approved Lithuanian phone only")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_regression_al_891_sb_lt_contact_phone_and_titles(driver):
    driver.get(f"{SB_LT.base_url.rstrip('/')}/contacts")
    expected_href = "tel:+37060894673"
    tel_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='tel:']")
    assert any(link.get_attribute("href") == expected_href for link in tel_links), (
        "AL-891: approved LT contact number +370 608 94673 is absent"
    )
    # Section headings must not themselves be telephone/mail/location links.
    linked_headings = driver.execute_script(
        """
        return [...document.querySelectorAll('a h1,a h2,a h3,a h4,a h5,a h6')]
          .map(item => item.textContent.trim()).filter(Boolean);
        """
    )
    assert not linked_headings, f"AL-891: clickable contact headings: {linked_headings}"


@allure.feature("Jira regressions")
@allure.story("AL-883: LT Ask Us a Question has SportBenefit placeholder")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_regression_al_883_sb_lt_question_form_has_no_allsports_placeholder(driver):
    _test_question_cta_placeholder(driver, SB_LT)

# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.contacts_sb import ContactsPageSb
from pages.new_web_site_sb.facilities_sb import FacilitiesPageSb
from pages.new_web_site_sb.main_page_sb import MainPageSb
from test_new_web_site_sb.form_helpers_sb import (
    assert_modal_send_disabled,
    assert_modal_send_enabled,
    ensure_modal_checkbox_checked,
    fill_inline_contacts_values,
    fill_modal_input,
    get_modal_send_button,
    inline_submit_enabled,
    open_modal_by_cta_text,
)


MOBILE_VIEWPORTS = [
    (360, 800),
    (390, 844),
    (768, 1024),
]


@allure.feature("SB Mobile Regression")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_main_modal_flow_sb(driver, viewport):
    width, height = viewport
    driver.set_window_size(width, height)

    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()

    open_modal_by_cta_text(driver, "Get an Offer", required_placeholder="Company")
    assert_modal_send_disabled(driver)

    fill_modal_input(driver, "Name", "QA Mobile")
    fill_modal_input(driver, "Enter phone number", "+357 99 11 22 66")
    fill_modal_input(driver, "qwerty@sportbenefit.eu", "qa.mobile@example.com")
    fill_modal_input(driver, "Company", "QA Mobile Co")
    fill_modal_input(driver, "Enter the city", "Limassol")
    ensure_modal_checkbox_checked(driver)
    assert_modal_send_enabled(driver)

    # Do not submit real request in mobile regression.
    send_button = get_modal_send_button(driver)
    assert send_button.is_displayed(), f"Send button is not visible on viewport {width}x{height}"


@allure.feature("SB Mobile Regression")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_facilities_map_filters_and_table_sb(driver, viewport):
    width, height = viewport
    driver.set_window_size(width, height)

    page = FacilitiesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_visible()
    page.check_map_controls()
    page.check_filter_buttons_visible()
    page.check_map_reacts_to_filters(section_title="City", option_text="Limassol")

    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_basics()
    page.check_table_search("yoga")
    page.check_table_filter_content_matches(
        section_title="City",
        option_text="Limassol",
        content_kind="city",
    )


@allure.feature("SB Mobile Regression")
@allure.severity("Normal")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_contacts_inline_form_validation_gate_sb(driver, viewport):
    width, height = viewport
    driver.set_window_size(width, height)

    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()

    fill_inline_contacts_values(
        driver,
        name="QA Mobile Inline",
        phone="+357 99 11 22 77",
        email="qa.mobile.inline@example.com",
        company="QA Mobile Inline Co",
    )
    assert inline_submit_enabled(driver), (
        f"Inline submit should be enabled for valid values on viewport {width}x{height}"
    )

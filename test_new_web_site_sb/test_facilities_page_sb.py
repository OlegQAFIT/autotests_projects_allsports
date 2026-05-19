# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.facilities_sb import FacilitiesPageSb


@allure.feature("Facilities SB")
@allure.severity("Blocker")
def test_open_facilities_page_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_opened()


@allure.feature("Facilities SB")
@allure.severity("Critical")
def test_facilities_map_and_controls_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_visible()
    page.check_map_controls()
    page.check_filter_buttons_visible()


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_map_markers_and_popup_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_marker_popup()


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_map_reaction_to_filters_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_reacts_to_filters(section_title="City", option_text="Limassol")


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_basics_and_search_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_basics()
    page.check_table_search("yoga")


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_filter_city_content_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_content_matches(
        section_title="City",
        option_text="Limassol",
        content_kind="city",
    )


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_filter_activity_content_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_content_matches(
        section_title="Activities",
        option_text="Aerobics",
        content_kind="activity",
    )


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_filter_membership_vip_content_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_content_matches(
        section_title="Membership type",
        option_text="VIP",
        content_kind="level",
    )


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_filter_combination_two_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_combination(
        [
            {"section": "City", "option": "Limassol", "show_all": True},
            {"section": "Activities", "option": "Aerobics", "show_all": True},
        ]
    )


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_filter_combination_three_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_filter_combination(
        [
            {"section": "City", "option": "Limassol", "show_all": True},
            {"section": "Activities", "option": "Aerobics", "show_all": True},
            {"section": "Activities", "option": "Aerial Yoga", "show_all": True},
        ]
    )


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_search_filters_reset_empty_state_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_search_filters_reset_empty_state(
        search_query="yoga",
        city="Limassol",
        activity="Aerial Yoga",
        empty_query="zzzzzzzzzz_not_found",
    )


@allure.feature("Facilities SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_facilities_table_reset_returns_baseline_sb(driver):
    page = FacilitiesPageSb(driver)
    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_reset_returns_baseline(
        [
            {"section": "City", "option": "Limassol", "show_all": True},
            {"section": "Activities", "option": "Aerobics", "show_all": True},
            {"section": "Activities", "option": "Aerial Yoga", "show_all": True},
        ],
        attempts=2,
    )

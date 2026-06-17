# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.app_page_sb import AppPageSb
from pages.new_web_site_sb.companies_sb import CompaniesPageSb
from pages.new_web_site_sb.contacts_sb import ContactsPageSb
from pages.new_web_site_sb.facilities_sb import FacilitiesPageSb
from pages.new_web_site_sb.footer_sb import FooterPageSb
from pages.new_web_site_sb.header_sb import HeaderPageSb
from pages.new_web_site_sb.levels_sb import LevelsPageSb
from pages.new_web_site_sb.main_page_sb import MainPageSb
from pages.new_web_site_sb.partners_sb import PartnersPageSb
from pages.new_web_site_sb.site_health_sb import SiteHealthSb


pytestmark = [pytest.mark.smoke, pytest.mark.release_gate]


CRITICAL_HTTP_URLS = SiteHealthSb.PUBLIC_ENDPOINTS
CRITICAL_CONSOLE_URLS = SiteHealthSb.UI_PAGES_FOR_CONSOLE


@allure.feature("Smoke SB")
@allure.story("Post-release: homepage and header")
@allure.severity("Blocker")
def test_post_release_homepage_and_header_smoke_sb(driver):
    main_page = MainPageSb(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.check_main_page_basics()
    main_page.check_main_cta_buttons()

    header_page = HeaderPageSb(driver)
    header_page.check_header_links_present()


@allure.feature("Smoke SB")
@allure.story("Post-release: header navigation across key sections")
@allure.severity("Blocker")
def test_post_release_header_navigation_smoke_sb(driver):
    page = HeaderPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_header_navigation()


@allure.feature("Smoke SB")
@allure.story("Post-release: facilities and levels")
@allure.severity("Critical")
def test_post_release_facilities_and_levels_smoke_sb(driver):
    facilities_page = FacilitiesPageSb(driver)
    facilities_page.open()
    facilities_page.accept_cookie_consent()
    facilities_page.check_map_visible()
    facilities_page.check_map_controls()
    facilities_page.check_filter_buttons_visible()

    levels_page = LevelsPageSb(driver)
    levels_page.open()
    levels_page.accept_cookie_consent()
    levels_page.check_levels_cards_present()
    levels_page.check_levels_card_links()


@allure.feature("Smoke SB")
@allure.story("Post-release: B2B pages and contacts")
@allure.severity("Critical")
def test_post_release_b2b_and_contacts_smoke_sb(driver):
    companies_page = CompaniesPageSb(driver)
    companies_page.open()
    companies_page.accept_cookie_consent()
    companies_page.open_get_offer_modal()
    companies_page.check_companies_modal_structure()

    partners_page = PartnersPageSb(driver)
    partners_page.open()
    partners_page.accept_cookie_consent()
    partners_page.open_become_partner_modal()
    partners_page.check_partner_modal_structure()

    contacts_page = ContactsPageSb(driver)
    contacts_page.open()
    contacts_page.accept_cookie_consent()
    contacts_page.check_page_opened()
    contacts_page.check_form_structure()
    contacts_page.check_map_visible()


@allure.feature("Smoke SB")
@allure.story("Post-release: app page and footer")
@allure.severity("Critical")
def test_post_release_app_and_footer_smoke_sb(driver):
    app_page = AppPageSb(driver)
    app_page.open()
    app_page.accept_cookie_consent()
    app_page.check_page_opened()
    app_page.check_store_links()

    footer_page = FooterPageSb(driver)
    footer_page.open()
    footer_page.check_contacts()
    footer_page.check_social_links()
    footer_page.check_app_links()
    footer_page.check_navigation_links()
    footer_page.check_legal_links()
    footer_page.check_footer_link_statuses()


@allure.feature("Smoke SB")
@allure.story("Post-release: HTTP availability of critical pages and resources")
@allure.severity("Critical")
@pytest.mark.parametrize("url", CRITICAL_HTTP_URLS)
def test_post_release_http_health_smoke_sb(driver, url):
    page = SiteHealthSb(driver)
    page.check_public_endpoint_status_200(url)


@allure.feature("Smoke SB")
@allure.story("Post-release: no severe console errors on key UI pages")
@allure.severity("Critical")
@pytest.mark.parametrize("url", CRITICAL_CONSOLE_URLS)
def test_post_release_console_health_smoke_sb(driver, url):
    page = SiteHealthSb(driver)
    page.check_page_has_no_severe_console_errors(url)

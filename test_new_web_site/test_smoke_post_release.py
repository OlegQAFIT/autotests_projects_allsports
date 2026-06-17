# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site.app_page import AppPage
from pages.new_web_site.companies import CompaniesPage
from pages.new_web_site.contacts import ContactsPage
from pages.new_web_site.facilities import FacilitiesPage
from pages.new_web_site.footer import FooterPage
from pages.new_web_site.header import HeaderPage
from pages.new_web_site.levels import LevelsPage
from pages.new_web_site.main_page import MainPage
from pages.new_web_site.partners import PartnersPage
from pages.new_web_site.site_health import SiteHealthPage


pytestmark = [pytest.mark.smoke, pytest.mark.release_gate]


CRITICAL_HTTP_URLS = [
    "https://www.allsports.by/ru-by/",
    "https://www.allsports.by/ru-by/facilities",
    "https://www.allsports.by/ru-by/facilities-table",
    "https://www.allsports.by/ru-by/levels",
    "https://www.allsports.by/ru-by/companies",
    "https://www.allsports.by/ru-by/partners",
    "https://www.allsports.by/ru-by/contacts",
    "https://www.allsports.by/ru-by/app",
    "https://www.allsports.by/ru-by/license",
    "https://www.allsports.by/ru-by/user-agreements",
    "https://www.allsports.by/ru-by/policy/251010_processing_personal_data",
    "https://www.allsports.by/ru-by/license/241009_license",
    "https://www.allsports.by/ru-by/individual_license/241009_license",
    "https://www.allsports.by/ru-by/rule/250731_rule",
    "https://www.allsports.by/ru-by/cookie/cookie-policy",
]

CRITICAL_CONSOLE_URLS = [
    "https://www.allsports.by/ru-by/",
    "https://www.allsports.by/ru-by/facilities",
    "https://www.allsports.by/ru-by/facilities-table",
    "https://www.allsports.by/ru-by/levels",
    "https://www.allsports.by/ru-by/companies",
    "https://www.allsports.by/ru-by/partners",
    "https://www.allsports.by/ru-by/contacts",
    "https://www.allsports.by/ru-by/app",
]


@allure.feature("Smoke")
@allure.story("Post-release: главная страница и шапка")
@allure.severity("Blocker")
def test_post_release_homepage_and_header_smoke(driver):
    main_page = MainPage(driver)
    main_page.open()
    main_page.accept_cookie_consent()
    main_page.check_promo_block()
    main_page.check_regular_subscription_cards()
    main_page.check_contacts_section_present()

    header_page = HeaderPage(driver)
    header_page.check_header_buttons()


@allure.feature("Smoke")
@allure.story("Post-release: навигация по ключевым разделам")
@allure.severity("Blocker")
def test_post_release_header_navigation_smoke(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_facilities()

    page.open()
    page.check_link_levels()

    page.open()
    page.check_link_companies()

    page.open()
    page.check_link_partners()

    page.open()
    page.check_link_contacts()


@allure.feature("Smoke")
@allure.story("Post-release: объекты и типы подписок")
@allure.severity("Critical")
def test_post_release_facilities_and_levels_smoke(driver):
    facilities_page = FacilitiesPage(driver)
    facilities_page.open()
    facilities_page.accept_cookie_consent()
    facilities_page.check_page_opened()
    facilities_page.check_map_visible()
    facilities_page.check_map_controls()
    facilities_page.check_objects_table_block()

    levels_page = LevelsPage(driver)
    levels_page.open()
    levels_page.accept_cookie_consent()
    levels_page.check_levels_section_present()
    levels_page.check_subscription_cards_present()


@allure.feature("Smoke")
@allure.story("Post-release: компании, партнёры и контакты")
@allure.severity("Critical")
def test_post_release_b2b_and_contacts_smoke(driver):
    companies_page = CompaniesPage(driver)
    companies_page.open()
    companies_page.accept_cookie_consent()
    companies_page.check_promo_block()
    companies_page.check_benefit_section()
    companies_page.check_contacts_section_present()

    partners_page = PartnersPage(driver)
    partners_page.open()
    partners_page.accept_cookie_consent()
    partners_page.check_promo_content()
    partners_page.check_benefits_title()
    partners_page.check_contacts_presence()

    contacts_page = ContactsPage(driver)
    contacts_page.open()
    contacts_page.accept_cookie_consent()
    contacts_page.check_page_header()
    contacts_page.check_address_block()
    contacts_page.check_google_map()


@allure.feature("Smoke")
@allure.story("Post-release: app page и футер")
@allure.severity("Critical")
def test_post_release_app_and_footer_smoke(driver):
    app_page = AppPage(driver)
    app_page.open()
    app_page.accept_cookie_consent()
    app_page.check_page_opened()
    app_page.check_store_links()

    footer_page = FooterPage(driver)
    footer_page.open()
    footer_page.accept_cookie_consent()
    footer_page.check_footer_contacts()
    footer_page.check_footer_navigation_links()


@allure.feature("Smoke")
@allure.story("Post-release: HTTP доступность критичных страниц и документов")
@allure.severity("Critical")
@pytest.mark.parametrize("url", CRITICAL_HTTP_URLS)
def test_post_release_http_health_smoke(url):
    page = SiteHealthPage(None)
    page.check_public_endpoint_status_200(url)


@allure.feature("Smoke")
@allure.story("Post-release: отсутствие критичных ошибок в консоли на ключевых страницах")
@allure.severity("Critical")
@pytest.mark.parametrize("url", CRITICAL_CONSOLE_URLS)
def test_post_release_console_health_smoke(driver, url):
    page = SiteHealthPage(driver)
    page.check_page_has_no_severe_console_errors(url)

# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.header_sb import HeaderPageSb


@allure.feature("Header SB")
@allure.severity("Blocker")
def test_header_links_present_sb(driver):
    page = HeaderPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_header_links_present()


@allure.feature("Header SB")
@allure.severity("Critical")
def test_header_navigation_sb(driver):
    page = HeaderPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_header_navigation()


@allure.feature("Header SB")
@allure.severity("Critical")
@pytest.mark.release_gate
def test_header_get_offer_modal_structure_sb(driver):
    page = HeaderPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_get_offer_modal()
    page.check_offer_modal_structure()
    page.check_offer_modal_partner_tab()
    page.close_modal()

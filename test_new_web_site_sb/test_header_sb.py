# -*- coding: utf-8 -*-
import allure

from pages.new_web_site_sb.header_sb import HeaderPageSb


@allure.feature("Header SB")
@allure.severity("Blocker")
def test_header_links_present_sb(driver):
    """Проверка наличия основных ссылок в header."""
    page = HeaderPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_header_links_present()


@allure.feature("Header SB")
@allure.severity("Critical")
def test_header_navigation_sb(driver):
    """Проверка переходов по ссылкам header."""
    page = HeaderPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_header_navigation()

# -*- coding: utf-8 -*-
import allure

from pages.new_web_site_sb.footer_sb import FooterPageSb


@allure.feature("Footer SB")
@allure.severity("Critical")
def test_footer_integrity_sb(driver):
    page = FooterPageSb(driver)
    page.open()
    page.check_contacts()
    page.check_social_links()
    page.check_app_links()
    page.check_navigation_links()
    page.check_legal_links()
    page.check_footer_link_statuses()

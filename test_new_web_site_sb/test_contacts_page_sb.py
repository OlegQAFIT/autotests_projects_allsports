# -*- coding: utf-8 -*-
import allure

from pages.new_web_site_sb.contacts_sb import ContactsPageSb


@allure.feature("Contacts SB")
@allure.severity("Critical")
def test_contacts_map_visible_sb(driver):
    """Проверка отображения карты на странице Contacts."""
    page = ContactsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_visible()

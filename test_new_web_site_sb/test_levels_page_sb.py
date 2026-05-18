# -*- coding: utf-8 -*-
import allure

from pages.new_web_site_sb.levels_sb import LevelsPageSb


@allure.feature("Levels SB")
@allure.severity("Critical")
def test_levels_cards_presence_sb(driver):
    page = LevelsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_levels_cards_present()


@allure.feature("Levels SB")
@allure.severity("Critical")
def test_levels_cards_links_sb(driver):
    page = LevelsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_levels_card_links()

# -*- coding: utf-8 -*-
import allure

from pages.new_web_site_sb.levels_sb import LevelsPageSb


@allure.feature("Levels SB")
@allure.severity("Critical")
def test_levels_cards_presence_sb(driver):
    """Проверка наличия карточек уровней и обязательных названий."""
    page = LevelsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_levels_cards_present()


@allure.feature("Levels SB")
@allure.severity("Critical")
def test_levels_cards_links_sb(driver):
    """Проверка ссылок внутри карточек уровней на корректные разделы."""
    page = LevelsPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_levels_card_links()

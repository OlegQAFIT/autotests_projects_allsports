# -*- coding: utf-8 -*-
import allure

from pages.new_web_site_sb.main_page_sb import MainPageSb


@allure.feature("Main SB")
@allure.severity("Critical")
def test_main_page_basics_sb(driver):
    """Проверка базовой структуры главной страницы."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_main_page_basics()


@allure.feature("Main SB")
@allure.severity("Critical")
def test_main_page_cta_buttons_sb(driver):
    """Проверка наличия ключевых CTA-кнопок на главной странице."""
    page = MainPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_main_cta_buttons()

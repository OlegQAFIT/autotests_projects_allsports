# -*- coding: utf-8 -*-
import allure

from pages.new_web_site.smoke_pages import SmokePages


@allure.feature('Smoke')
@allure.story('Post-release: ключевые UI страницы')
@allure.severity('Blocker')
def test_post_release_smoke_ui(driver):
    page = SmokePages(driver)
    page.run_post_release_smoke_ui()


@allure.feature('Smoke')
@allure.story('Post-release: доступность критичных служебных страниц')
@allure.severity('Critical')
def test_post_release_smoke_http(driver):
    page = SmokePages(driver)
    page.run_post_release_smoke_http()

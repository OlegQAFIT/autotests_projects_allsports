# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.smoke_pages_sb import SmokePagesSb


@allure.feature("Smoke SB")
@allure.story("Post-release UI smoke for Sportbenefit")
@allure.severity("Blocker")
@pytest.mark.smoke
@pytest.mark.release_gate
def test_post_release_smoke_ui_sb(driver):
    page = SmokePagesSb(driver)
    page.run_post_release_smoke_ui()


@allure.feature("Smoke SB")
@allure.story("Post-release HTTP smoke for Sportbenefit")
@allure.severity("Critical")
@pytest.mark.smoke
@pytest.mark.release_gate
def test_post_release_smoke_http_sb(driver):
    page = SmokePagesSb(driver)
    page.run_post_release_smoke_http()

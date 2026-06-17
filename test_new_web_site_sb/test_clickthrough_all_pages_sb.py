# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.clickthrough_sb import ClickthroughSb


@allure.feature("SB Clickthrough")
@allure.severity("Critical")
@pytest.mark.pre_release
def test_internal_links_clickthrough_status_sb(driver):
    page = ClickthroughSb(driver)
    page.check_internal_links_clickthrough_status()


@allure.feature("SB Clickthrough")
@allure.severity("Critical")
@pytest.mark.pre_release
def test_primary_buttons_tabs_clickthrough_sb(driver):
    page = ClickthroughSb(driver)
    page.check_primary_buttons_tabs_clickthrough()

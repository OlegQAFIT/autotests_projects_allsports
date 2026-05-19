# -*- coding: utf-8 -*-
import allure
import pytest

from locators.elements_for_new_web_site_sb.regression_pages_locators_sb import RegressionPagesLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


STRICT_CONSOLE_PAGES = sorted(set(L.KEY_PAGES + L.LEGAL_PAGES))


@allure.feature("SB Console Strict")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.console_strict
@pytest.mark.parametrize("url", STRICT_CONSOLE_PAGES)
def test_pages_have_no_console_issues_strict_sb(driver, url):
    page = BasePageSb(driver)
    page.open_url(url)
    page.accept_cookie_consent()
    page.assert_no_console_issues_strict()

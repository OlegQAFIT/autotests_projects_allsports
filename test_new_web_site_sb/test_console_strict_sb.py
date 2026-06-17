# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.base_page_sb import BasePageSb
from pages.new_web_site_sb.site_health_sb import SiteHealthSb


STRICT_CONSOLE_PAGES = sorted(set(SiteHealthSb.UI_PAGES_FOR_CONSOLE + SiteHealthSb.LEGAL_ENDPOINTS))


@allure.feature("SB Console Strict")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.console_strict
@pytest.mark.parametrize("url", STRICT_CONSOLE_PAGES)
def test_pages_have_no_console_issues_strict_sb(driver, url):
    """Проверка strict-режима консоли: отсутствуют ошибки и критичные предупреждения."""
    page = BasePageSb(driver)
    page.open_url(url)
    page.accept_cookie_consent()
    page.assert_no_console_issues_strict()

# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.internal_links_crawler_sb import InternalLinksCrawlerSb


pytestmark = [pytest.mark.release_gate]


@allure.feature("Links SB")
@allure.story("Crawler внутренних ссылок: HTTP + canonical + final URL")
@allure.severity("Critical")
def test_internal_links_crawler_http_and_canonical_sb(driver):
    page = InternalLinksCrawlerSb(driver)
    page.check_internal_links_http_and_canonical()

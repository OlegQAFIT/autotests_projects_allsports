# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site.internal_links_crawler import InternalLinksCrawlerPage


pytestmark = [pytest.mark.release_gate]


@allure.feature("Links")
@allure.severity("Critical")
@allure.story("Crawler внутренних ссылок: HTTP + canonical + final URL")
def test_internal_links_crawler_http_and_canonical(driver):
    page = InternalLinksCrawlerPage(driver)
    page.check_internal_links_http_and_canonical()

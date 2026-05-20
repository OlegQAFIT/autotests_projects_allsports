# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.facilities_sb import FacilitiesPageSb


MOBILE_VIEWPORTS = [
    (360, 800),
    (390, 844),
    (768, 1024),
]


@allure.feature("SB Mobile Regression")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_mobile_facilities_map_filters_and_table_sb(driver, viewport):
    """Проверка мобильной работы карты, фильтров и таблицы Facilities для разных viewport."""
    width, height = viewport
    driver.set_window_size(width, height)

    page = FacilitiesPageSb(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_map_visible()
    page.check_map_controls()
    page.check_filter_buttons_visible()
    page.check_map_reacts_to_filters(section_title="City", option_text="Limassol")

    page.open_table_page()
    page.accept_cookie_consent()
    page.check_table_basics()
    page.check_table_search("yoga")
    page.check_table_filter_content_matches(
        section_title="City",
        option_text="Limassol",
        content_kind="city",
    )

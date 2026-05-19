# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.regression_pages_sb import RegressionPagesSb


@allure.feature("Regression SB")
@allure.severity("Critical")
def test_legal_pages_content_sb(driver):
    page = RegressionPagesSb(driver)
    page.check_legal_pages()


@allure.feature("Regression SB")
@allure.severity("Normal")
@pytest.mark.release_gate
def test_mobile_viewports_key_pages_sb(driver):
    page = RegressionPagesSb(driver)
    page.check_mobile_layouts()


@allure.feature("Regression SB UI")
@allure.severity("Critical")
@pytest.mark.pre_release
def test_no_cyrillic_copywriting_and_ui_integrity_all_pages_sb(driver):
    page = RegressionPagesSb(driver)
    page.check_copywriting_and_ui_integrity_on_all_pages()


@allure.feature("Regression SB UI")
@allure.severity("Critical")
@pytest.mark.cyrillic_gate
def test_cyrillic_fast_gate_sb(driver):
    page = RegressionPagesSb(driver)
    page.check_cyrillic_fast_gate()


@allure.feature("Regression SB UI")
@allure.severity("Critical")
@pytest.mark.pre_release
def test_images_and_logo_assets_key_pages_sb(driver):
    page = RegressionPagesSb(driver)
    page.check_images_and_logo_assets_on_key_pages()


@allure.feature("Regression SB UI")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.cyrillic_gate
def test_mobile_facilities_table_filter_modal_copywriting_sb(driver):
    page = RegressionPagesSb(driver)
    page.check_mobile_facilities_table_filter_modal_copywriting()

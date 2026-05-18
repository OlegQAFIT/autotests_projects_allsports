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

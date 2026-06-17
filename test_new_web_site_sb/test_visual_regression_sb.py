# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.visual_regression_sb import VisualRegressionSb


@allure.feature("SB Visual Regression")
@allure.severity("Normal")
@pytest.mark.pre_release
@pytest.mark.visual_regression
def test_visual_baseline_hashes_sb(driver):
    page = VisualRegressionSb(driver)
    page.check_visual_baseline_hashes()

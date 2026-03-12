# -*- coding: utf-8 -*-
import allure
import pytest
from pages.new_web_site.regression_pages import RegressionPages


@allure.feature('Regression')
@allure.severity('Blocker')
@allure.story('Полная регрессия перед релизом и по расписанию')
@pytest.mark.pre_release
@pytest.mark.schedule
def test_all_site_pages(driver):
    """
    Полный прогон регрессии.

    Запуск перед релизом:
    pytest test_new_web_site/test_regression_pages.py -m pre_release

    Запуск по расписанию:
    pytest test_new_web_site/test_regression_pages.py -m schedule
    """
    page = RegressionPages(driver)
    page.run_full_regression()

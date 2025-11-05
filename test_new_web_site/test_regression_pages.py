# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.regression_pages import RegressionPages


@allure.feature('Regression')
@allure.severity('Critical')
@allure.story('Проверка всех основных страниц сайта')
def test_all_site_pages(driver):
    """Регрессионная проверка открытия всех страниц сайта и наличия ключевых элементов."""
    page = RegressionPages(driver)
    page.run_full_regression()

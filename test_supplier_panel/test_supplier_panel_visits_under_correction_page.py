from pages.supplier_panel.visit_under_correction_page import SupplierPanelVisitsUnderCorrection
import allure


@allure.feature('Supplier Panel Visit under correction')
@allure.severity('critical')
@allure.story('Checking Elements on Page in Russian on Supplier Panel')
def test_checking_elements_on_page_supplier_panel_ru(driver):
    """
    Проверка элементов на странице на русском языке на панели поставщика
    """
    visits_under_correction_supplier_panel = SupplierPanelVisitsUnderCorrection(driver)
    visits_under_correction_supplier_panel.open_sp()
    visits_under_correction_supplier_panel.login_supplier_panel()
    visits_under_correction_supplier_panel.click_visit_under_correction()
    visits_under_correction_supplier_panel.assert_found_elements_on_visit_under_correction_page_ru()


@allure.feature('Supplier Panel Visit under correction')
@allure.severity('critical')
@allure.story('Checking Elements on Page in EN on Supplier Panel')
def test_checking_elements_on_page_supplier_panel_en(driver):
    """
    Проверка элементов на странице на английском языке на панели поставщика
    """
    visits_under_correction_supplier_panel = SupplierPanelVisitsUnderCorrection(driver)
    visits_under_correction_supplier_panel.open_sp()
    visits_under_correction_supplier_panel.login_supplier_panel()
    visits_under_correction_supplier_panel.click_visit_under_correction()
    visits_under_correction_supplier_panel.select_language()
    visits_under_correction_supplier_panel.assert_found_elements_on_visit_under_correction_page_en()


@allure.feature('Supplier Panel Visit under correction')
@allure.severity('critical')
@allure.story('Checking Calendar with Visits on Supplier Panel')
def test_checking_kalendar_with_visits_supplier_panel(driver):
    """
    Проверка календаря с визитами на панели поставщика
    """
    visits_under_correction_supplier_panel = SupplierPanelVisitsUnderCorrection(driver)
    visits_under_correction_supplier_panel.open_sp()
    visits_under_correction_supplier_panel.login_supplier_panel()
    visits_under_correction_supplier_panel.click_visit_under_correction()
    visits_under_correction_supplier_panel.click_calendar_history()
    visits_under_correction_supplier_panel.check_month_selection()


@allure.feature('Supplier Panel Visit under correction')
@allure.severity('critical')
@allure.story('Checking Calendar with Visits on Supplier Panel')
def test_checking_period_with_visits_supplier_panel_en(driver):
    """
    Проверка периода с визитами на панели поставщика
    """
    visits_under_correction_supplier_panel = SupplierPanelVisitsUnderCorrection(driver)
    visits_under_correction_supplier_panel.open_sp()
    visits_under_correction_supplier_panel.login_supplier_panel()
    visits_under_correction_supplier_panel.click_visit_under_correction()
    visits_under_correction_supplier_panel.select_language()
    visits_under_correction_supplier_panel.click_period_en()
    visits_under_correction_supplier_panel.assert_found_elements_on_visit_under_correction_period_page_en()


@allure.feature('Supplier Panel Visit under correction')
@allure.severity('critical')
@allure.story('Checking Calendar with Visits on Supplier Panel')
def test_checking_period_with_visits_supplier_panel_ru(driver):
    """
    Проверка периода с визитами на панели поставщика
    """
    visits_under_correction_supplier_panel = SupplierPanelVisitsUnderCorrection(driver)
    visits_under_correction_supplier_panel.open_sp()
    visits_under_correction_supplier_panel.login_supplier_panel()
    visits_under_correction_supplier_panel.click_visit_under_correction()
    visits_under_correction_supplier_panel.click_period()
    visits_under_correction_supplier_panel.assert_found_elements_on_visit_under_correction_period_page_ru()

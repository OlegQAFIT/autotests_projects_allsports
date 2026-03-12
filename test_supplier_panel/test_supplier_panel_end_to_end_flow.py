import allure
import pytest

from pages.supplier_panel.registration_visits_page import SupplierPanelRegistrationVisits
from pages.supplier_panel.visit_history_page import SupplierPanelVisitsHistory
from pages.supplier_panel.visit_under_correction_page import SupplierPanelVisitsUnderCorrection


@allure.feature("Supplier Panel End-to-End")
@allure.severity("critical")
@allure.story("Create visit -> history -> correction flow")
@pytest.mark.pre_release
@pytest.mark.live_api
def test_supplier_panel_end_to_end_visit_flow(driver):
    registration_page = SupplierPanelRegistrationVisits(driver)
    registration_page.open_sp()
    registration_page.login_and_create_visit()
    registration_page.login_supplier_panel(role="reception")
    registration_page.assert_sidebar_visibility_by_role("reception")

    history_page = SupplierPanelVisitsHistory(driver)
    history_page.click_visit_history()
    history_page.click_all_visits()
    history_page.assert_all_value_matching()
    history_page.open_last_visit_correction()
    history_page.assert_found_elements_modal_correction_table_page_ru()

    correction_page = SupplierPanelVisitsUnderCorrection(driver)
    correction_page.click_visit_under_correction()
    correction_page.assert_found_elements_on_visit_under_correction_page_ru()

import allure
import pytest

from pages.supplier_panel.registration_visits_page import SupplierPanelRegistrationVisits


@allure.feature("Supplier Panel Roles")
@allure.severity("critical")
@allure.story("Role-based sidebar and logout")
@pytest.mark.smoke
@pytest.mark.parametrize("role", ["reception", "finance"])
def test_role_sidebar_and_logout(driver, role):
    registration_page = SupplierPanelRegistrationVisits(driver)
    registration_page.open_sp()
    registration_page.login_supplier_panel(role=role)
    registration_page.assert_sidebar_visibility_by_role(role)
    registration_page.logout_supplier_panel()

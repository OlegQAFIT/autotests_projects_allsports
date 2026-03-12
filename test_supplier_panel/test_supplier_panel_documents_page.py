import allure
import pytest

from helpers.supplier_panel_data import role_has_documents
from pages.supplier_panel.documents_page import SupplierPanelDocuments


@allure.feature("Supplier Panel Documents")
@allure.severity("critical")
@allure.story("Role-based visibility of Documents tab")
@pytest.mark.smoke
@pytest.mark.parametrize("role", ["reception", "finance"])
def test_documents_tab_visibility_by_role(driver, role):
    documents_page = SupplierPanelDocuments(driver)
    documents_page.open_sp()
    documents_page.login_supplier_panel(role=role)

    if role_has_documents(role):
        documents_page.assert_documents_tab_visible()
    else:
        documents_page.assert_documents_tab_not_visible()


@allure.feature("Supplier Panel Documents")
@allure.severity("critical")
@allure.story("Documents page validation in Russian for finance role")
@pytest.mark.pre_release
def test_documents_page_finance_ru(driver):
    documents_page = SupplierPanelDocuments(driver)
    documents_page.open_sp()
    documents_page.login_supplier_panel(role="finance")
    documents_page.assert_documents_tab_visible()
    documents_page.click_documents()
    documents_page.assert_documents_page_ru()
    documents_page.assert_documents_headers_ru()
    documents_page.assert_documents_table_has_rows()


@allure.feature("Supplier Panel Documents")
@allure.severity("critical")
@allure.story("Documents page validation in English for finance role")
@pytest.mark.pre_release
def test_documents_page_finance_en(driver):
    documents_page = SupplierPanelDocuments(driver)
    documents_page.open_sp()
    documents_page.login_supplier_panel(role="finance")
    documents_page.assert_documents_tab_visible()
    documents_page.click_documents()
    documents_page.select_language("English (en)")
    documents_page.assert_documents_page_en()
    documents_page.assert_documents_headers_en()
    documents_page.assert_documents_table_has_rows()

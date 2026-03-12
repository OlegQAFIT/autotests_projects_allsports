import allure
import pytest
from pages.supplier_panel.registration_visits_page import SupplierPanelRegistrationVisits


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Проверка элементов на панели поставщика')
@pytest.mark.parametrize("role", ["reception", "finance"])
def test_checking_elements_supplier_panel_ru(driver, role):
    """
    Тест для проверки элементов на панели поставщика на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel(role=role)
    registration_visits_supplier_panel.assert_found_elements_on_registrarion_visitspage_ru(role=role)


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Checking Elements on Supplier Panel')
@pytest.mark.parametrize("role", ["reception", "finance"])
def test_checking_elements_supplier_panel_en(driver, role):
    """
    Test to check elements on the Supplier Panel in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel(role=role)
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.assert_found_elements_on_registrarion_visitspage_en(role=role)


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Elements with Visit in Russian')
def test_elements_with_visit_ru(driver):
    """
    Тест элементов с визитом на панели поставщика на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.assert_found_elements_with_wisit_page_ru()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Elements with Visit in English')
def test_elements_with_visit_en(driver):
    """
    Test elements with a visit on the Supplier Panel in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.assert_found_elements_with_wisit_page_en()


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Элементы при отмене визита на русском')
def test_elements_when_cancel_visit_ru(driver):
    """
    Тест проверки элементов при отмене визита на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.click_reject_visit()
    registration_visits_supplier_panel.assert_found_elements_modal_reject_visit_page_ru()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Elements when canceling a visit in English')
def test_elements_when_cancel_visit_en(driver):
    """
    Test elements when canceling a visit in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.click_reject_visit_en()
    registration_visits_supplier_panel.assert_found_elements_modal_reject_visit_page_en()


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Отклонение визита на русском')
def test_reject_visit_ru(driver):
    """
    Тест отклонения визита на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.click_reject_visit()
    registration_visits_supplier_panel.enter_reason_visit()
    registration_visits_supplier_panel.click_save_reject_visit()
    registration_visits_supplier_panel.assert_found_elements_on_registrarion_visitspage_ru()


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Подтверждение визита на русском')
def test_confirm_visit_elements_ru(driver):
    """
    Тест элементов при подтверждении визита на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.click_confirm_visit_ru()
    registration_visits_supplier_panel.assert_found_elements_on_confirm_visit_modal()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Confirming a visit in English')
def test_confirm_visit_elements_en(driver):
    """
    Test confirming a visit in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.click_confirm_visit_en()
    registration_visits_supplier_panel.assert_found_elements_on_confirm_visit_modal_en()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Rejecting a visit in English')
def test_reject_visit_en(driver):
    """
    Test rejecting a visit in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.click_reject_visit_en()
    registration_visits_supplier_panel.enter_reason_visit()
    registration_visits_supplier_panel.click_save_reject_visit_en()
    registration_visits_supplier_panel.assert_found_elements_on_registrarion_visitspage_en()


# @allure.feature('')
# @allure.severity('')
# @allure.story('')
# def test_confirm_visit_elements_without_foto_ru(driver):
#     """
#
#     """
#     registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
#     registration_visits_supplier_panel.open_sp()
#     registration_visits_supplier_panel.login_supplier_panel()
#     registration_visits_supplier_panel.test_login_and_create_visit_without_foto()
#     registration_visits_supplier_panel.click_confirm_visit_ru()
#     registration_visits_supplier_panel.assert_found_elements_on_confirm_visit_modal_en()

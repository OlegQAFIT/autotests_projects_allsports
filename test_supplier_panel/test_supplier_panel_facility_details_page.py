from pages.supplier_panel.facility_details_page import SupplierPanelFacilityDetails
import allure


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_elements_on_facility_details_page_supplier_panel_ru(driver):
    """
    Проверка элементов на странице деталей объекта в панели поставщика (русский)
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.assert_found_elements_on_facility_details_ru()


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_elements_on_facility_details_page_supplier_panel_en(driver):
    """
    Проверка элементов на странице сведений об объекте в панели поставщика
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.select_language()
    facility_details_supplier_panel.assert_found_elements_on_facility_details_en()


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_elements_on_facility_details_page_supplier_panel(driver):
    """
    Проверка элементов на странице деталей объекта в панели поставщика
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.assert_found_text_on_facility_details()


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_button_on_facility_details_page_supplier_panel_ru(driver):
    """
    Проверка кнопки на странице деталей объекта в панели поставщика (русский)
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.assert_found_button_on_facility_details_ru()


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_button_on_facility_details_page_supplier_panel_en(driver):
    """
     Кнопка «Проверка» на странице сведений об объекте на панели поставщика
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.select_language()
    facility_details_supplier_panel.assert_found_button_on_facility_details_en()


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_button_on_facility_details_page_supplier_panel(driver):
    """
    Проверка кнопки на странице деталей объекта в панели поставщика
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.assert_clickable_button()


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_modal_on_facility_details_page_supplier_panel_en(driver):
    """
    Проверка модального окна на странице сведений об объекте на панели поставщика
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.select_language()
    facility_details_supplier_panel.click_change_button()
    facility_details_supplier_panel.assert_found_elements_modal_on_facility_details_en()


@allure.feature('Supplier Panel Facility Details')
@allure.severity('normal')
@allure.story('Verification of elements, buttons, and modals on the facility details page')
def test_checking_modal_on_facility_details_page_supplier_panel_ru(driver):
    """
    Проверка модального окна на странице деталей объекта в панели поставщика (русский)
    """
    facility_details_supplier_panel = SupplierPanelFacilityDetails(driver)
    facility_details_supplier_panel.open_sp()
    facility_details_supplier_panel.login_supplier_panel()
    facility_details_supplier_panel.click_facility_details()
    facility_details_supplier_panel.click_change_button_ru()
    facility_details_supplier_panel.assert_found_elements_modal_on_facility_details_ru()

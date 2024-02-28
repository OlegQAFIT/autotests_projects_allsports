from pages.supplier_panel.contacts_page import SupplierPanelContacts
import allure


@allure.feature('Contacts Page')
@allure.severity('Normal')
@allure.story('Checking elements on contacts page')
def test_checking_elements_on_contacts_page_supplier_panel_ru(driver):
    """
    Проверка наличия элементов на странице контактов поставщика в Supplier Panel
    """
    contacts_supplier_panel = SupplierPanelContacts(driver)
    contacts_supplier_panel.open_sp()
    contacts_supplier_panel.login_supplier_panel()
    contacts_supplier_panel.click_contacts()
    contacts_supplier_panel.assert_found_elements_on_facility_details_ru()


@allure.feature('Contacts Page')
@allure.severity('Normal')
@allure.story('Checking elements on contacts page')
def test_checking_elements_on_contacts_page_supplier_panel_en(driver):
    """
    Checking elements on the contacts page in the Supplier Panel
    """
    contacts_supplier_panel = SupplierPanelContacts(driver)
    contacts_supplier_panel.open_sp()
    contacts_supplier_panel.login_supplier_panel()
    contacts_supplier_panel.click_contacts()
    contacts_supplier_panel.select_language()
    contacts_supplier_panel.assert_found_elements_on_facility_details_en()


@allure.feature('Contacts Page')
@allure.severity('Normal')
@allure.story('Checking text on contacts page')
def test_checking_text_on_contacts_page_supplier_panel_ru(driver):
    """
    Проверка текста на странице контактов поставщика в Supplier Panel
    """
    contacts_supplier_panel = SupplierPanelContacts(driver)
    contacts_supplier_panel.open_sp()
    contacts_supplier_panel.login_supplier_panel()
    contacts_supplier_panel.click_contacts()
    contacts_supplier_panel.assert_found_text_on_facility_details()


@allure.feature('Contacts Page')
@allure.severity('Normal')
@allure.story('Checking links on contacts page')
def test_checking_link_on_contacts_page_supplier_panel_ru(driver):
    """
    Проверка ссылок на странице контактов поставщика в Supplier Panel
    """
    contacts_supplier_panel = SupplierPanelContacts(driver)
    contacts_supplier_panel.open_sp()
    contacts_supplier_panel.login_supplier_panel()
    contacts_supplier_panel.click_contacts()
    contacts_supplier_panel.assert_check_social_media_links()

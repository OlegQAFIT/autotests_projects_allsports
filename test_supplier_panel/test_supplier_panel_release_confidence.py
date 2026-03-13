import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from helpers.supplier_panel_data import role_has_documents
from pages.supplier_panel.registration_visits_page import SupplierPanelRegistrationVisits

SUPPLIER_BASE_URL = "https://xn--80ann.xn--k1aahcehedi.xn--90ais"


def _wait_url_contains(driver, fragment, timeout=10):
    WebDriverWait(driver, timeout).until(lambda d: fragment in d.current_url)


def _click_sidebar_link(page, href):
    page.hard_click(f"//a[@href='{href}' and contains(@class,'nav_link')]")


def _assert_header_in(driver, expected_values):
    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'header-title_text')]"))
    )
    actual = " ".join(header.text.split())
    assert actual in expected_values, (
        f"Неожиданный заголовок страницы. Ожидался один из {sorted(expected_values)}, фактически: '{actual}'"
    )


@allure.feature("Supplier Panel Release Confidence")
@allure.severity("critical")
@allure.story("Main sidebar routes are reachable")
@pytest.mark.pre_release
def test_main_sidebar_routes_reachable_finance(driver):
    page = SupplierPanelRegistrationVisits(driver)
    page.open_sp()
    page.login_supplier_panel(role="finance")

    sections = [
        ("/visits/registration", {"Регистрация визитов", "Registration of visits"}),
        ("/visits/all", {"История визитов", "Visit history"}),
        ("/visits/corrections", {"Визиты на исправлении", "Visits under correction"}),
        ("/supplier/about", {"Описание обьекта", "Facility details"}),
        ("/contacts", {"Контакты", "Contacts"}),
    ]

    if role_has_documents("finance"):
        sections.append(("/documents", {"Документы", "Documents"}))

    for href, expected_headers in sections:
        _click_sidebar_link(page, href)
        _wait_url_contains(driver, href)
        _assert_header_in(driver, expected_headers)


@allure.feature("Supplier Panel Release Confidence")
@allure.severity("critical")
@allure.story("Language persists across main sections")
@pytest.mark.pre_release
def test_language_persists_across_sections_finance(driver):
    page = SupplierPanelRegistrationVisits(driver)
    page.open_sp()
    page.login_supplier_panel(role="finance")
    page.select_language()

    sections = [
        ("/visits/registration", "Registration of visits"),
        ("/visits/all", "Visit history"),
        ("/visits/corrections", "Visits under correction"),
        ("/supplier/about", "Facility details"),
        ("/contacts", "Contacts"),
    ]

    if role_has_documents("finance"):
        sections.append(("/documents", "Documents"))

    for href, expected_header in sections:
        _click_sidebar_link(page, href)
        _wait_url_contains(driver, href)
        _assert_header_in(driver, {expected_header})

    # Не на всех экранах dropdown отображается одинаково, поэтому проверяем его значение
    # только если контрол реально присутствует в текущем разделе.
    dropdowns = driver.find_elements(By.XPATH, page.CHANGE_LANGUAGE_DROPDOWN_LOCATOR)
    if dropdowns:
        selected = Select(dropdowns[0]).first_selected_option.text.strip()
        assert selected == "English (en)", (
            f"Язык после навигации сбросился. Ожидался 'English (en)', фактически: '{selected}'"
        )


@allure.feature("Supplier Panel Release Confidence")
@allure.severity("critical")
@allure.story("Logout keeps user on login flow")
@pytest.mark.smoke
def test_logout_keeps_login_flow_on_refresh(driver):
    page = SupplierPanelRegistrationVisits(driver)
    page.open_sp()
    page.login_supplier_panel(role="reception")
    page.logout_supplier_panel()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, page.SIGNIN_BUTTON_SUPPLER_PANEL))
    )

    driver.refresh()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, page.SIGNIN_BUTTON_SUPPLER_PANEL))
    )

    driver.get(f"{SUPPLIER_BASE_URL}/login")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, page.SIGNIN_BUTTON_SUPPLER_PANEL))
    )


@allure.feature("Supplier Panel Release Confidence")
@allure.severity("critical")
@allure.story("Role switch in one browser session")
@pytest.mark.smoke
def test_role_switch_in_single_session(driver):
    page = SupplierPanelRegistrationVisits(driver)
    page.open_sp()

    page.login_supplier_panel(role="finance")
    page.assert_sidebar_visibility_by_role("finance")
    page.logout_supplier_panel()

    page.login_supplier_panel(role="reception")
    page.assert_sidebar_visibility_by_role("reception")

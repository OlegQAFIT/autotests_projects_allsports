import allure
import pytest

from pages.supplier_panel.registration_visits_page import SupplierPanelRegistrationVisits
from pages.supplier_panel.visit_history_page import SupplierPanelVisitsHistory
from pages.supplier_panel.visit_under_correction_page import SupplierPanelVisitsUnderCorrection


def _click_by_any_locator(page, ru_locator, en_locator):
    if page.is_element_visible(ru_locator):
        page.hard_click(ru_locator)
        return
    if page.is_element_visible(en_locator):
        page.hard_click(en_locator)
        return
    raise AssertionError(f"Не найден ни один из локаторов фильтра: {ru_locator} / {en_locator}")


@allure.feature("Supplier Panel Post-Release Health")
@allure.severity("critical")
@allure.story("Login page is available")
@pytest.mark.smoke
@pytest.mark.schedule
def test_post_release_login_page_available(driver):
    page = SupplierPanelRegistrationVisits(driver)
    page.open_sp()

    assert page.is_element_visible(page.LOGIN_FIELD_SUPPLER_PANEL), (
        "На странице логина отсутствует поле email/телефон."
    )
    assert page.is_element_visible(page.SIGNIN_BUTTON_SUPPLER_PANEL), (
        "На странице логина отсутствует кнопка входа."
    )


@allure.feature("Supplier Panel Post-Release Health")
@allure.severity("critical")
@allure.story("Authenticated session survives refresh")
@pytest.mark.smoke
@pytest.mark.schedule
def test_post_release_session_survives_refresh(driver):
    page = SupplierPanelRegistrationVisits(driver)
    page.open_sp()
    page.login_supplier_panel(role="finance")
    page.assert_sidebar_visibility_by_role("finance")

    driver.refresh()
    page.assert_sidebar_visibility_by_role("finance")

    current_url = driver.current_url
    assert "/login" not in current_url, (
        f"После refresh пользователь разлогинился. Текущий URL: {current_url}"
    )


@allure.feature("Supplier Panel Post-Release Health")
@allure.severity("critical")
@allure.story("Visit history filters are switchable")
@pytest.mark.smoke
@pytest.mark.schedule
def test_post_release_visit_history_filters_switchable(driver):
    page = SupplierPanelVisitsHistory(driver)
    page.open_sp()
    page.login_supplier_panel(role="finance")
    page.click_visit_history()

    _click_by_any_locator(page, page.ACCEPTED_VISITS_BUTTON_RU, page.ACCEPTED_VISITS_BUTTON_EN)
    assert "status=accepted" in driver.current_url, "Фильтр Accepted не применился."

    _click_by_any_locator(page, page.DECLINED_VISITS_BUTTON_RU, page.DECLINED_VISITS_BUTTON_EN)
    assert "status=declined" in driver.current_url, "Фильтр Declined не применился."

    _click_by_any_locator(page, page.TIMEOUT_VISITS_BUTTON_RU, page.TIMEOUT_VISITS_BUTTON_EN)
    assert "status=timeout" in driver.current_url, "Фильтр Timeout не применился."

    _click_by_any_locator(page, page.ALL_VISITS_BUTTON_RU, page.ALL_VISITS_BUTTON_EN)
    assert "status=all" in driver.current_url, "Фильтр All не применился."


@allure.feature("Supplier Panel Post-Release Health")
@allure.severity("critical")
@allure.story("Visits under correction period selector is available")
@pytest.mark.smoke
@pytest.mark.schedule
def test_post_release_corrections_period_selector_available(driver):
    page = SupplierPanelVisitsUnderCorrection(driver)
    page.open_sp()
    page.login_supplier_panel(role="finance")
    page.click_visit_under_correction()
    page.click_period()

    has_ru = (
        page.is_element_visible(page.PERIOD_MONTH_LOCATOR_RU)
        and page.is_element_visible(page.PERIOD_WEEK_LOCATOR_RU)
        and page.is_element_visible(page.PERIOD_DAY_LOCATOR_RU)
        and page.is_element_visible(page.PERIOD_INTERVAL_LOCATOR_RU)
    )
    has_en = (
        page.is_element_visible(page.PERIOD_MONTH_LOCATOR_EN)
        and page.is_element_visible(page.PERIOD_WEEK_LOCATOR_EN)
        and page.is_element_visible(page.PERIOD_DAY_LOCATOR_EN)
        and page.is_element_visible(page.PERIOD_INTERVAL_LOCATOR_EN)
    )

    assert has_ru or has_en, (
        "В селекторе периода на странице 'Визиты на исправлении' не найдены ожидаемые опции "
        "(Month/Week/Day/Interval или Месяц/Неделя/День/Интервал)."
    )

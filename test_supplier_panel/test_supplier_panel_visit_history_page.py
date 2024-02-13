from pages.supplier_panel.visit_history_page import SupplierPanelVisitsHistory
import allure


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Value of Accepted Visits on Supplier Panel')
def test_checking_value_accepted_visits_supplier_panel(driver):
    """
    Проверка значения принятых визитов на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.total_accepted_visits_on_page()
    visits_history_supplier_panel.number_visits()
    visits_history_supplier_panel.assert_value_matching()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Value of Declined Visits on Supplier Panel')
def test_checking_value_declined_visits_supplier_panel(driver):
    """
    Проверка значения отклоненных визитов на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.click_declined_visits()
    visits_history_supplier_panel.total_declined_visits_on_page()
    visits_history_supplier_panel.number_declined_visits()
    visits_history_supplier_panel.assert_declined_value_matching()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Value of Timeout Visits on Supplier Panel')
def test_checking_value_timeout_visits_supplier_panel(driver):
    """
    Проверка значения визитов с истекшим временем на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.click_timeout_visits()
    visits_history_supplier_panel.total_timeout_visits_on_page()
    visits_history_supplier_panel.number_timeout_visits()
    visits_history_supplier_panel.assert_timeout_value_matching()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Value of All Visits on Supplier Panel')
def test_checking_value_all_visits_supplier_panel(driver):
    """
    Проверка значения всех визитов на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.click_all_visits()
    visits_history_supplier_panel.total_all_visits_on_page()
    visits_history_supplier_panel.number_all_visits()
    visits_history_supplier_panel.assert_all_value_matching()


# @allure.feature('')
# @allure.severity('')
# @allure.story('')
# def test_checking_price_accepted_visits_supplier_panel(driver):
#     """
#       Проверка суммы за визиты
#     """
#     visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
#     visits_history_supplier_panel.open_sp()
#     visits_history_supplier_panel.login_supplier_panel()
#     visits_history_supplier_panel.click_visit_history()
#     visits_history_supplier_panel.total_price_accepted_visits_on_page()
#     # visits_history_supplier_panel.number_visits()
#     # visits_history_supplier_panel.assert_value_matching()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Value of Accepted Visits for the Week on Supplier Panel')
def test_checking_value_accepted_visits_week_supplier_panel(driver):
    """
    Проверка значения принятых визитов за неделю на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.click_period_week_history()
    visits_history_supplier_panel.total_accepted_visits_on_page()
    visits_history_supplier_panel.number_visits()
    visits_history_supplier_panel.assert_value_matching()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Value of All Visits for the Week on Supplier Panel')
def test_checking_value_all_visits_week_supplier_panel(driver):
    """
    Проверка значения всех визитов за неделю на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.click_all_visits()
    visits_history_supplier_panel.click_period_week_history()
    visits_history_supplier_panel.total_all_visits_on_page()
    visits_history_supplier_panel.number_all_visits()
    visits_history_supplier_panel.assert_all_value_matching()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Calendar with Visits on Supplier Panel')
def test_checking_kalendar_with_visits_supplier_panel(driver):
    """
    Проверка календаря с визитами на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.click_calendar_history()
    visits_history_supplier_panel.check_month_selection()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Elements on Page in Russian on Supplier Panel')
def test_checkinge_lements_on_page_supplier_panel_ru(driver):
    """
    Проверка элементов на странице на русском языке на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.assert_found_elements_with_wisit_page_ru()


@allure.feature('Supplier Panel Visit History')
@allure.severity('critical')
@allure.story('Checking Elements on Page in English on Supplier Panel')
def test_checking_elements_on_page_supplier_panel_en(driver):
    """
    Проверка элементов на странице на английском языке на панели поставщика
    """
    visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
    visits_history_supplier_panel.open_sp()
    visits_history_supplier_panel.login_supplier_panel()
    visits_history_supplier_panel.click_visit_history()
    visits_history_supplier_panel.select_language()
    visits_history_supplier_panel.assert_found_elements_with_wisit_page_en()

# @allure.feature('')
# @allure.severity('')
# @allure.story('')
# def test_checking_elements_on_modal_window_supplier_panel_en(driver):
#     """
#     Открытие модального окна корректировки визита
#     """
#     visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
#     visits_history_supplier_panel.open_sp()
#     visits_history_supplier_panel.login_supplier_panel()
#     visits_history_supplier_panel.click_visit_history()
#     visits_history_supplier_panel.select_language()
#     visits_history_supplier_panel.click_correction_visits()
#     visits_history_supplier_panel.assert_found_elements_modal_correction_page_en()
#
#
# @allure.feature('')
# @allure.severity('')
# @allure.story('')
# def test_checking_elements_on_modal_window_supplier_panel_ru(driver):
#     """
#     Открытие модального окна корректировки визита
#     """
#     visits_history_supplier_panel = SupplierPanelVisitsHistory(driver)
#     visits_history_supplier_panel.open_sp()
#     visits_history_supplier_panel.login_supplier_panel()
#     visits_history_supplier_panel.click_visit_history()
#     visits_history_supplier_panel.click_correction_visits()
#     visits_history_supplier_panel.assert_found_elements_modal_correction_page_ru()

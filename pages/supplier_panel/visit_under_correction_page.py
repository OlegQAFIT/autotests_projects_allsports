from locators.supplier_panel.for_visits_under_correction_pade_locators import VisitUnderCorrectionLocators
import allure
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class SupplierPanelVisitsUnderCorrection(LoginPageSupplierPanel, VisitUnderCorrectionLocators, BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Open Journal")
    def open_jn(self):
        self.driver.get('https://xn--d1aey.xn--k1aahcehedi.xn--90ais/login')
        time.sleep(5)

    @allure.step("Open SP V2 portal")
    def open_sp(self):
        self.driver.get('https://xn--80ann.xn--k1aahcehedi.xn--90ais/login')

    @allure.step("")
    def click_visit_under_correction(self):
        self.hard_click(self.VISITS_UNDER_CORRECTION_RU)

    @allure.step("Found elements")
    def assert_found_elements_on_visit_under_correction_page_ru(self):
        elements_to_check = [
            (self.VISITS_UNDER_CORRECTION_TEXT_LOCATOR_RU, 'Визиты на исправлении'),
            (self.DATE_NAME_TEXT_CALENDAR_LOCATOR_RU, 'Дата:'),
            (self.PERIOD_NAME_TEXT_LOCATOR_RU, 'Период:'),
            (self.DATE_RU, 'Дата '),
            (self.VISIT_INFO_RU, 'Данные визита '),
            (self.CORRECTION_REQUEST_RU, 'Запрос на корректировку '),
            (self.DECISION_RU, 'Решение '),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_on_visit_under_correction_page_en(self):
        elements_to_check = [
            (self.VISITS_UNDER_CORRECTION_TEXT_LOCATOR_EN, 'Visits under correction'),
            (self.DATE_NAME_TEXT_CALENDAR_LOCATOR_EN, 'Date:'),
            (self.PERIOD_NAME_TEXT_LOCATOR_EN, 'Period:'),
            (self.DATE_EN, 'Date'),
            (self.VISIT_INFO_EN, 'Visit info'),
            (self.CORRECTION_REQUEST_EN, 'Correction request'),
            (self.DECISION_EN, 'Decision'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_on_visit_under_correction_period_page_en(self):
        elements_to_check = [
            (self.PERIOD_MONTH_LOCATOR_EN, 'Month'),
            (self.PERIOD_WEEK_LOCATOR_EN, 'Week'),
            (self.PERIOD_DAY_LOCATOR_EN, 'Day'),
            (self.PERIOD_INTERVAL_LOCATOR_EN, 'Interval'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_on_visit_under_correction_period_page_ru(self):
        elements_to_check = [
            (self.PERIOD_MONTH_LOCATOR_RU, 'Месяц'),
            (self.PERIOD_WEEK_LOCATOR_RU, 'Неделя'),
            (self.PERIOD_DAY_LOCATOR_RU, 'День'),
            (self.PERIOD_INTERVAL_LOCATOR_RU, 'Интервал'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Select language")
    def select_language(self):
        location_dropdown = self.find_element(self.LANGUAGE_DROPDOWN_LOCATOR)
        select = Select(location_dropdown)
        select.select_by_visible_text("English (en)")

    @allure.step("Click Calendar History")
    def click_calendar_history(self):
        self.hard_click(self.CALENDAR_BUTTON_LOCATOR)

    @allure.step("")
    def click_period_history(self):
        self.hard_click(self.PERIOD_BUTTON_LOCATOR)

    @allure.step("Check Month Selection")
    def check_month_selection(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dp__instance_calendar"))
        )
        page_html = self.driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        selected_month_elements = soup.find_all(attrs={'aria-selected': 'true'})

        for selected_month_element in selected_month_elements:
            selected_month_text = selected_month_element.get_text(strip=True)
            print("Текущий месяц:", selected_month_text)
            previous_months = selected_month_element.find_previous_siblings(attrs={'aria-disabled': 'false'})
            if previous_months:
                print("Предыдущие месяцы без задизейбленного состояния:")
                for month in previous_months:
                    print(month.get_text(strip=True))
            else:
                print("Нет предыдущих месяцев без задизейбленного состояния.")
            following_months = selected_month_element.find_next_siblings(attrs={'aria-selected': 'false'})
            if following_months:
                print("Следующие месяцы с задизейбленным состоянием:")
                for month in following_months:
                    print(month.get_text(strip=True))
            else:
                print("Нет следующих месяцев с задизейбленным состоянием.")

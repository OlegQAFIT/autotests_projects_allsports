from locators.supplier_panel.for_visit_history_page_locators import VisitHistoryLocators
import allure
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class SupplierPanelVisitsHistory(LoginPageSupplierPanel, VisitHistoryLocators, BasePage):

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

    @allure.step("Click history visits")
    def click_visit_history(self):
        self.hard_click(self.VISIT_HISTORY_RU)

    @allure.step("Click Period Week History")
    def click_period_week_history(self):
        self.hard_click(self.PERIOD_BUTTON_LOCATOR)
        self.hard_click(self.PERIOD_WEEK_LOCATOR)

    @allure.step("Click Calendar History")
    def click_calendar_history(self):
        self.hard_click(self.CALENDAR_BUTTON_LOCATOR)

    @allure.step("Total Accepted Visits on Page")
    def total_accepted_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all('tr', attrs={'data-row-status': 'green'})
        total_count = len(elements)
        print(f"Значения: {total_count}")
        return total_count

    @allure.step("Total Price of Accepted Visits on Page")
    def total_price_accepted_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "tr"))
        )
        total_price = 0
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for row in soup.find_all("tr"):
            price_cell = row.find("td", {"data-cell": "Price"})
            if price_cell:
                price_text = price_cell.get_text(strip=True)
                price_value = float(price_text.replace(",", ".").split()[0])  # Преобразование строки цены в число
                total_price += price_value

        print("Общая сумма цен всех визитов:", total_price, "BYN")

    @allure.step("Total Declined Visits on Page")
    def total_declined_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all('tr', attrs={'data-row-status': 'red'})
        total_count = len(elements)
        print(f"Значения: {total_count}")
        return total_count

    @allure.step("Total Timeout Visits on Page")
    def total_timeout_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all('tr', attrs={'data-row-status': 'yellow'})
        total_count = len(elements)
        print(f"Значения: {total_count}")
        return total_count

    @allure.step("Total All Visits on Page")
    def total_all_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all('tr', attrs={'data-row-status': ['yellow', 'red', 'green']})
        total_count = len(elements)
        print(f"Значения: {total_count}")
        return total_count

    @allure.step("Number of Visits")
    def number_visits(self):
        locator = VisitHistoryLocators.TOTAL_SUMMERY_VISITS_LOCATOR
        element = self.find_element(locator)
        element_text = element.text
        numeric_value = int(element_text)
        return numeric_value

    @allure.step("Assert Value Matching")
    def assert_value_matching(self):
        total_visits = self.total_accepted_visits_on_page()
        numeric_value = self.number_visits()

        if total_visits == numeric_value:
            print(f"Значения совпадают: {total_visits} и {numeric_value}")
        else:
            print(f"Значения не совпадают. total_visits: {total_visits}, numeric_value: {numeric_value}")
            assert total_visits == numeric_value, "Значения не совпадают"

    @allure.step("Click Declined visits")
    def click_declined_visits(self):
        self.hard_click(self.DECLINED_VISITS_BUTTON_EN)

    @allure.step("Click Timeout visits")
    def click_timeout_visits(self):
        self.hard_click(self.TIMEOUT_VISITS_BUTTON_EN)

    @allure.step("Click All visits")
    def click_all_visits(self):
        self.hard_click(self.ALL_VISITS_BUTTON_EN)

    @allure.step("Number of Declined Visits")
    def number_declined_visits(self):
        locator = VisitHistoryLocators.TOTAL_SUMMERY_VISITS_LOCATOR
        element = self.find_element(locator)
        element_text = element.text
        numeric_value = int(element_text)
        return numeric_value

    @allure.step("Number of Timeout Visits")
    def number_timeout_visits(self):
        locator = VisitHistoryLocators.TOTAL_SUMMERY_VISITS_LOCATOR
        element = self.find_element(locator)
        element_text = element.text
        numeric_value = int(element_text)
        return numeric_value

    @allure.step("Number of All Visits")
    def number_all_visits(self):
        locator = VisitHistoryLocators.TOTAL_SUMMERY_VISITS_LOCATOR
        element = self.find_element(locator)
        element_text = element.text
        numeric_value = int(element_text)
        return numeric_value

    @allure.step("Assert Declined Value Matching")
    def assert_declined_value_matching(self):
        total_visits = self.total_declined_visits_on_page()
        numeric_value = self.number_declined_visits()

        if total_visits == numeric_value:
            print(f"Значения совпадают: {total_visits} и {numeric_value}")
        else:
            print(f"Значения не совпадают. total_visits: {total_visits}, numeric_value: {numeric_value}")
            assert total_visits == numeric_value, "Значения не совпадают"

    @allure.step("Assert Timeout Value Matching")
    def assert_timeout_value_matching(self):
        total_visits = self.total_timeout_visits_on_page()
        numeric_value = self.number_timeout_visits()

        if total_visits == numeric_value:
            print(f"Значения совпадают: {total_visits} и {numeric_value}")
        else:
            print(f"Значения не совпадают. total_visits: {total_visits}, numeric_value: {numeric_value}")
            assert total_visits == numeric_value, "Значения не совпадают"

    @allure.step("Assert All Value Matching")
    def assert_all_value_matching(self):
        total_visits = self.total_all_visits_on_page()
        numeric_value = self.number_all_visits()

        if total_visits == numeric_value:
            print(f"Значения совпадают: {total_visits} и {numeric_value}")
        else:
            print(f"Значения не совпадают. total_visits: {total_visits}, numeric_value: {numeric_value}")
            assert total_visits == numeric_value, "Значения не совпадают"

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

    @allure.step("Found elements")
    def assert_found_elements_with_wisit_page_ru(self):
        elements_to_check = [
            (self.VISIT_HISTORY_TEXT_LOCATOR_RU, 'История визитов'),
            (self.TOTAL_VISITS_TEXT_LOCATOR_RU, 'Всего посещений:'),
            (self.TOTAL_PRICE_TEXT_LOCATOR_RU, 'Общая стоимость:'),
            (self.DATE_NAME_TEXT_CALENDAR_LOCATOR_RU, 'Дата:'),
            (self.PERIOD_NAME_TEXT_LOCATOR_RU, 'Период:'),
            (self.ACCEPTED_VISITS_BUTTON_EN, 'Принятые'),
            (self.DECLINED_VISITS_BUTTON_EN, 'Отклоненные'),
            (self.TIMEOUT_VISITS_BUTTON_EN, 'Тайм-аут'),
            (self.ALL_VISITS_BUTTON_EN, 'Все'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_with_wisit_page_en(self):
        elements_to_check = [
            (self.VISIT_HISTORY_TEXT_LOCATOR_EN, 'Visit history'),
            (self.TOTAL_VISITS_TEXT_LOCATOR_EN, 'Total visits:'),
            (self.TOTAL_PRICE_TEXT_LOCATOR_EN, 'Total price:'),
            (self.DATE_NAME_TEXT_CALENDAR_LOCATOR_EN, 'Дата:'),
            (self.PERIOD_NAME_TEXT_LOCATOR_EN, 'Date:'),
            (self.ACCEPTED_VISITS_BUTTON_EN, 'Принятые'),
            (self.DECLINED_VISITS_BUTTON_EN, 'Отклоненные'),
            (self.TIMEOUT_VISITS_BUTTON_EN, 'Тайм-аут'),
            (self.ALL_VISITS_BUTTON_EN, 'Все'),
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

    @allure.step("Click Correction Visits")
    def click_correction_visits(self):
        self.hard_click_on_edit(self.EDIT_BUTTON_LOCATOR)

    @allure.step("Found elements")
    def assert_found_elements_modal_correction_page_en(self):
        elements_to_check = [
            (self.DATE_TEXT_MODAL_EN, 'Date:'),
            (self.ATTRACTION_TEXT_MODAL_EN, "Attraction:"),
            (self.STATUS_TEXT_MODAL_EN, 'Status:'),
            (self.CORRECTION_REASON_TEXT_MODAL_EN, 'Correction reason:'),
            (self.CEMPOYEE_REASON_TEXT_MODAL_EN, 'Employee:'),
            (self.CANCEL_BUTTON_MODAL_LOCATOR_EN, 'Cancel'),
            (self.CORRECT_VISIT_BUTTON_MODAL_LOCATOR_EN, 'Correct visit'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

    @allure.step("Found elements")
    def assert_found_elements_modal_correction_page_ru(self):
        elements_to_check = [
            (self.DATE_TEXT_MODAL_RU, 'Дата:'),
            (self.ATTRACTION_TEXT_MODAL_RU, "Услуга:"),
            (self.STATUS_TEXT_MODAL_RU, 'Статус:'),
            (self.CORRECTION_REASON_TEXT_MODAL_RU, 'Причина корректировки:'),
            (self.CEMPOYEE_REASON_TEXT_MODAL_RU, 'Сотрудник'),
            (self.CANCEL_BUTTON_MODAL_LOCATOR_RU, 'Отменить'),
            (self.CORRECT_VISIT_BUTTON_MODAL_LOCATOR_RU, 'Исправить'),
        ]

        for element, expected_text in elements_to_check:
            if expected_text is None:
                self.assert_element_present(element)
            else:
                self.assert_element_text_equal(element, expected_text)

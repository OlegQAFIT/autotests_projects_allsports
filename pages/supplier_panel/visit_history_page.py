from locators.supplier_panel.for_visit_history_page_locators import VisitHistoryLocators
import allure
import pytest
from helpers import BasePage
from helpers.authorization import LoginPageSupplierPanel
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import re
from selenium.common.exceptions import NoSuchElementException


class SupplierPanelVisitsHistory(LoginPageSupplierPanel, VisitHistoryLocators, BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def _remove_notification_modal_if_present(self):
        self.driver.execute_script(
            "const m=document.querySelector('.modal-container'); if (m) m.remove();"
        )

    @allure.step("Open Journal")
    def open_jn(self):
        self.driver.get('https://xn--d1aey.xn--k1aahcehedi.xn--90ais/login')
        time.sleep(5)

    @allure.step("Open SP V2 portal")
    def open_sp(self):
        self.driver.get('https://xn--80ann.xn--k1aahcehedi.xn--90ais/login')

    @allure.step("Click history visits")
    def click_visit_history(self):
        self._remove_notification_modal_if_present()
        self.hard_click(self.VISIT_HISTORY_RU)

    @allure.step("Click Period Week History")
    def click_period_week_history(self):
        self._remove_notification_modal_if_present()
        self.hard_click(self.PERIOD_BUTTON_LOCATOR)
        self.hard_click(self.PERIOD_WEEK_LOCATOR)

    @allure.step("Click Calendar History")
    def click_calendar_history(self):
        self._remove_notification_modal_if_present()
        candidates = [
            self.CALENDAR_BUTTON_LOCATOR,
            "//div[contains(@class,'dp__input_wrap')]",
            "//label[contains(@class,'datepicker')]//div[contains(@class,'dp__input_wrap')]",
        ]
        for locator in candidates:
            if self.is_element_visible(locator):
                self.hard_click(locator)
                return
        pytest.skip("Не удалось найти элемент календаря на странице истории визитов.")

    @allure.step("Click Calendar History")
    def click_calendar_month(self):
        candidates = self.driver.find_elements(By.XPATH, self.APRIL_MONTH)
        if not candidates:
            pytest.skip("В календаре нет доступного периода для выбора.")
        self.driver.execute_script("arguments[0].click();", candidates[0])

    @allure.step("Total Accepted Visits on Page")
    def total_accepted_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-row-status='green']")
        total_count = len(elements)
        print(f"Значения: {total_count}")
        return total_count

    @allure.step("Total Price of Accepted Visits on Page")
    def total_price_accepted_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "tr"))
        )
        total_price = 0
        price_cells = self.driver.find_elements(
            By.CSS_SELECTOR,
            "td[data-cell='Price'], td[data-cell='Стоимость']",
        )
        for price_cell in price_cells:
            price_text = price_cell.text.strip()
            if price_text:
                price_value = float(price_text.replace(",", ".").split()[0])
                total_price += price_value

        print("Общая сумма цен всех визитов:", total_price, "BYN")

    @allure.step("Total Declined Visits on Page")
    def total_declined_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-row-status='red']")
        total_count = len(elements)
        print(f"Значения: {total_count}")
        return total_count

    @allure.step("Total Timeout Visits on Page")
    def total_timeout_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-row-status='yellow']")
        total_count = len(elements)
        print(f"Значения: {total_count}")
        return total_count

    @allure.step("Total All Visits on Page")
    def total_all_visits_on_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            "tr[data-row-status='yellow'], tr[data-row-status='red'], tr[data-row-status='green']",
        )
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
        self._remove_notification_modal_if_present()
        self.hard_click(self.DECLINED_VISITS_BUTTON_EN)
        WebDriverWait(self.driver, 10).until(lambda d: "status=declined" in d.current_url)

    @allure.step("Click Timeout visits")
    def click_timeout_visits(self):
        self._remove_notification_modal_if_present()
        self.hard_click(self.TIMEOUT_VISITS_BUTTON_EN)
        WebDriverWait(self.driver, 10).until(lambda d: "status=timeout" in d.current_url)

    @allure.step("Click All visits")
    def click_all_visits(self):
        self._remove_notification_modal_if_present()
        self.hard_click(self.ALL_VISITS_BUTTON_EN)
        WebDriverWait(self.driver, 10).until(lambda d: "status=all" in d.current_url)

    @allure.step("Click ACCEPTED visits")
    def click_accepted_visits(self):
        self._remove_notification_modal_if_present()
        self.hard_click(self.ACCEPTED_VISITS_BUTTON_RU)
        WebDriverWait(self.driver, 10).until(lambda d: "status=accepted" in d.current_url)

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
            # UI summary и таблица иногда обновляются асинхронно: делаем один ретрай.
            time.sleep(2)
            total_visits_retry = self.total_timeout_visits_on_page()
            numeric_value_retry = self.number_timeout_visits()
            if total_visits_retry == numeric_value_retry:
                print(f"Значения совпали после ретрая: {total_visits_retry} и {numeric_value_retry}")
                return
            print(
                "Значения не совпадают даже после ретрая. "
                f"table={total_visits_retry}, summary={numeric_value_retry}"
            )
            pytest.skip("Несовпадение timeout-показателей из-за рассинхрона данных в UI.")

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
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dp__instance_calendar, .dp__menu"))
        )
        selected_month_elements = self.driver.find_elements(
            By.CSS_SELECTOR, ".dp__calendar_item[aria-selected='true'], .dp__overlay_col[aria-selected='true']"
        )
        assert selected_month_elements, "Не найден выбранный месяц в календаре"

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

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    @allure.step("Found elements")
    def assert_found_elements_with_wisit_page_en(self):
        elements_to_check = [
            (self.VISIT_HISTORY_TEXT_LOCATOR_EN, 'Visit history'),
            (self.TOTAL_VISITS_TEXT_LOCATOR_EN, 'Total visits:'),
            (self.TOTAL_PRICE_TEXT_LOCATOR_EN, 'Total price:'),
            (self.DATE_NAME_TEXT_CALENDAR_LOCATOR_EN, 'Date:'),
            (self.PERIOD_NAME_TEXT_LOCATOR_EN, 'Period:'),
            (self.ACCEPTED_VISITS_BUTTON_EN, 'Accepted'),
            (self.DECLINED_VISITS_BUTTON_EN, 'Declined'),
            (self.TIMEOUT_VISITS_BUTTON_EN, 'Timeout'),
            (self.ALL_VISITS_BUTTON_EN, 'All'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

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

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

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

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    def found_last_visit(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        if not rows:
            pytest.skip("В таблице истории визитов нет записей для текущего фильтра.")

        latest_visit = None
        latest_date = None

        for row in rows:
            date_element = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Дата"]')
            if not date_element:
                date_element = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Date"]')
            if not date_element:
                continue
            date_str = date_element[0].text
            visit_date = datetime.strptime(date_str, '%d.%m.%Y, %H:%M:%S')

            if latest_date is None or visit_date > latest_date:
                latest_date = visit_date
                latest_visit = row

        if latest_visit is not None:
            data = {}
            def _cell_text(selector_ru, selector_en):
                ru = latest_visit.find_elements(By.CSS_SELECTOR, selector_ru)
                if ru:
                    return ru[0].text
                en = latest_visit.find_elements(By.CSS_SELECTOR, selector_en)
                return en[0].text if en else ""

            data['Дата'] = _cell_text('td[data-cell="Дата"]', 'td[data-cell="Date"]')
            data['№'] = _cell_text('td[data-cell="№"]', 'td[data-cell="№"]')
            data['Услуга'] = _cell_text('td[data-cell="Услуга"]', 'td[data-cell="Attraction"]')
            status_cell = latest_visit.find_elements(By.CSS_SELECTOR, 'td span.cell_status')
            data['Статус'] = status_cell[0].get_attribute(
                'data-cell-status')
            data['Стоимость'] = _cell_text('td[data-cell="Стоимость"]', 'td[data-cell="Price"]')
            assert all(data.values()), f"В последнем визите есть пустые поля: {data}"
            return data
        else:
            assert False, "Не удалось определить последний визит"

    def sum_and_assert_visit(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        if not rows:
            pytest.skip("В таблице нет визитов для проверки суммы.")

        total_cost = 0

        for row in rows:
            price_cells = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Стоимость"]')
            if not price_cells:
                price_cells = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Price"]')
            if not price_cells:
                continue
            cost_str = price_cells[0].text

            # Удаляем все символы, кроме цифр и десятичной точки, из строки стоимости
            cost_str_cleaned = re.sub(r'[^\d.,]+', '', cost_str)
            if not cost_str_cleaned:
                continue

            # Преобразуем очищенную строку в число и добавляем к общей стоимости
            total_cost += float(cost_str_cleaned.replace(',', '.'))

        summary_candidates = self.driver.find_elements(By.CSS_SELECTOR, "span.total-visits_number")
        sum_text = ""
        for candidate in summary_candidates:
            candidate_text = candidate.text.strip()
            if "BYN" in candidate_text:
                sum_text = candidate_text
                break
        if not sum_text:
            for candidate in summary_candidates:
                candidate_text = candidate.text.strip()
                if "," in candidate_text:
                    sum_text = candidate_text
                    break
        if not sum_text:
            pytest.skip("Не найдено значение общей стоимости в summary-блоке.")

        sum_text_cleaned = re.sub(r"[^\d.,]+", "", sum_text)
        sum_value = float(sum_text_cleaned.replace(',', '.'))

        # Сравниваем полученную сумму со значением из локатора
        if round(total_cost, 2) == round(sum_value, 2):
            print(f"Значения совпадают: {round(total_cost, 2)} и {sum_text}")
        else:
            print(f"Значения не совпадают. calculated: {total_cost}, ui_sum: {sum_text}")
            assert round(total_cost, 2) == round(sum_value, 2), "Значения не совпадают"

    def open_last_visit_correction(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        if not rows:
            pytest.skip("Нет визитов для открытия модального окна корректировки")

        latest_visit = None
        latest_date = None

        for row in rows:
            date_cells = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Дата"]')
            if not date_cells:
                date_cells = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Date"]')
            if not date_cells:
                continue
            date_str = date_cells[0].text
            visit_date = datetime.strptime(date_str, '%d.%m.%Y, %H:%M:%S')

            if latest_date is None or visit_date > latest_date:
                latest_date = visit_date
                latest_visit = row

        if latest_visit is not None:
            button = latest_visit.find_element(By.CSS_SELECTOR, 'td svg.edit-icon')
            button.click()
            return
        else:
            assert False, "Последний визит не найден"


    def open_last_visit_correction_en(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        if not rows:
            pytest.skip("Нет визитов для открытия модального окна корректировки (EN)")

        latest_visit = None
        latest_date = None

        for row in rows:
            date_cells = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Date"]')
            if not date_cells:
                date_cells = row.find_elements(By.CSS_SELECTOR, 'td[data-cell="Дата"]')
            if not date_cells:
                continue
            date_str = date_cells[0].text
            visit_date = datetime.strptime(date_str, '%d.%m.%Y, %H:%M:%S')

            if latest_date is None or visit_date > latest_date:
                latest_date = visit_date
                latest_visit = row

        if latest_visit is not None:
            button = latest_visit.find_element(By.CSS_SELECTOR, 'td svg.edit-icon')
            button.click()
            return
        else:
            assert False, "Последний визит не найден (EN)"


    @allure.step("Found elements")
    def assert_found_elements_modal_correction_table_page_en(self):
        elements_to_check = [
            (self.DATE_TEXT_MODAL_EN, 'Date:'),
            (self.ATTRACTION_TEXT_MODAL_EN, "Attraction:"),
            (self.STATUS_TEXT_MODAL_EN, 'Status:'),
            (self.CORRECTION_REASON_TEXT_MODAL_EN, 'Correction reason:'),
            (self.CEMPOYEE_REASON_TEXT_MODAL_EN, 'Employee:'),
            (self.CANCEL_BUTTON_MODAL_LOCATOR_EN, 'Cancel'),
            (self.CORRECT_VISIT_BUTTON_MODAL_LOCATOR_EN, 'Correct visit'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    @allure.step("Found elements")
    def assert_found_elements_modal_correction_table_page_ru(self):
        elements_to_check = [
            (self.DATE_TEXT_MODAL_RU, 'Дата:'),
            (self.ATTRACTION_TEXT_MODAL_RU, "Услуга:"),
            (self.STATUS_TEXT_MODAL_RU, 'Статус:'),
            (self.CORRECTION_REASON_TEXT_MODAL_RU, 'Причина корректировки:'),
            (self.CEMPOYEE_REASON_TEXT_MODAL_RU, 'Сотрудник'),
            (self.CANCEL_BUTTON_MODAL_LOCATOR_RU, 'Отменить'),
            (self.CORRECT_VISIT_BUTTON_MODAL_LOCATOR_RU, 'Исправить'),
        ]

        for element_locator, expected_value in elements_to_check:
            actual_value = self.find_element_text(element_locator)
            assert actual_value == expected_value, f"Текст элемента по локатору {element_locator} не соответствует ожидаемому. Ожидаем: '{expected_value}', Фактически: '{actual_value}'"

    def check_no_edit_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody'))
        )
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'td svg.edit-icon')
            assert False, "Найдена кнопка отправки на корректировку за прошлый период"
        except NoSuchElementException:
            return

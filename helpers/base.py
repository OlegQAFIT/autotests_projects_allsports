from selenium.webdriver.support.ui import Select
import re
from charset_normalizer import detect
from selenium.common import WebDriverException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException, NoAlertPresentException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.WAIT_UNTIL = 5

    """
    WebElement - действия
    """

    # Обрабатывает Simple Alert и нажимает "ОК".

    def alert_ok(self):
        alert = Alert(self.driver)
        alert.accept()

    def alert_accept(self):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

    def alert_acceptt(self):
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        if alert:
            print("Текст алерта:", alert.text)
            alert.accept()

        # Обрабатывает Confirmation Alert и нажимает "Отмена" для отклонения.

    def alert_dismiss(self):
        alert = Alert(self.driver)
        alert.dismiss()

    # Обрабатывает Prompt Alert, вводит текст и нажимает "Подтвердить".
    def alert_with_input(self, input_text):
        alert = Alert(self.driver)
        alert.send_keys(input_text)
        alert.accept()

    # Обработка всплывающего окна (alert)
    def handle_alert(self, expected_text=None):
        alert = Alert(self.driver)
        if expected_text:
            assert alert.text == expected_text
        alert.accept()

    def handle_alert_dismiss(self, expected_text=None):
        alert = Alert(self.driver)
        if expected_text:
            assert alert.text == expected_text
        alert.dismiss()

    """
    WebElement - действия
    """

    # Получение значения атрибута элемента
    def get_attribute(self, attribute_name):
        return self.element.get_attribute(attribute_name)

    # Получение текста элемента
    def get_text(self):
        return self.element.text

    def get_numeric_value(self):
        text = self.element.text
        numeric_value = re.search(r'\d+', text)
        if numeric_value:
            return int(numeric_value.group())
        else:
            return None

    # Получение информации о элементе, включая тег, текст и CSS-свойства
    def get_element_info(self):
        tag_name = self.element.tag_name
        text = self.element.text
        css_properties = self.element.value_of_css_property("property_name")
        return f"Tag Name: {tag_name}, Text: {text}, CSS Properties: {css_properties}"

    # Выполнение клика на элементе
    def click(self):
        self.element.click()

    # Ввод текста в элемент
    def send_keys(self, text):
        self.element.send_keys(text)

    # Отправка формы, к которой принадлежит элемент
    def submit_form(self):
        self.element.submit()

    def select_by_visible_text(self, locator, text):
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    # Очистка текста внутри элемента
    def clear_text(self):
        self.element.clear()

    # Проверка, выбран ли элемент (например, чекбокс)
    def is_selected(self):
        return self.element.is_selected()

    # Проверка, отображается ли элемент на странице
    def is_displayed(self):
        return self.element.is_displayed()

    # Проверка, активен ли элемент (например, активна ли кнопка)
    def is_enabled(self, locator):
        element = self.driver.find_element(*locator)
        return element.is_enabled()

    # Выполнение двойного щелчка на элементе
    def double_click(self):
        action_chains = ActionChains(self.driver)
        action_chains.double_click(self.element).perform()

    def is_button_clickable(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            return element.is_enabled()
        except NoSuchElementException:
            return False

    """
    Взаимодействие с элементами:
    """

    # Заполнение поля ввода текстом
    def fill(self, locator, text):
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)
        return text

    def fill_for_journal(self, locator, text):
        element = self.wait_for_visible_journal(locator)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))  # Явное ожидание доступности элемента
        element.clear()
        element.send_keys(text)
        return text

    def fills(self, locator, text):
        element = self.wait_for_visible(locator)
        element.send_keys(text)
        return text

    def fills_fild(self, locator, text):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            element.click()
            element.clear()
            element.send_keys(text)
        except Exception as e:
            print(f"Ошибка при взаимодействии с элементом: {e}")
        return text

    def assert_text_on_page(self, text_to_find):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text
            assert text_to_find in page_text, f"Текст '{text_to_find}' не найден на странице."
        except WebDriverException:
            assert False, f"Произошла ошибка при поиске текста '{text_to_find}' на странице."

    # Очистка поля ввода
    def clear(self, locator):
        element = self.wait_for_visible(locator)
        element.clear()

    # Клик на элементе
    def click_on(self, locator):
        element = self.wait_for_visible(locator)
        element.click()

    # Выбор чекбокса
    def check_checkbox(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        element.click()

    # Снятие выбора с чекбокса
    def uncheck_checkbox(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        if element.is_selected():
            element.click()
        else:
            print("Элемент уже выбран")

    # Выбор радиокнопки
    def select_radio_button(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        element.click()

    # Выбор значения в выпадающем списке
    def dropdown_select(self, locator, value):
        element = Select(self.driver.find_element(By.XPATH, locator))
        element.select_by_value(value)

    def click_and_select_option_in_dropdown(self, dropdown_locator, option_locator):
        dropdown = self.driver.find_element(By.XPATH, dropdown_locator)
        dropdown.click()

        option = self.driver.find_element(By.XPATH, option_locator)
        option.click()

    # "Жесткий" клик на элементе
    def hard_click(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        self.driver.execute_script("arguments[0].click();", element)

    def hard_click_on_edit(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        element.click()

    # Прокрутка страницы вниз
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, window.innerHeight);")

    # Нажатие клавиши Enter
    def press_enter(self, locator):
        element = self.wait_for_visible(locator)
        element.send_keys(Keys.RETURN)

    # Наведение курсора мыши на элемент
    # Получение элемента и наведение курсора
    def hover_over_element(self, locator):
        element = self.wait_for_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    # Перетаскивание элемента
    # Получение исходного и целевого элементов и выполнение перетаскивания
    def drag_and_drop(self, source_locator, target_locator):
        source_element = self.wait_for_visible(source_locator)
        target_element = self.wait_for_visible(target_locator)
        ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()

    # Сохранение скриншота страницы
    # Сохранение скриншота в указанный файл
    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    # Выполнение JavaScript-скрипта на странице
    # Выполнение JavaScript-скрипта на странице
    def execute_js_script(self, script):
        self.driver.execute_script(script)

    # Переключение на окно по индексу
    # Получение списка окон и переключение на указанное по индексу
    def switch_to_window_by_index(self, index):
        handles = self.driver.window_handles
        if 0 <= index < len(handles):
            self.driver.switch_to.window(handles[index])
        else:
            raise Exception(f"Недопустимый индекс окна: {index}")

    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[1])

    # Закрытие текущего окна
    # Закрытие текущего окна
    def close_current_window(self):
        self.driver.close()

    # Переключение на родительское окно
    # Переключение на родительское окно
    def switch_to_parent_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    # Открытие в новом окне
    def open_new_window(self):
        self.driver.execute_script("window.open()")
        handles = self.driver.window_handles
        self.driver.switch_to_window(handles[1])

    """
    Взаимодействие с текстом и элементами:
    """

    # Клик по кнопке по тексту на ней
    # Поиск и клик по кнопке с указанным текстом
    def click_button_by_text(self, text):
        locator = f"//button[contains(text(), '{text}')]"
        element = self.wait_for_visible(locator)
        element.click()

    # Выбор опции из выпадающего списка по тексту
    # Выбор опции по-видимому тексту
    def select_option_by_text(self, select_locator, option_text):
        select = Select(self.wait_for_visible(select_locator))
        select.select_by_visible_text(option_text)

    def switch_to_main_window(self):
        self.driver.switch_to.window(self.main_window_handle)

    # Выбор опции из выпадающего списка по индексу
    # Выбор опции по индексу
    def select_option_by_index(self, select_locator, index):
        select = Select(self.wait_for_visible(select_locator))
        select.select_by_index(index)

    # Выбор опции из выпадающего списка по значению
    # Выбор опции по значению
    def select_option_by_value(self, select_locator, value):
        select = Select(self.wait_for_visible(select_locator))
        select.select_by_value(value)

    # Клик по ссылке по тексту на ней
    # Поиск и клик по ссылке с указанным текстом
    def click_link_by_text(self, text):
        locator = f"//a[contains(text(), '{text}')]"
        element = self.wait_for_visible(locator)
        element.click()

    # Загрузка файла в элемент input
    # Поиск элемента input и загрузка файла
    def upload_file(self, input_locator, file_path):
        element = self.wait_for_visible(input_locator)
        element.send_keys(file_path)

    # Переключение на iframe по его локатору
    def switch_to_frame_by(self, frame_locator):
        frame_element = self.wait_for_visible(frame_locator)
        self.driver.switch_to.frame(frame_element)

    # Переключение на основной контент страницы
    # Переключение на основной контент страницы
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def is_element_clickable(driver, element):
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            return False

    def is_element_not_clickable(driver, element):
        try:
            element.click()
            return False
        except ElementClickInterceptedException:
            return True

    """
    Другие действия с элементами:
    """

    # Переключение на iframe
    def switch_to_iframe(self):
        self.driver.switch_to.frame(self.wait_for_visible('//iframe'))

    # Добавление cookie
    def add_cookie(self, name, value):
        self.driver.add_cookie({'name': name, 'value': value})
        self.driver.refresh()

    # Удаление cookie
    def delete_cookies(self):
        self.driver.delete_cookies()
        self.driver.refresh()

    # Ожидание видимости элемента
    def wait_for_visible(self, locator):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator)))
        except WebDriverException:
            assert False, f"Элемент {locator} не кликабельный"

    def wait_for_visible_journal(self, locator):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator))
        except WebDriverException:
            assert False, f"Элемент {locator} не кликабельный"

    def wait_for_visible_2(self, *locators):
        try:
            for locator in locators:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, locator))
                )
        except TimeoutException:
            assert False, f"Один из элементов {locators} не присутствует на странице"

    # Получение значения атрибута элемента
    def get_attribute(self, locator, attribute_name):
        element = self.driver.find_element(By.XPATH, locator)
        element.get_attribute(attribute_name)

    # Ожидание отображения элемента
    def wait_for_element_is_displayed(self, locator):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator)))
        except WebDriverException:
            assert False, f"Элемент {locator} не отображается"

    # Получение текста элемента
    def find_element_text(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        return element.text

    def find_elements(self, xpath, timeout=10):

        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # Получение текста из поля ввода
    def get_input_text(self, locator, text):
        element = self.driver.find_element(By.XPATH, locator)
        element.clear()
        element.send_keys(text)
        return element.get_attribute("value")

    def find_elementtt(driver, locator):
        try:
            element = driver.find_element(*locator)
            return element
        except NoSuchElementException:
            print("Элемент не найден:", locator)
            return None

    """
    Проверки Asserts:
    """

    # Проверка наличия элемента на странице
    def assert_element_present(self, locator):
        try:
            self.wait_for_visible(locator)
        except Exception as e:
            assert False, f"Элемент {locator} отсутствует на странице"

    # Проверка отсутствия элемента на странице
    def assert_element_not_present(self, locator):
        try:
            self.wait_for_visible(locator)
            assert False, f"Элемент {locator} присутствует на странице"
        except Exception as e:
            pass

    # Проверка текста элемента на равенство ожидаемому тексту
    def assert_element_text_equal(self, locator, expected_text):
        element_text = self.find_element(locator).text
        return element_text

    # Проверка значения атрибута элемента на равенство ожидаемому значению
    def assert_element_attribute_equal(self, locator, attribute_name, expected_value):
        element = self.wait_for_visible(locator)
        actual_value = element.get_attribute(attribute_name)
        assert actual_value == expected_value, f"Атрибут элемента {locator} '{attribute_name}' - '{actual_value}', ожидаем - '{expected_value}'"

    # Проверка, что URL содержит ожидаемый фрагмент
    def assert_url_contains(self, expected_fragment):
        current_url = self.get_current_url()
        assert expected_fragment in current_url, f"URL '{current_url}' не содержит фрагмент '{expected_fragment}'"

    def get_current_url(self):
        return self.driver.current_url

    def get_current_url_1(self):
        current_url = self.driver.current_url
        print("URL открывшейся страницы:", current_url)
        return current_url

    # Проверка равенства текущего URL ожидаемому
    def assert_url_matches(self, expected_url, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_url))
        current_url = self.get_current_url()
        assert current_url == expected_url, f"Ожидаемый URL: '{expected_url}', Фактический URL: '{current_url}'"

    # Проверка, что элемент включен (активен)
    def assert_element_enabled(self, locator):
        element = self.wait_for_visible(locator)
        assert element.is_enabled(), f"Элемент {locator} не активен"

    # Проверка, что элемент выключен (неактивен)
    def assert_element_disabled(self, locator):
        element = self.wait_for_visible(locator)
        assert not element.is_enabled(), f"Элемент {locator} активен"

    def assert_elements_disabled(self, *locators):
        self.wait_for_visible_2(*locators)
        for locator in locators:
            element = self.find_element(locator)
            assert not element.is_enabled(), f"Элемент {locator} активен"

    def assert_element_disabld(self, locator):
        element = self.wait_for_visible(locator)
        assert element is not None, f"Элемент {locator} не найден"
        assert not element.is_enabled(), f"Элемент {locator} активен"

    # Проверка, что элемент выбран (например, чекбокс)
    def assert_element_selected(self, locator):
        element = self.wait_for_visible(locator)
        assert element.is_selected(), f"Элемент {locator} не выбран"

    # Проверка, что элемент не выбран (например, чекбокс)
    def assert_element_not_selected(self, locator):
        element = self.wait_for_visible(locator)
        assert not element.is_selected(), f"Элемент {locator} выбран"

    def assert_text_in_element(self, locator, expected_result):
        element = self.driver.find_element(By.XPATH, locator)
        assert expected_result == element.text, "Текст не совпадает"

    # Проверка значения атрибута элемента
    def assert_value_in_element_attribute(self, locator, attribute, expected_result):
        element = self.driver.find_element(By.XPATH, locator)
        value = element.get_attribute(attribute)
        assert value == expected_result, "Значение атрибута не совпадает"

    # Проверка, что две строки равны
    def assert_strings_equal(self, actual_string, expected_string):
        assert actual_string == expected_string, f"Ожидалось: '{expected_string}', Фактически: '{actual_string}'"

    # Проверка, что две строки не равны
    def assert_strings_not_equal(self, actual_string, expected_string):
        assert actual_string != expected_string, f"Строки совпадают: '{actual_string}'"

    # Проверка, что число больше определенного значения
    def assert_number_greater_than(self, actual_number, expected_number):
        assert actual_number > expected_number, f"Ожидалось число больше {expected_number}, получено {actual_number}"

    # Проверка, что число меньше определенного значения
    def assert_number_less_than(self, actual_number, expected_number):
        assert actual_number < expected_number, f"Ожидалось число меньше {expected_number}, получено {actual_number}"

    def check_for_words(self, language='russian'):
        page_text = self.driver.page_source

        if language == 'russian':
            pattern = re.compile(r'\b[А-Яа-я]+\b', re.IGNORECASE)
        elif language == 'english':
            pattern = re.compile(r'\b[A-Za-z]+\b')
        elif language == 'armenian':
            pattern = re.compile(r'\b[\u0531-\u0587\u0561-\u0587]+\b')
        elif language == 'lithuanian':
            pattern = re.compile(r'\b[A-Za-zĄąČčĘęĖėĮįŠšŲųŪūŽž]+\b')
        else:
            raise ValueError(f"Unsupported language: {language}")

        words = pattern.findall(page_text)

        assert words, f"No {language} words found on the page"
        assert len(words) > 0, f"No {language} words found on the page"
        return words  # Возвращаем найденные слова

    def found_other_language_words(self, language_code='ru'):
        page_text = self.driver.page_source.encode('utf-8')  # Преобразование в байтовый формат
        detected_language = detect(page_text)
        assert detected_language != language_code, f"{language_code} words found on the page"

    def get_number_from_element(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        text = element.text
        number = int(''.join(filter(str.isdigit, text)))  # Извлекаем числа из текста
        return number

    def find_element(self, locator):
        return self.driver.find_element(By.XPATH, locator)

    def find_element_portal(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def search_text_on_page(self, text):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//*[text()='{text}']"))
            )
            return True
        except:
            return False

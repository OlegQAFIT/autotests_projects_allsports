# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from helpers.base import BasePage
from locators.elements_for_new_web_site.header_elements_new_web_site import HeaderLocators as L

# Для проверки кодов ответа (например, у политики конфиденциальности)
try:
    import requests
except Exception:
    requests = None


class HeaderPage(BasePage):

    # =========================
    # == Базовые утилиты ==
    # =========================
    @allure.step("Открыть главную страницу")
    def open(self, url=L.BASE_URL):
        self.driver.get(url)
        self.accept_cookie_consent()
        return self

    @allure.step("Принять cookies (если показано)")
    def accept_cookie_consent(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, WebDriverException
        try:
            accept = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "cookie-primary-modal__confirm"))
            )
            accept.click()
        except (TimeoutException, WebDriverException):
            pass

    @allure.step("Проверить, что URL '{1}' отдаёт 200")
    def check_url_status_200(self, url, timeout=10):
        if not requests:
            assert False, "Модуль 'requests' недоступен — не могу проверить код 200."
        r = requests.get(url, timeout=timeout)
        assert r.status_code == 200, f"Ожидался код 200 от {url}, получено {r.status_code}"

    # ======================================================
    # == Проверки основного хедера ==
    # ======================================================
    @allure.step("Проверить отображение и корректность логотипа")
    def check_logo(self):
        self.assert_element_present(L.LOGO)
        by, value = L.LOGO_IMG  # ✅ распаковали tuple
        src = self.driver.find_element(by, value).get_attribute("src")
        assert src.endswith("/image/logo/logo-allsports.svg"), f"Некорректный src логотипа: {src}"

    @allure.step("Проверить, что клик по логотипу ведет на главную страницу")
    def check_logo_navigation(self):
        self.hard_click(L.LOGO)
        self.assert_url_matches(L.BASE_URL)

    @allure.step("Проверить ссылку 'Объекты'")
    def check_link_facilities(self):
        self.scroll_to_element(L.FACILITIES)
        self.hard_click(L.FACILITIES)
        self.assert_url_matches(L.URL_FACILITIES)
        self.assert_text_on_page(L.TEXT_FACILITIES)

    @allure.step("Проверить ссылку 'Типы подписок'")
    def check_link_levels(self):
        self.scroll_to_element(L.LEVELS)
        self.hard_click(L.LEVELS)
        self.assert_url_matches(L.URL_LEVELS)
        self.assert_text_on_page(L.TEXT_LEVELS)

    @allure.step("Проверить ссылку 'Компаниям'")
    def check_link_companies(self):
        self.scroll_to_element(L.COMPANIES)
        self.hard_click(L.COMPANIES)
        self.assert_url_matches(L.URL_COMPANIES)
        self.assert_text_on_page(L.TEXT_COMPANIES_H1)

    @allure.step("Проверить ссылку 'Партнерам'")
    def check_link_partners(self):
        self.scroll_to_element(L.PARTNERS)
        self.hard_click(L.PARTNERS)
        self.assert_url_matches(L.URL_PARTNERS)
        self.assert_text_on_page(L.TEXT_PARTNERS_H1)

    @allure.step("Проверить ссылку 'Контакты'")
    def check_link_contacts(self):
        self.scroll_to_element(L.CONTACTS)
        self.hard_click(L.CONTACTS)
        self.assert_url_matches(L.URL_CONTACTS)
        self.assert_text_on_page(L.TEXT_CONTACTS)

    @allure.step("Проверить наличие кнопок 'Получить предложение' и 'Задать вопрос'")
    def check_header_buttons(self):
        self.assert_element_present(L.BUTTON_GET_OFFER_HEADER)
        self.assert_element_present(L.BUTTON_ASK_QUESTION)

    # ======================================================
    # == Модалка «Получить предложение» ==
    # ======================================================
    @allure.step("Открыть модалку 'Получить предложение'")
    def open_modal_offer(self):
        self.click_on(L.BUTTON_GET_OFFER_HEADER)
        self.assert_element_present(L.MODAL_HEADER)
        self.assert_text_on_page("Получить предложение")

    @allure.step("Проверить наличие вкладок 'Подключить компанию' и 'Стать партнёром'")
    def check_offer_tabs(self):
        self.assert_element_present(L.TAB_CONNECT_COMPANY)
        self.assert_element_present(L.TAB_BECOME_PARTNER)

    @allure.step("Проверить переключение вкладок")
    def check_offer_tabs_switch(self):
        self.hard_click(L.TAB_BECOME_PARTNER)
        self.assert_text_on_page("Стать партнером")
        self.hard_click(L.TAB_CONNECT_COMPANY)
        self.assert_text_on_page("Подключить компанию")

    @allure.step("Проверить обязательные поля формы 'Подключить компанию'")
    def check_offer_fields(self):
        # Дождаться появления модалки и формы
        self.wait_for_visible("//div[contains(@class,'modal-body')]", timeout=15)
        self.wait_for_visible("//form[contains(@class,'modal-form')]", timeout=10)

        # Скроллим вниз, чтобы все элементы гарантированно появились
        self.scroll_to_element(L.INPUT_CITY)

        required_locators = [
            L.INPUT_NAME,
            L.INPUT_PHONE,
            L.INPUT_EMAIL,
            L.INPUT_COMPANY,
            L.INPUT_CITY,
            L.CHECKBOX_POLICY,
            L.BUTTON_SEND,
        ]

        for loc in required_locators:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    lambda d: d.find_element(*loc)
                )
                assert element.is_displayed(), f"Элемент {loc} не отображается!"
            except Exception:
                self.scroll_to_element(loc)
                element = self.driver.find_element(*loc)
                assert element.is_displayed(), f"Элемент {loc} не найден даже после скролла!"

    @allure.step("Проверить ссылку политики персональных данных и код 200")
    def check_offer_policy_link(self):
        self.hard_click(L.LINK_POLICY)
        self.switch_to_new_window()
        self.assert_url_contains("/policy/251010_processing_personal_data")
        self.assert_text_on_page("Политика компании")
        self.check_url_status_200(self.get_current_url())
        self.close_current_window()
        self.switch_to_parent_window()

    @allure.step("Проверить неактивность кнопки без чекбокса")
    def check_offer_button_disabled(self):
        # Убедиться, что форма действительно загрузилась
        self.wait_for_visible("//form[contains(@class,'modal-form')]", timeout=10)

        # Скроллим вниз — кнопка находится внизу модалки
        self.scroll_to_element(L.INPUT_CITY)

        # Ищем кнопку без проверки кликабельности
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException

        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(L.BUTTON_SEND)
            )
        except TimeoutException:
            # Повторный скролл на случай, если модалка подгружается с анимацией
            self.scroll_to_element(L.BUTTON_SEND)
            button = self.driver.find_element(*L.BUTTON_SEND)

        # Проверяем disabled-состояние
        is_disabled = button.get_attribute("disabled")
        assert is_disabled is not None, "Кнопка 'Отправить' активна без чекбокса!"

    @allure.step("Проверить активность кнопки после заполнения формы (без отправки)")
    def check_offer_button_enabled(self):
        self.fill(L.INPUT_NAME, "Олег")
        self.fill(L.INPUT_PHONE, "375297777777")
        self.fill(L.INPUT_EMAIL, "oleg@example.com")
        self.fill(L.INPUT_COMPANY, "ООО Автотесты")
        self.click_on(L.CHECKBOX_POLICY)
        btn = self.wait_for_visible(L.BUTTON_SEND)
        assert btn.is_enabled(), "Кнопка не активна после заполнения!"

    @allure.step("Отправить форму 'Подключить компанию' и проверить успешный ответ")
    def submit_offer_form(self):
        self.fill(L.INPUT_NAME, "Олег")
        self.fill(L.INPUT_PHONE, "375297777777")
        self.fill(L.INPUT_EMAIL, "oleg@example.com")
        self.fill(L.INPUT_COMPANY, "ООО Автотесты")
        self.click_on(L.CHECKBOX_POLICY)
        self.click_on(L.BUTTON_SEND)
        self.assert_text_on_page("Спасибо")

    @allure.step("Проверить закрытие модалки крестиком")
    def check_offer_close(self):
        self.hard_click(L.BUTTON_CLOSE)
        self.assert_element_not_present(L.MODAL_HEADER)

    @allure.step("Проверить наличие и корректность телефонного номера в модалке")
    def check_offer_phone(self):
        tel = (By.XPATH, "//a[contains(@href, 'tel:+375 44 771 09 47')]")

        # Скроллим именно к элементу, передавая tuple, а не строку
        self.scroll_to_element(tel)

        # После скролла ждём появления ссылки и проверяем содержимое
        self.wait_for_visible(tel, timeout=10)
        self.assert_element_present(tel)
        self.assert_text_on_page("+375 44 771 09 47")

    # ----- Валидации (Offer) -----


    @allure.step("Проверить логику активности кнопки 'Отправить'")
    def check_offer_button_validation_logic(self):
        # Ждем появления формы
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//form[contains(@class,'modal-form')]"))
        )

        self.scroll_to_element((By.XPATH, "//button[@type='submit']"))


        def get_button():
            # Возвращает сам элемент кнопки без требования кликабельности
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
            )

        # --- 1. Пустая форма ---
        btn = get_button()
        assert not btn.is_enabled(), "Ошибка: кнопка активна при пустой форме!"

        # --- 2. Только обязательные поля без чекбокса ---
        self.fill(L.INPUT_NAME, "Олег")
        self.fill(L.INPUT_EMAIL, "oleg@example.com")
        self.fill(L.INPUT_PHONE, "+375 29 123 45 67")
        self.fill(L.INPUT_COMPANY, "ООО Автотесты")
        btn = get_button()
        assert not btn.is_enabled(), "Ошибка: кнопка активна без чекбокса!"

        # --- 3. Обязательные поля + чекбокс ---
        self.click_on(L.CHECKBOX_POLICY)
        btn = get_button()
        assert btn.is_enabled(), "Ошибка: кнопка неактивна при обязательных полях и чекбоксе!"
        self.click_on(L.CHECKBOX_POLICY)  # снимаем

        # --- 4. Все поля без чекбокса ---
        self.fill(L.INPUT_CITY, "Минск")
        btn = get_button()
        assert not btn.is_enabled(), "Ошибка: кнопка активна без чекбокса при всех полях!"

        # --- 5. Все поля + чекбокс ---
        self.click_on(L.CHECKBOX_POLICY)
        btn = get_button()
        assert btn.is_enabled(), "Ошибка: кнопка неактивна при всех полях и чекбоксе!"

    @allure.step("Валидация: неверный email (Offer)")
    def check_offer_invalid_email_validation(self):
        """Проверяет, что при вводе некорректного email появляется сообщение об ошибке.
           Работает даже если локатор задан строкой (а не tuple)."""

        self.fill(L.INPUT_EMAIL, "oleg@@bad")

        # Триггерим валидацию: кликаем в другое поле, чтобы потерять фокус
        self.click_on(L.INPUT_NAME)
        self.scroll_to_element(L.INPUT_EMAIL)

        # Небольшая пауза — фронт может отрисовать сообщение с задержкой
        import time
        time.sleep(1.5)

        # Приводим локатор к tuple, если это строка
        locator = L.ERROR_EMAIL if isinstance(L.ERROR_EMAIL, tuple) else (By.XPATH, L.ERROR_EMAIL)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
        except Exception:
            html_snapshot = self.driver.page_source
            print(f"[DEBUG HTML SNAPSHOT]\n{html_snapshot[:1000]}...\n")
            assert False, f"Сообщение об ошибке email ({L.ERROR_EMAIL}) не появилось"

        # Проверяем текст ошибки, если он есть
        try:
            error_text = self.driver.find_element(*locator).text
        except Exception:
            error_text = ""

        assert error_text.strip() != "", "Элемент найден, но текст ошибки пустой"

    # ======================================================
    # == Вкладка «Стать партнёром» ==
    # ======================================================
    @allure.step("Проверить вкладку 'Стать партнёром'")
    def check_partner_tab(self):
        self.hard_click(L.TAB_BECOME_PARTNER)
        self.assert_text_on_page("Стать партнером")

    @allure.step("Проверить структуру формы 'Стать партнёром'")
    def check_partner_fields(self):
        # Переключаемся на вкладку "Стать партнёром"
        self.click_on(L.TAB_BECOME_PARTNER)
        self.wait_for_visible(L.INPUT_COMPANY, timeout=10)

        # Скроллим вниз
        self.scroll_down()

        # Проверяем все обязательные элементы формы
        required_elements = [
            L.INPUT_NAME,
            L.INPUT_PHONE,
            L.INPUT_EMAIL,
            L.INPUT_COMPANY,
            L.INPUT_CITY,
            L.CHECKBOX_POLICY,
            L.BUTTON_SEND,  # кнопка есть, но не кликабельна — проверим просто наличие
        ]

        for loc in required_elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(loc)  # <-- вместо element_to_be_clickable
                )
            except Exception:
                # fallback — лог и попытка проскроллить
                self.scroll_to_element(loc)
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(loc)
                    )
                except Exception:
                    assert False, f"Элемент {loc} не найден в DOM даже после скролла"

    @allure.step("Проверить ссылку политики в форме 'Стать партнёром' и код 200")
    def check_partner_policy_link(self):
        self.hard_click(L.LINK_POLICY)
        self.switch_to_new_window()
        self.assert_url_contains("/policy/251010_processing_personal_data")
        self.check_url_status_200(self.get_current_url())
        self.close_current_window()
        self.switch_to_parent_window()

    @allure.step("Проверить активность кнопки отправки (без отправки) — Partner")
    def check_partner_button_enabled(self):
        self.fill(L.INPUT_NAME, "Олег")
        self.fill(L.INPUT_PHONE, "375297777777")
        self.fill(L.INPUT_EMAIL, "oleg@example.com")
        self.fill(L.INPUT_COMPANY, "ООО СпортПартнёр")
        self.click_on(L.CHECKBOX_POLICY)
        btn = self.wait_for_visible(L.BUTTON_SEND)
        assert btn.is_enabled(), "Кнопка партнёра не активна!"

    @allure.step("Отправить форму 'Стать партнёром' и проверить успешный ответ")
    def submit_partner_form(self):
        self.fill(L.INPUT_NAME, "Олег")
        self.fill(L.INPUT_PHONE, "375297777777")
        self.fill(L.INPUT_EMAIL, "oleg@example.com")
        self.fill(L.INPUT_COMPANY, "ООО СпортПартнёр")
        self.click_on(L.CHECKBOX_POLICY)
        self.click_on(L.BUTTON_SEND)
        self.assert_text_on_page("Спасибо")

    # ----- Валидации (Partner) -----


    @allure.step("Валидация: неверный email (Partner)")
    def check_partner_invalid_email_validation(self):
        self.hard_click(L.TAB_BECOME_PARTNER)
        self.fill(L.INPUT_EMAIL, "oleg@@bad")
        self.click_on(L.INPUT_NAME)
        if L.ERROR_EMAIL:
            self.assert_element_present(L.ERROR_EMAIL)

    @allure.step("Валидация: неверный телефон (Partner)")
    def check_partner_invalid_phone_validation(self):
        self.hard_click(L.TAB_BECOME_PARTNER)
        self.fill(L.INPUT_PHONE, "123")
        self.click_on(L.INPUT_NAME)
        if L.ERROR_PHONE:
            self.assert_element_present(L.ERROR_PHONE)

    # ======================================================
    # == Модалка «Задать вопрос» ==
    # ======================================================
    @allure.step("Открыть модалку 'Задать вопрос'")
    def open_modal_question(self):
        self.click_on(L.BUTTON_ASK_QUESTION)
        self.assert_text_on_page("Задать вопрос")

    @allure.step("Проверить поля формы 'Задать вопрос'")
    def check_question_fields(self):
        # Скроллим вниз, чтобы чекбокс и кнопка попали в зону видимости
        self.scroll_down()

        fields = [
            L.INPUT_QUESTION_NAME,
            L.INPUT_QUESTION_PHONE,
            L.INPUT_QUESTION_TEXT,
            L.CHECKBOX_QUESTION,
            L.BUTTON_SEND_QUESTION,
        ]

        for loc in fields:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(loc)  # ✅ проверяем наличие в DOM
                )
            except Exception:
                # Если не нашли — пробуем проскроллить до элемента
                self.scroll_to_element(loc)
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(loc)
                    )
                except Exception:
                    assert False, f"Элемент {loc} не найден на странице даже после скролла"

    @allure.step("Проверить ссылку политики в форме 'Задать вопрос' и код 200")
    def check_question_policy_link(self):
        self.hard_click(L.LINK_POLICY)
        self.switch_to_new_window()
        self.assert_url_contains("/policy/251010_processing_personal_data")
        self.check_url_status_200(self.get_current_url())
        self.close_current_window()
        self.switch_to_parent_window()

    @allure.step("Проверить неактивность кнопки при пустой форме")
    def check_question_button_disabled(self):
        # Прокрутка до кнопки, чтобы точно попасть в видимую область
        self.scroll_to_element(L.BUTTON_SEND_QUESTION)

        # Ждём, пока кнопка появится в DOM (не обязательно кликабельна)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(L.BUTTON_SEND_QUESTION)
        )

        # Берём сам элемент
        btn = self.driver.find_element(*L.BUTTON_SEND_QUESTION)

        # Проверяем, что кнопка отключена
        assert not btn.is_enabled(), "Кнопка активна при пустой форме!"

    @allure.step("Проверить активность кнопки после заполнения (без отправки)")
    def check_question_button_enabled(self):
        self.fill(L.INPUT_QUESTION_NAME, "Олег")
        self.fill(L.INPUT_QUESTION_PHONE, "375297777777")
        self.fill(L.INPUT_QUESTION_TEXT, "Проверка.Тест.Олег QA")
        self.click_on(L.CHECKBOX_QUESTION)
        btn = self.wait_for_visible(L.BUTTON_SEND_QUESTION)
        assert btn.is_enabled(), "Кнопка не активна после заполнения!"

    @allure.step("Отправить форму 'Задать вопрос' и проверить успешный ответ")
    def submit_question_form(self):
        self.fill(L.INPUT_QUESTION_NAME, "Олег")
        self.fill(L.INPUT_QUESTION_PHONE, "375297777777")
        self.fill(L.INPUT_QUESTION_TEXT, "Проверка.Тест.Олег QA")
        self.click_on(L.CHECKBOX_QUESTION)
        self.click_on(L.BUTTON_SEND_QUESTION)
        self.assert_text_on_page("Спасибо")

    @allure.step("Отправить форму 'Получить предложение' и проверить сообщение")
    def submit_and_check_offer_form(self):
        """Полный цикл заполнения и проверки формы 'Получить предложение'"""
        self.fill(L.INPUT_NAME, "Олег")
        self.fill(L.INPUT_PHONE, "+375297777777")
        self.fill(L.INPUT_EMAIL, "oleg@example.com")
        self.fill(L.INPUT_COMPANY, "ООО Автотесты")
        self.fill(L.INPUT_CITY, "Минск")
        self.scroll_to_element(L.CHECKBOX_POLICY)
        self.click_on(L.CHECKBOX_POLICY)
        self.click_on(L.BUTTON_SEND)

        # Проверяем содержимое финальной модалки
        self.assert_text_on_page("Спасибо за ваш запрос!")
        self.assert_text_on_page("Ваш запрос очень важен для нас")
        self.assert_text_on_page("Ожидайте звонка от нашего менеджера")
        self.assert_text_on_page("индивидуальное предложение для уникальных потребностей вашей компании")
        self.assert_element_present((By.XPATH, "//button[contains(.,'Закрыть')]"))

    @allure.step("Отправить форму 'Стать партнёром' и проверить сообщение")
    def submit_and_check_partner_form(self):
        """Полный цикл заполнения и проверки формы 'Стать партнёром'"""
        self.hard_click(L.TAB_BECOME_PARTNER)
        self.wait_for_visible(L.INPUT_COMPANY, timeout=10)
        self.fill(L.INPUT_NAME, "Олег")
        self.fill(L.INPUT_PHONE, "+375297777777")
        self.fill(L.INPUT_EMAIL, "oleg@example.com")
        self.fill(L.INPUT_COMPANY, "ООО СпортПартнёр")
        self.fill(L.INPUT_CITY, "Минск")
        self.scroll_to_element(L.CHECKBOX_POLICY)
        self.click_on(L.CHECKBOX_POLICY)
        self.click_on(L.BUTTON_SEND)

        # Проверяем содержимое финальной модалки
        self.assert_text_on_page("Спасибо за ваш запрос!")
        self.assert_text_on_page("Ваш запрос очень важен для нас")
        self.assert_text_on_page("Ожидайте звонка от нашего менеджера")
        self.assert_text_on_page("индивидуальное предложение для уникальных потребностей вашей компании")
        self.assert_element_present((By.XPATH, "//button[contains(.,'Закрыть')]"))

    @allure.step("Отправить форму 'Задать вопрос' и проверить сообщение")
    def submit_and_check_question_form(self):
        """Полный цикл заполнения и проверки формы 'Задать вопрос'"""
        self.fill(L.INPUT_QUESTION_NAME, "Олег")
        self.fill(L.INPUT_QUESTION_PHONE, "+375297777777")
        self.fill(L.INPUT_QUESTION_TEXT, "Тест QA вопрос о продукте")
        self.scroll_to_element(L.CHECKBOX_QUESTION)
        self.click_on(L.CHECKBOX_QUESTION)
        self.click_on(L.BUTTON_SEND_QUESTION)

        # Проверяем содержимое финальной модалки
        self.assert_text_on_page("Спасибо за ваш запрос!")
        self.assert_text_on_page("Ваш запрос очень важен для нас")
        self.assert_element_present((By.XPATH, "//button[contains(.,'Закрыть')]"))
# -*- coding: utf-8 -*-
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from helpers.base import BasePage
from locators.elements_for_new_web_site.for_partners_page import PartnersLocators as L
import allure
import time
import re
import unicodedata


class PartnersPage(BasePage):
    # =====================
    # ОБЩИЕ МЕТОДЫ
    # =====================
    @allure.step("Открыть страницу Партнёрам")
    def open(self):
        self.driver.get(L.BASE_URL)
        return self

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        try:
            self.click_if_visible(("css selector", ".cookie-primary-modal__confirm"))
        except Exception:
            pass

    def _safe_scroll(self, locator):
        """Безопасно скроллит к элементу, даже если он лениво подгружается или не виден сразу."""
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.4)
        except Exception:
            for _ in range(5):
                self.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(0.6)
                if self.is_element_present(locator):
                    break

    def _get_error_text(self):
        """Возвращает первый видимый текст ошибки (без падений)."""
        try:
            errors = self.driver.find_elements(By.XPATH, "//*[contains(@class,'error') or contains(@style,'red')]")
            for e in errors:
                if e.is_displayed() and e.text.strip():
                    return e.text.strip()
        except Exception:
            pass
        return ""

    def _wait_form_ready(self):
        """Универсальное ожидание появления и готовности формы."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form | //input | //textarea"))
        )
        time.sleep(0.5)

    def _wait_success_message(self, timeout=10):
        """Ожидает появления текста 'Спасибо' или 'Заявка отправлена'."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(),'Спасибо') or contains(text(),'отправлена') or contains(text(),'успешно')]"))
            )
        except TimeoutException:
            raise AssertionError("Не появилось сообщение об успешной отправке формы")

    # =====================
    # PROMO БЛОК
    # =====================
    @allure.step("Проверить промо-блок")
    def check_promo_content(self):
        self.assert_element_present(L.PROMO_BLOCK)
        self.assert_element_present(L.PROMO_TITLE)
        self.assert_element_present(L.PROMO_SUBTITLE)
        self.assert_element_present(L.PROMO_DESC)
        self.assert_element_present(L.BTN_BECOME_PARTNER)
        self.assert_element_present(L.BTN_ASK_QUESTION)

    @allure.step("Проверить тексты промо-блока")
    def check_promo_texts(self):
        self.assert_text_on_page("Для партнеров")

    @allure.step("Проверить наличие логотипа Allsports")
    def check_promo_logo(self):
        self.assert_text_on_page("Allsports")

    @allure.step("Клик по кнопке 'Стать партнёром'")
    def click_become_partner(self):
        self.hard_click(L.BTN_BECOME_PARTNER)
        self._wait_form_ready()

    @allure.step("Клик по кнопке 'Задать вопрос'")
    def click_ask_question(self):
        self._safe_scroll(L.BTN_ASK_QUESTION)
        self.hard_click(L.BTN_ASK_QUESTION)
        self._wait_form_ready()

    # =====================
    # BENEFITS
    # =====================
    @allure.step("Проверить блок Преимущества")
    def check_benefits_title(self):
        self._safe_scroll((By.ID, "benefitSection"))
        self.assert_element_present((By.XPATH, "//*[@id='benefitSection']//h2[normalize-space()='Преимущества']"))

    @allure.step("Проверить количество элементов в блоке 'Преимущества'")
    def check_benefits_items(self):
        self._safe_scroll((By.ID, "benefitSection"))
        items = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "#benefitSection li.item")
        )
        assert len(items) >= 3, f"Ожидалось ≥3 элементов, найдено: {len(items)}"

    @allure.step("Проверить стрелки навигации блока 'Преимущества'")
    def check_benefits_slider(self):
        self._safe_scroll((By.ID, "benefitSection"))
        prev_buttons = self.driver.find_elements(By.CSS_SELECTOR, "#benefitSection .scroll-slider-control__prev")
        next_buttons = self.driver.find_elements(By.CSS_SELECTOR, "#benefitSection .scroll-slider-control__next")
        assert prev_buttons and next_buttons, "Отсутствуют стрелки навигации"

    @allure.step("Проверить тексты элементов блока 'Преимущества'")
    def check_benefits_texts(self):
        self._safe_scroll((By.ID, "benefitSection"))
        expected_texts = [
            "Рост клиентской базы",
            "Увеличение узнаваемости вашего заведения",
            "Полное отсутствие вложений и затрат с Вашей стороны",
        ]
        full_text = self.driver.page_source
        for text in expected_texts:
            assert text in full_text, f"Текст '{text}' не найден в блоке Преимущества"

    @allure.step("Проверить адаптивность блока 'Преимущества'")
    def check_benefits_responsive(self):
        self._safe_scroll((By.ID, "benefitSection"))
        self.resize_window(800, 900)
        assert self.is_element_visible((By.ID, "benefitSection")), "Блок не виден при ширине 800px"
        self.resize_window(1920, 1080)
        self.driver.maximize_window()

    # =====================
    # COOPERATION
    # =====================
    @allure.step("Проверить наличие блока 'Сотрудничество'")
    def check_cooperation_block(self):
        self._safe_scroll((By.ID, "cooperationSection"))
        self.assert_element_present(L.COOP_SECTION)

    @allure.step("Проверить количество шагов блока 'Сотрудничество'")
    def check_cooperation_steps(self):
        self._safe_scroll((By.ID, "cooperationSection"))
        items = self.driver.find_elements(*L.COOP_ITEMS)
        assert len(items) == 4, f"Ожидалось 4 шага, найдено: {len(items)}"

    @allure.step("Проверить тексты шагов блока 'Сотрудничество'")
    def check_cooperation_texts(self):
        self._safe_scroll((By.ID, "cooperationSection"))
        expected_texts = [
            "Свяжитесь с нашим менеджером для заключения договора",
            "Установите наше ПО на своем устройстве",
            "Отмечайте визиты владельцев подписки Allsports",
            "Ощутите пользу для своего бизнеса!"
        ]
        full_text = self.driver.page_source
        for text in expected_texts:
            assert text in full_text, f"Текст '{text}' не найден"

    @allure.step("Проверить стрелки навигации блока 'Сотрудничество'")
    def check_cooperation_controls(self):
        self._safe_scroll((By.ID, "cooperationSection"))
        prev = self.driver.find_elements(By.CSS_SELECTOR, "#cooperationSection .scroll-slider-control__prev")
        next_ = self.driver.find_elements(By.CSS_SELECTOR, "#cooperationSection .scroll-slider-control__next")
        assert prev and next_, "Кнопки навигации не найдены"

    # =====================
    # VIDEO
    # =====================
    @allure.step("Проверить наличие iframe с видео YouTube")
    def check_video_iframe(self):
        self._safe_scroll((By.ID, "videoSection"))
        self.assert_element_present(L.VIDEO_IFRAME)

    @allure.step("Проверить корректность источника iframe (YouTube)")
    def check_video_src(self):
        self._safe_scroll((By.ID, "videoSection"))
        iframe = self.driver.find_element(*L.VIDEO_IFRAME)
        assert "youtube.com" in iframe.get_attribute("src"), "Неверный источник iframe"

    @allure.step("Проверить, что iframe имеет атрибут allowfullscreen")
    def check_video_allowfullscreen(self):
        self._safe_scroll((By.ID, "videoSection"))
        iframe = self.driver.find_element(*L.VIDEO_IFRAME)
        assert iframe.get_attribute("allowfullscreen") is not None, "Нет атрибута allowfullscreen"

    # =====================
    # FAQ
    # =====================
    @allure.step("Проверить наличие заголовка блока FAQ")
    def check_faq_title(self):
        self._safe_scroll((By.ID, "faqSection"))
        self.assert_element_present(L.FAQ_TITLE)

    @allure.step("Проверить кнопку 'Задать вопрос' в FAQ")
    def check_faq_button(self):
        self.assert_element_present(L.FAQ_BUTTON)

    @allure.step("Открыть модалку 'Задать вопрос' из FAQ")
    def open_faq_modal(self):
        self.hard_click(L.FAQ_BUTTON)
        self._wait_form_ready()

    @allure.step("Отправить вопрос в FAQ")
    def submit_faq_question(self):
        """Заполнение и отправка формы 'Задать вопрос' из FAQ с учётом всех обязательных полей."""
        self._wait_form_ready()

        name = self.driver.find_element(By.XPATH, "//input[@placeholder='Ваше имя']")
        phone = self.driver.find_element(By.XPATH, "//input[@type='tel']")
        email = self.driver.find_element(By.XPATH, "//input[@type='email']")
        textarea = self.driver.find_element(By.TAG_NAME, "textarea")
        label_checkbox = self.driver.find_element(By.CSS_SELECTOR, ".agreement label.checkbox")
        submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        with allure.step("Заполнить все обязательные поля"):
            name.send_keys("Олег Тестировщик")
            phone.send_keys("375297000000")
            email.send_keys("oleg@example.com")
            textarea.send_keys("Тестовое сообщение из формы FAQ")

        with allure.step("Поставить галочку согласия"):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_checkbox)
            time.sleep(0.3)
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".agreement label.checkbox"))
            )
            label_checkbox.click()

        with allure.step("Дождаться активации кнопки и отправить"):
            WebDriverWait(self.driver, 10).until(lambda d: submit.is_enabled())
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
            submit.click()

        self._wait_success_message()

    # =====================
    # FAQ — РАСШИРЕННЫЕ ПРОВЕРКИ
    # =====================
    @allure.step("Проверить количество пунктов FAQ")
    def check_faq_count(self):
        """Проверяет, что количество вопросов FAQ не меньше 6."""
        self._safe_scroll((By.ID, "faqSection"))
        items = self.driver.find_elements(*L.FAQ_ITEMS)
        assert len(items) >= 6, f"Недостаточно пунктов FAQ: найдено {len(items)}"

    @allure.step("Проверить раскрытие первых трёх вопросов FAQ")
    def check_faq_expand(self):
        """Проверяет, что вопросы FAQ раскрываются по клику."""
        self._safe_scroll((By.ID, "faqSection"))
        questions = self.driver.find_elements(*L.FAQ_QUESTIONS)
        assert questions, "Не найдено ни одного вопроса FAQ"
        for q in questions[:3]:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", q)
            time.sleep(0.3)
            q.click()
            time.sleep(0.3)

    @allure.step("Проверить тексты всех вопросов FAQ")
    def check_faq_question_texts(self, expected_texts):
        """Сравнивает найденные вопросы FAQ с ожидаемыми."""
        self._safe_scroll((By.ID, "faqSection"))
        questions = self.driver.find_elements(*L.FAQ_QUESTIONS)
        found = [
            re.sub(r"\s+", " ", unicodedata.normalize("NFKC", q.text.strip().lower()))
            for q in questions
        ]
        for expected in expected_texts:
            normalized_expected = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", expected.strip().lower()))
            assert any(normalized_expected in f for f in found), \
                f"FAQ вопрос '{expected}' не найден. Найденные: {found}"

    @allure.step("Раскрыть вопрос FAQ по индексу")
    def expand_faq_question_by_index(self, index):
        """Открывает конкретный вопрос FAQ по номеру (индексу)."""
        self._safe_scroll((By.ID, "faqSection"))
        questions = self.driver.find_elements(*L.FAQ_QUESTIONS)
        assert questions, "Вопросы FAQ не найдены"
        assert index < len(questions), f"FAQ индекс {index} вне диапазона ({len(questions)} вопросов)"
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", questions[index])
        time.sleep(0.3)
        questions[index].click()
        time.sleep(0.3)

    @allure.step("Проверить содержимое ответа FAQ по индексу")
    def verify_faq_answer_contains(self, index, expected_text):
        """Проверяет, что ответ на вопрос содержит указанный текст."""
        answers = self.driver.find_elements(By.CSS_SELECTOR, "section.faq .expansion-item-text")
        WebDriverWait(self.driver, 10).until(EC.visibility_of(answers[index]))
        actual_text = answers[index].text.strip().lower()
        assert expected_text.lower() in actual_text, \
            f"Ожидалось '{expected_text}', получено '{actual_text}'"

    @allure.step("Раскрыть все вопросы FAQ и убедиться, что ответы видимы")
    def expand_all_faq_questions(self):
        """Раскрывает все вопросы FAQ и проверяет, что есть видимые ответы."""
        self._safe_scroll((By.ID, "faqSection"))
        questions = self.driver.find_elements(*L.FAQ_QUESTIONS)
        assert questions, "Вопросы FAQ не найдены"
        visible_answers = []
        for q in questions:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", q)
            time.sleep(0.3)
            q.click()
            time.sleep(0.4)
            answers = self.driver.find_elements(By.CSS_SELECTOR, "section.faq .expansion-item-text")
            for a in answers:
                if a.is_displayed() and a.text.strip():
                    visible_answers.append(a.text.strip())
        assert visible_answers, "После кликов ни один ответ FAQ не стал видимым"

    @allure.step("Проверить кнопку 'Задать вопрос' под списком FAQ")
    def check_faq_bottom_button(self):
        """Проверяет наличие кнопки 'Задать вопрос' под блоком FAQ."""
        self._safe_scroll((By.ID, "faqSection"))
        self.assert_element_present(L.FAQ_BUTTON)


    # =====================
    # CONTACTS
    # =====================
    @allure.step("Проверить наличие блока Контакты")
    def check_contacts_presence(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        self.assert_element_present(L.CONTACTS_SECTION)

    @allure.step("Проверить телефоны отделов")
    def check_contacts_phones(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        self.assert_element_present(L.CONTACTS_PHONE)

    @allure.step("Проверить email адреса отделов")
    def check_contacts_emails(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        self.assert_element_present(L.CONTACTS_EMAIL)

    @allure.step("Проверить адрес компании")
    def check_contacts_address(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        self.assert_element_present(L.CONTACTS_ADDRESS)

    @allure.step("Проверить наличие карты на странице")
    def check_contacts_map(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        self.assert_element_present(L.MAP_CANVAS)

    @allure.step("Проверить наличие кнопок зума карты")
    def check_contacts_zoom_buttons(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        self.assert_element_present(L.MAP_ZOOM_IN)
        self.assert_element_present(L.MAP_ZOOM_OUT)

    @allure.step("Проверить наличие логотипа Mapbox")
    def check_contacts_map_logo(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        logo_elements = self.driver.find_elements(By.CSS_SELECTOR, ".mapboxgl-ctrl-logo")
        text_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'mapbox.com')]")
        assert logo_elements or text_links, "Элемент логотипа Mapbox не найден"

    @allure.step("Проверить адаптивность блока Контакты")
    def check_contacts_responsive(self):
        self._safe_scroll((By.CSS_SELECTOR, "#contactsSection"))
        self.resize_window(800, 900)
        assert self.is_element_visible(L.CONTACTS_SECTION)
        self.resize_window(1920, 1080)
        self.driver.maximize_window()

    # =====================
    # ФОРМЫ И ОТПРАВКА
    # =====================
    @allure.step("Отправить форму 'Задать вопрос'")
    def submit_question_modal(self):
        """Отправка формы 'Задать вопрос' (из промо-блока) с учётом всех обязательных полей."""
        self._wait_form_ready()

        # === Локаторы элементов формы ===
        name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Ваше имя']")
        phone_input = self.driver.find_element(By.XPATH, "//input[@type='tel']")
        email_input = self.driver.find_element(By.XPATH, "//input[@type='email']")
        textarea = self.driver.find_element(By.XPATH, "//textarea")
        label_checkbox = self.driver.find_element(By.CSS_SELECTOR, ".agreement label.checkbox")
        submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        # === Заполнение всех обязательных полей ===
        with allure.step("Заполнить все обязательные поля"):
            name_input.send_keys("Олег Тестировщик")
            phone_input.send_keys("375297000000")
            email_input.send_keys("oleg@example.com")
            textarea.send_keys("Тестовая форма через модалку 'Задать вопрос'.")

        # === Клик по чекбоксу согласия ===
        with allure.step("Поставить галочку согласия"):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_checkbox)
            time.sleep(0.3)
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".agreement label.checkbox"))
            )
            ActionChains(self.driver).move_to_element(label_checkbox).click().perform()

        # === Ожидание активации кнопки и отправка формы ===
        with allure.step("Отправить форму"):
            WebDriverWait(self.driver, 10).until(lambda d: submit_btn.is_enabled())
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            submit_btn.click()

        # === Проверка успешной отправки ===
        self._wait_success_message()

    @allure.step("Проверить появление подтверждения отправки")
    def verify_success_modal(self):
        self._wait_success_message()

    @allure.step("Проверить ошибки в форме 'Стать партнёром'")
    def verify_promo_partner_form_errors(self):
        """Проверка ошибок валидации полей телефона и email в форме 'Стать партнёром'."""
        self._wait_form_ready()

        phone = self.driver.find_element(*L.JOIN_INPUT_PHONE)
        email = self.driver.find_element(*L.JOIN_INPUT_EMAIL)

        # === Проверка ошибки телефона ===
        phone.send_keys("111")
        email.click()  # теряем фокус, чтобы запустить валидацию телефона
        time.sleep(0.5)
        err1 = self._get_error_text_for_element(phone)
        assert "Неверный формат номера" in err1, f"Ошибка телефона не отображается: {err1}"

        # === Проверка ошибки email ===
        phone.clear()
        phone.send_keys("+375297000000")
        email.clear()
        email.send_keys("тест@@")
        email.send_keys(Keys.TAB)
        time.sleep(0.5)
        err2 = self._get_error_text_for_element(email)
        assert any(s in err2 for s in [
            "должен быть действительным",
            "Поле содержит запрещенные символы"
        ]), f"Ошибка email не отображается: {err2}"

    def _get_error_text_for_element(self, element):
        """Возвращает текст ошибки, относящийся к конкретному полю (используется только в тесте формы 'Стать партнёром')."""
        try:
            # Ошибка сразу после поля
            err_el = element.find_element(
                By.XPATH,
                ".//following-sibling::*[contains(@class,'error') or contains(@class,'invalid')]"
            )
            if err_el.is_displayed():
                return err_el.text.strip()
        except Exception:
            pass

        try:
            # Ошибка в родительском контейнере
            container = element.find_element(
                By.XPATH,
                "./ancestor::*[contains(@class,'form-field') or contains(@class,'input')]"
            )
            err_el = container.find_element(
                By.XPATH,
                ".//*[contains(@class,'error') or contains(@class,'invalid')]"
            )
            if err_el.is_displayed():
                return err_el.text.strip()
        except Exception:
            pass

        return ""

    @allure.step("Проверить ошибки в форме 'Стать партнёром'")
    def verify_promo_partner_form_errors(self):
        """Проверка ошибок валидации полей телефона и email в форме 'Стать партнёром'."""
        self._wait_form_ready()

        phone = self.driver.find_element(*L.JOIN_INPUT_PHONE)
        email = self.driver.find_element(*L.JOIN_INPUT_EMAIL)

        # === Проверка ошибки телефона ===
        with allure.step("Проверка ошибки телефона"):
            phone.send_keys("111")
            email.click()  # теряем фокус, чтобы запустить валидацию телефона
            time.sleep(0.5)
            err1 = self._get_error_text_for_element(phone)
            assert "Неверный формат номера" in err1, f"Ошибка телефона не отображается: {err1}"

        # === Проверка ошибки email ===
        with allure.step("Проверка ошибки email"):
            phone.clear()
            phone.send_keys("+375297000000")
            email.clear()
            email.send_keys("тест@@")
            email.send_keys(Keys.TAB)
            time.sleep(0.5)
            err2 = self._get_error_text_for_element(email)
            assert any(s in err2 for s in [
                "должен быть действительным",
                "Поле содержит запрещенные символы"
            ]), f"Ошибка email не отображается: {err2}"

    @allure.step("Проверить наличие всех обязательных полей формы Join")
    def check_join_form_fields(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        required = [
            L.JOIN_INPUT_NAME, L.JOIN_INPUT_PHONE, L.JOIN_INPUT_EMAIL,
            L.JOIN_INPUT_COMPANY, L.JOIN_CHECKBOX, L.JOIN_BUTTON
        ]
        for locator in required:
            assert self.is_element_present(locator), f"Элемент {locator} не найден"

    @allure.step("Проверить наличие чекбокса политики")
    def check_join_policy_checkbox(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        self.assert_element_present(L.JOIN_CHECKBOX)

    @allure.step("Проверить валидацию телефона в форме Join")
    def check_join_phone_validation(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        self.fill(L.JOIN_INPUT_PHONE, "bad")
        btn = self.driver.find_element(*L.JOIN_BUTTON)
        assert not btn.is_enabled(), "Кнопка должна быть неактивна при невалидном телефоне"

    @allure.step("Проверить валидацию email в форме Join")
    def check_join_email_validation(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        self.fill(L.JOIN_INPUT_EMAIL, "bad@@mail")
        btn = self.driver.find_element(*L.JOIN_BUTTON)
        assert not btn.is_enabled(), "Кнопка должна быть неактивна при невалидном email"

    @allure.step("Проверить успешную отправку формы Join")
    def submit_join_form_success(self):
        """Заполняет и отправляет форму 'Присоединяйтесь к Allsports' и проверяет успешное подтверждение."""
        self._safe_scroll((By.ID, "getDetailsSection"))
        self._wait_form_ready()

        # Находим поля
        name = self.driver.find_element(*L.JOIN_INPUT_NAME)
        phone = self.driver.find_element(*L.JOIN_INPUT_PHONE)
        email = self.driver.find_element(*L.JOIN_INPUT_EMAIL)
        company = self.driver.find_element(*L.JOIN_INPUT_COMPANY)
        label_checkbox = self.driver.find_element(By.CSS_SELECTOR, ".agreement label.checkbox")
        submit_btn = self.driver.find_element(*L.JOIN_BUTTON)

        with allure.step("Заполнить все поля формы"):
            name.send_keys("Олег Тестировщик")
            phone.send_keys("375297000000")
            email.send_keys("oleg@example.com")
            company.send_keys("ООО Автотест")

        with allure.step("Отметить чекбокс политики"):
            # Скроллим к нему и кликаем по label (input скрыт стилями)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_checkbox)
            time.sleep(0.3)
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".agreement label.checkbox"))
            )
            ActionChains(self.driver).move_to_element(label_checkbox).click().perform()

        with allure.step("Дождаться активации кнопки и отправить форму"):
            WebDriverWait(self.driver, 10).until(lambda d: submit_btn.is_enabled())
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            submit_btn.click()

        self._wait_success_message()

    @allure.step("Отправить форму 'Стать партнёром' (из модалки, промо-блок)")
    def submit_become_partner_modal(self):
        """Заполняет и отправляет форму 'Стать партнёром' из модального окна."""
        self._wait_form_ready()

        # Находим все нужные поля
        name = self.driver.find_element(By.XPATH, "//input[@placeholder='Ваше имя']")
        phone = self.driver.find_element(By.XPATH, "//input[@type='tel']")
        email = self.driver.find_element(By.XPATH, "//input[@name='email']")
        company = self.driver.find_element(By.XPATH, "//input[@placeholder='Название объекта']")
        city = self.driver.find_element(By.XPATH, "//input[@placeholder='Введите город']")
        checkbox_label = self.driver.find_element(By.XPATH, "//label[@class='checkbox']")
        submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        # Заполнение полей
        name.send_keys("Олег Тестировщик")
        phone.send_keys("375297000000")
        email.send_keys("oleg@example.com")
        company.send_keys("ООО Автотест")
        city.send_keys("Минск")

        # Клик по чекбоксу через JS (он скрыт стилями)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox_label)
        self.driver.execute_script("arguments[0].click();", checkbox_label)

        # Клик по кнопке "Отправить" (через JS на случай disabled -> активируется автоматически)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        self.driver.execute_script("arguments[0].click();", submit_btn)

        # Ожидаем успешное сообщение
        self._wait_success_message()

    @allure.step("Проверить disabled кнопку при пустых полях")
    def check_join_button_disabled(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        btn = self.driver.find_element(*L.JOIN_BUTTON)
        assert not btn.is_enabled(), "Кнопка должна быть неактивна при пустых полях"

    @allure.step("Проверить текст-подсказку формата телефона")
    def check_join_help_text(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        self.assert_text_on_page("Формат номера: +375 00 000 00 00")

    @allure.step("Проверить ссылку политики обработки данных")
    def check_join_policy_link(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        self.assert_element_present(L.JOIN_POLICY_LINK)

    @allure.step("Проверить заполнение валидными данными в форме Join")
    def fill_join_form_valid(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        self.fill(L.JOIN_INPUT_NAME, L.VALID_NAME)
        self.fill(L.JOIN_INPUT_PHONE, L.VALID_PHONE)
        self.fill(L.JOIN_INPUT_EMAIL, L.VALID_EMAIL)
        self.fill(L.JOIN_INPUT_COMPANY, L.VALID_COMPANY)
        self.hard_click(L.JOIN_CHECKBOX)
        assert self.driver.find_element(*L.JOIN_BUTTON).is_enabled()

    @allure.step("Очистить поля формы Join")
    def check_join_clear_fields(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        for locator in [L.JOIN_INPUT_NAME, L.JOIN_INPUT_EMAIL]:
            self.fill(locator, "")
        assert True

    # =====================
    # ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ ВАЛИДАЦИИ ФОРМ
    # =====================
    @allure.step("Проверить ошибки в модалке 'Задать вопрос' (FAQ)")
    def verify_faq_question_errors(self):
        self._wait_form_ready()
        email = self.driver.find_element(By.XPATH, "//input[@type='email']")
        phone = self.driver.find_element(By.XPATH, "//input[@type='tel']")

        email.send_keys("bad@@")
        phone.click()
        time.sleep(0.5)
        err = self._get_error_text()
        assert "должен быть действительным" in err or "запрещенные символы" in err, f"Ошибка email не отобразилась: {err}"

        phone.clear()
        phone.send_keys("12")
        email.click()
        time.sleep(0.5)
        err2 = self._get_error_text()
        assert "Неверный формат номера" in err2, f"Ошибка телефона не отобразилась: {err2}"

    @allure.step("Проверить ошибки в модалке 'Задать вопрос' (из промо-блока)")
    def verify_promo_question_errors(self):
        """Проверка ошибок валидации телефона и email в модалке 'Задать вопрос'."""
        self._wait_form_ready()

        phone = self.driver.find_element(By.XPATH, "//input[@type='tel']")
        email = self.driver.find_element(By.XPATH, "//input[@type='email']")

        # === Проверка ошибки телефона ===
        with allure.step("Проверка ошибки телефона"):
            phone.send_keys("222")
            email.click()  # теряем фокус, чтобы сработала валидация
            time.sleep(0.5)
            err1 = self._get_error_text_for_element(phone)
            assert "Неверный формат номера" in err1, f"Ошибка телефона не отобразилась: {err1}"

        # === Проверка ошибки email ===
        with allure.step("Проверка ошибки email"):
            phone.clear()
            phone.send_keys("+375297000000")
            email.clear()
            email.send_keys("тест@@")
            email.send_keys(Keys.TAB)  # корректная потеря фокуса
            time.sleep(0.5)
            err2 = self._get_error_text_for_element(email)
            assert any(s in err2 for s in [
                "должен быть действительным",
                "запрещенные символы"
            ]), f"Ошибка email не отобразилась: {err2}"

    @allure.step("Проверить ошибки формы 'Присоединяйтесь к Allsports'")
    def verify_join_form_errors(self):
        self._safe_scroll((By.ID, "getDetailsSection"))
        email = self.driver.find_element(*L.JOIN_INPUT_EMAIL)
        phone = self.driver.find_element(*L.JOIN_INPUT_PHONE)

        email.send_keys("oleg@@")
        phone.click()
        time.sleep(0.5)
        err1 = self._get_error_text()
        assert "должен быть действительным" in err1 or "запрещенные символы" in err1, f"Ошибка email не отображается: {err1}"

        email.clear()
        email.send_keys("oleg@example.com")
        phone.clear()
        phone.send_keys("123")
        email.click()
        time.sleep(0.5)
        err2 = self._get_error_text()
        assert "Неверный формат номера" in err2, f"Ошибка телефона не отображается: {err2}"

    @allure.step("Проверить ошибки при пустых полях в любой форме")
    def verify_empty_input_errors(self):
        inputs = self.driver.find_elements(By.XPATH, "//input")
        for inp in inputs[:3]:
            inp.click()
            time.sleep(0.2)
            self.driver.execute_script("arguments[0].blur();", inp)
            time.sleep(0.3)
        errors = [e.text.strip() for e in self.driver.find_elements(By.XPATH, "//*[contains(@class,'error')]") if e.is_displayed()]
        assert errors, "Ошибки при пустых полях не отображаются"

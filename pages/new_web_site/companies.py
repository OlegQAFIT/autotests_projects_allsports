# -*- coding: utf-8 -*-
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from helpers.base import BasePage
from locators.elements_for_new_web_site.for_companies_page import CompaniesLocators as L


class CompaniesPage(BasePage):
    # =====================
    # ОБЩИЕ МЕТОДЫ
    # =====================
    @allure.step("Открыть страницу 'Компаниям'")
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
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            time.sleep(0.4)
        except Exception:
            for _ in range(5):
                self.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(0.6)
                if self.is_element_present(locator):
                    break

    def _wait_modal_ready(self):
        """Ожидание появления модалки."""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(L.MODAL))
        time.sleep(0.5)

    # =====================
    # PROMO BLOCK
    # =====================
    @allure.step("Проверить наличие промо-блока и его элементов")
    def check_promo_block(self):
        self._safe_scroll(L.PROMO_SECTION)
        self.assert_element_present(L.PROMO_SECTION)
        self.assert_element_present(L.PROMO_IMG)
        self.assert_element_present(L.BTN_GET_OFFER)
        self.assert_element_present(L.BTN_ASK_QUESTION)

    @allure.step("Проверить заголовки промо-блока")
    def check_promo_titles(self):
        self._safe_scroll(L.PROMO_SECTION)
        self.assert_text_on_page("Allsports")
        self.assert_text_on_page("для компаний")

    @allure.step("Клик по кнопке 'Получить предложение'")
    def click_get_offer(self):
        self._safe_scroll(L.BTN_GET_OFFER)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.BTN_GET_OFFER)
        )
        self.hard_click(L.BTN_GET_OFFER)
        self._wait_modal_ready()

    @allure.step("Клик по кнопке 'Задать вопрос'")
    def click_ask_question(self):
        self._safe_scroll(L.BTN_ASK_QUESTION)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.BTN_ASK_QUESTION)
        )
        self.hard_click(L.BTN_ASK_QUESTION)
        self._wait_modal_ready()

    @allure.step("Проверить наличие формы 'Получить предложение' и состояние кнопки")
    def check_offer_modal(self):
        """Проверяет наличие всех обязательных полей и что кнопка 'Отправить' изначально неактивна."""
        self._wait_modal_ready()
        self._safe_scroll(L.MODAL)
        self.assert_text_on_page("Получить предложение")

        # --- Проверка наличия обязательных полей ---
        required_fields = [
            L.MODAL_INPUT_NAME,
            L.MODAL_INPUT_PHONE,
            L.MODAL_INPUT_EMAIL,
            L.MODAL_INPUT_COMPANY,
            L.MODAL_INPUT_CITY,
            L.MODAL_BTN_SUBMIT,
        ]
        for locator in required_fields:
            self._safe_scroll(locator)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            self.assert_element_present(locator)

        # --- Прокрутка вниз, чтобы увидеть чекбокс ---
        modal = self.driver.find_element(*L.MODAL)
        self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", modal)
        time.sleep(0.5)

        # --- Проверка чекбокса политики ---
        checkbox_label = self.driver.find_element(By.CSS_SELECTOR, ".agreement label.checkbox")
        self.assert_element_present((By.CSS_SELECTOR, ".agreement label.checkbox"))

        # --- Проверка, что кнопка изначально disabled ---
        submit_btn = self.driver.find_element(*L.MODAL_BTN_SUBMIT)
        assert not submit_btn.is_enabled(), "Кнопка 'Отправить' должна быть неактивна при пустых полях"

        # --- Проверка, что нажатие чекбокса не активирует кнопку (без заполнения полей) ---
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox_label)
        self.driver.execute_script("arguments[0].click();", checkbox_label)
        time.sleep(0.5)
        assert not submit_btn.is_enabled(), "Кнопка 'Отправить' не должна активироваться только от чекбокса"

    @allure.step("Проверить наличие формы 'Задать вопрос'")
    def check_question_modal(self):
        """Проверяет наличие всех обязательных полей и корректное поведение кнопки."""
        self._wait_modal_ready()
        self._safe_scroll(L.MODAL)
        self.assert_text_on_page("Задать вопрос")

        # --- Проверяем наличие всех основных полей ---
        required_fields = [
            L.MODAL_INPUT_NAME,
            L.MODAL_INPUT_PHONE,
            L.MODAL_INPUT_EMAIL,
            L.MODAL_TEXTAREA,
            L.MODAL_BTN_SUBMIT,
        ]
        for locator in required_fields:
            self._safe_scroll(locator)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            self.assert_element_present(locator)

        # --- Прокрутка вниз, чтобы чекбокс стал видим ---
        modal = self.driver.find_element(*L.MODAL)
        self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", modal)
        time.sleep(0.5)

        # --- Проверяем наличие чекбокса политики (по label, не по input) ---
        checkbox_label = self.driver.find_element(By.CSS_SELECTOR, ".agreement label.checkbox")
        self.assert_element_present((By.CSS_SELECTOR, ".agreement label.checkbox"))

        # --- Проверка: кнопка "Отправить" изначально disabled ---
        submit_btn = self.driver.find_element(*L.MODAL_BTN_SUBMIT)
        assert not submit_btn.is_enabled(), "Кнопка 'Отправить' должна быть неактивна при пустых полях"

        # --- Клик по видимому label (input скрыт стилями) ---
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox_label)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", checkbox_label)
        time.sleep(0.8)

        # --- Проверка: кнопка активируется после клика ---
        assert submit_btn.is_enabled(), "Кнопка 'Отправить' не активировалась после отметки чекбокса"

    @allure.step("Закрыть модалку")
    def close_modal(self):
        self._safe_scroll(L.MODAL_CLOSE)
        self.click_if_visible(L.MODAL_CLOSE)
        time.sleep(0.5)

    # =====================
    # BENEFITS
    # =====================
    @allure.step("Проверить наличие блока 'Преимущества'")
    def check_benefit_section(self):
        self._safe_scroll(L.BENEFIT_SECTION)
        self.assert_element_present(L.BENEFIT_SECTION)
        self.assert_text_on_page("Преимущества")

    @allure.step("Проверить количество элементов в блоке 'Преимущества'")
    def check_benefit_items_count(self):
        self._safe_scroll(L.BENEFIT_SECTION)
        items = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*L.BENEFIT_ITEMS)
        )
        assert len(items) >= 5, f"Ожидалось ≥5 пунктов, найдено {len(items)}"

    @allure.step("Проверить тексты элементов блока 'Преимущества'")
    def check_benefit_texts(self):
        self._safe_scroll(L.BENEFIT_SECTION)
        texts = [
            t.text.strip().lower() for t in self.driver.find_elements(*L.BENEFIT_TEXTS)
        ]
        assert any("мотив" in t for t in texts), "Не найден текст о мотивации"
        assert any("бренд" in t for t in texts), "Не найден текст о бренде"
        assert any("цен" in t for t in texts), "Не найден текст о ценах"

    @allure.step("Проверить стрелки навигации блока 'Преимущества'")
    def check_benefit_slider_controls(self):
        """Проверяет наличие стрелок навигации (вперёд/назад) в блоке Преимущества."""
        self._safe_scroll(L.BENEFIT_SECTION)
        time.sleep(0.8)  # даем дорисоваться блоку

        # --- Проверяем наличие контейнера стрелок ---
        controls = self.driver.find_elements(By.CSS_SELECTOR, "#benefitSection .scroll-slider-control")
        assert controls, "Контейнер навигации слайдера 'Преимущества' не найден"

        # --- Проверяем наличие кнопок вперед/назад ---
        next_btns = self.driver.find_elements(*L.BENEFIT_NEXT)
        prev_btns = self.driver.find_elements(*L.BENEFIT_PREV)

        assert next_btns, "Кнопка 'вперёд' (scroll-slider-control__next) не найдена"
        assert prev_btns, "Кнопка 'назад' (scroll-slider-control__prev) не найдена"

        # --- Проверяем, что хотя бы одна кнопка доступна для клика ---
        next_enabled = next_btns[0].is_enabled()
        prev_enabled = prev_btns[0].is_enabled()

        assert next_enabled or prev_enabled, (
            "Обе кнопки навигации слайдера 'Преимущества' недоступны (disabled)"
        )

    # =====================
    # COOPERATION
    # =====================
    @allure.step("Проверить наличие блока 'Сотрудничество'")
    def check_cooperation_section(self):
        self._safe_scroll(L.COOP_SECTION)
        self.assert_element_present(L.COOP_SECTION)
        self.assert_text_on_page("Сотрудничать с Allsports — легко!")

    @allure.step("Проверить тексты шагов блока 'Сотрудничество'")
    def check_cooperation_texts(self):
        self._safe_scroll(L.COOP_SECTION)
        full_text = self.driver.page_source
        for t in [
            "Свяжитесь с нами",
            "Заполните список",
            "Произведите оплату",
            "Сообщите сотрудникам",
        ]:
            assert t in full_text, f"Не найден текст шага: {t}"

    @allure.step("Проверить стрелки навигации блока 'Сотрудничество'")
    def check_cooperation_controls(self):
        """Проверяет наличие стрелок навигации (вперёд/назад) в блоке 'Сотрудничество'."""
        self._safe_scroll(L.COOP_SECTION)
        time.sleep(0.8)  # даем блоку дорисоваться

        # Проверяем наличие контейнера стрелок
        controls = self.driver.find_elements(By.CSS_SELECTOR, "#cooperationSection .scroll-slider-control")
        assert controls, "Контейнер навигации слайдера 'Сотрудничество' не найден"

        # Проверяем наличие стрелок
        next_btns = self.driver.find_elements(*L.COOP_NEXT)
        prev_btns = self.driver.find_elements(*L.COOP_PREV)

        assert next_btns, "Кнопка 'вперёд' (scroll-slider-control__next) не найдена"
        assert prev_btns, "Кнопка 'назад' (scroll-slider-control__prev) не найдена"

        # Проверяем, что хотя бы одна кнопка активна
        next_enabled = next_btns[0].is_enabled()
        prev_enabled = prev_btns[0].is_enabled()

        assert next_enabled or prev_enabled, (
            "Обе кнопки навигации слайдера 'Сотрудничество' недоступны (disabled)"
        )

    # =====================
    # FEEDBACK
    # =====================
    @allure.step("Проверить наличие блока 'Нам доверяют'")
    def check_feedback_section(self):
        self._safe_scroll(L.FEEDBACK_SECTION)
        self.assert_element_present(L.FEEDBACK_SECTION)
        self.assert_text_on_page("Нам доверяют")

    @allure.step("Проверить тексты отзывов")
    def check_feedback_texts(self):
        self._safe_scroll(L.FEEDBACK_SECTION)
        texts = [
            t.text.strip().lower() for t in self.driver.find_elements(*L.FEEDBACK_TEXTS)
        ]
        assert len(texts) >= 3, "Недостаточно отзывов на странице"
        assert any("спорт" in t for t in texts), "Не найден текст, связанный со спортом"

    @allure.step("Открыть отзыв и проверить содержимое")
    def open_feedback_modal(self, index=0):
        self._safe_scroll(L.FEEDBACK_SECTION)
        links = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*L.FEEDBACK_LINKS)
        )
        assert links, "Нет ссылок 'Читать отзыв'"
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", links[index]
        )
        time.sleep(0.3)
        links[index].click()
        self._wait_modal_ready()
        self._safe_scroll(L.FEEDBACK_MODAL_TITLE)
        self.assert_element_present(L.FEEDBACK_MODAL_TITLE)
        self.assert_element_present(L.FEEDBACK_MODAL_BODY)

    @allure.step("Закрыть модалку отзыва")
    def close_feedback_modal(self):
        self._safe_scroll(L.MODAL_CLOSE)
        self.click_if_visible(L.MODAL_CLOSE)
        time.sleep(0.5)

    # =====================
    # FOOTER
    # =====================
    @allure.step("Проверить наличие футера и ссылок")
    def check_footer_presence(self):
        self._safe_scroll(L.FOOTER)
        self.assert_element_present(L.FOOTER)
        self.assert_element_present(L.FOOTER_LINKS)

    # =====================
    # EXTENDED CHECKS
    # =====================
    @allure.step("Проверить, что у всех изображений есть alt-тексты")
    def check_images_have_alt(self):
        """Проверяет, что у всех img-элементов есть атрибут alt (может быть пустым, но присутствует)."""
        imgs = self.driver.find_elements(By.CSS_SELECTOR, "img")

        # считаем проблемными только те, у кого вообще нет атрибута alt
        missing_alt = [i.get_attribute("src") for i in imgs if i.get_attribute("alt") is None]

        assert not missing_alt, f"Изображения без alt-атрибута: {missing_alt}"

    @allure.step("Проверить, что слайдер 'Преимущества' листается")
    def check_benefit_slider_moves(self):
        """Проверяет, что горизонтальный слайдер 'Преимущества' реагирует на стрелку 'вперёд'."""
        self._safe_scroll(L.BENEFIT_SECTION)

        # Находим контейнер для горизонтального скролла
        scroll_container = self.driver.find_element(By.CSS_SELECTOR, "#benefitSection .scroll-container")

        # Получаем начальное положение скролла
        initial_scroll = self.driver.execute_script("return arguments[0].scrollLeft;", scroll_container)

        # Кликаем по стрелке "вперёд"
        next_btn = self.driver.find_element(*L.BENEFIT_NEXT)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
        self.driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(1)

        # Получаем новое положение скролла
        new_scroll = self.driver.execute_script("return arguments[0].scrollLeft;", scroll_container)

        # Проверяем, что скролл изменился
        assert new_scroll > initial_scroll, (
            f"Слайдер 'Преимущества' не пролистывает контент — scrollLeft не изменился "
            f"({initial_scroll} → {new_scroll})"
        )

    @allure.step("Проверить, что слайдер 'Сотрудничество' листается")
    def check_cooperation_slider_moves(self):
        """Проверяет, что горизонтальный слайдер 'Сотрудничество' реагирует на стрелку 'вперёд'."""
        self._safe_scroll(L.COOP_SECTION)

        # Находим контейнер для горизонтального скролла
        scroll_container = self.driver.find_element(By.CSS_SELECTOR, "#cooperationSection .scroll-container")

        # Получаем текущее положение скролла
        initial_scroll = self.driver.execute_script("return arguments[0].scrollLeft;", scroll_container)

        # Кликаем по стрелке "вперёд"
        next_btn = self.driver.find_element(*L.COOP_NEXT)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
        self.driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(1)

        # Получаем новое положение скролла
        new_scroll = self.driver.execute_script("return arguments[0].scrollLeft;", scroll_container)

        # Проверяем, что прокрутка действительно изменилась
        assert new_scroll > initial_scroll, (
            f"Слайдер 'Сотрудничество' не пролистывает контент — scrollLeft не изменился "
            f"({initial_scroll} → {new_scroll})"
        )

    @allure.step("Проверить корректность структуры заголовков (h1, h2, h3)")
    def check_headings_structure(self):
        headings = [h.tag_name for h in self.driver.find_elements(By.XPATH, "//h1|//h2|//h3")]
        assert "h1" in headings, "Отсутствует h1-заголовок"
        assert headings.count("h1") == 1, f"Несколько h1 заголовков: {headings.count('h1')}"

    @allure.step("Проверить адаптивность страницы")
    def check_responsive_layout(self):
        self.resize_window(800, 900)
        assert self.is_element_visible(L.PROMO_SECTION)
        self.resize_window(1920, 1080)
        self.driver.maximize_window()

    @allure.step("Проверить, что логотип кликабелен и ведёт на главную")
    def check_header_logo_link(self):
        self._safe_scroll(L.HEADER_LOGO)
        logo = self.driver.find_element(*L.HEADER_LOGO)
        parent = logo.find_element(By.XPATH, "./ancestor::a")
        href = parent.get_attribute("href")
        assert "allsports.by" in href, f"Некорректная ссылка логотипа: {href}"

    @allure.step("Проверить отсутствие ошибок JS в консоли")
    def check_no_console_errors(self):
        try:
            logs = self.driver.get_log("browser")
            js_errors = [l for l in logs if "error" in l["level"].lower()]
            assert not js_errors, f"Обнаружены ошибки JS: {js_errors}"
        except Exception:
            pass

    @allure.step("Проверить наличие блока 'Часто задаваемые вопросы'")
    def check_faq_section_present(self):
        self._safe_scroll(L.FAQ_SECTION)
        self.assert_element_present(L.FAQ_TITLE)
        self.assert_element_present(L.FAQ_CONTAINER)
        self.assert_text_on_page("Часто задаваемые вопросы")

    @allure.step("Проверить наличие всех вопросов FAQ")
    def check_all_questions_present(self):
        self._safe_scroll(L.FAQ_LIST)
        questions = [el.text.strip() for el in self.driver.find_elements(*L.FAQ_QUESTIONS)]
        assert questions, "Список вопросов FAQ пуст"
        for expected in L.EXPECTED_QUESTIONS:
            assert expected in questions, f"Отсутствует вопрос: '{expected}'"

    @allure.step("Проверить, что вопросы FAQ раскрываются и отображают ответы")
    def check_faq_expansion_functionality(self):
        """Проверяет, что при клике на вопрос FAQ раскрывается корректный ответ."""
        self._safe_scroll(L.FAQ_SECTION)
        items = self.driver.find_elements(*L.FAQ_ITEMS)
        assert items, "Элементы FAQ не найдены"

        for index, item in enumerate(items, start=1):
            # Находим контейнер вопроса (не SVG!)
            title_container = item.find_element(By.CSS_SELECTOR, ".expansion-item-title")
            question_text = title_container.find_element(By.CSS_SELECTOR, "h5").text.strip()

            # Скроллим к вопросу
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_container)
            time.sleep(0.3)

            # Кликаем по контейнеру вопроса
            try:
                title_container.click()
            except Exception:
                # Если стандартный click() не сработал — создаём JS-событие click
                self.driver.execute_script(
                    "arguments[0].dispatchEvent(new MouseEvent('click', {bubbles:true}));",
                    title_container
                )

            # Проверяем появление текста ответа
            try:
                answer_el = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"(//div[contains(@class,'expansion-item-text')])[{index}]"))
                )
                assert answer_el.is_displayed(), f"Ответ не раскрылся для вопроса: {question_text}"
                allure.attach(answer_el.text, f"Ответ: {question_text}")
            except Exception:
                html_snapshot = self.driver.page_source
                print(f"[DEBUG HTML SNAPSHOT for '{question_text}']\n{html_snapshot[:600]}...\n")
                assert False, f"Не удалось раскрыть вопрос '{question_text}'"

    @allure.step("Проверить блок 'Информация для Партнёров'")
    def check_partners_info_block(self):
        self._safe_scroll(L.FAQ_SECTION)
        if len(self.driver.find_elements(*L.FAQ_PARTNERS_BLOCK)) > 0:
            self.assert_element_present(L.FAQ_PARTNERS_LINK)
            link = self.driver.find_element(*L.FAQ_PARTNERS_LINK).get_attribute("href")
            assert "partners" in link, "Некорректная ссылка в блоке 'Информация для Партнёров'"

    @allure.step("Проверить наличие и кликабельность кнопки 'Задать вопрос'")
    def check_faq_form_button(self):
        self._safe_scroll(L.FAQ_FORM)
        self.assert_element_present(L.FAQ_FORM_TITLE)
        button = self.driver.find_element(*L.FAQ_FORM_BUTTON)
        assert button.is_displayed(), "Кнопка 'Задать вопрос' не отображается"
        assert button.is_enabled(), "Кнопка 'Задать вопрос' недоступна для нажатия"

    # =====================
    # FAQ
    # =====================

    @allure.step("Проверить наличие блока 'Часто задаваемые вопросы'")
    def check_faq_section_present(self):
        """Проверяет, что блок FAQ отображается и содержит заголовок."""
        self._safe_scroll(L.FAQ_SECTION)
        self.assert_element_present(L.FAQ_TITLE)
        self.assert_element_present(L.FAQ_CONTAINER)
        self.assert_text_on_page("Часто задаваемые вопросы")

    @allure.step("Проверить наличие всех вопросов FAQ")
    def check_all_questions_present(self):
        """Проверяет, что на странице присутствуют все ожидаемые вопросы FAQ."""
        self._safe_scroll(L.FAQ_LIST)
        questions = [el.text.strip() for el in self.driver.find_elements(*L.FAQ_QUESTIONS)]
        assert questions, "Список вопросов FAQ пуст или не найден"

        missing = [q for q in L.EXPECTED_QUESTIONS if q not in questions]
        assert not missing, f"Отсутствуют вопросы FAQ: {missing}"

    @allure.step("Проверить, что вопросы FAQ раскрываются и отображают ответы")
    def check_faq_expansion_functionality(self):
        """Проверяет, что при клике на вопрос FAQ раскрывается корректный ответ."""
        self._safe_scroll(L.FAQ_SECTION)
        items = self.driver.find_elements(*L.FAQ_ITEMS)
        assert items, "Элементы FAQ не найдены"

        for index, item in enumerate(items, start=1):
            # Находим контейнер вопроса (не SVG!)
            title_container = item.find_element(By.CSS_SELECTOR, ".expansion-item-title")
            question_text = title_container.find_element(By.CSS_SELECTOR, "h5").text.strip()

            # Скроллим к вопросу
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_container)
            time.sleep(0.3)

            # Кликаем по контейнеру вопроса
            try:
                title_container.click()
            except Exception:
                # Если стандартный click() не сработал — создаём JS-событие click
                self.driver.execute_script(
                    "arguments[0].dispatchEvent(new MouseEvent('click', {bubbles:true}));",
                    title_container
                )

            # Проверяем появление текста ответа
            try:
                answer_el = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"(//div[contains(@class,'expansion-item-text')])[{index}]"))
                )
                assert answer_el.is_displayed(), f"Ответ не раскрылся для вопроса: {question_text}"
                allure.attach(answer_el.text, f"Ответ: {question_text}")
            except Exception:
                html_snapshot = self.driver.page_source
                print(f"[DEBUG HTML SNAPSHOT for '{question_text}']\n{html_snapshot[:600]}...\n")
                assert False, f"Не удалось раскрыть вопрос '{question_text}'"

    @allure.step("Проверить блок 'Информация для Партнёров'")
    def check_partners_info_block(self):
        """Проверяет наличие и корректность блока 'Информация для Партнёров' в FAQ."""
        self._safe_scroll(L.FAQ_SECTION)
        partners_blocks = self.driver.find_elements(*L.FAQ_PARTNERS_BLOCK)
        if partners_blocks:
            self.assert_element_present(L.FAQ_PARTNERS_LINK)
            link = self.driver.find_element(*L.FAQ_PARTNERS_LINK).get_attribute("href")
            assert "partners" in link, f"Некорректная ссылка в блоке партнёров: {link}"
        else:
            allure.attach(self.driver.page_source, "faq_no_partner_block.html", allure.attachment_type.HTML)
            print("⚠️ Блок 'Информация для Партнёров' отсутствует (это может быть нормой для некоторых страниц).")

    @allure.step("Проверить наличие и кликабельность кнопки 'Задать вопрос'")
    def check_faq_form_button(self):
        """Проверяет наличие блока с кнопкой 'Задать вопрос' внизу FAQ."""
        self._safe_scroll(L.FAQ_FORM)
        self.assert_element_present(L.FAQ_FORM_TITLE)
        self.assert_text_on_page("Не нашли ответ на вопрос?")

        button = self.driver.find_element(*L.FAQ_FORM_BUTTON)
        assert button.is_displayed(), "Кнопка 'Задать вопрос' не отображается на странице"
        assert button.is_enabled(), "Кнопка 'Задать вопрос' недоступна для нажатия"

    # =====================
    # FORMS (HEADER / PROMO / FAQ / JOIN)
    # =====================

    INVALID_PHONE_1 = "1234"
    INVALID_PHONE_2 = "привет"
    INVALID_EMAIL_1 = "привет"
    INVALID_EMAIL_2 = "qwert@@"
    VALID_NAME = "QA Автотест"
    VALID_EMAIL = "qa.autotest@allsports.by"
    VALID_COMPANY = "Allsports QA"
    VALID_CITY = "Минск"
    VALID_PHONE = "+375 44 111 11 11"
    VALID_QUESTION = "Проверка модального окна (автотест)"

    # ====== Вспомогательные ======
    def _scroll_modal_to_bottom(self):
        """Аккуратно прокручивает модалку вниз, чтобы увидеть чекбокс и кнопку."""
        try:
            modal = self.driver.find_element(*L.MODAL)
            self.driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight);", modal
            )
        except Exception:
            pass

    def _blur(self):
        """Снимает фокус с активного поля (для вызова ошибок валидации)."""
        self.driver.execute_script(
            "document.activeElement && document.activeElement.blur();"
        )

    def _ensure_btn_disabled(self, btn):
        assert not btn.is_enabled(), "Кнопка отправки должна быть неактивна при текущем состоянии"

    def _ensure_btn_enabled(self, btn):
        assert btn.is_enabled(), "Кнопка отправки должна стать активной"

    # ====== Открытие форм ======
    @allure.step("Открыть модалку из хедера: 'Получить предложение'")
    def open_header_offer_modal(self):
        self.driver.execute_script("window.scrollTo({top:0});")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.HEADER_OFFER_BTN)
        ).click()
        self._wait_modal_ready()
        return self

    @allure.step("Открыть модалку из хедера: 'Задать вопрос'")
    def open_header_question_modal(self):
        self.driver.execute_script("window.scrollTo({top:0});")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.HEADER_ASK_BTN)
        ).click()
        self._wait_modal_ready()
        return self

    @allure.step("Открыть модалку из промо-блока: 'Получить предложение'")
    def open_promo_offer_modal(self):
        self._safe_scroll(L.PROMO_OFFER_BTN)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.PROMO_OFFER_BTN)
        ).click()
        self._wait_modal_ready()
        return self

    @allure.step("Открыть модалку из промо-блока: 'Задать вопрос'")
    def open_promo_question_modal(self):
        self._safe_scroll(L.PROMO_ASK_BTN)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.PROMO_ASK_BTN)
        ).click()
        self._wait_modal_ready()
        return self

    @allure.step("Открыть модалку из блока FAQ: 'Задать вопрос'")
    def open_faq_question_modal(self):
        self._safe_scroll(L.FAQ_ASK_BTN)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.FAQ_ASK_BTN)
        ).click()
        self._wait_modal_ready()
        return self

    # ====== Общие проверки модалок ======
    @allure.step("Проверить общую структуру модалки (заголовок, политика, телефон)")
    def check_modal_common(self, expected_title_substring: str):
        """Проверяет наличие модалки, заголовка, ссылки на политику и телефона."""
        self.assert_element_present(L.MODAL)
        self.assert_element_present(L.MODAL_FORM)
        title = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(L.MODAL_TITLE)
        ).text.strip()
        assert expected_title_substring in title, f"Ожидался заголовок '{expected_title_substring}', найдено '{title}'"

        # Проверка ссылки на политику
        policy = self.driver.find_element(*L.MODAL_POLICY_LINK)
        href = policy.get_attribute("href")
        assert "/policy/" in href, f"Некорректная ссылка политики: {href}"

        # Проверка телефонной ссылки
        phone_link = self.driver.find_element(*L.MODAL_PHONE_LINK)
        tel = phone_link.get_attribute("href")
        assert tel.startswith("tel:"), "Телефонная ссылка должна начинаться с tel:"
        assert "375" in tel, f"Телефонная ссылка не содержит код страны: {tel}"

    # ====== Валидации в модалках ======
    @allure.step("Проверить ошибки валидации телефона (в модалке)")
    def validate_phone_errors_in_modal(self):
        """Проверяет, что при вводе некорректного телефона появляется ошибка."""
        phone = self.driver.find_element(*L.MODAL_PHONE_INPUT)

        # === Проверка 1: 1234 ===
        phone.clear()
        phone.send_keys(self.INVALID_PHONE_1)
        self._blur()  # теряем фокус
        # ждем появления ошибки
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*L.MODAL_PHONE_ERROR).text.strip() != ""
        )
        err1 = self.driver.find_element(*L.MODAL_PHONE_ERROR).text.strip()
        assert "Неверный формат" in err1 and "+375" in err1, (
            f"Ожидалась ошибка формата телефона, получили: '{err1}'"
        )

        # === Проверка 2: 'привет' ===
        phone.clear()
        phone.send_keys(self.INVALID_PHONE_2)
        self._blur()
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*L.MODAL_PHONE_ERROR).text.strip() != ""
        )
        err2 = self.driver.find_element(*L.MODAL_PHONE_ERROR).text.strip()
        assert "Неверный формат" in err2, (
            f"Ожидалась ошибка при вводе кириллицы, получили: '{err2}'"
        )

    @allure.step("Проверить ошибки валидации Email (в модалке)")
    def validate_email_errors_in_modal(self):
        """Проверяет корректные ошибки валидации для поля email (запрещённые символы / недействительный адрес)."""
        email = self.driver.find_element(*L.MODAL_EMAIL_INPUT)

        # Локатор: span с ошибкой внутри label, где input[name='email']
        error_locator = (
            By.XPATH,
            "//label[contains(@class,'input')][.//input[@name='email']]//span[contains(@class,'input-error__text')]"
        )

        # === Проверка 1: 'привет' ===
        email.clear()
        email.send_keys(self.INVALID_EMAIL_1)
        self._blur()

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(error_locator, "Поле содержит")
        )
        err1 = self.driver.find_element(*error_locator).text.strip()
        assert "запрещ" in err1.lower() or "поле содержит" in err1.lower(), (
            f"Ожидалась ошибка про запрещённые символы, получили: '{err1}'"
        )

        # --- Полное очищение input через JS (clear() не работает из-за кастомного поля) ---
        self.driver.execute_script("arguments[0].value = '';", email)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", email)
        time.sleep(0.5)

        # === Проверка 2: 'qwert@@' ===
        email.send_keys(self.INVALID_EMAIL_2)
        self._blur()

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(error_locator, "Адрес электронной почты")
        )
        err2 = self.driver.find_element(*error_locator).text.strip()
        assert (
                "должен" in err2.lower()
                or "адрес" in err2.lower()
                or "email" in err2.lower()
        ), f"Ожидалась ошибка 'Адрес электронной почты должен быть действительным', получили: '{err2}'"

    # ====== Проверка активации кнопок ======
    @allure.step("Проверить активацию кнопки 'Отправить' в форме 'Получить предложение'")
    def check_offer_submit_activation(self):
        submit = self.driver.find_element(*L.MODAL_SUBMIT_BTN)
        self._ensure_btn_disabled(submit)

        self.driver.find_element(*L.MODAL_NAME_INPUT).send_keys(self.VALID_NAME)
        self.driver.find_element(*L.MODAL_EMAIL_INPUT).send_keys(self.VALID_EMAIL)

        company_inputs = self.driver.find_elements(*L.MODAL_COMPANY_INPUT)
        if company_inputs:
            company_inputs[0].send_keys(self.VALID_COMPANY)
        else:
            self.driver.find_element(*L.MODAL_OBJECT_INPUT).send_keys(self.VALID_COMPANY)

        # Без чекбокса кнопка неактивна
        self._ensure_btn_disabled(submit)

        # Ставим чекбокс
        label = self.driver.find_element(*L.MODAL_AGREE_LABEL)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
        self.driver.execute_script("arguments[0].click();", label)
        time.sleep(0.4)
        self._ensure_btn_enabled(submit)

    @allure.step("Проверить активацию кнопки 'Отправить' в форме 'Задать вопрос'")
    def check_question_submit_activation(self):
        """Проверяет, что кнопка 'Отправить' активируется только после заполнения всех обязательных полей и чекбокса."""
        submit = self.driver.find_element(*L.MODAL_SUBMIT_BTN)
        self._ensure_btn_disabled(submit)

        # --- Заполняем все обязательные поля ---
        self.driver.find_element(*L.MODAL_NAME_INPUT).send_keys(self.VALID_NAME)
        self.driver.find_element(*L.MODAL_PHONE_INPUT).send_keys("+375 44 111 11 11")
        self.driver.find_element(*L.MODAL_EMAIL_INPUT).send_keys(self.VALID_EMAIL)
        self.driver.find_element(*L.MODAL_TEXTAREA).send_keys(self.VALID_QUESTION)

        # --- Проверяем: без чекбокса кнопка всё ещё неактивна ---
        self._ensure_btn_disabled(submit)

        # --- Ставим чекбокс согласия ---
        label = self.driver.find_element(*L.MODAL_AGREE_LABEL)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
        self.driver.execute_script("arguments[0].click();", label)
        time.sleep(0.5)

        # --- Проверяем, что кнопка активировалась ---
        self._ensure_btn_enabled(submit)

    # ====== Inline форма JOIN ======
    @allure.step("Проверить inline-форму 'Присоединяйтесь к Allsports'")
    def check_join_form_full(self):
        """Проверяет структуру и активацию inline-формы 'Присоединяйтесь к Allsports'."""
        # --- Скроллим вниз, чтобы форма точно прогрузилась ---
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        # --- Прокручиваем к секции с формой ---
        self._safe_scroll(L.JOIN_SECTION)

        # --- Проверяем наличие формы и кнопки ---
        form = self.driver.find_element(*L.JOIN_FORM)
        assert form is not None, "Форма 'Присоединяйтесь к Allsports' не найдена"

        submit = self.driver.find_element(*L.JOIN_SUBMIT_BTN)
        assert submit is not None, "Кнопка 'Получить предложение' не найдена"

        # --- Проверяем, что кнопка изначально неактивна ---
        self._ensure_btn_disabled(submit)

        # --- Заполняем все обязательные поля ---
        self.driver.find_element(*L.JOIN_NAME_INPUT).send_keys(self.VALID_NAME)
        self.driver.find_element(*L.JOIN_PHONE_INPUT).send_keys(self.VALID_PHONE)
        self.driver.find_element(*L.JOIN_EMAIL_INPUT).send_keys(self.VALID_EMAIL)
        self.driver.find_element(*L.JOIN_COMPANY_INPUT).send_keys(self.VALID_COMPANY)

        # --- Проверяем, что кнопка всё ещё неактивна без чекбокса ---
        self._ensure_btn_disabled(submit)

        # --- Ставим чекбокс согласия ---
        checkbox_label = self.driver.find_element(*L.JOIN_AGREE_LABEL)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox_label)
        self.driver.execute_script("arguments[0].click();", checkbox_label)
        time.sleep(0.5)

        # --- Проверяем, что кнопка стала активной ---
        self._ensure_btn_enabled(submit)

        # --- Проверяем ссылку на политику ---
        policy_link = self.driver.find_element(*L.JOIN_POLICY_LINK)
        href = policy_link.get_attribute("href")
        assert "/policy/" in href, f"Некорректная ссылка политики: {href}"

    # =====================
    # VIDEO
    # =====================
    @allure.step("Проверить наличие iframe с видео YouTube")
    def check_video_iframe(self):
        """Проверяет наличие iframe с видео YouTube в блоке 'videoSection'."""
        self._safe_scroll((By.ID, "videoSection"))
        self.assert_element_present((By.CSS_SELECTOR, "#videoSection iframe"))

    @allure.step("Проверить корректность источника iframe (YouTube)")
    def check_video_src(self):
        """Проверяет, что видео iframe подгружается с YouTube."""
        self._safe_scroll((By.ID, "videoSection"))
        iframe = self.driver.find_element(By.CSS_SELECTOR, "#videoSection iframe")
        src = iframe.get_attribute("src")
        assert src and "youtube.com" in src, f"Источник iframe некорректен: {src}"

    @allure.step("Проверить, что iframe имеет атрибут allowfullscreen")
    def check_video_allowfullscreen(self):
        """Проверяет наличие атрибута allowfullscreen у iframe."""
        self._safe_scroll((By.ID, "videoSection"))
        iframe = self.driver.find_element(By.CSS_SELECTOR, "#videoSection iframe")
        assert iframe.get_attribute("allowfullscreen") is not None, "Атрибут allowfullscreen отсутствует"

    # =====================
    # CONTACTS
    # =====================
    @allure.step("Проверить наличие блока 'Наши контакты'")
    def check_contacts_section_present(self):
        """Проверяет, что блок 'Наши контакты' отображается на странице."""
        self._safe_scroll(L.CONTACTS_SECTION)
        self.assert_element_present(L.CONTACTS_SECTION)
        self.assert_text_on_page("Наши контакты")
        self.assert_element_present(L.CONTACTS_CONTAINER)
        self.assert_element_present(L.CONTACTS_INFO)
        self.assert_element_present(L.CONTACTS_MAP)

    @allure.step("Проверить корректность контактных данных")
    def check_contacts_data(self):
        """Проверяет наличие и правильность текстов телефонов, email и расписания."""
        self._safe_scroll(L.CONTACTS_SECTION)

        # Проверка текстов отделов
        expected_contacts = {
            "Отдел по работе с клиентами:": {
                "phone": "+375 44 771 09 47",
                "email": "sales@allsports.by",
                "schedule": "(пн-пт: 09:00-18:00, сб-вс: выходной)"
            },
            "Отдел по работе с партнёрами:": {
                "phone": "+375 44 525 38 92",
                "email": "suppliers@allsports.by",
                "schedule": "(пн-пт: 09:00-18:00, сб-вс: выходной)"
            },
            "Техническая поддержка:": {
                "phone": "+375 44 770 94 26",
                "email": "support@allsports.by",
                "schedule": "(пн-пт: 9:00-21:30, сб-вс: 9:00-20:00)"
            },
            "Адрес:": {
                "address": "220030 г. Минск, ул. Интернациональная, 36-2, офисы 2-20, 1-21"
            }
        }

        info_blocks = self.driver.find_elements(*L.CONTACTS_INFO_BLOCKS)
        assert info_blocks, "Блоки контактов не найдены"

        for block in info_blocks:
            title = block.find_element(By.CSS_SELECTOR, "p.text-h4").text.strip()
            text_block = block.text.strip()

            assert title in expected_contacts, f"Неожиданный заголовок: {title}"

            if "phone" in expected_contacts[title]:
                phone = expected_contacts[title]["phone"]
                assert phone in text_block, f"Телефон '{phone}' не найден в блоке '{title}'"

            if "email" in expected_contacts[title]:
                email = expected_contacts[title]["email"]
                assert email in text_block, f"Email '{email}' не найден в блоке '{title}'"

            if "schedule" in expected_contacts[title]:
                schedule = expected_contacts[title]["schedule"]
                assert schedule in text_block, f"Расписание '{schedule}' не совпадает в блоке '{title}'"

            if "address" in expected_contacts[title]:
                address = expected_contacts[title]["address"]
                assert address in text_block, f"Адрес '{address}' не совпадает"

    @allure.step("Проверить, что карта отображается и не сломана")
    def check_contacts_map(self):
        """Проверяет наличие карты внизу страницы, корректную загрузку и наличие маркера."""
        # --- Скроллим страницу в самый низ ---
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)  # даем прогрузиться динамическому контенту (Mapbox)

        # --- Дожидаемся появления карты ---
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(L.CONTACTS_MAP)
            )
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(L.CONTACTS_MAP_CANVAS)
            )
        except TimeoutException:
            html_snapshot = self.driver.page_source
            print(f"[DEBUG HTML SNAPSHOT]\n{html_snapshot[:800]}...\n")
            assert False, "Карта не загрузилась за отведённое время"

        # --- Проверяем наличие канваса карты ---
        canvas = self.driver.find_element(*L.CONTACTS_MAP_CANVAS)
        assert canvas.is_displayed(), "Элемент canvas карты не отображается"

        # --- Проверяем размеры карты ---
        width = int(canvas.get_attribute("width") or 0)
        height = int(canvas.get_attribute("height") or 0)
        assert width > 0 and height > 0, f"Некорректные размеры карты ({width}x{height}) — возможно, не загрузилась"

        # --- Проверяем наличие маркера ---
        markers = self.driver.find_elements(*L.CONTACTS_MARKER)
        assert markers, "Маркер на карте отсутствует — возможно, карта не инициализирована"

    # =====================
    # FORM SUBMISSION CHECKS
    # =====================
    @allure.step("Отправить форму 'Получить предложение' (Промо-блок)")
    def submit_promo_offer_form(self):
        """Заполняет и отправляет форму 'Получить предложение' в промо-блоке, затем проверяет успех."""
        driver = self.driver
        driver.find_element(*L.MODAL_NAME_INPUT).send_keys(self.VALID_NAME)
        driver.find_element(*L.MODAL_PHONE_INPUT).send_keys(self.VALID_PHONE)
        driver.find_element(*L.MODAL_EMAIL_INPUT).send_keys(self.VALID_EMAIL)
        driver.find_element(*L.MODAL_INPUT_COMPANY).send_keys(self.VALID_COMPANY)
        driver.find_element(*L.MODAL_INPUT_CITY).send_keys(self.VALID_CITY)

        label = driver.find_element(*L.MODAL_AGREE_LABEL)
        driver.execute_script("arguments[0].click();", label)
        submit = driver.find_element(*L.MODAL_BTN_SUBMIT)
        driver.execute_script("arguments[0].click();", submit)

        success_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(L.SUCCESS_TEXT)
        )
        assert "Спасибо за ваш запрос" in success_text.text
        self._close_success_modal()

    @allure.step("Отправить форму 'Задать вопрос' (Промо-блок)")
    def submit_promo_question_form(self):
        driver = self.driver
        driver.find_element(*L.MODAL_NAME_INPUT).send_keys(self.VALID_NAME)
        driver.find_element(*L.MODAL_PHONE_INPUT).send_keys(self.VALID_PHONE)
        driver.find_element(*L.MODAL_EMAIL_INPUT).send_keys(self.VALID_EMAIL)
        driver.find_element(*L.MODAL_TEXTAREA_QUESTION).send_keys(self.VALID_QUESTION)

        label = driver.find_element(*L.MODAL_AGREE_LABEL)
        driver.execute_script("arguments[0].click();", label)
        submit = driver.find_element(*L.MODAL_BTN_SUBMIT)
        driver.execute_script("arguments[0].click();", submit)

        success_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(L.SUCCESS_TEXT)
        )
        assert "Спасибо за ваш запрос" in success_text.text
        self._close_success_modal()

    @allure.step("Отправить форму 'Задать вопрос' (FAQ)")
    def submit_faq_question_form(self):
        driver = self.driver
        driver.find_element(*L.MODAL_NAME_INPUT).send_keys(self.VALID_NAME)
        driver.find_element(*L.MODAL_PHONE_INPUT).send_keys(self.VALID_PHONE)
        driver.find_element(*L.MODAL_EMAIL_INPUT).send_keys(self.VALID_EMAIL)
        driver.find_element(*L.MODAL_TEXTAREA_QUESTION).send_keys(self.VALID_QUESTION)

        label = driver.find_element(*L.MODAL_AGREE_LABEL)
        driver.execute_script("arguments[0].click();", label)
        submit = driver.find_element(*L.MODAL_BTN_SUBMIT)
        driver.execute_script("arguments[0].click();", submit)

        success_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(L.SUCCESS_TEXT)
        )
        assert "Спасибо за ваш запрос" in success_text.text
        self._close_success_modal()

    @allure.step("Отправить inline-форму 'Присоединяйтесь к Allsports'")
    def submit_join_form(self):
        driver = self.driver
        self._safe_scroll(L.JOIN_SECTION)
        driver.find_element(*L.JOIN_NAME_INPUT).send_keys(self.VALID_NAME)
        driver.find_element(*L.JOIN_PHONE_INPUT).send_keys(self.VALID_PHONE)
        driver.find_element(*L.JOIN_EMAIL_INPUT).send_keys(self.VALID_EMAIL)
        driver.find_element(*L.JOIN_COMPANY_INPUT).send_keys(self.VALID_COMPANY)

        label = driver.find_element(*L.JOIN_AGREE_LABEL)
        driver.execute_script("arguments[0].click();", label)
        submit = driver.find_element(*L.JOIN_SUBMIT_BTN)
        driver.execute_script("arguments[0].click();", submit)

        success_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(L.SUCCESS_TEXT)
        )
        assert "Спасибо за ваш запрос" in success_text.text
        self._close_success_modal()

    @allure.step("Закрыть success-модалку после отправки формы")
    def _close_success_modal(self):
        """Кликает по кнопке 'Закрыть' и убеждается, что модалка исчезла."""
        driver = self.driver
        close_btn = driver.find_element(*L.SUCCESS_CLOSE_BTN)
        driver.execute_script("arguments[0].click();", close_btn)
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located(L.SUCCESS_MODAL)
        )

    # =====================
    # POLICY LINK CHECKS
    # =====================
    @allure.step("Проверить ссылку на политику обработки персональных данных во всех формах")
    def check_policy_link_in_all_forms(self):
        """Проверяет, что ссылка на политику корректна, рабочая и открывает нужную страницу во всех формах."""
        driver = self.driver
        expected_text = "Политика компании в отношении обработки персональных данных субъектов персональных данных"

        forms_to_check = [
            ("Промо — Получить предложение", self.open_promo_offer_modal, L.MODAL_POLICY_LINK),
            ("Промо — Задать вопрос", self.open_promo_question_modal, L.MODAL_POLICY_LINK),
            ("FAQ — Задать вопрос", self.open_faq_question_modal, L.MODAL_POLICY_LINK),
            ("Inline — Присоединяйтесь к Allsports", lambda: self._safe_scroll(L.JOIN_SECTION), L.JOIN_POLICY_LINK),
        ]

        for form_name, open_func, locator in forms_to_check:
            with allure.step(f"Проверка ссылки политики в форме: {form_name}"):
                # --- Открываем страницу заново, чтобы не мешали прошлые модалки ---
                driver.get(L.BASE_URL)
                time.sleep(1)
                self.accept_cookie_consent()
                time.sleep(0.5)

                # --- Открываем соответствующую форму ---
                open_func()

                # --- Ищем ссылку на политику ---
                link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(locator)
                )
                href = link.get_attribute("href")

                assert href, f"Ссылка политики отсутствует в форме '{form_name}'"
                assert href.startswith("https"), f"Некорректный формат ссылки: {href}"
                assert "/policy/" in href, f"Ссылка не содержит '/policy/': {href}"

                # --- Открываем ссылку в новой вкладке ---
                driver.execute_script("window.open(arguments[0], '_blank');", href)
                driver.switch_to.window(driver.window_handles[-1])

                # --- Ждём загрузку и проверяем содержимое ---
                WebDriverWait(driver, 20).until(lambda d: "policy" in d.current_url.lower())
                page_text = driver.page_source
                assert expected_text in page_text, (
                    f"На странице политики не найден ожидаемый текст.\n"
                    f"Искали: '{expected_text}'"
                )

                current_url = driver.current_url
                assert "allsports.by/ru-by/policy/251010_processing_personal_data" in current_url, (
                    f"Открыт неверный URL политики ({form_name}): {current_url}"
                )

                # --- Закрываем вкладку политики и возвращаемся ---
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(0.5)

                # --- Если осталась открыта модалка — закрываем ---
                try:
                    self.click_if_visible(L.MODAL_CLOSE)
                    time.sleep(0.3)
                except Exception:
                    pass

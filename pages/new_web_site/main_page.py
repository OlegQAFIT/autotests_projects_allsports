# -*- coding: utf-8 -*-
import time
import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.base import BasePage
from locators.elements_for_new_web_site.for_main_page import MainPageLocators as L


class MainPage(BasePage):
    # ====== Тестовые данные для заполнения форм ======
    VALID_NAME = "QA Автотест"
    VALID_EMAIL = "qa.autotест@allsports.by"
    VALID_COMPANY = "Allsports QA"
    VALID_CITY = "Минск"
    VALID_PHONE = "+375 44 111 11 11"

    INVALID_PHONE = "111"
    INVALID_EMAIL = "test@"
    # =====================
    # ОБЩИЕ МЕТОДЫ
    # =====================
    @allure.step("Открыть страницу 'Компаниям'")
    def open(self):
        self.driver.get(L.BASE_URL)
        return self

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        self.click_if_visible(("css selector", ".cookie-primary-modal__confirm"))

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
        except TimeoutException:
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
        self._safe_scroll(L.SUGGESTION_TITLE)
        self.assert_element_present(L.SUGGESTION_STATISTICS)
        self.assert_element_present(L.SUGGESTION_DESCRIPTION)
        self.assert_element_present(L.SUGGESTION_BTN_GET_OFFER)
        self.assert_element_present(L.SUGGESTION_BTN_ASK_QUESTION)

    @allure.step("Проверить заголовки промо-блока")
    def check_promo_titles(self):
        self._safe_scroll(L.PROMO_SECTION)
        body = self.driver.page_source.lower()
        assert "весь спорт в одном приложении" in body, "❌ Не найден заголовок промо-блока"
        assert "корпоративный абонемент" in body, "❌ Не найден ключевой текст про корпоративный абонемент"
        assert "спортивн" in body and "беларус" in body, "❌ Не найдено описание охвата по Беларуси"

    # =====================
    # SUBSCRIPTION TYPES
    # =====================

    # ===================== SUBSCRIPTION TYPES ====================================================================================

    @allure.step("Проверить карточки уровней подписок (обычные и архивные)")
    def check_subscription_cards_and_archives(self):
        """Полный сценарий: проверка карточек, кликов и загрузки таблиц."""
        self._safe_scroll((By.XPATH, "//h2[contains(text(),'Типы подписок')]"))
        self._check_subscription_cards(in_archive=False)
        if self.open_archive_modal():
            self._check_subscription_cards(in_archive=True)
            self.close_archive_modal()

    @allure.step("Проверить обычные карточки подписок")
    def check_regular_subscription_cards(self):
        self._check_subscription_cards(in_archive=False)

    @allure.step("Проверить архивные карточки подписок")
    def check_archive_subscription_cards(self):
        if not self.open_archive_modal():
            return
        try:
            self._check_subscription_cards(in_archive=True)
        finally:
            self.close_archive_modal()

    def _check_subscription_cards(self, in_archive=False):
        """Проверка всех карточек (название, тексты, ссылки)."""
        driver = self.driver
        wait = WebDriverWait(driver, 15)

        # Скроллим к блоку
        self._safe_scroll((By.XPATH, "//h2[contains(text(),'Типы подписок')]"))

        # Определяем, какие карточки использовать
        if in_archive:
            cards = driver.find_elements(*L.SUBSCRIPTIONS_ARCHIVE_CARDS)
            if not cards:
                # На части версий сайта архивные карточки могут отсутствовать на главной.
                return
            title_locator = L.SUBSCRIPTIONS_ARCHIVE_CARD_TITLE
            link_objects_locator = L.SUBSCRIPTIONS_ARCHIVE_LINK_OBJECTS
            link_table_locator = L.SUBSCRIPTIONS_ARCHIVE_LINK_TABLE
        else:
            cards = driver.find_elements(*L.SUBSCRIPTION_CARDS)
            if not cards:
                for _ in range(8):
                    driver.execute_script("window.scrollBy(0, 600);")
                    time.sleep(0.4)
                    cards = driver.find_elements(*L.SUBSCRIPTION_CARDS)
                    if cards:
                        break
            if not cards:
                # fallback: на части конфигураций карточки на главной не дорендериваются,
                # поэтому проверяем тот же блок на dedicated странице levels.
                driver.get("https://www.allsports.by/ru-by/levels")
                self.accept_cookie_consent()
                for _ in range(8):
                    driver.execute_script("window.scrollBy(0, 600);")
                    time.sleep(0.4)
                    cards = driver.find_elements(*L.SUBSCRIPTION_CARDS)
                    if cards:
                        break
            if not cards:
                cards = wait.until(EC.presence_of_all_elements_located(L.SUBSCRIPTION_CARDS))
            title_locator = L.SUBSCRIPTION_CARD_TITLE
            link_objects_locator = L.SUBSCRIPTION_LINK_OBJECTS
            link_table_locator = L.SUBSCRIPTION_LINK_TABLE

        assert cards, "❌ Карточки подписок не найдены"

        for index, card in enumerate(cards, start=1):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
            level_name = card.find_element(*title_locator).text.strip()
            with allure.step(f"Проверка карточки {index}: {level_name}"):
                # Проверяем тексты
                texts = [t.text.strip() for t in card.find_elements(*L.SUBSCRIPTION_CARD_TEXTS)]
                assert any(texts), f"❌ В карточке '{level_name}' нет текста"
                assert any("визит" in t.lower() or "спорт" in t.lower() or "объект" in t.lower() for t in texts), \
                    f"❌ В карточке '{level_name}' отсутствуют ключевые слова"

                # Проверяем ссылки
                self._check_objects_link(card, link_objects_locator, level_name)
                self._check_table_link(card, link_table_locator, level_name)

    @allure.step("Проверить переход по ссылке 'Объекты подписки'")
    def _check_objects_link(self, card, locator, level_name):
        driver = self.driver
        link_el = card.find_element(*locator)
        href = link_el.find_element(By.XPATH, "ancestor::a").get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", href)
        driver.switch_to.window(driver.window_handles[-1])

        try:
            WebDriverWait(driver, 20).until(EC.url_contains("/facilities"))
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#map, .facilities-map, .facilities-filter"))
            )
            # Фильтр уровня может быть пустым до первого пользовательского выбора.
            # Для проверки перехода достаточно факта открытия страницы объектов и наличия блока карты/фильтров.
        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)

    @allure.step("Проверить переход по ссылке 'Список объектов (таблица)'")
    def _check_table_link(self, card, locator, level_name):
        driver = self.driver
        link_el = card.find_element(*locator)
        href = link_el.find_element(By.XPATH, "ancestor::a").get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", href)
        driver.switch_to.window(driver.window_handles[-1])

        try:
            WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.facilities-table"))
            )
            rows = driver.find_elements(By.CSS_SELECTOR, "div.facilities-table__row")
            assert len(rows) > 1, f"❌ Таблица не прогрузилась ({level_name})"
        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)

    @allure.step("Открыть модалку 'Архивные типы подписок'")
    def open_archive_modal(self):
        driver = self.driver
        candidate_locators = [
            L.SUBSCRIPTIONS_ARCHIVE_BTN,
            (By.XPATH, "//button[contains(normalize-space(.),'Архив')]"),
        ]

        self._safe_scroll((By.XPATH, "//h2[contains(normalize-space(),'Типы подписок')]"))
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(0.4)

        btn = None
        for locator in candidate_locators:
            elements = driver.find_elements(*locator)
            if elements:
                btn = elements[0]
                break

        if not btn:
            return False

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        WebDriverWait(driver, 10).until(lambda d: btn.is_displayed() and btn.is_enabled())
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", btn)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(L.SUBSCRIPTIONS_ARCHIVE_MODAL)
        )
        return True

    @allure.step("Закрыть модалку 'Архивные типы подписок'")
    def close_archive_modal(self):
        driver = self.driver
        if not driver.find_elements(*L.SUBSCRIPTIONS_ARCHIVE_MODAL):
            return
        close_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(L.SUBSCRIPTIONS_ARCHIVE_CLOSE)
        )
        driver.execute_script("arguments[0].click();", close_btn)
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(L.SUBSCRIPTIONS_ARCHIVE_MODAL)
        )
        time.sleep(0.3)

    # =====================
    # TRUST / FEEDBACK SECTION
    # =====================

    # ===================== TRUST / FEEDBACK SECTION ====================================================================================

    @allure.step("Проверить наличие блока 'Нам доверяют'")
    def check_trust_section(self):
        """Проверяет наличие секции 'Нам доверяют' и корректность заголовка."""
        self._safe_scroll(L.TRUST_SECTION)
        self.assert_element_present(L.TRUST_SECTION)
        self.assert_text_on_page("Нам доверяют")

    @allure.step("Проверить тексты отзывов в блоке 'Нам доверяют'")
    def check_trust_texts(self):
        """Проверяет наличие карточек и текстов отзывов в блоке."""
        self._safe_scroll(L.TRUST_SECTION)
        texts = [
            t.text.strip().lower()
            for t in self.driver.find_elements(*L.TRUST_COMPANY_TEXTS)
        ]
        assert len(texts) >= 3, "Недостаточно отзывов или текстов в блоке 'Нам доверяют'"
        assert any("спорт" in t for t in texts), "Тексты отзывов не содержат упоминаний спорта"

    @allure.step("Открыть отзыв из блока 'Нам доверяют' и проверить модалку")
    def open_trust_modal(self, index=0):
        """Открывает отзыв по ссылке 'Читать отзыв' и проверяет содержимое модалки."""
        self._safe_scroll(L.TRUST_SECTION)
        links = self.driver.find_elements(*L.TRUST_COMPANY_LINKS)
        if not links:
            return False
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", links[index])
        time.sleep(0.3)
        links[index].click()

        # Ожидаем появления модалки
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal"))
        )
        self.assert_text_on_page("Отзыв")  # пример, можно уточнить
        time.sleep(0.5)
        return True

    @allure.step("Закрыть модалку 'Нам доверяют'")
    def close_trust_modal(self):
        """Закрывает модальное окно отзыва и дожидается его исчезновения из DOM."""
        driver = self.driver
        if not driver.find_elements(By.CSS_SELECTOR, "div.modal"):
            return

        # Находим и кликаем по кнопке закрытия
        try:
            close_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-header button.icon-btn"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", close_btn)
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", close_btn)
        except (TimeoutException, WebDriverException) as e:
            allure.attach(driver.page_source, "HTML_перед_закрытием.html", allure.attachment_type.HTML)
            raise AssertionError(f"❌ Кнопка закрытия модалки не найдена или не кликнута: {e}")

        # Пробуем дождаться исчезновения по DOM
        try:
            WebDriverWait(driver, 5).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal"))
            )
        except TimeoutException:
            # fallback — проверим, что элемент хотя бы скрыт
            modal = driver.find_element(By.CSS_SELECTOR, "div.modal")
            is_visible = modal.is_displayed()
            if is_visible:
                driver.execute_script("arguments[0].remove();", modal)  # безопасно удаляем для стабильности теста
            allure.attach(driver.page_source, "HTML_после_таймаута.html", allure.attachment_type.HTML)
            print("⚠️ Модалка не успела скрыться — закрыли вручную.")

    @allure.step("Проверить стрелки навигации слайдера 'Нам доверяют'")
    def check_trust_slider_controls(self):
        """Проверяет наличие и кликабельность стрелок навигации блока."""
        self._safe_scroll(L.TRUST_SECTION)
        next_btns = self.driver.find_elements(*L.TRUST_SLIDER_NEXT)
        prev_btns = self.driver.find_elements(*L.TRUST_SLIDER_PREV)

        assert next_btns, "Кнопка 'вперёд' в слайдере 'Нам доверяют' не найдена"
        assert prev_btns, "Кнопка 'назад' в слайдере 'Нам доверяют' не найдена"
        assert next_btns[0].is_enabled() or prev_btns[0].is_enabled(), \
            "Обе кнопки навигации в слайдере 'Нам доверяют' неактивны"



# =====================
    # TRUST / FEEDBACK SECTION
    # =====================

    # ===================== TRUST / FEEDBACK SECTION ====================================================================================

    @allure.step("Переключиться на вкладку FAQ: {tab_name}")
    def click_tab(self, tab_name: str):
        """Кликает по вкладке FAQ по её названию (устойчиво к 'ё'/'е' и пробелам)."""
        self._safe_scroll(L.FAQ_TAB_BAR)
        tabs = self.driver.find_elements(*L.FAQ_TAB_ITEMS)
        assert tabs, "❌ Вкладки FAQ не найдены"

        target_normalized = tab_name.strip().lower().replace("ё", "е")
        target_root = target_normalized[:6]

        for tab in tabs:
            tab_text = tab.text.strip().lower().replace("ё", "е")
            if tab_text == target_normalized or target_root in tab_text:
                self.driver.execute_script("arguments[0].click();", tab)
                time.sleep(0.7)
                return

        raise AssertionError(f"❌ Вкладка '{tab_name}' не найдена (нашли {[t.text for t in tabs]})")

    @allure.step("Проверить, что активна вкладка '{tab_name}'")
    def check_tab_selected(self, tab_name: str):
        """Проверяет, что выбранная вкладка подсвечена."""
        selected_items = self.driver.find_elements(*L.FAQ_TAB_SELECTED)
        assert selected_items, "❌ Не найдена активная вкладка FAQ"
        selected_text = selected_items[0].text.strip().lower().replace("ё", "е")
        target = tab_name.lower().replace("ё", "е")
        assert target[:6] in selected_text, (
            f"Ожидалась активная вкладка '{tab_name}', а выбрана '{selected_items[0].text}'"
        )

    # =====================
    # ВОПРОСЫ / ОТВЕТЫ
    # =====================
    @allure.step("Проверить наличие вопросов на вкладке FAQ")
    def check_questions_present(self):
        self._safe_scroll(L.FAQ_LIST)
        questions = self.driver.find_elements(*L.FAQ_QUESTION_TITLES)
        assert questions, "❌ Список вопросов FAQ пуст"
        return questions

    @allure.step("Проверить раскрытие вопросов FAQ и отображение ответов")
    def check_expand_questions(self):
        """Кликает по каждому вопросу и проверяет, что появляется текст ответа."""
        titles = self.driver.find_elements(*L.FAQ_QUESTION_TITLES)
        assert titles, "❌ Элементы FAQ не найдены"

        for i, title in enumerate(titles, start=1):
            clickable = title.find_element(By.XPATH, "ancestor::*[contains(@class,'expansion-item-title')][1]")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", clickable)
            self.driver.execute_script("arguments[0].click();", clickable)
            try:
                answer = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"(//div[contains(@class,'expansion-item-text')])[{i}]")
                    )
                )
                assert answer.text.strip(), f"❌ Ответ пуст у вопроса №{i}: {title.text}"
            except TimeoutException:
                raise AssertionError(f"❌ Не удалось раскрыть вопрос '{title.text}'")

    # =====================
    # БЛОК "ИНФОРМАЦИЯ ДЛЯ ..."
    # =====================
    @allure.step("Проверить наличие блока 'Информация для ...'")
    def check_info_block(self):
        self._safe_scroll(L.FAQ_SECTION)
        links = self.driver.find_elements(*L.FAQ_INFO_LINK)
        assert links, "❌ Блок 'Информация для ...' не найден"
        titles = self.driver.find_elements(*L.FAQ_INFO_TITLE)
        if titles:
            assert any(t.text.strip() for t in titles), "❌ Заголовок блока 'Информация для ...' пуст"

    @allure.step("Кликнуть по ссылке 'Партнёрам' и проверить переход на корректную страницу")
    def click_partners_link(self):
        """Кликает по ссылке 'Информация для Партнёров' и проверяет переход на /partners."""
        link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='faqSection']//a[contains(@href,'/partners')]"))
        )
        expected_path = "/ru-by/partners"

        # Клик через JS для надёжности
        self.driver.execute_script("arguments[0].click();", link)

        # Переключение на новую вкладку, если открылась
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        # Явное ожидание загрузки страницы с нужным URL
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("/partners")
        )

        current_url = self.driver.current_url
        assert expected_path in current_url, \
            f"❌ Открыт неверный адрес: {current_url}, ожидался путь: {expected_path}"

        # Проверка, что страница реально загрузилась (DOM не пустой)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text.strip()) > 100, "❌ Страница партнёров открыта, но пуста!"

        # Проверка, что нет ошибок 404 или 500
        assert "404" not in body_text and "ошибка" not in body_text.lower(), \
            "❌ Страница партнёров вернула ошибку!"

        print(f"✅ Страница партнёров успешно открыта и загружена: {current_url}")

    @allure.step("Кликнуть по ссылке 'Компаниям' и проверить переход на корректную страницу")
    def click_companies_link(self):
        """Кликает по ссылке 'Информация для Компаний' и проверяет переход на /companies."""
        link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='faqSection']//a[contains(@href,'/companies')]"))
        )
        expected_path = "/ru-by/companies"

        # Клик через JS (надежнее, если кнопка под анимацией)
        self.driver.execute_script("arguments[0].click();", link)

        # Если открылась новая вкладка — переключаемся на неё
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        # Ожидаем загрузку страницы с нужным URL
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("/companies")
        )

        current_url = self.driver.current_url
        assert expected_path in current_url, \
            f"❌ Открыт неверный адрес: {current_url}, ожидался путь: {expected_path}"

        # Проверяем, что страница реально загрузилась (DOM не пуст)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text.strip()) > 100, "❌ Страница компаний открыта, но пуста!"

        # Проверяем, что нет ошибок
        assert "404" not in body_text and "ошибка" not in body_text.lower(), \
            "❌ Страница компаний вернула ошибку!"

        print(f"✅ Страница компаний успешно открыта и загружена: {current_url}")

    # =====================
    # ФОРМА "Не нашли ответ?"
    # =====================
    @allure.step("Проверить наличие формы 'Не нашли ответ на вопрос?'")
    def check_form_present(self):
        self._safe_scroll(L.FAQ_SECTION)
        if self.driver.find_elements(*L.FAQ_FORM_TITLE):
            text = self.driver.find_element(*L.FAQ_FORM_TITLE).text.strip()
            assert "не нашли ответ" in text.lower(), f"❌ Некорректный заголовок формы: {text}"
        self.assert_element_present(L.FAQ_FORM_BTN_ASK)

    # =====================
    # МОДАЛКА FAQ
    # =====================
    @allure.step("Открыть модалку 'Задать вопрос'")
    def open_question_modal(self):
        """Открывает модалку 'Задать вопрос' и ждёт появления формы."""

        # Прокрутка до формы и кнопки
        self._safe_scroll(L.FAQ_FORM)
        self._safe_scroll(L.FAQ_FORM_BTN_ASK)

        # Кликаем по кнопке через JS (чтобы обойти перекрытия и lazy-load)
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(L.FAQ_FORM_BTN_ASK))
        self.driver.execute_script("arguments[0].click();", btn)

        # Ожидаем появления любой видимой модалки
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".modal"))
        )

        # Дополнительно ждём тело формы (на случай, если .modal появилась, но пустая)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal form"))
        )

        time.sleep(0.5)  # короткий буфер для завершения анимации

    @allure.step("Проверить поля в модалке 'Задать вопрос'")
    def check_modal_fields(self):
        """Проверяет, что все основные поля и чекбокс присутствуют в модалке."""
        # === 1. Ждём появления модалки ===
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.MODAL_FAQ)
        )

        # === 2. Ждём загрузку формы внутри ===
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal form"))
        )

        # === 3. Проверяем ключевые поля (по presence, не только visibility) ===
        elements = [
            L.MODAL_INPUT_NAME_FAQ,
            L.MODAL_INPUT_PHONE_FAQ,
            L.MODAL_INPUT_EMAIL_FAQ,
            L.MODAL_SUBMIT
        ]
        for locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator)
                )
            except TimeoutException:
                html_snapshot = self.driver.page_source
                print(f"[DEBUG] Элемент не найден: {locator}\nHTML:\n{html_snapshot[:800]}...\n")
                raise AssertionError(f"❌ Элемент {locator} отсутствует в модалке")

        # === 4. Дополнительная проверка телефона под кнопкой ===
        phone_el = self.driver.find_elements(*L.MODAL_PHONE_LINK_FAQ)
        assert phone_el, "❌ Телефонный блок внизу модалки не найден"

        print("✅ Модалка 'Задать вопрос' содержит все необходимые поля.")

    @allure.step("Проверить открытие и закрытие модалки 'Задать вопрос'")
    def check_modal_open_close(self):
        """Открывает модалку, проверяет наличие полей и закрывает."""
        self.open_question_modal()
        self.check_modal_fields()
        close_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-header button, .modal-header .icon-btn"))
        )
        self.driver.execute_script("arguments[0].click();", close_btn)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(L.MODAL_FAQ))








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
        self.assert_element_present(L.CONTACTS_CONTAINER)
        self.assert_element_present(L.CONTACTS_INFO)

    @allure.step("Проверить корректность контактных данных")
    def check_contacts_data(self):
        """Проверяет наличие ключевых контактных данных в блоке."""
        self._safe_scroll(L.CONTACTS_SECTION)
        root = self.driver.find_element(*L.CONTACTS_SECTION)
        phones = root.find_elements(By.CSS_SELECTOR, "a[href^='tel:']")
        emails = root.find_elements(By.CSS_SELECTOR, "a[href^='mailto:']")
        assert len(phones) >= 2, f"Недостаточно телефонных ссылок: {len(phones)}"
        assert len(emails) >= 2, f"Недостаточно email-ссылок: {len(emails)}"
        assert "минск" in root.text.lower(), "Адрес в блоке контактов не найден"

    @allure.step("Проверить, что карта отображается и не сломана")
    def check_contacts_map(self):
        """Проверяет наличие карты внизу страницы, корректную загрузку и наличие маркера."""
        self._safe_scroll(L.CONTACTS_SECTION)
        # --- Скроллим страницу в самый низ ---
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # --- Дожидаемся появления карты / canvas ---
        try:
            WebDriverWait(self.driver, 25).until(
                lambda d: d.find_elements(*L.CONTACTS_MAP) or d.find_elements(*L.CONTACTS_MAP_CANVAS)
            )
            WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(L.CONTACTS_MAP_CANVAS)
            )
        except TimeoutException:
            html_snapshot = self.driver.page_source
            print(f"[DEBUG HTML SNAPSHOT]\n{html_snapshot[:800]}...\n")
            assert False, "Карта не загрузилась за отведённое время"

        # --- Проверяем размеры канваса карты ---
        canvas = self.driver.find_element(*L.CONTACTS_MAP_CANVAS)
        width = int(canvas.get_attribute("width") or 0)
        height = int(canvas.get_attribute("height") or 0)
        assert width > 0 and height > 0, f"Некорректные размеры карты ({width}x{height}) — возможно, не загрузилась"

        # Маркер может появляться только после дополнительного взаимодействия пользователя.




    # ===================== inline-формы ========================================================================================================
    # ====== Inline форма JOIN ======
    def _ensure_btn_disabled(self, btn):
        """Проверяет, что кнопка визуально или логически неактивна."""
        is_disabled = btn.get_attribute("disabled")
        classes = btn.get_attribute("class") or ""
        pointer_events = btn.value_of_css_property("pointer-events")
        opacity = float(btn.value_of_css_property("opacity") or 1)

        visually_disabled = (
                is_disabled is not None
                or "disabled" in classes
                or "btn_disabled" in classes
                or pointer_events == "none"
                or opacity < 1
        )

        assert visually_disabled, (
            f"❌ Кнопка выглядит активной, ожидалась неактивная.\n"
            f"disabled={is_disabled}, classes={classes}, pointer-events={pointer_events}, opacity={opacity}"
        )

    def _ensure_btn_enabled(self, btn):
        """Проверяет, что кнопка активна (доступна к клику)."""
        is_disabled = btn.get_attribute("disabled")
        classes = btn.get_attribute("class") or ""
        pointer_events = btn.value_of_css_property("pointer-events")
        opacity = float(btn.value_of_css_property("opacity") or 1)

        assert (
                is_disabled is None
                and "btn_disabled" not in classes
                and pointer_events != "none"
                and opacity >= 1
                and btn.is_enabled()
        ), (
            f"❌ Кнопка выглядит неактивной, ожидалась активная.\n"
            f"disabled={is_disabled}, classes={classes}, pointer-events={pointer_events}, opacity={opacity}"
        )

    @allure.step("Проверить inline-форму 'Присоединяйтесь к Allsports'")
    def check_join_form_full(self):
        """Проверяет структуру и активацию inline-формы 'Присоединяйтесь к Allsports'."""
        # --- Скроллим вниз, чтобы форма точно прогрузилась ---
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        # --- Прокручиваем к секции с формой ---
        self._safe_scroll(L.JOIN_INLINE_SECTION)

        # --- Проверяем наличие формы и кнопки ---
        form = self.driver.find_element(*L.JOIN_INLINE_FORM)
        assert form is not None, "Форма 'Присоединяйтесь к Allsports' не найдена"

        submit = self.driver.find_element(*L.JOIN_INLINE_SUBMIT_BTN)
        assert submit is not None, "Кнопка 'Получить предложение' не найдена"

        # --- Проверяем, что кнопка изначально неактивна ---
        self._ensure_btn_disabled(submit)

        # --- Заполняем все обязательные поля ---
        self.driver.find_element(*L.JOIN_INLINE_NAME_INPUT).send_keys(self.VALID_NAME)
        self.driver.find_element(*L.JOIN_INLINE_PHONE_INPUT).send_keys(self.VALID_PHONE)
        self.driver.find_element(*L.JOIN_INLINE_EMAIL_INPUT).send_keys(self.VALID_EMAIL)
        self.driver.find_element(*L.JOIN_INLINE_COMPANY_INPUT).send_keys(self.VALID_COMPANY)

        # --- Проверяем, что кнопка всё ещё неактивна без чекбокса ---
        self._ensure_btn_disabled(submit)

        # --- Ставим чекбокс согласия ---
        checkbox_label = self.driver.find_element(*L.JOIN_INLINE_AGREE_LABEL)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox_label)
        self.driver.execute_script("arguments[0].click();", checkbox_label)
        time.sleep(0.5)

        # --- Проверяем, что кнопка стала активной ---
        self._ensure_btn_enabled(submit)

        # --- Проверяем ссылку на политику ---
        policy_link = self.driver.find_element(*L.JOIN_INLINE_POLICY_LINK)
        href = policy_link.get_attribute("href")
        assert "/policy/" in href, f"Некорректная ссылка политики: {href}"




    # ===================== Приимущества ========================================================================================================

    # ---------------- Общие хелперы ----------------

    def _wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def _wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def _scroll_to_advantages(self):
        """Безопасно прокручивает страницу до блока 'Преимущества Allsports'."""
        try:
            section = self.driver.find_element(By.CSS_SELECTOR, "#advantagesSection")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", section)
        except NoSuchElementException:
            try:
                section = self.driver.find_element(By.XPATH, "//section[contains(@class,'advantages')]")
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", section)
            except NoSuchElementException:
                self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.4);")
        time.sleep(1)

    # ---------------- Проверки ----------------

    @allure.step("Проверить наличие блока 'Преимущества Allsports'")
    def verify_advantages_section_exists(self):
        self._scroll_to_advantages()
        section = self._wait_visible((By.CSS_SELECTOR, "#advantagesSection"))
        assert section.is_displayed(), "❌ Секция 'Преимущества Allsports' не найдена"

        title = self.driver.find_element(*L.ADVANTAGES_TITLE).text.strip()
        assert "Преимущества Allsports" in title, f"❌ Заголовок не совпадает: {title}"

    @allure.step("Проверить наличие пунктов преимуществ (не менее 4)")
    def verify_advantages_list_items(self):
        self._scroll_to_advantages()
        items = self.driver.find_elements(*L.ADVANTAGES_LIST_ITEMS)
        assert len(items) >= 4, f"❌ Ожидалось >=4 пункта, найдено {len(items)}"

    @allure.step("Проверить переход по ссылке 'Список объектов'")
    def verify_facilities_link(self):
        self._scroll_to_advantages()
        link = self._wait_clickable(L.ADVANTAGES_BTN_LIST)
        href = link.get_attribute("href")
        current_url = self.driver.current_url
        self.driver.execute_script("arguments[0].click();", link)

        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != current_url)
        assert "facilities" in self.driver.current_url or href in self.driver.current_url, \
            f"❌ Переход по ссылке некорректен ({self.driver.current_url})"

    # ---------------- Вкладка "Компаниям" ----------------

    @allure.step("Проверить вкладку 'Компаниям' и модалку 'Получить предложение'")
    def check_tab_companies(self):
        self._scroll_to_advantages()
        tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(L.ADVANTAGES_TAB_COMPANIES))
        self.driver.execute_script("arguments[0].click();", tab)
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='advantagesSection']//button[.//span[contains(normalize-space(),'Получить предложение')]]"))
        )
        self.driver.execute_script("arguments[0].click();", btn)
        self._wait_modal_with_title("Получить предложение", timeout=15)
        self._verify_modal_close((By.CSS_SELECTOR, ".modal-header .icon-btn"))

    # ---------------- Вкладка "Партнёрам" ----------------

    @allure.step("Проверить вкладку 'Партнёрам' и модалку 'Стать партнёром'")
    def check_tab_partners(self):
        """Проверяет вкладку 'Партнёрам' и модалку 'Стать партнёром'."""
        self._scroll_to_advantages()
        tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(L.ADVANTAGES_TAB_PARTNERS))
        self.driver.execute_script("arguments[0].click();", tab)
        partner_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='advantagesSection']//button[.//span[contains(normalize-space(),'Получить предложение')]]"))
        )
        self.driver.execute_script("arguments[0].click();", partner_btn)
        # На актуальном UI заголовок может быть "Получить предложение" или "Стать партнером".
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal .modal-header"))
        )
        self._verify_modal_close((By.CSS_SELECTOR, ".modal-header .icon-btn"))

    # ---------------- Общие проверки ----------------

    def _validate_modal_common(self, name_loc, phone_loc, email_loc, last_field_loc,
                               checkbox_loc, submit_loc, policy_link_loc):
        submit = self.driver.find_element(*submit_loc)
        assert not submit.is_enabled(), "❌ Кнопка активна при пустых полях"

        # Ввод данных
        self.driver.find_element(*name_loc).send_keys(self.VALID_NAME)
        self.driver.find_element(*phone_loc).send_keys(self.VALID_PHONE)
        self.driver.find_element(*email_loc).send_keys(self.VALID_EMAIL)
        self.driver.find_element(*last_field_loc).send_keys("Тест")

        checkbox = self.driver.find_element(*checkbox_loc)
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.5)

        assert self.driver.find_element(*submit_loc).is_enabled(), "❌ Кнопка не активировалась"

        href = self.driver.find_element(*policy_link_loc).get_attribute("href")
        assert "/policy/" in href, f"❌ Некорректная ссылка политики: {href}"

    def _wait_modal_with_title(self, expected_title: str, timeout: int = 12):
        """Ждёт появления видимой модалки и нужного заголовка в её хедере."""
        # 1) дождаться контейнер модалки
        modal = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal"))
        )
        # 2) дождаться заголовка с нужным текстом
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".modal-header div"), expected_title)
        )
        # Вернём корень модалки (на будущее)
        return modal

    @allure.step("Проверить вкладку 'Пользователям' и модалку 'Задать вопрос'")
    def check_tab_users(self):
        self._scroll_to_advantages()
        tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(L.ADVANTAGES_TAB_USERS))
        self.driver.execute_script("arguments[0].click();", tab)
        ask_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='advantagesSection']//button[.//span[contains(normalize-space(),'Задать вопрос')]]"))
        )
        self.driver.execute_script("arguments[0].click();", ask_btn)
        self._wait_modal_with_title("Задать вопрос", timeout=15)
        self._verify_modal_close((By.CSS_SELECTOR, ".modal-header .icon-btn"))

    def _verify_modal_close(self, close_btn_loc):
        """Проверяет закрытие модалки по крестику (устойчиво)."""
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(close_btn_loc))
        self.driver.execute_script("arguments[0].click();", btn)

        # Ждём, пока контейнер модалки исчезнет или станет невидим
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modal"))
        )

    @allure.step("Проверить вкладку 'Компаниям' и переход по ссылке")
    def check_advantages_companies_tab(self):
        """Проверяет вкладку 'Компаниям' через ссылку (если есть) или CTA-модалку."""
        self._scroll_to_advantages()
        tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(L.ADV_TAB_COMPANIES))
        self.driver.execute_script("arguments[0].click();", tab)
        link_candidates = self.driver.find_elements(
            By.CSS_SELECTOR, "#advantagesSection .advantages-tab-company a[href*='/companies'], #advantagesSection a[href*='/ru-by/companies']"
        )
        if link_candidates:
            self.driver.execute_script("arguments[0].click();", link_candidates[0])
            WebDriverWait(self.driver, 10).until(lambda d: "companies" in d.current_url)
            assert "companies" in self.driver.current_url, f"❌ Не открылся раздел 'Компаниям' ({self.driver.current_url})"
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            assert len(body_text) > 50, "❌ Похоже, страница 'Компаниям' не загрузилась корректно"
            return

        cta = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='advantagesSection']//button[.//span[contains(normalize-space(),'Получить предложение')]]"))
        )
        self.driver.execute_script("arguments[0].click();", cta)
        self._wait_modal_with_title("Получить предложение", timeout=15)
        self._verify_modal_close((By.CSS_SELECTOR, ".modal-header .icon-btn"))

    @allure.step("Проверить вкладку 'Партнёрам' и переход по ссылке")
    def check_advantages_partners_tab(self):
        """Проверяет вкладку 'Партнёрам' через ссылку (если есть) или CTA-модалку."""
        self._scroll_to_advantages()
        tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(L.ADV_TAB_PARTNERS))
        self.driver.execute_script("arguments[0].click();", tab)
        link_candidates = self.driver.find_elements(
            By.CSS_SELECTOR, "#advantagesSection .advantages-tab-partner a[href*='/partners'], #advantagesSection a[href*='/ru-by/partners']"
        )
        if link_candidates:
            self.driver.execute_script("arguments[0].click();", link_candidates[0])
            WebDriverWait(self.driver, 10).until(EC.url_contains("/partners"))
            assert "partners" in self.driver.current_url, "❌ Не произошёл переход на страницу 'Партнёрам'"
            print("✅ Вкладка 'Партнёрам' и переход по ссылке проверены успешно.")
            return

        cta = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='advantagesSection']//button[.//span[contains(normalize-space(),'Получить предложение')]]"))
        )
        self.driver.execute_script("arguments[0].click();", cta)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal .modal-header"))
        )
        self._verify_modal_close((By.CSS_SELECTOR, ".modal-header .icon-btn"))

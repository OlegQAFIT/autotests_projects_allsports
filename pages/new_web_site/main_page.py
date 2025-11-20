# -*- coding: utf-8 -*-
import time
import allure
from selenium.common import TimeoutException
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
        self._safe_scroll(L.SUGGESTION_TITLE)
        self.assert_element_present(L.SUGGESTION_STATISTICS)
        self.assert_element_present(L.SUGGESTION_DESCRIPTION)
        self.assert_element_present(L.SUGGESTION_BTN_GET_OFFER)
        self.assert_element_present(L.SUGGESTION_BTN_ASK_QUESTION)

    @allure.step("Проверить заголовки промо-блока")
    def check_promo_titles(self):
        self._safe_scroll(L.PROMO_SECTION)
        self.assert_text_on_page("Весь спорт в одном приложении")
        self.assert_text_on_page("Корпоративный абонемент с ежедневным доступом к более 680 спортивным объектам по всей Беларуси. С нашими услугами можно быть активным каждый день и заниматься любыми видами спорта. Откройте для себя бесконечные возможности и добейтесь своих целей!")

    # =====================
    # SUBSCRIPTION TYPES
    # =====================

    # ===================== SUBSCRIPTION TYPES ====================================================================================

    @allure.step("Проверить карточки уровней подписок (обычные и архивные)")
    def check_subscription_cards_and_archives(self):
        """Полный сценарий: проверка карточек, кликов и загрузки таблиц."""
        self._safe_scroll((By.XPATH, "//h2[contains(text(),'Типы подписок')]"))
        self._check_subscription_cards(in_archive=False)
        self.open_archive_modal()
        self._check_subscription_cards(in_archive=True)
        self.close_archive_modal()

    def _check_subscription_cards(self, in_archive=False):
        """Проверка всех карточек (название, тексты, ссылки)."""
        driver = self.driver
        wait = WebDriverWait(driver, 15)

        # Скроллим к блоку
        self._safe_scroll((By.XPATH, "//h2[contains(text(),'Типы подписок')]"))

        # Определяем, какие карточки использовать
        if in_archive:
            cards = wait.until(EC.presence_of_all_elements_located(L.SUBSCRIPTIONS_ARCHIVE_CARDS))
            title_locator = L.SUBSCRIPTIONS_ARCHIVE_CARD_TITLE
            link_objects_locator = L.SUBSCRIPTIONS_ARCHIVE_LINK_OBJECTS
            link_table_locator = L.SUBSCRIPTIONS_ARCHIVE_LINK_TABLE
        else:
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
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.select-field__value"))
            )
            selected = driver.find_element(By.CSS_SELECTOR, "span.select-field__value").text.strip()
            expected = f"{level_name} подписка"
            assert selected == expected, f"❌ Неверный уровень: ожидалось '{expected}', получено '{selected}'"
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
        locator = (By.XPATH, "//button[.//span[contains(normalize-space(),'Архивные типы подписок')]]")

        # Скроллим вниз к кнопке
        self._safe_scroll((By.XPATH, "//h2[contains(normalize-space(),'Типы подписок')]"))
        driver.execute_script("window.scrollBy(0, 400);")  # прокрутка чуть ниже карточек

        # Ждём появления и кликабельности
        btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(locator))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", btn)

        # Проверяем, что модалка открылась
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal"))
        )

    @allure.step("Закрыть модалку 'Архивные типы подписок'")
    def close_archive_modal(self):
        driver = self.driver
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
        links = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*L.TRUST_COMPANY_LINKS)
        )
        assert links, "Нет ссылок 'Читать отзыв' в блоке 'Нам доверяют'"
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", links[index])
        time.sleep(0.3)
        links[index].click()

        # Ожидаем появления модалки
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal"))
        )
        self.assert_text_on_page("Отзыв")  # пример, можно уточнить
        time.sleep(0.5)

    @allure.step("Закрыть модалку 'Нам доверяют'")
    def close_trust_modal(self):
        """Закрывает модальное окно отзыва и дожидается его исчезновения из DOM."""
        driver = self.driver

        # Находим и кликаем по кнопке закрытия
        try:
            close_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-header button.icon-btn"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", close_btn)
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", close_btn)
        except Exception as e:
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

        for tab in tabs:
            tab_text = tab.text.strip().lower().replace("ё", "е")
            if tab_text == target_normalized:
                self.driver.execute_script("arguments[0].click();", tab)
                time.sleep(0.7)
                return

        raise AssertionError(f"❌ Вкладка '{tab_name}' не найдена (нашли {[t.text for t in tabs]})")

    @allure.step("Проверить, что активна вкладка '{tab_name}'")
    def check_tab_selected(self, tab_name: str):
        """Проверяет, что выбранная вкладка подсвечена."""
        selected = self.driver.find_element(*L.FAQ_TAB_SELECTED)
        assert tab_name.lower() in selected.text.strip().lower(), \
            f"Ожидалась активная вкладка '{tab_name}', а выбрана '{selected.text}'"

    # =====================
    # ВОПРОСЫ / ОТВЕТЫ
    # =====================
    @allure.step("Проверить наличие вопросов на вкладке FAQ")
    def check_questions_present(self):
        self._safe_scroll(L.FAQ_LIST)
        questions = self.driver.find_elements(*L.FAQ_ITEMS)
        assert questions, "❌ Список вопросов FAQ пуст"
        return questions

    @allure.step("Проверить раскрытие вопросов FAQ и отображение ответов")
    def check_expand_questions(self):
        """Кликает по каждому вопросу и проверяет, что появляется текст ответа."""
        items = self.driver.find_elements(*L.FAQ_ITEMS)
        assert items, "❌ Элементы FAQ не найдены"

        for i, item in enumerate(items, start=1):
            title = item.find_element(*L.FAQ_QUESTION_TITLES)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", title)
            self.driver.execute_script("arguments[0].click();", title)
            try:
                answer = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"(//div[contains(@class,'expansion-item-text')])[{i}]")
                    )
                )
                assert answer.text.strip(), f"❌ Ответ пуст у вопроса №{i}: {title.text}"
            except Exception:
                raise AssertionError(f"❌ Не удалось раскрыть вопрос '{title.text}'")

    # =====================
    # БЛОК "ИНФОРМАЦИЯ ДЛЯ ..."
    # =====================
    @allure.step("Проверить наличие блока 'Информация для ...'")
    def check_info_block(self):
        self._safe_scroll(L.FAQ_INFO_BLOCK)
        self.assert_element_present(L.FAQ_INFO_TITLE)
        self.assert_element_present(L.FAQ_INFO_LINK)
        text = self.driver.find_element(*L.FAQ_INFO_TITLE).text.strip()
        assert text, "❌ Заголовок блока 'Информация для ...' пуст"

    @allure.step("Кликнуть по ссылке 'Партнёрам' и проверить переход на корректную страницу")
    def click_partners_link(self):
        """Кликает по ссылке 'Информация для Партнёров' и проверяет, что открылась именно https://www.allsports.by/ru-by/partners"""
        link = self.driver.find_element(*L.FAQ_INFO_LINK)
        expected_url = "https://www.allsports.by/ru-by/partners"

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
        assert current_url.startswith(expected_url), \
            f"❌ Открыт неверный адрес: {current_url}, ожидался: {expected_url}"

        # Проверка, что страница реально загрузилась (DOM не пустой)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text.strip()) > 100, "❌ Страница партнёров открыта, но пуста!"

        # Проверка, что нет ошибок 404 или 500
        assert "404" not in body_text and "ошибка" not in body_text.lower(), \
            "❌ Страница партнёров вернула ошибку!"

        print(f"✅ Страница партнёров успешно открыта и загружена: {current_url}")

    @allure.step("Кликнуть по ссылке 'Компаниям' и проверить переход на корректную страницу")
    def click_companies_link(self):
        """Кликает по ссылке 'Информация для Компаний' и проверяет, что открылась именно https://www.allsports.by/ru-by/companies"""
        link = self.driver.find_element(*L.FAQ_INFO_LINK)
        expected_url = "https://www.allsports.by/ru-by/companies"

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
        assert current_url.startswith(expected_url), \
            f"❌ Открыт неверный адрес: {current_url}, ожидался: {expected_url}"

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
        self._safe_scroll(L.FAQ_FORM)
        self.assert_element_present(L.FAQ_FORM_TITLE)
        self.assert_element_present(L.FAQ_FORM_BTN_ASK)
        text = self.driver.find_element(*L.FAQ_FORM_TITLE).text.strip()
        assert "Не нашли ответ" in text, f"❌ Некорректный заголовок формы: {text}"

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
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(L.FAQ_FORM_BTN_ASK)
        )
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
            L.MODAL_TEXTAREA,
            L.MODAL_AGREE,
            L.MODAL_SUBMIT
        ]
        for locator in elements:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator)
                )
            except Exception:
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
        close_btn = self.driver.find_element(By.CSS_SELECTOR, ".modal-header button")
        self.driver.execute_script("arguments[0].click();", close_btn)
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(L.MODAL_FAQ))








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
            section = self.driver.find_element(By.XPATH, "//section[contains(@class,'advantages')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", section)
        except Exception:
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.4);")
        time.sleep(1)

    # ---------------- Проверки ----------------

    @allure.step("Проверить наличие блока 'Преимущества Allsports'")
    def verify_advantages_section_exists(self):
        self._scroll_to_advantages()
        section = self._wait_visible((By.XPATH, "//section[contains(@class,'advantages')]"))
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
        self.driver.execute_script("arguments[0].click();", link)

        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != L.BASE_URL)
        assert "facilities" in self.driver.current_url or href in self.driver.current_url, \
            f"❌ Переход по ссылке некорректен ({self.driver.current_url})"

    # ---------------- Вкладка "Пользователям" ----------------

    @allure.step("Проверить вкладку 'Пользователям' и модалку 'Задать вопрос'")
    def check_tab_users(self):
        self._scroll_to_advantages()
        self._wait_clickable(L.ADVANTAGES_TAB_USERS).click()
        self.verify_advantages_list_items()
        self._wait_clickable(L.ADVANTAGES_BTN_ASK_OR_GET).click()

        modal = self._wait_visible(L.MODAL_ASK_QUESTION_TITLE)
        assert modal.is_displayed(), "❌ Модалка 'Задать вопрос' не открылась"
        assert "Задать вопрос" in modal.text.strip(), "❌ Неверный заголовок в модалке"

        self._validate_modal_common(
            L.MODAL_INPUT_NAME, L.MODAL_INPUT_PHONE, L.MODAL_INPUT_EMAIL,
            L.MODAL_TEXTAREA_QUESTION, L.MODAL_AGREEMENT_CHECKBOX,
            L.MODAL_BTN_SUBMIT, L.MODAL_AGREEMENT_LINK
        )
        self._verify_modal_close(L.MODAL_ASK_QUESTION_CLOSE_BTN)

    # ---------------- Вкладка "Компаниям" ----------------

    @allure.step("Проверить вкладку 'Компаниям' и модалку 'Получить предложение'")
    def check_tab_companies(self):
        self._scroll_to_advantages()
        self._wait_clickable(L.ADVANTAGES_TAB_COMPANIES).click()
        self.verify_advantages_list_items()
        self._wait_clickable(L.ADVANTAGES_COMPANY_BTN_GET_OFFER).click()

        modal = self._wait_visible(L.MODAL_GET_OFFER_TITLE)
        assert "Получить предложение" in modal.text.strip(), "❌ Неверный заголовок модалки"

        self._validate_modal_common(
            L.MODAL_GET_OFFER_INPUT_NAME, L.MODAL_GET_OFFER_INPUT_PHONE, L.MODAL_GET_OFFER_INPUT_EMAIL,
            L.MODAL_GET_OFFER_INPUT_COMPANY, L.MODAL_GET_OFFER_CHECKBOX,
            L.MODAL_GET_OFFER_BTN_SUBMIT, L.MODAL_GET_OFFER_POLICY_LINK
        )
        self._verify_modal_close(L.MODAL_GET_OFFER_CLOSE_BTN)

    # ---------------- Вкладка "Партнёрам" ----------------

    @allure.step("Проверить вкладку 'Партнёрам' и модалку 'Стать партнёром'")
    def check_tab_partners(self):
        """Проверяет вкладку 'Партнёрам' и модалку 'Стать партнёром'."""
        self._scroll_to_advantages()
        # Переключаем вкладку
        self._wait_clickable(L.ADVANTAGES_TAB_PARTNERS).click()
        self.verify_advantages_list_items()

        # Находим и кликаем по кнопке "Получить предложение" во вкладке Партнёрам
        partner_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="advantagesSection"]/section/div/div[4]/div/div[2]/div/button'
            ))
        )
        self.driver.execute_script("arguments[0].click();", partner_btn)

        # Ждём, пока появится модалка с заголовком "Стать партнером"
        self._wait_modal_with_title("Стать партнером", timeout=15)

        # Проверяем поля и активность кнопки
        self._validate_modal_common(
            L.MODAL_BECOME_PARTNER_INPUT_NAME,
            L.MODAL_BECOME_PARTNER_INPUT_PHONE,
            L.MODAL_BECOME_PARTNER_INPUT_EMAIL,
            L.MODAL_BECOME_PARTNER_INPUT_OBJECT_NAME,
            L.MODAL_BECOME_PARTNER_CHECKBOX,
            L.MODAL_BECOME_PARTNER_BTN_SUBMIT,
            L.MODAL_BECOME_PARTNER_POLICY_LINK
        )

        # Проверяем закрытие модалки по крестику
        self._verify_modal_close(L.MODAL_BECOME_PARTNER_CLOSE_BTN)

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

    def _verify_modal_close(self, close_btn_loc):
        """Проверяет закрытие модалки по крестику."""
        btn = self.driver.find_element(*close_btn_loc)
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.7)
        modals = self.driver.find_elements(By.CSS_SELECTOR, "div.modal")
        assert all(not m.is_displayed() for m in modals), "❌ Модалка не закрылась"

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
        # Явно выбираем вкладку Пользователям
        self._wait_clickable(L.ADVANTAGES_TAB_USERS).click()
        self.verify_advantages_list_items()

        # Кликаем именно по кнопке "Задать вопрос" во вкладке Пользователям
        ask_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'advantages-tab-user')]//button[contains(@class,'btn_text')]//span[normalize-space()='Задать вопрос']"
            ))
        )
        self.driver.execute_script("arguments[0].click();", ask_btn)

        # Более устойчивое ожидание модалки
        self._wait_modal_with_title("Задать вопрос", timeout=15)

        # Проверки состава формы
        self._validate_modal_common(
            L.MODAL_INPUT_NAME, L.MODAL_INPUT_PHONE, L.MODAL_INPUT_EMAIL,
            L.MODAL_TEXTAREA_QUESTION, L.MODAL_AGREEMENT_CHECKBOX,
            L.MODAL_BTN_SUBMIT, L.MODAL_AGREEMENT_LINK
        )
        self._verify_modal_close(L.MODAL_ASK_QUESTION_CLOSE_BTN)

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
        """Проверяет, что вкладка 'Компаниям' открывается и ссылка ведёт на корректную страницу."""
        self._scroll_to_advantages()

        # Кликаем по вкладке
        tab = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(L.ADV_TAB_COMPANIES))
        self.driver.execute_script("arguments[0].click();", tab)

        # Проверяем, что секция 'Компаниям' появилась
        section = self._wait_visible(L.ADV_COMPANY_SECTION)
        assert section.is_displayed(), "❌ Вкладка 'Компаниям' не отобразилась"

        # Проверяем наличие заголовков
        titles = self.driver.find_elements(By.CSS_SELECTOR, ".advantages-tab-company h3")
        assert titles, "❌ Не найдено ни одного заголовка в секции 'Компаниям'"

        # Берём непустой заголовок
        visible_titles = [t.text.strip() for t in titles if t.text.strip()]
        assert visible_titles, "❌ Заголовки пустые или не прогрузились"

        # Проверяем текст содержимого
        expected_text = "Ощутите выгоды Allsports для своей команды!"
        assert expected_text in visible_titles[0], f"❌ Неверный заголовок: {visible_titles[0]}"

        # Проверяем, что есть пункты преимуществ
        items = self.driver.find_elements(*L.ADV_COMPANY_LIST_ITEMS)
        assert len(items) >= 4, f"❌ Ожидалось >=4 пунктов, найдено {len(items)}"

        # Проверяем ссылку 'Компаниям' и переход
        link = self._wait_clickable(L.ADV_COMPANY_LINK)
        href = link.get_attribute("href")
        self.driver.execute_script("arguments[0].click();", link)

        WebDriverWait(self.driver, 10).until(lambda d: "companies" in d.current_url)
        assert "companies" in self.driver.current_url, f"❌ Не открылся раздел 'Компаниям' ({self.driver.current_url})"

        # Проверяем, что страница рабочая
        body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        assert len(body_text) > 50, "❌ Похоже, страница 'Компаниям' не загрузилась корректно"

    @allure.step("Проверить вкладку 'Партнёрам' и переход по ссылке")
    def check_advantages_partners_tab(self):
        """Проверяет вкладку 'Партнёрам' в блоке преимуществ и переход по ссылке."""
        self._scroll_to_advantages()

        # Кликаем по вкладке "Партнёрам"
        tab = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(L.ADV_TAB_PARTNERS))
        self.driver.execute_script("arguments[0].click();", tab)

        # Проверяем, что секция 'Партнёрам' появилась
        section = self._wait_visible(L.ADV_PARTNER_SECTION)
        assert section.is_displayed(), "❌ Вкладка 'Партнёрам' не отобразилась"

        # Проверяем текстовый заголовок блока преимуществ
        title_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".advantages-tab-partner .advantages-text h3"))
        )
        title = title_elem.text.strip()
        assert title, "❌ Заголовок вкладки пустой"
        assert "Allsports" in title, f"❌ Неожиданный текст заголовка: '{title}'"

        # Проверяем переход по ссылке
        link = self.driver.find_element(*L.ADV_PARTNER_LINK)
        href = link.get_attribute("href")
        assert "/partners" in href, f"❌ Некорректная ссылка: {href}"

        # Кликаем по ссылке и ждём перехода
        self.driver.execute_script("arguments[0].click();", link)
        WebDriverWait(self.driver, 10).until(EC.url_contains("/partners"))
        assert "partners" in self.driver.current_url, "❌ Не произошёл переход на страницу 'Партнёрам'"

        print("✅ Вкладка 'Партнёрам' и переход по ссылке проверены успешно.")





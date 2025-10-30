# -*- coding: utf-8 -*-
import datetime
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from helpers.base import BasePage
from locators.elements_for_new_web_site.for_levels_page import LevelsLocators as L


class LevelsPage(BasePage):
    """Полный набор методов для страницы /levels (по аналогии с CompaniesPage)."""

    # =====================
    # ОСНОВНЫЕ МЕТОДЫ
    # =====================
    @allure.step("Открыть страницу 'Типы подписок'")
    def open(self):
        """Открывает страницу уровней подписок и дожидается загрузки контента."""
        self.driver.get(L.BASE_URL)

        # Небольшая пауза, чтобы баннер успел отрисоваться
        time.sleep(2)

        # Сначала пытаемся закрыть cookie-модалку
        try:
            self.accept_cookie_consent()
        except Exception as e:
            print(f"[DEBUG] Cookie accept failed (можно игнорировать, если баннера нет): {e}")

        # Теперь ждём появления основного заголовка или контента страницы
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[self::h1 or self::h2][contains(.,'Типы подписок')]")
                )
            )
        except Exception:
            # на случай ленивой подгрузки — скролл и повторная проверка
            self.driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(1.5)
            WebDriverWait(self.driver, 15).until(
                lambda d: "Типы подписок" in d.page_source
            )

        print("[DEBUG] ✅ Страница 'Типы подписок' успешно открыта.")
        return self

    @allure.step("Принять cookies (если баннер есть)")
    def accept_cookie_consent(self):
        """Нажимает 'Принять' в cookie-баннере, если он отображается. Без создания скриншотов."""
        try:
            # Явно ждём до 5 сек появления кнопки 'Принять'
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cookie-primary-modal__confirm"))
            )
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new MouseEvent('click', {bubbles:true,cancelable:true,view:window}));", btn
            )
            time.sleep(1)
            print("[DEBUG] Cookie-модалка успешно закрыта.")
        except TimeoutException:
            print("[DEBUG] Cookie-баннер не найден — пропускаем.")
        except Exception as e:
            print(f"[DEBUG] Ошибка при попытке закрыть cookie-баннер: {e}")

    # =====================
    # ПОДПИСКИ / УРОВНИ
    # =====================
    @allure.step("Проверить наличие блока 'Типы подписок'")
    def check_levels_section_present(self):
        """Проверяет, что блок 'Типы подписок' отображается на странице."""
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(L.LEVELS_SECTION)
        )
        element = self.driver.find_element(*L.LEVELS_SECTION)
        assert element.is_displayed(), "Блок 'Типы подписок' найден, но не отображается"
        print("[DEBUG] ✅ Найден блок 'Типы подписок'")

    def _safe_scroll(self, locator, offset=150):
        """
        Аккуратно скроллит к элементу, чтобы он оказался в центре экрана
        (и не перекрывался фиксированным хедером или баннером).
        """
        try:
            element = self.driver.find_element(*locator)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); window.scrollBy(0, -arguments[1]);",
                element,
                offset
            )
            time.sleep(0.5)
            print(f"[DEBUG] Прокрутка к элементу: {locator}")
        except Exception as e:
            print(f"[DEBUG] ⚠️ Не удалось проскроллить к элементу {locator}: {e}")


    @allure.step("Проверить наличие карточек подписок")
    def check_subscription_cards_present(self):
        self._safe_scroll(L.LEVELS_SECTION)
        cards = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(*L.SUBSCRIPTION_CARDS))
        assert cards, "❌ Карточки подписок не найдены"

    @allure.step("Проверить тексты карточек (ключевые слова)")
    def check_card_texts_regular(self):
        keywords = ["визит", "объект", "спорт", "приостан", "безлимит", "трениров", "секции"]
        cards = self.driver.find_elements(*L.SUBSCRIPTION_CARDS)
        for idx, card in enumerate(cards, start=1):
            text = (card.text or "").lower()
            assert any(k in text for k in keywords), f"❌ Нет ключевых слов в карточке {idx}: {text[:200]}"

    # === Переходы по ссылкам ===
    @allure.step("Проверить переходы по ссылкам карточек (основные)")
    def check_links_regular_cards(self):
        cards = self.driver.find_elements(*L.SUBSCRIPTION_CARDS)
        for idx, card in enumerate(cards[:2], start=1):
            title = card.find_element(*L.SUBSCRIPTION_CARD_TITLE).text
            with allure.step(f"Карточка {idx}: {title}"):
                self._check_objects_link(card, L.SUBSCRIPTION_LINK_OBJECTS, title)
                self._check_table_link(card, L.SUBSCRIPTION_LINK_TABLE, title)

    def _check_objects_link(self, card, locator, title):
        href = card.find_element(*locator).get_attribute("href")
        self.driver.execute_script("window.open(arguments[0]);", href)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.FACILITIES_SELECT_VALUE))
        selected = self.driver.find_element(*L.FACILITIES_SELECT_VALUE).text
        assert title.lower() in selected.lower() or "подписк" in selected.lower()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def _check_table_link(self, card, locator, title):
        href = card.find_element(*locator).get_attribute("href")
        self.driver.execute_script("window.open(arguments[0]);", href)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(L.FACILITIES_TABLE_ROWS))
        rows = self.driver.find_elements(*L.FACILITIES_TABLE_ROWS)
        assert len(rows) > 1, f"❌ Таблица пуста для {title}"
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    # === Модалка архивных уровней ===
    @allure.step("Открыть модалку 'Архивные типы подписок'")
    def open_archive_modal(self):
        self._safe_scroll(L.ARCHIVE_BTN)
        self.hard_click(L.ARCHIVE_BTN)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(L.ARCHIVE_MODAL))

    @allure.step("Закрыть модалку архивных подписок")
    def close_archive_modal(self):
        self.click_if_visible(L.ARCHIVE_CLOSE)
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(L.ARCHIVE_MODAL))

    @allure.step("Проверить карточки в архивной модалке")
    def check_card_texts_archive(self):
        cards = self.driver.find_elements(*L.SUBSCRIPTIONS_ARCHIVE_CARDS)
        for card in cards:
            text = card.text.lower()
            assert any(k in text for k in ["визит", "спорт", "объект"]), "❌ Текст не содержит ключевых слов"

    # =====================
    # INLINE-ФОРМА JOIN
    # =====================
    @allure.step("Проверить inline-форму 'Присоединяйтесь к Allsports'")
    def check_join_form_full(self):
        self._safe_scroll(L.JOIN_SECTION)
        form = self.driver.find_element(*L.JOIN_FORM)
        assert form, "❌ Форма не найдена"
        submit = self.driver.find_element(*L.JOIN_SUBMIT_BTN)
        assert not submit.is_enabled(), "❌ Кнопка активна при пустых полях"
        self.driver.find_element(*L.JOIN_NAME_INPUT).send_keys("QA Тест")
        self.driver.find_element(*L.JOIN_PHONE_INPUT).send_keys("+375 44 123 45 67")
        self.driver.find_element(*L.JOIN_EMAIL_INPUT).send_keys("qa@example.com")
        self.driver.find_element(*L.JOIN_COMPANY_INPUT).send_keys("ООО Автотест")
        assert not submit.is_enabled(), "❌ Кнопка активна без чекбокса"
        label = self.driver.find_element(*L.JOIN_AGREE_LABEL)
        self.driver.execute_script("arguments[0].click();", label)
        assert submit.is_enabled(), "❌ Кнопка не активировалась"
        policy = self.driver.find_element(*L.JOIN_POLICY_LINK)
        assert "/policy/" in policy.get_attribute("href")

    @allure.step("Проверить ошибки валидации телефона")
    def validate_join_phone_errors(self):
        """Проверяет, что при неверном вводе телефона отображается сообщение об ошибке или подсказка формата."""
        phone = self.driver.find_element(*L.JOIN_PHONE_INPUT)
        email_field = self.driver.find_element(*L.JOIN_EMAIL_INPUT)

        # --- Проверка ввода цифр (неполный номер)
        phone.clear()
        phone.send_keys("1234")
        email_field.click()
        time.sleep(0.6)

        # Ищем текст ошибки (span внутри div.input-error)
        err_text = ""
        try:
            err_text = self.driver.find_element(
                By.CSS_SELECTOR, "div.input-error span.input-error__text"
            ).text.strip()
        except Exception:
            pass

        # Ищем help-текст, если ошибка не появилась
        help_text = ""
        try:
            help_text = self.driver.find_element(
                By.CSS_SELECTOR, "p.input__help-text"
            ).text.strip()
        except Exception:
            pass

        combined = f"{err_text} {help_text}".lower()
        assert any(word in combined for word in ["неверный формат", "формат", "+375"]), (
            f"❌ Не найдено сообщение об ошибке или подсказка формата. Получено: '{combined}'"
        )

        # --- Проверка ввода текста (кириллица)
        phone.clear()
        phone.send_keys("привет")
        email_field.click()
        time.sleep(0.6)

        err_text2 = ""
        try:
            err_text2 = self.driver.find_element(
                By.CSS_SELECTOR, "div.input-error span.input-error__text"
            ).text.strip()
        except Exception:
            pass

        help_text2 = ""
        try:
            help_text2 = self.driver.find_element(
                By.CSS_SELECTOR, "p.input__help-text"
            ).text.strip()
        except Exception:
            pass

        combined2 = f"{err_text2} {help_text2}".lower()
        assert any(word in combined2 for word in ["неверный формат", "формат", "+375"]), (
            f"❌ Нет сообщения об ошибке при вводе текста. Получено: '{combined2}'"
        )

    @allure.step("Проверить ошибки валидации Email")
    def validate_join_email_errors(self):
        """Проверяет корректные ошибки валидации для поля email (запрещённые символы / недействительный адрес)."""
        email = self.driver.find_element(*L.JOIN_EMAIL_INPUT)

        # Точный локатор ошибки для поля email
        error_locator = (
            By.XPATH,
            "//label[contains(@class,'input')][.//input[@name='email']]//span[contains(@class,'input-error__text')]"
        )

        # === Проверка 1: 'привет' ===
        email.clear()
        email.send_keys("привет")
        # Снимаем фокус, чтобы валидация сработала
        self.driver.find_element(*L.JOIN_PHONE_INPUT).click()

        try:
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element(error_locator, "Поле содержит")
            )
        except Exception:
            # Если текст другой (например, “Неверный email”), не падаем, читаем актуальный текст
            pass

        err1 = ""
        try:
            err1 = self.driver.find_element(*error_locator).text.strip()
        except Exception:
            pass

        assert any(word in err1.lower() for word in [
            "запрещ", "поле содержит", "некоррект", "email", "действительн", "адрес"
        ]), f"Ожидалась ошибка про запрещённые символы, получили: '{err1}'"

        # --- Полное очищение input через JS ---
        self.driver.execute_script("arguments[0].value = '';", email)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            email
        )
        time.sleep(0.3)

        # === Проверка 2: 'qwert@@' ===
        email.send_keys("qwert@@")
        self.driver.find_element(*L.JOIN_PHONE_INPUT).click()

        try:
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element(error_locator, "Адрес")
            )
        except Exception:
            pass

        err2 = ""
        try:
            err2 = self.driver.find_element(*error_locator).text.strip()
        except Exception:
            pass

        assert any(word in err2.lower() for word in [
            "должен", "адрес", "email", "некоррект", "формат"
        ]), f"Ожидалась ошибка 'Адрес электронной почты должен быть действительным', получили: '{err2}'"

    @allure.step("Отправить inline-форму 'Присоединяйтесь к Allsports'")
    def submit_join_form(self):
        self._safe_scroll(L.JOIN_SECTION)
        self.driver.find_element(*L.JOIN_NAME_INPUT).send_keys("QA Автотест")
        self.driver.find_element(*L.JOIN_PHONE_INPUT).send_keys("+375 44 111 11 11")
        self.driver.find_element(*L.JOIN_EMAIL_INPUT).send_keys("qa@allsports.by")
        self.driver.find_element(*L.JOIN_COMPANY_INPUT).send_keys("Allsports QA")
        label = self.driver.find_element(*L.JOIN_AGREE_LABEL)
        self.driver.execute_script("arguments[0].click();", label)
        btn = self.driver.find_element(*L.JOIN_SUBMIT_BTN)
        self.driver.execute_script("arguments[0].click();", btn)
        success = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(L.SUCCESS_TEXT))
        assert "спасибо" in success.text.lower()

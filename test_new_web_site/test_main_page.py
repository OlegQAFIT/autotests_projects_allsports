# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site.main_page import MainPage


# ===================== PROMO BLOCK =====================
@allure.feature('Main Page')
@allure.severity('Critical')
@allure.story('Промо-блок — наличие элементов')
def test_promo_block_elements(driver):
    "Проверка наличия заголовков, изображений и кнопок промо-блока."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_promo_block()


@allure.feature('Main Page')
@allure.severity('Normal')
@allure.story('Промо-блок — корректность текстов')
def test_promo_titles(driver):
    "Проверка корректности заголовков промо-блока."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_promo_titles()


# ===================== Advantages Allsports  =====================



# ===================== SUBSCRIPTION TYPES ====================================================================================
@allure.feature("Main Page")
@allure.severity("Critical")
@allure.story("Типы подписок — проверка карточек и ссылок")
def test_subscription_cards_texts_and_links(driver):
    """Проверка карточек всех типов подписок (основные и архивные):
    - наличие карточек;
    - наличие текста (визиты, спортивные объекты, приостановка);
    - наличие ссылок 'Объекты подписки' и 'Список объектов (таблица)'.
    """
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Проверяем обычные карточки
    page._check_subscription_cards(in_archive=False)

    # Проверяем архивные карточки
    page.open_archive_modal()
    page._check_subscription_cards(in_archive=True)
    page.close_archive_modal()


@allure.feature("Main Page")
@allure.severity("Critical")
@allure.story("Типы подписок — переходы по ссылкам обычных карточек")
def test_subscription_links_regular_cards(driver):
    """Проверяет переходы по ссылкам обычных подписок:
    - 'Объекты подписки' открывает страницу с правильным уровнем (например, 'Region подписка');
    - 'Список объектов (таблица)' открывает таблицу, которая успешно загружается.
    """
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page._check_subscription_cards(in_archive=False)


@allure.feature("Main Page")
@allure.severity("Critical")
@allure.story("Типы подписок — переходы по ссылкам архивных карточек")
def test_subscription_links_archive_cards(driver):
    """Проверяет переходы по ссылкам в архивных карточках:
    - корректность выбранного уровня ('Lite подписка', 'Region подписка' и т.п.);
    - успешную загрузку таблицы объектов.
    """
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Открываем модалку архивных подписок
    page.open_archive_modal()

    # Проверяем переходы по ссылкам
    page._check_subscription_cards(in_archive=True)

    # Закрываем модалку
    page.close_archive_modal()


@allure.feature("Main Page")
@allure.severity("High")
@allure.story("Типы подписок — полный сценарий проверки блока")
def test_full_subscription_block_flow(driver):
    """Полный сценарий проверки блока 'Типы подписок':
    - карточки обычных и архивных уровней;
    - клики по обеим ссылкам;
    - корректный уровень и успешная загрузка таблицы.
    """
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_subscription_cards_and_archives()


@allure.feature("Main Page")
@allure.severity("Normal")
@allure.story("Типы подписок — стабильность загрузки таблиц")
def test_subscription_facilities_tables_load(driver):
    """Проверяет, что страницы 'Список объектов (таблица)' корректно подгружаются:
    - таблица видна;
    - есть хотя бы одна строка данных;
    - не возникает таймаутов загрузки.
    """
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Проверяем таблицы обычных карточек
    page._check_subscription_cards(in_archive=False)

    # Проверяем таблицы архивных карточек
    page.open_archive_modal()
    page._check_subscription_cards(in_archive=True)
    page.close_archive_modal()


@allure.feature("Main Page")
@allure.severity("Normal")
@allure.story("Типы подписок — проверка текстов в карточках")
def test_subscription_card_texts_valid(driver):
    """Проверяет, что в карточках содержатся корректные тексты:
    - упоминается 'визит';
    - есть 'спорт' или 'объект';
    - указано о 'приостановке' подписки.
    """
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Проверяем тексты карточек обычных подписок
    page._check_subscription_cards(in_archive=False)

    # Проверяем тексты карточек архивных подписок
    page.open_archive_modal()
    page._check_subscription_cards(in_archive=True)
    page.close_archive_modal()

    # ===================== TRUST / FEEDBACK SECTION ====================================================================================

# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.companies import CompaniesPage


@allure.feature("Main Page")
@allure.severity("Critical")
@allure.story("Нам доверяют — наличие секции и заголовка")
def test_trust_section_presence(driver):
    """Проверка наличия секции 'Нам доверяют' и заголовка."""
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_trust_section()


@allure.feature("Main Page")
@allure.severity("Normal")
@allure.story("Нам доверяют — тексты отзывов")
def test_trust_texts(driver):
    """Проверка текстов отзывов и количества карточек."""
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_trust_texts()


@allure.feature("Main Page")
@allure.severity("High")
@allure.story("Нам доверяют — открытие модалки отзыва")
def test_trust_modal_open(driver):
    """Проверка открытия и закрытия модалки отзыва."""
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_trust_modal(0)
    page.close_trust_modal()


@allure.feature("Main Page")
@allure.severity("Normal")
@allure.story("Нам доверяют — стрелки навигации")
def test_trust_slider_controls(driver):
    """Проверка наличия стрелок навигации в слайдере отзывов."""
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_trust_slider_controls()



    # ===================== FAQ ====================================================================================

# ===================== ОСНОВНОЙ ТЕСТ ПО ВКЛАДКАМ =====================
@allure.feature("Main Page")
@allure.severity("Critical")
@allure.story("FAQ — Проверка вкладок, вопросов, ответов и модалки")
@pytest.mark.parametrize("tab_name", ["Пользователям", "Партнерам", "Компаниям"])
def test_faq_full_flow_per_tab(driver, tab_name):
    """
    Проверяет:
    - Переключение вкладок
    - Наличие вопросов
    - Раскрытие ответов
    - Наличие формы "Не нашли ответ?"
    - Открытие модалки "Задать вопрос"
    """
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_tab(tab_name)
    page.check_tab_selected(tab_name)
    page.check_questions_present()
    page.check_expand_questions()
    page.check_form_present()
    page.open_question_modal()
    page.check_modal_fields()


# ===================== ИНФОРМАЦИЯ ДЛЯ ПАРТНЁРОВ =====================
@allure.feature("Main Page")
@allure.severity("High")
@allure.story("FAQ — Блок 'Информация для Партнёров'")
def test_faq_info_block_partners(driver):
    """Проверяет блок 'Информация для Партнёров' и переход по ссылке."""
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_tab("Партнёрам")
    page.check_info_block()
    page.click_partners_link()


# ===================== ИНФОРМАЦИЯ ДЛЯ КОМПАНИЙ =====================
@allure.feature("Main Page")
@allure.severity("High")
@allure.story("FAQ — Блок 'Информация для Компаний'")
def test_faq_info_block_companies(driver):
    """Проверяет блок 'Информация для Компаний' и переход по ссылке."""
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_tab("Компаниям")
    page.check_info_block()
    page.click_companies_link()


# ===================== МОДАЛКА — ПРОВЕРКА ОТКРЫТИЯ/ЗАКРЫТИЯ =====================
@allure.feature("Main Page")
@allure.severity("Critical")
@allure.story("FAQ — Модалка 'Задать вопрос' корректно открывается и закрывается")
def test_faq_modal_open_close(driver):
    """Проверяет, что модалка открывается, содержит все поля и корректно закрывается."""
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_tab("Пользователям")
    page.check_form_present()
    page.check_modal_open_close()



# ===================== VIDEO ==============================================================================================================================
@allure.feature('Main Page')
@allure.severity('Normal')
@allure.story('Видео — наличие iframe')
def test_video_iframe(driver):
    "Проверка наличия видео iframe на странице."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_iframe()


@allure.feature('Main Page')
@allure.severity('Low')
@allure.story('Видео — корректность источника YouTube')
def test_video_src(driver):
    "Проверка, что видео подгружается с YouTube."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_src()


@allure.feature('Main Page')
@allure.severity('Low')
@allure.story('Видео — атрибут allowfullscreen')
def test_video_allowfullscreen(driver):
    "Проверка, что iframe имеет атрибут allowfullscreen."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_allowfullscreen()


# ===================== CONTACTS =========================================================================================================
@allure.feature('Main Page')
@allure.severity('Critical')
@allure.story('Контакты — наличие блока')
def test_contacts_section_present(driver):
    "Проверка наличия блока контактов на странице."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_section_present()


@allure.feature('Main Page')
@allure.severity('High')
@allure.story('Контакты — корректность данных')
def test_contacts_data(driver):
    "Проверка корректности номеров телефонов, email и расписаний."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_data()


@allure.feature('Main Page')
@allure.severity('Normal')
@allure.story('Контакты — корректность работы карты')
def test_contacts_map(driver):
    "Проверка, что карта отображается и не сломана."
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_map()


# ===================== inline-формы =========================================================================================================
# Пользователям
@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка наличия блока 'Преимущества Allsports'")
def test_advantages_section_exists(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.verify_advantages_section_exists()

@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Пользователям' и модалки 'Задать вопрос'")
def test_advantages_users_modal(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_tab_users()

@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Компаниям' и модалки 'Получить предложение'")
def test_advantages_companies_modal(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_tab_companies()

@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Партнёрам' и модалки 'Стать партнёром'")
def test_advantages_partners_modal(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_tab_partners()

@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка перехода по ссылке 'Список объектов'")
def test_facilities_link(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.verify_facilities_link()

@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Компаниям' в блоке 'Преимущества Allsports'")
def test_advantages_companies_tab(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_advantages_companies_tab()

@allure.feature('Main Page')
@allure.severity('Normal')
@allure.title("Проверка вкладки 'Партнёрам' в блоке 'Преимущества Allsports'")
def test_advantages_partners_tab(driver):
    page = MainPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_advantages_partners_tab()

# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.companies import CompaniesPage


# ===================== PROMO BLOCK =====================
@allure.feature('Companies Page')
@allure.severity('Critical')
@allure.story('Промо-блок — наличие элементов')
def test_promo_block_elements(driver):
    "Проверка наличия заголовков, изображений и кнопок промо-блока."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_promo_block()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Промо-блок — корректность текстов')
def test_promo_titles(driver):
    "Проверка корректности заголовков промо-блока."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_promo_titles()


# ===================== BENEFITS =====================
@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Преимущества — наличие блока и заголовка')
def test_benefits_section_presence(driver):
    """Проверка наличия блока Преимущества и заголовка."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefit_section()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Преимущества — количество элементов')
def test_benefits_items_count(driver):
    """Проверка количества элементов преимуществ."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefit_items_count()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Преимущества — корректность текстов')
def test_benefits_texts(driver):
    "Проверка текстов преимуществ."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefit_texts()


@allure.feature('Companies Page')
@allure.severity('Low')
@allure.story('Преимущества — стрелки навигации')
def test_benefits_slider_controls(driver):
    "Проверка стрелок навигации блока Преимущества."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefit_slider_controls()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Преимущества — движение слайдера')
def test_benefits_slider_moves(driver):
    "Проверка работы слайдера Преимущества."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefit_slider_moves()


# ===================== COOPERATION =====================
@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Сотрудничество — наличие блока')
def test_cooperation_section(driver):
    "Проверка наличия блока Сотрудничество."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_section()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Сотрудничество — тексты шагов')
def test_cooperation_texts(driver):
    "Проверка текстов шагов сотрудничества."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_texts()


@allure.feature('Companies Page')
@allure.severity('Low')
@allure.story('Сотрудничество — стрелки навигации')
def test_cooperation_controls(driver):
    "Проверка стрелок блока Сотрудничество."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_controls()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Сотрудничество — движение слайдера')
def test_cooperation_slider_moves(driver):
    "Проверка работы слайдера Сотрудничество."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_slider_moves()


# ===================== FEEDBACK =====================
@allure.feature('Companies Page')
@allure.severity('Critical')
@allure.story('Отзывы — наличие блока')
def test_feedback_section_presence(driver):
    "Проверка наличия блока Отзывы."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_feedback_section()


# @allure.feature('Companies Page')
# @allure.severity('Normal')
# @allure.story('Отзывы — тексты отзывов')
# def test_feedback_texts(driver):
#     "Проверка текстов отзывов."
#     page = CompaniesPage(driver)
#     page.open()
#     page.accept_cookie_consent()
#     page.check_feedback_texts()


@allure.feature('Companies Page')
@allure.severity('High')
@allure.story('Отзывы — открытие модалки')
def test_feedback_modal_open(driver):
    "Проверка открытия модалки отзыва."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_feedback_modal(0)
    page.close_feedback_modal()


# ===================== FOOTER =====================
@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Футер — наличие блока и ссылок')
def test_footer_presence(driver):
    "Проверка наличия футера и ссылок в нём."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_footer_presence()


# ===================== EXTENDED CHECKS =====================
@allure.feature('Companies Page')
@allure.severity('Low')
@allure.story('SEO — структура заголовков (h1, h2, h3)')
def test_headings_structure(driver):
    "Проверка структуры заголовков страницы."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_headings_structure()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Адаптивность — проверка отображения на мобильных разрешениях')
def test_responsive_layout(driver):
    "Проверка адаптивности страницы при разных разрешениях."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_responsive_layout()


@allure.feature('Companies Page')
@allure.severity('Low')
@allure.story('Хедер — логотип кликабелен и ведёт на главную')
def test_header_logo_link(driver):
    "Проверка ссылки логотипа в шапке."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_header_logo_link()


@allure.feature('Companies Page')
@allure.severity('High')
@allure.story('JS — отсутствие ошибок в консоли браузера')
def test_no_js_errors(driver):
    "Проверка отсутствия JavaScript ошибок в консоли."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_no_console_errors()


@allure.feature('Companies Page')
@allure.severity('Low')
@allure.story('Изображения — наличие alt-текста у всех изображений')
def test_images_have_alt(driver):
    "Проверка, что у всех изображений задан alt-текст."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_images_have_alt()


# ===================== EXTENDED CHECKS =====================
@allure.feature("Companies Page")
@allure.severity("Normal")
@allure.story("FAQ — наличие блока и заголовка")
def test_faq_section_present(driver):
    "Проверка наличия блока FAQ на странице."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_section_present()


@allure.feature("Companies Page")
@allure.severity("Normal")
@allure.story("FAQ — корректность списка вопросов")
def test_faq_all_questions_present(driver):
    "Проверка, что все ожидаемые вопросы присутствуют."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_all_questions_present()


@allure.feature("Companies Page")
@allure.severity("Critical")
@allure.story("FAQ — раскрытие вопросов и отображение ответов")
def test_faq_expand_questions(driver):
    "Проверка работы аккордеонов FAQ: клики по вопросам раскрывают ответы."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_expansion_functionality()


@allure.feature("Companies Page")
@allure.severity("Low")
@allure.story("FAQ — блок 'Информация для Партнёров'")
def test_faq_partners_block(driver):
    "Проверка наличия и корректности ссылки для партнёров."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_partners_info_block()


@allure.feature("Companies Page")
@allure.severity("Normal")
@allure.story("FAQ — форма 'Не нашли ответ на вопрос'")
def test_faq_form_button(driver):
    "Проверка наличия и активности кнопки 'Задать вопрос'."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_form_button()


# ===================== VIDEO =====================
@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Видео — наличие iframe')
def test_video_iframe(driver):
    "Проверка наличия видео iframe на странице."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_iframe()


@allure.feature('Companies Page')
@allure.severity('Low')
@allure.story('Видео — корректность источника YouTube')
def test_video_src(driver):
    "Проверка, что видео подгружается с YouTube."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_src()


@allure.feature('Companies Page')
@allure.severity('Low')
@allure.story('Видео — атрибут allowfullscreen')
def test_video_allowfullscreen(driver):
    "Проверка, что iframe имеет атрибут allowfullscreen."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_allowfullscreen()


# ===================== CONTACTS =====================
@allure.feature('Companies Page')
@allure.severity('Critical')
@allure.story('Контакты — наличие блока')
def test_contacts_section_present(driver):
    "Проверка наличия блока контактов на странице."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_section_present()


@allure.feature('Companies Page')
@allure.severity('High')
@allure.story('Контакты — корректность данных')
def test_contacts_data(driver):
    "Проверка корректности номеров телефонов, email и расписаний."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_data()


@allure.feature('Companies Page')
@allure.severity('Normal')
@allure.story('Контакты — корректность работы карты')
def test_contacts_map(driver):
    "Проверка, что карта отображается и не сломана."
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_map()


# ===================== FORMS =====================
@allure.story("Открытие форм из хедера")
@allure.severity("Critical")
def test_open_header_offer_modal(driver):
    """Проверка открытия модалки 'Получить предложение' из хедера."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_header_offer_modal()
    page.check_modal_common("Получить предложение")


@allure.story("Открытие формы 'Задать вопрос' из хедера")
@allure.severity("Critical")
def test_open_header_question_modal(driver):
    """Проверка открытия модалки 'Задать вопрос' из хедера."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_header_question_modal()
    page.check_modal_common("Задать вопрос")


@allure.story("Открытие форм из промо-блока")
@allure.severity("Critical")
def test_open_promo_offer_modal(driver):
    """Проверка открытия модалки 'Получить предложение' из промо-блока."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.check_modal_common("Получить предложение")


@allure.story("Открытие формы 'Задать вопрос' из промо-блока")
@allure.severity("Critical")
def test_open_promo_question_modal(driver):
    """Проверка открытия модалки 'Задать вопрос' из промо-блока."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_question_modal()
    page.check_modal_common("Задать вопрос")


@allure.story("Открытие формы из блока FAQ")
@allure.severity("Critical")
def test_open_faq_question_modal(driver):
    """Проверка открытия модалки 'Задать вопрос' из блока FAQ."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_question_modal()
    page.check_modal_common("Задать вопрос")


@allure.story("Валидации — телефон и email в модалке")
@allure.severity("Critical")
def test_modal_validation_phone_email(driver):
    """Проверка ошибок валидации для телефона и email."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()

    # Проверяем ошибки валидации
    page.validate_phone_errors_in_modal()
    page.validate_email_errors_in_modal()


@allure.story("Активация кнопки — 'Получить предложение'")
@allure.severity("Critical")
def test_offer_submit_activation(driver):
    """Проверка логики активации кнопки 'Отправить' в форме 'Получить предложение'."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.check_offer_submit_activation()


@allure.story("Активация кнопки — 'Задать вопрос'")
@allure.severity("Critical")
def test_question_submit_activation(driver):
    """Проверка активации кнопки 'Отправить' в форме 'Задать вопрос'."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_question_modal()
    page.check_question_submit_activation()


@allure.story("Inline-форма 'Присоединяйтесь к Allsports'")
@allure.severity("Major")
def test_join_form_full(driver):
    """Проверка inline-формы: структура, валидации и активация кнопки."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_form_full()


# ===================== FORM SUBMISSION SUCCESS TESTS =====================
@allure.feature("Companies Page")
@allure.story("Форма — 'Получить предложение' (Промо-блок)")
@allure.severity("Critical")
def test_promo_offer_form_submission(driver):
    """Проверка успешной отправки формы 'Получить предложение' из промо-блока."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.submit_promo_offer_form()


@allure.feature("Companies Page")
@allure.story("Форма — 'Задать вопрос' (Промо-блок)")
@allure.severity("Critical")
def test_promo_question_form_submission(driver):
    """Проверка успешной отправки формы 'Задать вопрос' из промо-блока."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_question_modal()
    page.submit_promo_question_form()


@allure.feature("Companies Page")
@allure.story("Форма — 'Задать вопрос' (FAQ)")
@allure.severity("Critical")
def test_faq_question_form_submission(driver):
    """Проверка успешной отправки формы 'Задать вопрос' из блока FAQ."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_question_modal()
    page.submit_faq_question_form()


@allure.feature("Companies Page")
@allure.story("Inline-форма — 'Присоединяйтесь к Allsports'")
@allure.severity("Major")
def test_join_form_submission(driver):
    """Проверка успешной отправки inline-формы 'Присоединяйтесь к Allsports'."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form()


# ===================== FORM LINKS VALIDITY =====================
@allure.feature("Companies Page")
@allure.story("Гиперссылки — политика и телефон")
@allure.severity("Normal")
def test_forms_links_validity(driver):
    """Проверка корректности гиперссылок (policy + tel) в формах."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_promo_offer_modal()
    page.check_modal_common("Получить предложение")


# ===================== POLICY LINK TEST =====================
@allure.feature("Companies Page")
@allure.story("Ссылки на политику обработки персональных данных во всех формах")
@allure.severity("Critical")
def test_policy_link_in_all_forms(driver):
    """Проверка, что ссылка на политику корректно работает во всех формах."""
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_policy_link_in_all_forms()



# ===================== SUBSCRIPTION TYPES ====================================================================================
@allure.feature("Companies Page")
@allure.severity("Critical")
@allure.story("Типы подписок — проверка карточек и ссылок")
def test_subscription_cards_texts_and_links(driver):
    """Проверка карточек всех типов подписок (основные и архивные):
    - наличие карточек;
    - наличие текста (визиты, спортивные объекты, приостановка);
    - наличие ссылок 'Объекты подписки' и 'Список объектов (таблица)'.
    """
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Проверяем обычные карточки
    page._check_subscription_cards(in_archive=False)

    # Проверяем архивные карточки
    page.open_archive_modal()
    page._check_subscription_cards(in_archive=True)
    page.close_archive_modal()


@allure.feature("Companies Page")
@allure.severity("Critical")
@allure.story("Типы подписок — переходы по ссылкам обычных карточек")
def test_subscription_links_regular_cards(driver):
    """Проверяет переходы по ссылкам обычных подписок:
    - 'Объекты подписки' открывает страницу с правильным уровнем (например, 'Region подписка');
    - 'Список объектов (таблица)' открывает таблицу, которая успешно загружается.
    """
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page._check_subscription_cards(in_archive=False)


@allure.feature("Companies Page")
@allure.severity("Critical")
@allure.story("Типы подписок — переходы по ссылкам архивных карточек")
def test_subscription_links_archive_cards(driver):
    """Проверяет переходы по ссылкам в архивных карточках:
    - корректность выбранного уровня ('Lite подписка', 'Region подписка' и т.п.);
    - успешную загрузку таблицы объектов.
    """
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Открываем модалку архивных подписок
    page.open_archive_modal()

    # Проверяем переходы по ссылкам
    page._check_subscription_cards(in_archive=True)

    # Закрываем модалку
    page.close_archive_modal()


@allure.feature("Companies Page")
@allure.severity("High")
@allure.story("Типы подписок — полный сценарий проверки блока")
def test_full_subscription_block_flow(driver):
    """Полный сценарий проверки блока 'Типы подписок':
    - карточки обычных и архивных уровней;
    - клики по обеим ссылкам;
    - корректный уровень и успешная загрузка таблицы.
    """
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_subscription_cards_and_archives()


@allure.feature("Companies Page")
@allure.severity("Normal")
@allure.story("Типы подписок — стабильность загрузки таблиц")
def test_subscription_facilities_tables_load(driver):
    """Проверяет, что страницы 'Список объектов (таблица)' корректно подгружаются:
    - таблица видна;
    - есть хотя бы одна строка данных;
    - не возникает таймаутов загрузки.
    """
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Проверяем таблицы обычных карточек
    page._check_subscription_cards(in_archive=False)

    # Проверяем таблицы архивных карточек
    page.open_archive_modal()
    page._check_subscription_cards(in_archive=True)
    page.close_archive_modal()


@allure.feature("Companies Page")
@allure.severity("Normal")
@allure.story("Типы подписок — проверка текстов в карточках")
def test_subscription_card_texts_valid(driver):
    """Проверяет, что в карточках содержатся корректные тексты:
    - упоминается 'визит';
    - есть 'спорт' или 'объект';
    - указано о 'приостановке' подписки.
    """
    page = CompaniesPage(driver)
    page.open()
    page.accept_cookie_consent()

    # Проверяем тексты карточек обычных подписок
    page._check_subscription_cards(in_archive=False)

    # Проверяем тексты карточек архивных подписок
    page.open_archive_modal()
    page._check_subscription_cards(in_archive=True)
    page.close_archive_modal()

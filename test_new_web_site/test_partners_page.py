# -*- coding: utf-8 -*-

import allure
from pages.new_web_site.partners import PartnersPage


# ===================== PROMO BLOCK =====================
@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Промо-блок — наличие элементов')
def test_promo_block_elements(driver):
    "Проверка наличия заголовков и кнопок в промо-блоке."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_promo_content()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Промо-блок — заголовки и тексты')
def test_promo_texts(driver):
    "Проверка корректности текстов заголовков и описаний."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_promo_texts()

@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Промо-блок — кнопка Стать партнёром')
def test_promo_become_partner_button(driver):
    "Проверка работы кнопки 'Стать партнёром'."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_become_partner()

@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Промо-блок — кнопка Задать вопрос')
def test_promo_ask_question_button(driver):
    "Проверка открытия модалки по кнопке 'Задать вопрос'."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_ask_question()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Промо-блок — визуальное наличие логотипа')
def test_promo_logo_presence(driver):
    "Проверка отображения логотипа Allsports."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_promo_logo()


# ===================== BENEFITS =====================
@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Преимущества — наличие блока и заголовка')
def test_benefits_title(driver):
    "Проверка наличия заголовка блока Преимущества."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefits_title()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Преимущества — количество элементов')
def test_benefits_items_count(driver):
    "Проверка количества элементов преимуществ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefits_items()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Преимущества — проверка стрелок навигации')
def test_benefits_slider_controls(driver):
    "Проверка кнопок навигации (вперёд/назад)."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefits_slider()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Преимущества — корректность текстов')
def test_benefits_texts(driver):
    "Проверка текстов элементов преимуществ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefits_texts()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Преимущества — адаптивность блока')
def test_benefits_responsive(driver):
    "Проверка адаптивности отображения блока преимуществ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_benefits_responsive()


# ===================== COOPERATION =====================
@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Сотрудничество — наличие блока')
def test_cooperation_block_presence(driver):
    "Проверка наличия блока Сотрудничество."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_block()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Сотрудничество — количество шагов')
def test_cooperation_steps(driver):
    "Проверка количества шагов сотрудничества."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_steps()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Сотрудничество — тексты шагов')
def test_cooperation_texts(driver):
    "Проверка текстов карточек шагов."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_texts()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Сотрудничество — проверка стрелок')
def test_cooperation_controls(driver):
    "Проверка кнопок пролистывания."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_cooperation_controls()



# ===================== VIDEO =====================
@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Видео — наличие iframe')
def test_video_iframe(driver):
    "Проверка наличия видео iframe."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_iframe()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Видео — корректность источника')
def test_video_src(driver):
    "Проверка, что видео загружается с YouTube."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_src()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Видео — атрибут allowfullscreen')
def test_video_allowfullscreen(driver):
    "Проверка, что iframe имеет allowfullscreen."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_video_allowfullscreen()


# ===================== JOIN FORM =====================
@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Форма Join — наличие полей')
def test_join_form_fields(driver):
    "Проверка наличия всех обязательных полей формы."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_form_fields()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — чекбокс политики')
def test_join_policy_checkbox(driver):
    "Проверка чекбокса согласия с политикой."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_policy_checkbox()

@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Форма Join — валидация телефона')
def test_join_phone_validation(driver):
    "Проверка валидации телефона (некорректный ввод)."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_phone_validation()

@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Форма Join — валидация email')
def test_join_email_validation(driver):
    "Проверка валидации email."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_email_validation()

@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Форма Join — успешная отправка')
def test_join_form_submit(driver):
    "Проверка успешной отправки формы."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form_success()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — disabled кнопка при пустых полях')
def test_join_button_disabled_initially(driver):
    "Проверка, что кнопка изначально неактивна."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_button_disabled()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Форма Join — отображение текста-подсказки')
def test_join_help_text(driver):
    "Проверка текста формата телефона."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_help_text()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — клик по ссылке политики')
def test_join_policy_link(driver):
    "Проверка ссылки на политику обработки данных."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_policy_link()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Форма Join — заполнение валидными данными')
def test_join_valid_data(driver):
    "Проверка активации кнопки при валидных данных."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.fill_join_form_valid()

@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('Форма Join — очистка полей')
def test_join_clear_fields(driver):
    "Проверка очистки полей перед вводом."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_join_clear_fields()


# ===================== FAQ =====================
@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('FAQ — наличие заголовка')
def test_faq_title(driver):
    "Проверка заголовка блока FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_title()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('FAQ — количество вопросов')
def test_faq_count(driver):
    "Проверка количества вопросов FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_count()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('FAQ — раскрытие вопросов')
def test_faq_expand(driver):
    "Проверка раскрытия пунктов FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_expand()

@allure.feature('Partners Page')
@allure.severity('High')
@allure.story('FAQ — кнопка Задать вопрос')
def test_faq_button(driver):
    "Проверка кнопки 'Задать вопрос' в FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_button()

@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — открытие модалки вопроса')
def test_faq_modal_open(driver):
    "Проверка открытия модалки при нажатии 'Задать вопрос'."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()

@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — отправка вопроса')
def test_faq_modal_submit(driver):
    "Проверка заполнения и отправки формы вопроса."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()  # ✅ открываем модалку
    page.submit_faq_question()




# ===================== FAQ — Расширенные проверки =====================
@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — проверка текста всех вопросов')
def test_faq_questions_texts(driver):
    "Проверка корректности текста заголовков FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    expected_questions = [
        "Как присоединиться к сервису Allsports в качестве партнера?",
        "Какие преимущества от сотрудничества с Allsports?",
        "Как работает система расчетов с партнерами?",
        "Требуется ли какое-либо дополнительное оборудование для участия в сервисе?",
        "Необходимо ли платить за присоединение к сервису в качестве партнера?",
        "Как происходит процесс регистрации пользователей на моем объекте через Allsports?",
        "Могу ли я отказаться от партнерства с Allsports, если это потребуется?",
    ]
    page.check_faq_question_texts(expected_questions)


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — раскрытие и текст первого ответа')
def test_faq_first_answer_text(driver):
    "Проверка раскрытия и корректности ответа на первый вопрос FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.expand_faq_question_by_index(0)
    page.verify_faq_answer_contains(0, "свяжитесь с нами по указанным контактным данным")





@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('FAQ — раскрытие всех вопросов подряд')
def test_faq_expand_all_questions(driver):
    "Проверка клика и раскрытия каждого вопроса FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.expand_all_faq_questions()


@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('FAQ — наличие кнопки Задать вопрос под списком')
def test_faq_bottom_button(driver):
    "Проверка кнопки 'Задать вопрос' под FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_faq_bottom_button()


# ===================== CONTACTS =====================
@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Контакты — наличие блока')
def test_contacts_presence(driver):
    "Проверка наличия блока Контакты."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_presence()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Контакты — телефоны')
def test_contacts_phones(driver):
    "Проверка телефонов отделов."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_phones()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Контакты — email адреса')
def test_contacts_emails(driver):
    "Проверка email-адресов отделов."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_emails()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Контакты — адрес')
def test_contacts_address(driver):
    "Проверка отображения адреса."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_address()

@allure.feature('Partners Page')
@allure.severity('Normal')
@allure.story('Контакты — карта')
def test_contacts_map(driver):
    "Проверка наличия карты и элементов управления."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_map()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Контакты — кнопки зума карты')
def test_contacts_zoom_buttons(driver):
    "Проверка кнопок зума карты."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_zoom_buttons()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Контакты — логотип Mapbox')
def test_contacts_map_logo(driver):
    "Проверка отображения логотипа Mapbox."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_map_logo()

@allure.feature('Partners Page')
@allure.severity('Low')
@allure.story('Контакты — адаптивность карты')
def test_contacts_responsive(driver):
    "Проверка адаптивности блока Контакты."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_responsive()


# ===================== FORMS SUBMISSION =====================

@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Промо — отправка формы через кнопку "Стать партнёром"')
def test_submit_become_partner_form(driver):
    "Проверка открытия и отправки формы через кнопку 'Стать партнёром'."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_become_partner()
    page.submit_become_partner_modal()  # ✅ новый метод



@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Промо — отправка формы через кнопку "Задать вопрос"')
def test_submit_question_modal_top(driver):
    "Проверка открытия и отправки модалки 'Задать вопрос' из промо-блока."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.click_ask_question()
    page.submit_question_modal()




@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — отправка вопроса из блока FAQ')
def test_submit_question_modal_faq(driver):
    "Проверка открытия и успешной отправки формы 'Задать вопрос' из FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()
    page.submit_question_modal()


@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('Join форма — успешная отправка')
def test_join_form_real_submit(driver):
    "Проверка успешной отправки формы 'Присоединяйтесь к Allsports' и появления подтверждения."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_join_form_success()
    page.verify_success_modal()


# ===================== VALIDATION TESTS (ошибки форм) =====================

@allure.feature('Partners Page')
@allure.severity('Critical')
@allure.story('FAQ — валидация формы "Задать вопрос" (ошибки ввода)')
def test_faq_modal_validation_errors(driver):
    "Проверка отображения ошибок валидации в модалке FAQ."
    page = PartnersPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.open_faq_modal()
    page.verify_faq_question_errors()








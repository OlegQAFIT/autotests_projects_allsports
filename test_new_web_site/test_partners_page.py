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








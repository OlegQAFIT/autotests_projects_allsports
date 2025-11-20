import allure
from pages.new_web_site.contacts import ContactsPage


# --- SMOKE ---

@allure.feature('Smoke')
@allure.severity('Blocker')
@allure.story('Проверка открытия страницы Контакты')
def test_open_contacts_page(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_header()


@allure.feature('Smoke')
@allure.severity('Blocker')
@allure.story('Проверка заголовка страницы Контакты')
def test_check_contacts_page_header(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_header()


# --- CONTACTS ---

@allure.feature('Contacts Info')
@allure.severity('Normal')
@allure.story('Проверка наличия блока с адресом и контактной информацией')
def test_check_address_block(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_address_block()


@allure.feature('Contacts Info')
@allure.severity('Critical')
@allure.story('Проверка текста контактных данных (точное совпадение)')
def test_check_contacts_text_exact(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_contacts_text_exact()



@allure.feature('Contacts Info')
@allure.severity('Normal')
@allure.story('Проверка формата телефонных ссылок tel:')
def test_check_phone_links_format(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    phones = page.get_phone_elements()
    assert len(phones) >= 1, "Телефонные ссылки не найдены"
    page.verify_tel_links_format()


@allure.feature('Contacts Info')
@allure.severity('Normal')
@allure.story('Проверка формата email-ссылок mailto:')
def test_check_email_links_format(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    emails = page.get_email_elements()
    assert len(emails) >= 1, "Email ссылки не найдены"
    page.verify_mailto_links_format()


@allure.feature('Contacts Info')
@allure.severity('Normal')
@allure.story('Проверка наличия социальных ссылок')
def test_check_social_links_exist(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_social_links_exist()


# --- MAP ---

@allure.feature('Map')
@allure.severity('Normal')
@allure.story('Проверка наличия и корректности карты Google')
def test_check_google_map(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_google_map()


# --- FORM: POSITIVE ---

@allure.feature('Send form')
@allure.severity('Critical')
@allure.story('Проверка успешной отправки формы (Подключить компанию)')
def test_send_form_valid_get_offer(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_valid_get_offer()
    # визуальная модалка или API
    page.check_success_modal()
    page.assert_form_get_offer()


# @allure.feature('Send form')
# @allure.severity('Critical')
# @allure.story('Проверка успешной отправки формы (Стать партнёром)')
# def test_send_form_valid_become_partner(driver):
#     page = ContactsPage(driver)
#     page.open()
#     page.accept_cookie_consent()
#     page.submit_form_valid_become_partner()
#     page.check_success_modal()
#     page.assert_form_become_partner()


@allure.feature('Send form')
@allure.severity('Critical')
@allure.story('Проверка, что кнопка Отправить активна (после заполнения и чекбокса)')
def test_send_button_enabled(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.switch_to_get_offer()
    page.fill_form_standard(page.text_name, page.text_phone_valid, page.text_email_valid, page.text_company)
    page.clc_checkbox(True)
    page.check_send_button_enabled()


# --- FORM: NEGATIVE ---

@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным email (get-offer)')
def test_invalid_email(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(email=True)
    page.assert_email_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным телефоном (get-offer)')
def test_invalid_phone(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(phone=True)
    page.assert_phone_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы с пустыми полями (get-offer)')
def test_empty_fields(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(empty=True)
    page.check_button_state_disabled()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы без согласия на обработку данных (get-offer)')
def test_without_agree_checkbox(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(no_agree=True)
    page.check_button_state_disabled()


# --- Доп. негативы для второй формы ---

@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным email (become-partner)')
def test_invalid_email_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, email=True)
    page.assert_email_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка валидации формы с невалидным телефоном (become-partner)')
def test_invalid_phone_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, phone=True)
    page.assert_phone_error()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы с пустыми полями (become-partner)')
def test_empty_fields_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, empty=True)
    page.check_button_state_disabled()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка отправки формы без согласия (become-partner)')
def test_without_checkbox_become_partner(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(for_partner=True, no_agree=True)
    page.check_button_state_disabled()


# --- FOOTER ---

@allure.feature('Footer')
@allure.severity('Normal')
@allure.story('Проверка элементов футера (реквизиты, копирайт, ссылка)')
def test_footer_elements(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_footer_all()


@allure.feature('Footer')
@allure.severity('Normal')
@allure.story('Проверка наличия ссылки \"Правила оказания услуг\"')
def test_footer_rules_link(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_footer_rules_link_present()


# --- SEO ---

@allure.feature('SEO')
@allure.severity('Normal')
@allure.story('Проверка наличия мета-тегов title и description')
def test_meta_tags(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_meta_tags()


# --- PERFORMANCE ---

@allure.feature('Performance')
@allure.severity('Normal')
@allure.story('Проверка, что страница загружается быстрее 3 секунд')
def test_page_load_speed(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_performance(max_load_ms=3000)


# --- CONSOLE ---

@allure.feature('Console')
@allure.severity('Normal')
@allure.story('Проверка отсутствия ошибок в консоли браузера')
def test_console_no_errors(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_console_errors()


# --- LINKS ---

@allure.feature('Links')
@allure.severity('Normal')
@allure.story('Проверка корректности внешних ссылок')
def test_external_links_format(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_external_links_format()


# --- COUNTS / AGGREGATED ---

@allure.feature('Contacts Info')
@allure.severity('Normal')
@allure.story('Проверка, что все телефонные ссылки найдены')
def test_all_phone_links_found(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    assert len(page.get_phone_elements()) >= 1, "Телефоны не найдены"


@allure.feature('Contacts Info')
@allure.severity('Normal')
@allure.story('Проверка, что все email ссылки найдены')
def test_all_email_links_found(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    assert len(page.get_email_elements()) >= 1, "Email ссылки не найдены"


# --- ADDITIONAL NEGATIVES (как у тебя: сначала невалидно, потом валидно) ---

@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка: невалидный email, затем валидный (get-offer)')
def test_invalid_email_then_valid(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invalid(email=True)
    page.assert_email_error()
    page.submit_form_valid_get_offer()
    page.check_success_modal()
    page.assert_form_get_offer()


@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Проверка: невалидный телефон, затем валидный (get-offer)')
def test_invalid_phone_then_valid(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.submit_form_invaliddd(phone=True)
    page.assert_phone_error()
    page.submit_form_valid_get_offer()
    page.check_success_modal()
    page.assert_form_get_offer()


# --- URL ---

@allure.feature('Smoke')
@allure.severity('Normal')
@allure.story('Проверка, что URL содержит /contacts')
def test_url_contains_contacts(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.assert_url_contains('/contacts')


# --- PRESENCE OF FORM FIELDS ---

@allure.feature('Form')
@allure.severity('Normal')
@allure.story('Проверка наличия всех обязательных полей (Имя, Телефон, Email, Компания/Сообщение)')
def test_presence_of_all_form_fields(driver):
    """
    У текущей формы поля: Имя, Телефон, Email, Компания (вместо 'Сообщение').
    Локатор INPUT_MESSAGE покрывает оба случая: textarea message ИЛИ input 'Компания'.
    """
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    assert page.is_element_exist(page.INPUT_NAME), "Поле Имя отсутствует"
    assert page.is_element_exist(page.INPUT_PHONE), "Поле Телефон отсутствует"
    assert page.is_element_exist(page.INPUT_EMAIL), "Поле Email отсутствует"
    assert page.is_element_exist(page.INPUT_MESSAGE), "Поле Сообщение/Компания отсутствует"


# --- E2E ---

@allure.feature('E2E')
@allure.severity('Blocker')
@allure.story('Полный путь пользователя: проверка инфо + отправка формы (get-offer)')
def test_e2e_contacts_page_flow(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_page_header()
    page.check_address_block()
    page.verify_tel_links_format()
    page.verify_mailto_links_format()
    page.check_google_map()
    page.submit_form_valid_get_offer()
    page.check_success_modal()
    page.assert_form_get_offer()


# --- Дополнительно: Кнопка неактивна до полного заполнения и чекбокса ---

@allure.feature('Validation')
@allure.severity('Critical')
@allure.story('Кнопка неактивна, пока не заполнены все поля и не нажат чекбокс')
def test_button_inactive_without_checkbox_or_fields(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.assert_button_inactive_until_all_required()

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


# --- URL ---

@allure.feature('Smoke')
@allure.severity('Normal')
@allure.story('Проверка, что URL содержит /contacts')
def test_url_contains_contacts(driver):
    page = ContactsPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.assert_url_contains('/contacts')

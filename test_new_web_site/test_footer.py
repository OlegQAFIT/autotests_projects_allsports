# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.footer import FooterPage


# --- SMOKE ---

@allure.feature('Smoke')
@allure.severity('Blocker')
@allure.story('Проверка целостности футера на главной странице')
def test_footer_integrity(driver):
    page = FooterPage(driver)
    page.open()
    page.check_footer_integrity()


# --- CONTACT INFO ---

@allure.feature('Contacts')
@allure.severity('Critical')
@allure.story('Проверка наличия и корректности телефона и email')
def test_footer_contacts_info(driver):
    page = FooterPage(driver)
    page.open()
    page.check_footer_contacts()


@allure.feature('Contacts')
@allure.severity('Normal')
@allure.story('Проверка, что телефон и email кликабельны')
def test_footer_contacts_clickable(driver):
    page = FooterPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.assert_element_present(page.L.PHONE)
    page.assert_element_present(page.L.EMAIL)


# --- SOCIAL LINKS ---

@allure.feature('Social Links')
@allure.severity('Normal')
@allure.story('Проверка, что ссылки на соцсети присутствуют и корректны')
def test_footer_social_links(driver):
    page = FooterPage(driver)
    page.open()
    page.check_social_links()


# --- APP STORE LINKS ---

@allure.feature('Apps')
@allure.severity('Normal')
@allure.story('Проверка, что ссылки на магазины приложений корректны')
def test_footer_app_links(driver):
    page = FooterPage(driver)
    page.open()
    page.check_app_store_links()


# --- NAVIGATION LINKS ---

@allure.feature('Navigation')
@allure.severity('Critical')
@allure.story('Проверка всех навигационных ссылок футера')
def test_footer_navigation_links(driver):
    page = FooterPage(driver)
    page.open()
    page.check_footer_navigation_links()


# --- COPYRIGHT / PROVIDER ---

@allure.feature('Footer Info')
@allure.severity('Normal')
@allure.story('Проверка копирайта и регистрационного номера')
def test_footer_copyright(driver):
    page = FooterPage(driver)
    page.open()
    page.check_copyright_and_provider()


# --- LEGAL DOCS ---

@allure.feature('Documents')
@allure.severity('Critical')
@allure.story('Проверка документов для юридических лиц')
def test_footer_legal_documents(driver):
    page = FooterPage(driver)
    page.open()
    page.check_legal_documents()


# --- USER AGREEMENTS ---

@allure.feature('User Agreements')
@allure.severity('Critical')
@allure.story('Проверка пользовательских соглашений и политик')
def test_footer_user_agreements(driver):
    page = FooterPage(driver)
    page.open()
    page.check_user_agreements()


# --- QUALITY CHECKS ---

@allure.feature('Quality')
@allure.severity('Normal')
@allure.story('Проверка отсутствия ошибок JavaScript')
def test_footer_no_js_errors(driver):
    page = FooterPage(driver)
    page.open()
    page.accept_cookie_consent()
    assert len(page.get_js_console_errors()) == 0, "Есть ошибки JS в консоли"


@allure.feature('Quality')
@allure.severity('Normal')
@allure.story('Проверка, что язык страницы русский')
def test_footer_language(driver):
    page = FooterPage(driver)
    page.open()
    page.accept_cookie_consent()
    page.check_for_words('russian')

import pytest
import allure
from locators.elements_from_links.for_elements_from_links import LocatorsFromPagesLinks
from pages.links.links import ElementsFromLinks


@allure.feature('Проверка доступности ссылок')
@allure.severity('critical')
@allure.story('Проверка страниц, которых нет на сайте и не должно быть редиректа')
@pytest.mark.parametrize("domain", [
    "https://оллспортс.бел/by",
    "https://www.allsports.fit/by"
])
def test_check_link_one(driver, domain):
    checking_links = ElementsFromLinks(driver, domain, domain_new=None)
    checking_links.check_links_one()


@allure.feature('Проверка доступности ссылок')
@allure.severity('normal')
@allure.story('Проверка страниц, редирект с заменой домена')
@pytest.mark.parametrize("domain, domain_new", [
    ("https://оллспортс.бел/by", "https://сайт.оллспортс.бел/ru-by"),
    ("https://www.allsports.fit/by", "https://www.allsports.by/ru-by")
])
def test_check_link_two(driver, domain, domain_new):
    checking_links = ElementsFromLinks(driver, domain, domain_new)
    checking_links.check_links_two()


@pytest.mark.parametrize("domain, domain_new", [
    ("https://оллспортс.бел/by", "https://сайт.оллспортс.бел/ru-by"),
    ("https://www.allsports.fit/by", "https://www.allsports.by/ru-by")
])
@allure.feature('Проверка доступности ссылок')
@allure.severity('normal')
@allure.story('Проверка страниц, редирект на другую страницу на новом сайте')
def test_check_link_three(driver, domain, domain_new):
    checking_links = ElementsFromLinks(driver, domain, domain_new, LocatorsFromPagesLinks.paths_and_redirects)
    checking_links.check_links_three()


@allure.feature('Проверка доступности ссылок')
@allure.severity('normal')
@allure.story('Проверка страниц, редирект с заменой домена и сохранением адреса в конце')
@pytest.mark.parametrize("domain, domain_new", [
    ("https://оллспортс.бел/by", "https://сайт.оллспортс.бел/ru-by"),
    ("https://www.allsports.fit/by", "https://www.allsports.by/ru-by")
])
def test_check_link_four(driver, domain, domain_new):
    checking_links = ElementsFromLinks(driver, domain, domain_new)
    checking_links.check_links_four()


@allure.feature('Проверка редиректа')
@allure.severity('critical')
@allure.story('Проверка страницы, главная для перехода')
def test_check_link_five(driver):
    checking_links = ElementsFromLinks(driver)
    checking_links.check_links_five()


@allure.feature('Проверка редиректа')
@allure.severity('critical')
@allure.story('Проверка страницы, главная для перехода')
def test_check_link_five(driver):
    domain = "https://оллспортс.бел/by"  # Укажите нужный домен, если он нужен для проверки
    checking_links = ElementsFromLinks(driver, domain)
    checking_links.check_links_for_404()

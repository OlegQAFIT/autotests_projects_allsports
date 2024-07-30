import allure
from pages.links.links import ElementsFromLinks

@allure.feature('Проверка доступности ссылок')
@allure.severity('critical')
@allure.story('Проверка страниц, которых нет на сайте и не должно быть редиректа')
def test_check_link_one(driver):
    checking_links = ElementsFromLinks(driver)
    checking_links.check_links_one()

@allure.feature('Проверка доступности ссылок')
@allure.severity('normal')
@allure.story('Проверка страниц, редирект с заменой домена')
def test_check_link_two(driver):
    checking_links = ElementsFromLinks(driver)
    checking_links.check_links_two()



@allure.feature('Проверка доступности ссылок')
@allure.severity('normal')
@allure.story('Проверка страниц, редирект на другую страницу на новом сайте')
def test_check_link_three(driver):
    checking_links = ElementsFromLinks(driver)
    checking_links.check_links_three()


@allure.feature('Проверка доступности ссылок')
@allure.severity('normal')
@allure.story('Проверка страниц, редирект с заменой домена и сохранением адреса в конце')
def test_check_link_four(driver):
    checking_links = ElementsFromLinks(driver)
    checking_links.check_links_four()



@allure.feature('Проверка редиректа')
@allure.severity('critical')
@allure.story('Проверка страницы, главная для перехода')
def test_check_link_five(driver):
    checking_links = ElementsFromLinks(driver)
    checking_links.check_links_five()



@allure.feature('Проверка доступности ссылок')
@allure.severity('normal')
@allure.story('Проверка страниц, редирект с заменой домена и сохранением адреса в конце')
def test_check_link_404(driver):
    checking_links = ElementsFromLinks(driver)
    checking_links.check_links_for_404()






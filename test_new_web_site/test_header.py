# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.header import HeaderPage


# =======================
# == Основной хедер ==
# =======================

@allure.feature('Header')
@allure.severity('Blocker')
@allure.story('Проверка логотипа')
def test_logo(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_logo()


@allure.feature('Header')
@allure.severity('Normal')
@allure.story('Проверка перехода по логотипу')
def test_logo_navigation(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_logo_navigation()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Объекты')
def test_link_facilities(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_facilities()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Типы подписок')
def test_link_levels(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_levels()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Компаниям')
def test_link_companies(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_companies()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Партнерам')
def test_link_partners(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_partners()


@allure.feature('Header Navigation')
@allure.story('Проверка ссылки Контакты')
def test_link_contacts(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_link_contacts()


@allure.feature('Header Buttons')
@allure.story('Проверка наличия кнопок в хедере')
def test_header_buttons(driver):
    page = HeaderPage(driver)
    page.open()
    page.check_header_buttons()


# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class RegressionLocators:
    """Список всех страниц сайта и ключевых элементов для проверки."""

    PAGES = {
        "main": {
            "url": "https://www.allsports.by/ru-by",
            "locators": [
                (By.XPATH, '//*[@id="defaultView"]/main/section/div[1]/p[1]'),
                (By.XPATH, '//*[@id="advantagesSection"]/section/h2'),
                (By.XPATH, '//*[@id="levelsSection"]/section/h2'),
                (By.XPATH, '//*[@id="feedbackSection"]/section/h2'),
                (By.XPATH, '//*[@id="faqSection"]/section/h2'),
                (By.CSS_SELECTOR, "section.youtube-video iframe[src*='youtube']"),
                (By.XPATH, '//*[@id="getDetailsSection"]/section/div/div[1]/h2'),
                (By.XPATH, '//*[@id="contactsSection"]'),
            ],
        },
        "facilities": {
            "url": "https://www.allsports.by/ru-by/facilities",
            "locators": [(By.XPATH, '//*[@id="map"]/div[2]/canvas')],
        },
        "levels": {
            "url": "https://www.allsports.by/ru-by/levels",
            "locators": [
                (By.XPATH, '//*[@id="defaultView"]/main/div[1]/section'),
                (By.XPATH, '//*[@id="getDetailsSection"]/section/div/div[1]/h2'),
                (By.XPATH, '//*[@id="getDetailsSection"]/section/div'),
            ],
        },
        "companies": {
            "url": "https://www.allsports.by/ru-by/companies",
            "locators": [
                (By.XPATH, '//*[@id="defaultView"]/main/section/div[1]'),
                (By.XPATH, '//*[@id="benefitSection"]/section/h2'),
                (By.XPATH, '//*[@id="cooperationSection"]/section/h2'),
                (By.XPATH, '//*[@id="feedbackSection"]/section/h2'),
                (By.XPATH, '//*[@id="levelsSection"]/section/h2'),
                (By.XPATH, '//*[@id="faqSection"]/section'),
                (By.CSS_SELECTOR, "section.youtube-video iframe[src*='youtube']"),
                (By.XPATH, '//*[@id="getDetailsSection"]/section'),
                (By.XPATH, '//*[@id="contactsSection"]'),
            ],
        },
        "partners": {
            "url": "https://www.allsports.by/ru-by/partners",
            "locators": [
                (By.XPATH, '//*[@id="defaultView"]/main/section'),
                (By.XPATH, '//*[@id="benefitSection"]/section'),
                (By.XPATH, '//*[@id="cooperationSection"]/section'),
                (By.XPATH, '//*[@id="faqSection"]/section'),
                (By.CSS_SELECTOR, "section.youtube-video iframe[src*='youtube']"),
                (By.XPATH, '//*[@id="getDetailsSection"]/section'),
                (By.XPATH, '//*[@id="contactsSection"]'),
            ],
        },
        "contacts": {
            "url": "https://www.allsports.by/ru-by/contacts",
            "locators": [
                (By.XPATH, '//*[@id="defaultView"]/main/section[1]'),
                (By.XPATH, '//*[@id="defaultView"]/main/section[2]'),
            ],
        },
        "license": {
            "url": "https://www.allsports.by/ru-by/license",
            "locators": [
                (By.XPATH, '//*[@id="defaultView"]/main/section/h2'),
                (By.XPATH, '//*[@id="defaultView"]/main/section/div/div[1]'),
            ],
        },
        "policy": {
            "url": "https://www.allsports.by/ru-by/policy/251010_processing_personal_data",
            "locators": [(By.XPATH, '//*[@id="defaultView"]/main/section/div/div[2]/article/h2')],
        },
        "license_doc": {
            "url": "https://www.allsports.by/ru-by/license/241009_license",
            "locators": [(By.XPATH, '//*[@id="defaultView"]/main/section/div/div[2]/article/h2')],
        },
        "user_agreement": {
            "url": "https://www.allsports.by/ru-by/user-agreements",
            "locators": [(By.XPATH, '//*[@id="defaultView"]/main/section/h2')],
        },
        "individual_license": {
            "url": "https://www.allsports.by/ru-by/individual_license/241009_license",
            "locators": [(By.XPATH, '//*[@id="defaultView"]/main/section/div/div[2]/article/h2')],
        },
        "rule": {
            "url": "https://www.allsports.by/ru-by/rule/250731_rule",
            "locators": [(By.XPATH, '//*[@id="defaultView"]/main/section/div/div[2]/article/h2')],
        },
        "cookie_policy": {
            "url": "https://www.allsports.by/ru-by/cookie/cookie-policy",
            "locators": [(By.XPATH, '//*[@id="defaultView"]/main/section/div/div[2]/article/h2')],
        },
        "facilities_table": {
            "url": "https://www.allsports.by/ru-by/facilities-table",
            "locators": [(By.XPATH, '//*[@id="defaultView"]/main/section/h2')],
        },
    }

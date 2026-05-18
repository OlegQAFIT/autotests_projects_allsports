# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class ContactsLocatorsSb:
    BASE_URL = "https://www.sportbenefit.eu/en-cy/contacts"

    PAGE_ROOT = (By.TAG_NAME, "body")
    CONTACT_FORM = (By.TAG_NAME, "form")
    CONTACT_FORM_INPUTS = (By.CSS_SELECTOR, "form input")
    CONTACT_FORM_SUBMIT = (By.CSS_SELECTOR, "form button[type='submit'], form button")

    PHONE_INPUT = (By.CSS_SELECTOR, "form input[name='phone']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "form input[name='email']")
    AGREEMENT_CHECKBOX = (By.CSS_SELECTOR, "form input[type='checkbox']")

    INPUT_ERRORS = (By.CSS_SELECTOR, "form .input-error")

    MAP_CANVAS = (By.CSS_SELECTOR, "#map .mapboxgl-canvas, .contacts-map .mapboxgl-canvas")
    MAP_ZOOM_IN = (By.CSS_SELECTOR, ".mapboxgl-ctrl-zoom-in")

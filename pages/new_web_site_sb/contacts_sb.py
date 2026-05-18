# -*- coding: utf-8 -*-
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.for_contacts_page_sb import ContactsLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class ContactsPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        return self

    def _wait_form_present(self):
        self.accept_cookie_consent()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(L.CONTACT_FORM))

    def check_page_opened(self):
        assert "/contacts" in self.driver.current_url, f"Unexpected contacts URL: {self.driver.current_url}"
        self._wait_form_present()
        forms = self.driver.find_elements(*L.CONTACT_FORM)
        assert forms, "Contacts form is missing"

    def check_form_structure(self):
        self._wait_form_present()

        inputs = self.driver.find_elements(*L.CONTACT_FORM_INPUTS)
        submit = self.driver.find_elements(*L.CONTACT_FORM_SUBMIT)
        assert len(inputs) >= 5, f"Expected >=5 inputs in contacts form, got {len(inputs)}"
        assert submit, "Contacts form submit button is missing"

        placeholders = [(el.get_attribute("placeholder") or "").strip() for el in inputs]
        assert "Name" in placeholders, f"Name placeholder missing: {placeholders}"
        assert "Enter phone number" in placeholders, f"Phone placeholder missing: {placeholders}"
        assert any("@sportbenefit.eu" in p for p in placeholders), f"Email placeholder missing: {placeholders}"
        assert "Company" in placeholders, f"Company placeholder missing: {placeholders}"

    def check_map_visible(self):
        # Map can render when section gets viewport.
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
        time.sleep(0.4)
        self.accept_cookie_consent()

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(L.MAP_CANVAS))

    def check_invalid_phone_validation(self):
        self._wait_form_present()

        phone = self.driver.find_element(*L.PHONE_INPUT)
        email = self.driver.find_element(*L.EMAIL_INPUT)

        phone.clear()
        phone.send_keys("123")

        email.clear()
        email.send_keys("bad")

        checkboxes = self.driver.find_elements(*L.AGREEMENT_CHECKBOX)
        if checkboxes:
            self.driver.execute_script("arguments[0].click();", checkboxes[0])

        submit = self.driver.find_element(*L.CONTACT_FORM_SUBMIT)
        submit_disabled = (not submit.is_enabled()) or (submit.get_attribute("disabled") is not None)
        if not submit_disabled:
            self.driver.execute_script("arguments[0].click();", submit)
            time.sleep(0.8)

        # Inline form can block invalid data before submit; this is the expected guard.
        submit_now = self.driver.find_element(*L.CONTACT_FORM_SUBMIT)
        submit_disabled_after = (not submit_now.is_enabled()) or (submit_now.get_attribute("disabled") is not None)
        assert submit_disabled_after, "Inline contacts submit should stay disabled for invalid phone/email"

        errors = [(el.text or "").strip() for el in self.driver.find_elements(*L.INPUT_ERRORS)]
        errors = [e for e in errors if e]
        if errors:
            assert any("invalid" in e.lower() or "format" in e.lower() for e in errors), (
                f"Unexpected validation errors: {errors}"
            )

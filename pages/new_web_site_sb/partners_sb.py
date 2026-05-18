# -*- coding: utf-8 -*-
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.for_partners_page_sb import PartnersLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class PartnersPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        return self

    def open_become_partner_modal(self):
        for _ in range(5):
            btn = WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(L.CTA_BECOME_PARTNER))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.45)

            placeholders = [(el.get_attribute("placeholder") or "").strip() for el in self.driver.find_elements(*L.MODAL_INPUTS)]
            if "Facility name" in placeholders:
                return

            self.accept_cookie_consent()

        assert False, "Become a Partner modal did not open on /partners"

    def check_partner_modal_structure(self):
        placeholders = [(el.get_attribute("placeholder") or "").strip() for el in self.driver.find_elements(*L.MODAL_INPUTS)]
        assert "Facility name" in placeholders, f"Facility name placeholder missing on partners modal: {placeholders}"
        assert "Enter phone number" in placeholders, f"Phone placeholder missing on partners modal: {placeholders}"
        assert any("@sportbenefit.eu" in p for p in placeholders), f"Email placeholder missing on partners modal: {placeholders}"

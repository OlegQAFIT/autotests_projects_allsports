# -*- coding: utf-8 -*-
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.for_companies_page_sb import CompaniesLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class CompaniesPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        return self

    def open_get_offer_modal(self):
        for _ in range(5):
            btn = WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(L.CTA_GET_OFFER))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.45)

            placeholders = [(el.get_attribute("placeholder") or "").strip() for el in self.driver.find_elements(*L.MODAL_INPUTS)]
            if "Company" in placeholders:
                return

            self.accept_cookie_consent()

        assert False, "Get an Offer modal did not open on /companies"

    def check_companies_modal_structure(self):
        tabs = [el.text.strip() for el in self.driver.find_elements(*L.MODAL_TABS) if el.text.strip()]
        placeholders = [(el.get_attribute("placeholder") or "").strip() for el in self.driver.find_elements(*L.MODAL_INPUTS)]

        assert any("Corporate" in t for t in tabs), f"Corporate tab missing on companies modal: {tabs}"
        assert "Company" in placeholders, f"Company placeholder missing on companies modal: {placeholders}"
        assert "Enter the city" in placeholders, f"City placeholder missing on companies modal: {placeholders}"

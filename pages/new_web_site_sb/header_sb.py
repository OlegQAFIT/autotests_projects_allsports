# -*- coding: utf-8 -*-
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.header_elements_new_web_site_sb import HeaderLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class HeaderPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        return self

    def check_header_links_present(self):
        links = self.driver.find_elements(*L.HEADER_LINKS)
        hrefs = {(el.get_attribute("href") or "").strip() for el in links}
        expected_paths = [
            "/en-cy",
            "/en-cy/facilities",
            "/en-cy/levels",
            "/en-cy/companies",
            "/en-cy/partners",
            "/en-cy/contacts",
        ]

        for path in expected_paths:
            assert any(path in href for href in hrefs), f"Header link is missing for path: {path}"

    def check_header_navigation(self):
        links = self.driver.find_elements(*L.HEADER_LINKS)
        hrefs = []
        for el in links:
            href = (el.get_attribute("href") or "").strip()
            if href and href not in hrefs:
                hrefs.append(href)

        for href in hrefs:
            if "/en-cy" not in href:
                continue
            self.open_url(href)
            self.accept_cookie_consent()
            assert "sportbenefit.eu" in self.driver.current_url, f"Unexpected host after nav: {self.driver.current_url}"

    def _modal_has_offer_form(self):
        tabs = self.driver.find_elements(*L.MODAL_TABS)
        inputs = self.driver.find_elements(*L.MODAL_INPUTS)
        send_btn = self.driver.find_elements(*L.MODAL_SEND_BUTTON)
        return bool((tabs and inputs) or (inputs and send_btn))

    def open_get_offer_modal(self):
        for _ in range(5):
            cta = WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(L.CTA_GET_OFFER))
            self.driver.execute_script("arguments[0].click();", cta)
            time.sleep(0.45)

            if self._modal_has_offer_form():
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(L.MODAL))
                return

            # Sometimes cookie dialog appears only after first interaction.
            self.accept_cookie_consent()

        assert False, "Get an Offer modal did not open"

    def check_offer_modal_structure(self):
        tabs = [el.text.strip() for el in self.driver.find_elements(*L.MODAL_TABS) if el.text.strip()]
        assert any("For Corporate Clients" in t for t in tabs), f"Corporate tab not found. Tabs={tabs}"
        assert any("Become a Partner" in t for t in tabs), f"Partner tab not found. Tabs={tabs}"

        placeholders = [(el.get_attribute("placeholder") or "").strip() for el in self.driver.find_elements(*L.MODAL_INPUTS)]
        assert "Name" in placeholders, f"Name placeholder missing: {placeholders}"
        assert "Enter phone number" in placeholders, f"Phone placeholder missing: {placeholders}"
        assert any("@sportbenefit.eu" in p for p in placeholders), f"Email placeholder missing: {placeholders}"
        assert "Company" in placeholders, f"Company placeholder missing: {placeholders}"
        assert "Enter the city" in placeholders, f"City placeholder missing: {placeholders}"

    def check_offer_modal_partner_tab(self):
        tabs = self.driver.find_elements(*L.MODAL_TABS)
        for tab in tabs:
            if "Partner" in (tab.text or ""):
                self.driver.execute_script("arguments[0].click();", tab)
                time.sleep(0.5)
                break

        placeholders = [(el.get_attribute("placeholder") or "").strip() for el in self.driver.find_elements(*L.MODAL_INPUTS)]
        assert "Facility name" in placeholders, f"Facility name placeholder missing on partner tab: {placeholders}"

    def close_modal(self):
        close_buttons = self.driver.find_elements(*L.MODAL_CLOSE)
        if close_buttons:
            self.driver.execute_script("arguments[0].click();", close_buttons[0])
            time.sleep(0.4)

        # Do not require all modal overlays to disappear (cookie modal may coexist).
        WebDriverWait(self.driver, 8).until(
            lambda d: len([el for el in d.find_elements(*L.MODAL_INPUTS) if el.is_displayed()]) == 0
        )

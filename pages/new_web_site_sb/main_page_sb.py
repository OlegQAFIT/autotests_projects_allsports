# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.for_main_page_sb import MainPageLocatorsSb as L
from pages.new_web_site_sb.header_sb import HeaderPageSb


class MainPageSb(HeaderPageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        return self

    def check_main_page_basics(self):
        self.assert_element_present(L.PAGE_ROOT)
        self.assert_element_present(L.HEADER)

        # Footer may require lazy scroll to render.
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(L.FOOTER))

    def check_main_cta_buttons(self):
        get_offer = self.driver.find_elements(*L.CTA_GET_OFFER)
        ask_question = self.driver.find_elements(*L.CTA_ASK_QUESTION)
        assert get_offer, "Get an Offer CTA is missing on main page"
        assert ask_question, "Ask Us a Question CTA is missing on main page"

    def check_main_offer_modal_flow(self):
        self.open_get_offer_modal()
        self.check_offer_modal_structure()
        self.check_offer_modal_partner_tab()
        self.close_modal()

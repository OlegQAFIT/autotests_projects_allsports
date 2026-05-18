# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.footer_elements_new_web_site_sb import FooterLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class FooterPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        self.accept_cookie_consent()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(L.FOOTER_ROOT))
        return self

    def check_contacts(self):
        self.assert_element_present(L.PHONE)
        self.assert_element_present(L.EMAIL)

        phone_href = (self.driver.find_element(*L.PHONE).get_attribute("href") or "").strip()
        email_href = (self.driver.find_element(*L.EMAIL).get_attribute("href") or "").strip()
        assert phone_href.startswith("tel:"), f"Invalid phone link: {phone_href}"
        assert email_href.startswith("mailto:"), f"Invalid email link: {email_href}"

    def check_social_links(self):
        for locator in (L.LINKEDIN, L.INSTAGRAM, L.FACEBOOK):
            self.assert_element_present(locator)

    def check_app_links(self):
        for locator in (L.APPLE, L.GOOGLE, L.HUAWEI):
            self.assert_element_present(locator)

    def check_navigation_links(self):
        for locator in (
            L.NAV_COMPANIES,
            L.NAV_PARTNERS,
            L.NAV_FACILITIES,
            L.NAV_LEVELS,
            L.NAV_CONTACTS,
        ):
            self.assert_element_present(locator)

    def check_legal_links(self):
        self.assert_element_present(L.LEGAL_LICENSE)
        self.assert_element_present(L.LEGAL_USER_AGREEMENTS)

    def check_footer_link_statuses(self):
        links = self.driver.find_elements(*L.FOOTER_LINKS)
        hrefs = [(el.get_attribute("href") or "").strip() for el in links]
        assert any("/en-cy/license" in h for h in hrefs), "License link missing in footer"
        assert any("/en-cy/user-agreements" in h for h in hrefs), "User agreements link missing in footer"
        assert any("play.google.com" in h for h in hrefs), "Google Play link missing in footer"

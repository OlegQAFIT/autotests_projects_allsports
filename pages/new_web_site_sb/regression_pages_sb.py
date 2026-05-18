# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.regression_pages_locators_sb import RegressionPagesLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class RegressionPagesSb(BasePageSb):
    def check_legal_pages(self):
        for url in L.LEGAL_PAGES:
            self.open_url(url)
            self.accept_cookie_consent()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            body_text = (self.driver.find_element(By.TAG_NAME, "body").text or "").strip()
            assert len(body_text) > 80, f"Legal page looks empty: {url}"

    def check_mobile_layouts(self):
        for width, height in L.MOBILE_VIEWPORTS:
            self.driver.set_window_size(width, height)
            for url in L.KEY_PAGES:
                self.open_url(url)
                self.accept_cookie_consent()
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                assert "sportbenefit.eu" in self.driver.current_url, (
                    f"Unexpected URL on viewport {width}x{height}: {self.driver.current_url}"
                )
                header_links = self.driver.find_elements(By.CSS_SELECTOR, "header a[href]")
                assert len(header_links) >= 1, f"Header links missing on {url} [{width}x{height}]"

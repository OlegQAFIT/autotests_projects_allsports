# -*- coding: utf-8 -*-
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.for_smoke_pages_sb import SmokePagesLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class SmokePagesSb(BasePageSb):
    def run_post_release_smoke_ui(self):
        for page_url in L.UI_PAGES:
            self.open_url(page_url)
            self.accept_cookie_consent()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(L.PAGE_ROOT))
            assert "sportbenefit.eu" in self.driver.current_url, f"Unexpected host: {self.driver.current_url}"

    def run_post_release_smoke_http(self):
        for page_url in L.HTTP_PAGES:
            response = requests.get(page_url, timeout=25, allow_redirects=True)
            assert response.status_code == 200, f"{page_url} returned {response.status_code}"

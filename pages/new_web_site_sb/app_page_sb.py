# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.elements_for_new_web_site_sb.for_app_page_sb import AppPageLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class AppPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(L.PAGE_ROOT))
        return self

    def check_page_opened(self):
        assert "/app" in self.driver.current_url, f"Unexpected app URL: {self.driver.current_url}"
        self.assert_element_present(L.DOWNLOAD_HEADING)

    def check_store_links(self):
        apple = self.driver.find_elements(*L.APPLE_LINKS)
        google = self.driver.find_elements(*L.GOOGLE_LINKS)
        huawei = self.driver.find_elements(*L.HUAWEI_LINKS)
        apk = self.driver.find_elements(*L.APK_LINKS)

        assert apple, "App Store links are missing"
        assert google, "Google Play links are missing"
        assert huawei, "Huawei AppGallery links are missing"
        assert apk, "APK link is missing"

        for el in apple:
            href = (el.get_attribute("href") or "").strip()
            assert "apps.apple.com" in href, f"Invalid App Store href: {href}"
        for el in google:
            href = (el.get_attribute("href") or "").strip()
            assert "play.google.com" in href, f"Invalid Google Play href: {href}"
        for el in huawei:
            href = (el.get_attribute("href") or "").strip()
            assert "appgallery.huawei.com" in href, f"Invalid AppGallery href: {href}"
        for el in apk:
            href = (el.get_attribute("href") or "").strip()
            assert href.endswith(".apk"), f"Invalid APK href: {href}"

    def check_meta(self):
        title = self.driver.title.strip()
        assert title, "Title for /app is empty"
        assert "sportbenefit" in title.lower(), f"Title does not contain SportBenefit: {title}"

        description = self.driver.execute_script(
            "const m=document.querySelector('meta[name=\"description\"]'); return m ? (m.content || '').trim() : '';"
        )
        assert description, "meta description for /app is empty"

    def check_canonical(self):
        self.assert_canonical_matches_current()

    def check_no_severe_console_errors(self):
        self.assert_no_severe_console_errors()

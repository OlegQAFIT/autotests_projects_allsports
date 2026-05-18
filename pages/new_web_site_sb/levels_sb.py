# -*- coding: utf-8 -*-

from locators.elements_for_new_web_site_sb.for_levels_page_sb import LevelsLocatorsSb as L
from pages.new_web_site_sb.base_page_sb import BasePageSb


class LevelsPageSb(BasePageSb):
    def open(self):
        self.open_url(L.BASE_URL)
        return self

    def check_levels_cards_present(self):
        cards = self.driver.find_elements(*L.LEVEL_CARDS)
        assert len(cards) >= 4, f"Expected at least 4 level cards, got {len(cards)}"

        titles = []
        for card in cards:
            title_elements = card.find_elements(*L.LEVEL_CARD_TITLE)
            if title_elements:
                titles.append((title_elements[0].text or "").strip())

        expected_names = {"VIP", "Platinum", "Gold", "Silver"}
        assert expected_names.issubset(set(titles)), f"Missing membership cards. Found: {titles}"

    def check_levels_card_links(self):
        cards = self.driver.find_elements(*L.LEVEL_CARDS)
        assert cards, "No cards found on levels page"

        for card in cards:
            links = [(a.get_attribute("href") or "").strip() for a in card.find_elements(*L.LEVEL_CARD_LINKS)]
            assert any("/en-cy/facilities?level=" in href for href in links), (
                f"Facilities link is missing in card links: {links}"
            )
            assert any("/en-cy/facilities-table" in href for href in links), (
                f"Facilities-table link is missing in card links: {links}"
            )

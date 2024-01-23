import allure

from pages.web_site_old.local import Local


@allure.feature('Localization')
@allure.severity('critical')
@allure.story('Test Russian Text on Armenian Page')
def test_found_ru_text_on_am_page(driver):
    """
    Test to check the absence of Russian text on the Armenian page.
    """
    local_am = Local(driver)
    local_am.open()
    local_am.drop_click_local_am()
    local_am.assert_no_russian_words_on_am_locale()
    local_am.click_on_objects_page()
    local_am.assert_no_russian_words_on_am_locale()
    local_am.click_on_subscription_types_page()
    local_am.assert_no_russian_words_on_am_locale()
    local_am.click_on_view_oll_buttom()
    local_am.assert_no_russian_words_on_am_locale()
    local_am.click_on_view_oll_buttom()
    local_am.assert_no_russian_words_on_am_locale()
    local_am.click_on_close_buttom()
    local_am.click_on_become_partner_page()
    local_am.assert_no_russian_words_on_am_locale()
    local_am.click_on_contacts_page()
    local_am.assert_no_russian_words_on_am_locale()


@allure.feature('Localization')
@allure.severity('normal')
@allure.story('Test Russian Text on Armenian-English Page')
def test_found_ru_text_on_am_en_page(driver):
    """
    Test to verify the absence of Russian text on the Armenian-English page.
    """
    local_am_en = Local(driver)
    local_am_en.open()
    local_am_en.drop_click_local_am_en()
    local_am_en.assert_no_russian_words_on_am_en_locale()


@allure.feature('Localization')
@allure.severity('minor')
@allure.story('Test Armenian Text on Russian Page')
def test_found_am_text_on_ru_page(driver):
    """
    Test to ensure the absence of Armenian text on the Russian page.
    """
    local_ru = Local(driver)
    local_ru.open()
    local_ru.drop_click_local_ru()
    local_ru.assert_no_armenia_words_on_ru_locale()


@allure.feature('Localization')
@allure.severity('blocker')
@allure.story('Test Russian Text on Belarusian Page')
def test_found_ru_text_on_by_page(driver):
    """
    Test to validate the absence of Russian text on the Belarusian page.
    """
    local_by = Local(driver)
    local_by.open()
    local_by.assert_no_armenia_words_on_by_locale()


@allure.feature('Localization')
@allure.severity('critical')
@allure.story('Test Armenian Text on Belarusian Page')
def test_found_am_text_on_by_page(driver):
    """
    Test to check the absence of Armenian text on the Belarusian page.
    """
    local_by = Local(driver)
    local_by.open()
    local_by.assert_no_armenia_words_on_by_locale()

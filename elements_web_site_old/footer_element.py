import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.base import BasePage
from locators.web_site_old.for_footer_testing import FooterLocators


class FooterElement(BasePage, FooterLocators):

    def __init__(self, driver):
        self.driver = driver
        self.main_window_handle = None

    @allure.step("Open the website")
    def open(self):
        self.driver.get('https://www.allsports.fit/by/')

    @allure.step("Click on 'Instagram' link")
    def click_on_instagram(self):
        self.click_on(self.INSTAGRAM)

    @allure.step("Click on 'Docs' link")
    def click_on_docs(self):
        self.click_on(self.USER_AGREEMENTS)

    @allure.step("Click on 'LinkedIn' link")
    def click_on_linkedin(self):
        self.click_on(self.LINKEDIN)

    @allure.step("Click on 'Employees' page")
    def click_on_employees_page(self):
        self.click_on(self.BUTTON_EMPLOYEE)

    @allure.step("Click on 'Partners' page")
    def click_on_partners_page(self):
        self.click_on(self.BUTTON_FOR_PARTNERS)

    @allure.step("Click on 'Contacts' page")
    def click_on_contacts_page(self):
        self.click_on(self.BUTTON_CONTACTS)

    @allure.step("Click on 'Agreements' page")
    def click_on_agreements_page(self):
        self.click_on(self.USER_AGREEMENTS)

    @allure.step("Click on 'Legal Documents' page")
    def click_on_legal_documents_page(self):
        self.click_on(self.DOCUMENTS_FOR_LEGAL_ENTITIES)

    @allure.step("Click on 'Company' page")
    def click_on_company_page(self):
        self.click_on(self.BUTTON_COMPANY)

    @allure.step("Click on 'Objects' page")
    def click_on_objects_page(self):
        self.click_on(self.BUTTON_OBJECTS)

    @allure.step("Click on 'Blog' page")
    def click_on_blog_page(self):
        self.click_on(self.BUTTON_BLOG)

    @allure.step("Assert dok")
    def assert_dok(self, file):
        documents = {
            "Индивидуальные лицензии": "/by/individual_license/220316_license/",
            "Политика в отношении обработки персональных данных": "/by/policy/220218_processing_personal_data/",
            "Правила доступа в спортивные объекты": "/by/rule/230801_rule/"
        }

        if file in documents:
            link = documents[file]
            try:
                element_present = EC.presence_of_element_located((By.XPATH, f"//a[@href='{link}']"))
                WebDriverWait(self.driver, 10).until(element_present)
                print(f"Документ '{file}' найден на странице.")
            except:
                print(f"Ссылка на документ '{file}' не найдена на странице.")
                assert False, f"Ссылка на документ '{file}' не найдена на странице."
        else:
            print(f"Документ '{file}' не существует.")
            assert False, f"Документ '{file}' не существует."

    @allure.step("Assert Instagram")
    def assert_instagram(self):
        current_url = self.get_current_url()
        print("Текущий URL (instagram):", current_url)
        assert self.get_current_url() == 'https://www.instagram.com/allsports.fit/'

    @allure.step("Assert LinkedIn")
    def assert_LinkedIn(self):
        current_url = self.get_current_url()
        print("Текущий URL (LinkedIn):", current_url)
        assert self.get_current_url() == 'https://www.linkedin.com/company/allsportsby'

    @allure.step("Assert phone numbers and email")
    def assert_phone_numbers_email(self):
        self.assert_element_text_equal(self.CONTACT_NUMBER, '+375 (44) 525-38-92')
        self.assert_element_text_equal(self.CONTACT_EMAIL, 'contact@allsports.by')

    @allure.step("Assert text in 'Employees' page")
    def assert_text_in_page_employees(self):
        self.assert_element_text_equal(self.SUBSCRIPTION_TYPES, 'Типы подписки')

    @allure.step("Assert text in 'Partners' page")
    def assert_text_in_page_partners(self):
        self.assert_element_text_equal(self.PARTNER, 'Что Allsports дает вашему фитнес-клубу?')

    @allure.step("Assert phone")
    def assert_phone(self):
        self.assert_text_in_element(self.ACT_RESULT, self.EXPECTED_RESULT_TEXT)

    @allure.step("Assert text in Legal 'Documents' page")
    def assert_text_in_page_documents(self):
        self.assert_element_text_equal(self.ELEMENT_IN_PERSONAL_INFORMATION, 'Политика в отношении обработки персональных данных')

    @allure.step("Assert element")
    def assert_element(self):
        self.wait_for_element_is_displayed(self.FOUND_ELEMENTS_DELETE)

    @allure.step("Assert element in 'Blog' page")
    def assert_element_blog(self):
        self.wait_for_element_is_displayed(self.ELEMENT_IN_BLOG_PAGE)

    @allure.step("Check the 'Companies' page")
    def assert_companies_page(self):
        self.wait_for_element_is_displayed(self.COMPANIES_PAGE)

    @allure.step("Switch to New Window instagram")
    def switch_to_new_window_with_instagram(self):
        self.switch_to_new_window()

    @allure.step("Switch to New Window linkedin")
    def switch_to_new_window_with_linkedin(self):
        self.switch_to_new_window()

    @allure.step("Click on read document first")
    def click_on_docs(self):
        self.hard_click(self.READ_FILE_1)

    @allure.step("Click on read document second")
    def click_on_docs(self):
        self.hard_click(self.READ_FILE_2)

    @allure.step("Click on read document three")
    def click_on_docs(self):
        self.hard_click(self.READ_FILE_3)

    @allure.step("Click on read document first")
    def click_on_read_buttom(self):
        self.hard_click(self.READ_FILE_1)

    @allure.step("Click on 'Read 2' button")
    def click_on_read_2_buttom(self):
        self.hard_click(self.READ_FILE_2)

    @allure.step("Open 'Individual Licenses' document")
    def open_doc_individual_licenses(self):
        self.wait_for_element_is_displayed(self.ELEMENT_IN_LICENSES_DOC)

    @allure.step("Assert 'Individual Licenses' document URL")
    def assert_doc_individual_licenses_url(self):
        current_url = self.get_current_url()
        print("Текущий URL (individual licenses):", current_url)
        assert self.get_current_url() == 'https://www.allsports.fit/by/individual_license/220316_license/'

    @allure.step("Open 'Personal Information' document")
    def open_doc_personal_information(self):
        self.wait_for_element_is_displayed(self.ELEMENT_IN_PERSONAL_INFORMATION)

    @allure.step("Check text in 'Personal Information' document")
    def text_checking(self):
        self.assert_text_in_element(self.ELEMENT_IN_PERSONAL_INFORMATION_DOC_FOR_TEXT, self.TEXT)

    @allure.step("Assert 'Personal Information' document URL")
    def assert_doc_personal_information_url(self):
        current_url = self.get_current_url()
        print("Текущий URL (personal information):", current_url)
        assert self.get_current_url() == 'https://www.allsports.fit/by/policy/220218_processing_personal_data/'

    @allure.step("Assert text for date checking")
    def assert_text_checking_date(self):
        self.assert_text_in_element(self.CHECK_DATE, self.TEXT_DATE)

    @allure.step("Click on Date 2")
    def click_on_date_2(self):
        self.hard_click(self.DATE_2)

    @allure.step("Assert text for date 2 checking")
    def assert_text_checking_date_2(self):
        self.assert_text_in_element(self.CHECK_DATE_2, self.TEXT_DATE_2)

    @allure.step("Click on Date 3")
    def click_on_date_3(self):
        self.hard_click(self.DATE_3)

    @allure.step("Assert text for Date 3 checking")
    def assert_text_checking_date_3(self):
        self.assert_text_in_element(self.CHECK_DATE_3, self.TEXT_DATE_3)

    @allure.step("Click on 'Read' button 3")
    def click_on_read_buttom_3(self):
        self.hard_click(self.READ_FILE_3)

    @allure.step("Open 'Access Rules' document")
    def open_doc_access_rules(self):
        self.wait_for_element_is_displayed(self.ELEMENT_IN_ACCESS_RULES)

    @allure.step("Assert 'Access Rules' document URL")
    def assert_doc_access_rules_url(self):
        current_url = self.get_current_url()
        print("Текущий URL (access rules):", current_url)
        assert self.get_current_url() == 'https://www.allsports.fit/by/rule/230801_rule/'

    def click_on_legal_documents_personal_information(self):
        self.hard_click(self.DATE_3)

    @allure.step("Click on 'Read' button for Access Rules")
    def click_on_read_buttom_access_rules(self):
        self.hard_click(self.READ_FILE_ACCESS_RULES_1)

    @allure.step("Click on 'Read' button for Access Rules 2")
    def click_on_read_buttom_access_rules_2(self):
        self.hard_click(self.READ_FILE_ACCESS_RULES_2)

    @allure.step("Click on Date 2 for Access Rules")
    def click_on_date_2_access_rules(self):
        self.hard_click(self.READ_FILE_ACCESS_RULES_1)

    @allure.step("Assert 'Access Rules' URL")
    def assert_access_rules_url(self):
        current_url = self.get_current_url()
        print("Текущий URL (22.02.18):", current_url)
        assert self.get_current_url() == 'https://www.allsports.fit/by/policy/220218_processing_personal_data/'

    @allure.step("Click on Date 2 for Access")
    def click_on_date_2_access(self):
        self.hard_click(self.DATE_ACCESS_2)

    @allure.step("Assert 'Access Rules' URL 1")
    def assert_access_rules_url_1(self):
        current_url = self.get_current_url()
        print("Текущий URL (22.01.27):", current_url)
        assert self.get_current_url() == 'https://www.allsports.fit/by/policy/220127_processing_personal_data/'

    @allure.step("Click on Date 3 for Access")
    def click_on_date_3_access(self):
        self.hard_click(self.DATE_ACCESS_3)

    @allure.step("Assert 'Access Rules' URL 2")
    def assert_access_rules_url_2(self):
        current_url = self.get_current_url()
        print("Текущий URL (21.11.15):", current_url)
        assert self.get_current_url() == 'https://www.allsports.fit/by/policy/211115_policy/'

    @allure.step("Click on 'Read' button 2 for Access Rules")
    def click_on_read_buttom_2_access_rules(self):
        self.hard_click(self.READ_FILE_ACCESS_RULES_2)

    @allure.step("Assert 'Access Rules' and Element URL 2")
    def assert_access_rules_and_alement_url_2(self):
        current_url = self.get_current_url()
        print("Текущий URL (license):", current_url)
        assert self.get_current_url() == 'https://www.allsports.fit/by/license/230306_license/'

    @allure.step("Open 'Access Rules' Page 2")
    def open_doc_access_rules_page_2(self):
        self.wait_for_element_is_displayed(self.ELEMENT_IN_ACCESS_RULES_2)

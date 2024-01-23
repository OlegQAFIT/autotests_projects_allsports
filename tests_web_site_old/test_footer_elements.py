import allure

from elements_web_site_old import FooterElement


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking social media links')
def test_soc_links_instagram(driver):
    """
    Checking social media links instagram
    """
    soc_media = FooterElement(driver)
    soc_media.open()
    soc_media.click_on_instagram()
    soc_media.switch_to_new_window_with_instagram()
    soc_media.assert_instagram()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking social media links')
def test_soc_links_linkedin(driver):
    """
    Checking social media links linkedin
    """
    soc_media = FooterElement(driver)
    soc_media.open()
    soc_media.click_on_linkedin()
    soc_media.switch_to_new_window_with_linkedin()
    soc_media.assert_LinkedIn()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking phone numbers and email')
def test_current_number_alert(driver):
    """
    Checking the unique number and alert
    """
    checking_number = FooterElement(driver)
    checking_number.open()
    checking_number.assert_phone_numbers_email()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking the employee page')
def test_checking_the_employee_page(driver):
    """
    Checking the opening in the footer of the page for employees
    """
    open_page_for_employees = FooterElement(driver)
    open_page_for_employees.open()
    open_page_for_employees.click_on_employees_page()
    open_page_for_employees.assert_text_in_page_employees()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking the partner page')
def test_checking_for_partners_page(driver):
    """
    Checking the opening in the footer of the page for partners
    """
    open_page_for_partners = FooterElement(driver)
    open_page_for_partners.open()
    open_page_for_partners.click_on_partners_page()
    open_page_for_partners.assert_text_in_page_partners()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking the correct phone number')
def test_checking_the_correct_phone_number(driver):
    """
    We check on the contact page, the correct phone number
    """
    check_phone = FooterElement(driver)
    check_phone.open()
    check_phone.click_on_contacts_page()
    check_phone.assert_phone()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking an existing document')
def test_checking_an_existing_document(driver):
    """
    We check in the documentation tab that there is a document with the name -"Индивидуальные лицензии"
    """
    found_text = FooterElement(driver)
    found_text.open()
    found_text.click_on_agreements_page()
    found_text.assert_dok("Индивидуальные лицензии")
    found_text.assert_dok("Политика в отношении обработки персональных данных")
    found_text.assert_dok("Правила доступа в спортивные объекты")


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking legal documents page')
def test_checking_legal_documents_page(driver):
    """
    Checking the opening of a page with documents for legal entities
    """
    check_legal_documents = FooterElement(driver)
    check_legal_documents.open()
    check_legal_documents.click_on_legal_documents_page()
    check_legal_documents.assert_text_in_page_documents()


@allure.feature("Company Page")
@allure.severity("normal")
@allure.story("Checking the opening of a page for companies")
def test_checking_legal_company_page(driver):
    """
    Checking the opening of a page for company's
    """
    check_company_page = FooterElement(driver)
    check_company_page.open()
    check_company_page.click_on_company_page()
    check_company_page.assert_companies_page()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking objects page')
def test_with_objects_page(driver):
    """
    Checking the opening of a page with objects
    """
    check_objects_page = FooterElement(driver)
    check_objects_page.open()
    check_objects_page.click_on_objects_page()
    check_objects_page.assert_element()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking blog page')
def test_with_blog_page(driver):
    """
    Checking the search for a button in the footer and when clicked, goes to the blog tab
    """
    check_blog_page = FooterElement(driver)
    check_blog_page.open()
    check_blog_page.click_on_blog_page()
    check_blog_page.assert_element_blog()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking individual licenses document')
def test_individual_licenses_doc(driver):
    """
    Test to verify the individual licenses document
    """
    check_individual_licenses = FooterElement(driver)
    check_individual_licenses.open()
    check_individual_licenses.click_on_agreements_page()
    check_individual_licenses.click_on_read_buttom()
    check_individual_licenses.open_doc_individual_licenses()
    check_individual_licenses.assert_doc_individual_licenses_url()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking personal information document')
def test_personal_information_doc(driver):
    """
    Test to check the personal information document
    """
    check_personal_information = FooterElement(driver)
    check_personal_information.open()
    check_personal_information.click_on_agreements_page()
    check_personal_information.click_on_read_2_buttom()
    check_personal_information.open_doc_personal_information()
    check_personal_information.text_checking()
    check_personal_information.assert_doc_personal_information_url()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking documents by date')
def test_checking_documents_by_date(driver):
    """
    Test to verify the documents by date
    """
    check_documents = FooterElement(driver)
    check_documents.open()
    check_documents.click_on_agreements_page()
    check_documents.click_on_read_2_buttom()
    check_documents.assert_text_checking_date()
    check_documents.click_on_date_2()
    check_documents.assert_text_checking_date_2()
    check_documents.click_on_date_3()
    check_documents.assert_text_checking_date_3()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking access rules document')
def test_access_rules_doc(driver):
    """
    Test to verify the access rules document
    """
    # Тело теста...
    check_access_rules_document = FooterElement(driver)
    check_access_rules_document.open()
    check_access_rules_document.click_on_agreements_page()
    check_access_rules_document.click_on_read_buttom_3()
    check_access_rules_document.open_doc_access_rules()
    check_access_rules_document.assert_doc_access_rules_url()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking legal documents on the personal information page')
def test_checking_legal_documents_personal_information_page(driver):
    """
    Test to check legal documents on the personal information page
    """
    legal_documents_personal_information = FooterElement(driver)
    legal_documents_personal_information.open()
    legal_documents_personal_information.click_on_legal_documents_page()
    legal_documents_personal_information.click_on_read_buttom_access_rules()
    legal_documents_personal_information.assert_access_rules_url()
    legal_documents_personal_information.click_on_date_2_access()
    legal_documents_personal_information.assert_access_rules_url_1()
    legal_documents_personal_information.click_on_date_3_access()
    legal_documents_personal_information.assert_access_rules_url_2()


@allure.feature('Footer Links')
@allure.severity('critical')
@allure.story('Checking legal documents on the personal information page - 2')
def test_checking_legal_documents_personal_information_page_2(driver):
    """
    Another test to check legal documents on the personal information page
    """
    legal_documents_personal_information = FooterElement(driver)
    legal_documents_personal_information.open()
    legal_documents_personal_information.click_on_legal_documents_page()
    legal_documents_personal_information.click_on_read_buttom_2_access_rules()
    legal_documents_personal_information.open_doc_access_rules_page_2()
    legal_documents_personal_information.assert_access_rules_and_alement_url_2()

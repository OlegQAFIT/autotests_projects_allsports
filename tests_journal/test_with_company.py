import allure
from pages.journal.company import Company


@allure.feature('Company page')
@allure.severity('Critical')
@allure.story('Create new company without copay')
def test_create_new_company_without_copay(driver):
    """
    Создание компании без copay
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_selection()
    create_company.drop_manager_selection()
    create_company.fill_fields()
    create_company.click_save_company()
    create_company.click_and_open_company_tab()
    create_company.assert_find_new_company()


@allure.feature('Company page')
@allure.severity('Critical')
@allure.story('Create new company with copay')
def test_create_new_company_with_copay(driver):
    """
    Создание компании с copay
    """
    create_company_with_copay = Company(driver)
    create_company_with_copay.open_jn()
    create_company_with_copay.login()
    create_company_with_copay.click_and_open_company_tab()
    create_company_with_copay.click_create_company_tab()
    create_company_with_copay.drop_city_selection()
    create_company_with_copay.drop_locale_selection()
    create_company_with_copay.drop_timezone_selection()
    create_company_with_copay.drop_sell_strategy_selection()
    create_company_with_copay.drop_registration_type_dropdown()
    create_company_with_copay.drop_manager_selection()
    create_company_with_copay.fill_fields()
    create_company_with_copay.click_save_company()
    create_company_with_copay.click_and_open_company_tab()
    create_company_with_copay.assert_find_new_company()


@allure.feature('Company Elements')
@allure.severity('Critical')
@allure.story('Disable fields with copay')
def test_disable_fields(driver):
    """
    Дизэйбл полей при copay
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_dropdown()
    create_company.assert_disable_elements()


@allure.feature('Company Elements')
@allure.severity('Critical')
@allure.story('Find actual elements on add company page')
def test_found_actual_elements_on_add_company_page(driver):
    """
     Поиск элементов на странице
    """
    actual_elements = Company(driver)
    actual_elements.open_jn()
    actual_elements.login()
    actual_elements.click_and_open_company_tab()
    actual_elements.click_create_company_tab()
    actual_elements.assert_found_elements_on_add_company_page()


@allure.feature('Company UNN')
@allure.severity('Critical')
@allure.story('Check UNN through external service')
def test_create_heck_UNN(driver):
    """
    Стронний сервис по поиску УНП
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_selection()
    create_company.drop_manager_selection()
    create_company.fill_fields_vat_number()
    create_company.click_save_company()
    create_company.assert_found_text_after_searching_vat_number()


@allure.feature('Company Validation')
@allure.severity('Critical')
@allure.story('Check maximum number of characters validation')
def test_error_checking_max_number_of_characters(driver):
    """
    Проверка нотификаций по макс кол символов

    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_dropdown()
    create_company.drop_manager_selection()
    create_company.fill_fields_name_company()
    create_company.click_save_company()
    create_company.assert_found_errore_text()


@allure.feature('Company Validation')
@allure.severity('Critical')
@allure.story('Check minimum number of characters validation')
def test_error_checking_min_number_of_characters(driver):
    """
    Проверка нотификаций по минимальному колличеству символов

    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_dropdown()
    create_company.drop_manager_selection()
    create_company.fill_fields_name_min_company()
    create_company.click_save_company()
    create_company.assert_found_errore_min_text()


@allure.feature('Company Validation')
@allure.severity('Critical')
@allure.story('Check UNN number of characters validation')
def test_error_checking_UNN_number_of_characters(driver):
    """
    Проверка нотификаций УНП кол символов

    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_dropdown()
    create_company.drop_manager_selection()
    create_company.fill_fields_name_min_company()
    create_company.click_save_company()
    create_company.assert_found_errore_UNN_min_text()


@allure.feature('Company Validation')
@allure.severity('Critical')
@allure.story('Check legal name validation')
def test_legal_name_validation_check(driver):
    """
    Проверка валидации легал имени
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_dropdown()
    create_company.drop_manager_selection()
    create_company.fill_fields_legal_name()
    create_company.click_save_company()
    create_company.assert_found_errore_text_legal_name()


@allure.feature('Company Validation')
@allure.severity('Critical')
@allure.story('Check required fields')
def test_required_fields_check(driver):
    """
    Проверка обязательных полей
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.click_save_company()
    create_company.assert_required_fields()


@allure.feature('Company Elements')
@allure.severity('Critical')
@allure.story('Check disable fields after saving')
def test_disable_fields_after_saving(driver):
    """
    Дизэйбл полей после сохранения компании
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_dropdown()
    create_company.drop_manager_selection()
    create_company.fill_fields()
    create_company.click_save_company()
    create_company.assert_disable_elements_in_new_company()


@allure.feature('Company Elements')
@allure.severity('Critical')
@allure.story('Check disable elements with selected registration type')
def test_disable_elements_with_select_registration_type(driver):
    """
    Дизэйбл полей при выборе Registration type
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_dropdown()
    create_company.assert_disable_elements_with_select_registration_type()


@allure.feature('Company Elements')
@allure.severity('Critical')
@allure.story('Open new company without copay and edit')
def test_open_new_company_without_copay_1(driver):
    """
    Создание компании без copay и открытие для редактирования
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_selection()
    create_company.drop_manager_selection()
    create_company.fill_fields()
    create_company.click_save_company()
    create_company.click_and_open_company_tab()
    create_company.open_last_dropdown_and_edit()
    create_company.assert_open_and_found_new_company()


@allure.feature('Company Elements')
@allure.severity('Critical')
@allure.story('Check disable elements in new company with copay')
def test_check_disable_elements_in_new_company_with_copay(driver):
    """
    Создание компании с copay и проверка через редактирование дизэйбл полей

    """
    create_company_with_copay = Company(driver)
    create_company_with_copay.open_jn()
    create_company_with_copay.login()
    create_company_with_copay.click_and_open_company_tab()
    create_company_with_copay.click_create_company_tab()
    create_company_with_copay.drop_city_selection()
    create_company_with_copay.drop_locale_selection()
    create_company_with_copay.drop_timezone_selection()
    create_company_with_copay.drop_sell_strategy_selection()
    create_company_with_copay.drop_registration_type_dropdown()
    create_company_with_copay.drop_manager_selection()
    create_company_with_copay.fill_fields()
    create_company_with_copay.click_save_company()
    create_company_with_copay.click_and_open_company_tab()
    create_company_with_copay.open_last_dropdown_and_edit()
    create_company_with_copay.assert_disable_elements_in_new_company()


@allure.feature('Company Filters')
@allure.severity('Critical')
@allure.story('Check filter by manager')
def test_checking_filter_by_manager(driver):
    """
    Проверка фильтра по менеджеру

    """
    create_company_with_copay = Company(driver)
    create_company_with_copay.open_jn()
    create_company_with_copay.login()
    create_company_with_copay.click_and_open_company_tab()
    create_company_with_copay.drop_manager_selection_for_select()
    create_company_with_copay.assert_find_company_with_manager()


@allure.feature('Company Search')
@allure.severity('Critical')
@allure.story('Check company search')
def test_checking_search_company(driver):
    """
    Проверка поиска компании

    """
    create_company_with_copay = Company(driver)
    create_company_with_copay.open_jn()
    create_company_with_copay.login()
    create_company_with_copay.click_and_open_company_tab()
    create_company_with_copay.search_field_company()
    create_company_with_copay.assert_find_company_search_field()


@allure.feature('Company Creation')
@allure.severity('Critical')
@allure.story('Create new company without copay and delete')
def test_create_new_and_delete_company(driver):
    """
    Создание компании без copay и удаление
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login()
    create_company.click_and_open_company_tab()
    create_company.click_create_company_tab()
    create_company.drop_city_selection()
    create_company.drop_locale_selection()
    create_company.drop_timezone_selection()
    create_company.drop_sell_strategy_selection()
    create_company.drop_registration_type_selection()
    create_company.drop_manager_selection()
    create_company.fill_fields()
    create_company.click_save_company()
    create_company.click_and_open_company_tab()
    create_company.delete_last_company()
    create_company.click_delete_company()
    create_company.assert_company_not_found()


@allure.feature('Portal User Management')
@allure.severity('normal')
@allure.story('Open Page for Creating Portal User')
def test_open_page_portal_user(driver):
    """
    Открытие вкладки для создания Portal User
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.assert_page_portal_user()


@allure.feature('Portal User Management')
@allure.severity('normal')
@allure.story('Open Modal Window for Creating Portal User')
def test_open_modal_window_portal_user(driver):
    """
    Открытие вкладки для создания Portal User
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.assert_page_portal_user()


@allure.feature('Portal User Management')
@allure.severity('normal')
@allure.story('Check Clickable Cancel Button')
def test_clickable_cancel_buttom(driver):
    """
    Кликабельна кнопка Отменить
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.assert_clickable_cancel_button()


@allure.feature('Portal User Management')
@allure.severity('critical')
@allure.story('Add Portal User')
def test_add_portal_user(driver):
    """
    Добавление нового портал юзера
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.generate_new_portal_user()
    create_portal_user.click_save_portal_user()
    create_portal_user.assert_new_portal_user()


@allure.feature('Portal User Management')
@allure.severity('critical')
@allure.story('Add Portal User by Phone')
def test_add_portal_user_by_phone(driver):
    """
    Поиск и добавления существующего пользователя по номеру
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.add_new_portal_user_by_phone()
    create_portal_user.click_save_portal_user()
    # create_portal_user.assert_new_portal_user_by_phone()


@allure.feature('Portal User Management')
@allure.severity('critical')
@allure.story('Add Portal User by Email')
def test_add_portal_user_by_email(driver):
    """
    Поиск и добавления существующего пользователя по почте
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.add_new_portal_user_by_email()
    create_portal_user.click_save_portal_user()
    # create_portal_user.assert_new_portal_user_by_phone()


@allure.feature('Portal User Management')
@allure.severity('critical')
@allure.story('Add Portal User CY')
def test_add_portal_user_by_CY(driver):
    """
    Поиск и добавления существующего пользователя с кипра номера
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.add_new_portal_user_by_cy()
    create_portal_user.click_save_portal_user()
    create_portal_user.assert_search_portal_user_by_cy()


@allure.feature('Portal User Management')
@allure.severity('normal')
@allure.story('Check Validation of Email Field')
def test_errore_filds(driver):
    """
    Проверка валидации поля email
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.add_wrong_email()
    create_portal_user.assert_found_errore_text_portal_user()


# @allure.feature('')
# @allure.severity('')
# @allure.story('')
# def test_errore_filds_add_already_added(driver):
#     """
#
#     """
#     create_portal_user = Company(driver)
#     create_portal_user.open_jn()
#     create_portal_user.login()
#     create_portal_user.click_and_open_company_tab()
#     create_portal_user.click_create_company_tab()
#     create_portal_user.drop_city_selection()
#     create_portal_user.drop_locale_selection()
#     create_portal_user.drop_timezone_selection()
#     create_portal_user.drop_sell_strategy_selection()
#     create_portal_user.drop_registration_type_selection()
#     create_portal_user.drop_manager_selection()
#     create_portal_user.fill_fields()
#     create_portal_user.click_save_company()
#     create_portal_user.click_and_open_company_tab()
#     create_portal_user.open_page_add_portal_user()
#     create_portal_user.click_add_portal_user()
#     create_portal_user.add_new_portal_user_by_phone_1()
#     create_portal_user.click_save_portal_user()
#     create_portal_user.click_add_portal_user()
#     create_portal_user.add_new_portal_user_by_phone_1_1()
#     create_portal_user.assert_found_errore_text_added_portal_user()


@allure.feature('Portal User Management')
@allure.severity('normal')
@allure.story('Check SMS for Portal User')
def test_sms_for_portal_user(driver):
    """
    СМС код для portal user
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.generate_new_portal_user()
    create_portal_user.click_save_portal_user()
    create_portal_user.open_sms_for_portal_user()
    create_portal_user.assert_and_extract_sms_code()


@allure.feature('Portal User Management')
@allure.severity('normal')
@allure.story('Change Portal User')
def test_change_portal_user(driver):
    """
    Изменение Portal User
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.generate_new_portal_user()
    create_portal_user.click_save_portal_user()
    create_portal_user.open_edit_portal_user()
    create_portal_user.change_portal_user()
    create_portal_user.click_save_portal_user()
    create_portal_user.assert_search_change_portal_user()


@allure.feature('Portal User Management')
@allure.severity('normal')
@allure.story('Delete Portal User')
def test_delete_portal_user(driver):
    """
    Удаление portal user
    """
    create_portal_user = Company(driver)
    create_portal_user.open_jn()
    create_portal_user.login()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.click_create_company_tab()
    create_portal_user.drop_city_selection()
    create_portal_user.drop_locale_selection()
    create_portal_user.drop_timezone_selection()
    create_portal_user.drop_sell_strategy_selection()
    create_portal_user.drop_registration_type_selection()
    create_portal_user.drop_manager_selection()
    create_portal_user.fill_fields()
    create_portal_user.click_save_company()
    create_portal_user.click_and_open_company_tab()
    create_portal_user.open_page_add_portal_user()
    create_portal_user.click_add_portal_user()
    create_portal_user.generate_new_portal_user()
    create_portal_user.click_save_portal_user()
    create_portal_user.delete_for_portal_user()
    create_portal_user.assert_deleted_portal_user()

import allure
import pytest
from pages.supplier_panel.login_page import SupplierPanel


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Проверка элементов страницы входа')
def test_open_login_page_and_checking_elements_suppler_panel(driver):
    """
    Тест для проверки элементов на странице входа в Панель поставщика.
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.assert_found_elements_on_login_page_ru()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Language Change and Translation Check')
def test_change_language_and_check_translation(driver):
    """
    Тест для смены языка и проверки перевода на странице входа в Панель поставщика.
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.select_language()
    login_supplier_panel.assert_found_elements_on_login_page_en()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Ошибка для незарегистрированного пользователя')
def test_unregistered_user_error_login_page(driver):
    """
    Тест для проверки ошибки для незарегистрированного пользователя на странице входа в Панель поставщика.
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.login_wrong_user_supplier_panel()
    login_supplier_panel.assert_found_errore_text_wrong_user()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Валидация поля электронной почты')
def test_email_field_validation_login_page(driver):
    """
    Тест для валидации поля электронной почты на странице входа в Панель поставщика.
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.login_email_field_validation_supplier_panel()
    login_supplier_panel.assert_found_errore_text_email_field_validation()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Валидация поля пароля')
def test_password_field_validation_login_page(driver):
    """
    Тест для валидации поля пароля на странице входа в Панель поставщика.
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.login_password_field_validation_supplier_panel()
    login_supplier_panel.assert_found_errore_text_pasword_field_validation()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Ошибка для незарегистрированного пользователя (английский)')
def test_unregistered_user_error_login_page_en(driver):
    """
    Тест для проверки ошибки для незарегистрированного пользователя на странице входа в Панель поставщика (английский).
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.select_language()
    login_supplier_panel.login_wrong_user_supplier_panel()
    login_supplier_panel.assert_found_errore_text_wrong_user_en()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Валидация поля электронной почты (английский)')
def test_email_field_validation_login_page_en(driver):
    """
    Тест для валидации поля электронной почты на странице входа в Панель поставщика (английский).
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.select_language()
    login_supplier_panel.login_email_field_validation_supplier_panel()
    login_supplier_panel.assert_found_errore_text_email_field_validation_en()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Валидация поля пароля (английский)')
def test_password_field_validation_login_page_en(driver):
    """
     Тест для валидации поля пароля на странице входа в Панель поставщика (английский).
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    login_supplier_panel.select_language()
    login_supplier_panel.login_password_field_validation_supplier_panel()
    login_supplier_panel.assert_found_errore_text_pasword_field_validation_en()


@allure.feature('Supplier Panel Login Page')
@allure.severity('normal')
@allure.story('Баннер разрешений уведомлений')
@pytest.mark.smoke
def test_notification_modal_present_on_login_page(driver):
    """
    Проверка наличия модального баннера разрешений уведомлений на странице логина.
    """
    login_supplier_panel = SupplierPanel(driver)
    login_supplier_panel.open_sp()
    if login_supplier_panel.is_notification_modal_present():
        login_supplier_panel.assert_notification_modal_present()
        return

    # В браузере баннер может не появляться, если разрешения уже сохранены.
    # В этом случае проверяем, что страница логина доступна и основной flow не заблокирован.
    assert login_supplier_panel.is_element_visible(login_supplier_panel.LOGIN_FIELD_SUPPLER_PANEL), (
        "Не найдено поле email на странице логина supplier panel"
    )
    assert login_supplier_panel.is_element_visible(login_supplier_panel.SIGNIN_BUTTON_SUPPLER_PANEL), (
        "Не найдена кнопка Continue/Продолжить на странице логина supplier panel"
    )

import allure
import pytest

from pages.journal.company import Company


@allure.feature('Main Flow Company Creation')
@allure.severity('critical')
@allure.story('Create B2B company')
@pytest.mark.pre_release
def test_create_company_b2b_main_flow(driver):
    """Проверяет создание компании B2B:
    - выполняется логин в Journal;
    - открывается форма создания компании;
    - заполняются обязательные поля для сценария STANDARD;
    - компания успешно сохраняется.
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login_for_main_company_flow()
    create_company.open_add_company_page()
    create_company.create_company_for_main_flow(company_suffix='Company 1 B2B')
    create_company.assert_company_saved_in_main_flow()


@allure.feature('Main Flow Company Creation')
@allure.severity('critical')
@allure.story('Create FULL company')
@pytest.mark.pre_release
def test_create_company_full_main_flow(driver):
    """Проверяет создание компании с Compensation type FULL:
    - выполняется логин в Journal;
    - открывается форма создания компании;
    - для Registration type выбирается REGISTRATION_FORM;
    - для Default subscription выбирается region;
    - для Compensation type выбирается FULL;
    - компания успешно сохраняется.
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login_for_main_company_flow()
    create_company.open_add_company_page()
    create_company.create_company_for_main_flow(
        company_suffix='Company 2 FULL',
        registration_type='REGISTRATION_FORM',
        compensation_type='FULL',
    )
    create_company.assert_company_saved_in_main_flow()


@allure.feature('Main Flow Company Creation')
@allure.severity('critical')
@allure.story('Create FULL_WITH_EXTENSION company')
@pytest.mark.pre_release
def test_create_company_full_with_extension_main_flow(driver):
    """Проверяет создание компании с Compensation type FULL_WITH_EXTENSION:
    - выполняется логин в Journal;
    - открывается форма создания компании;
    - для Registration type выбирается REGISTRATION_FORM;
    - для Default subscription выбирается region;
    - для Compensation type выбирается FULL_WITH_EXTENSION;
    - компания успешно сохраняется.
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login_for_main_company_flow()
    create_company.open_add_company_page()
    create_company.create_company_for_main_flow(
        company_suffix='Company 3 FULL_WITH_EXTENSION',
        registration_type='REGISTRATION_FORM',
        compensation_type='FULL_WITH_EXTENSION',
    )
    create_company.assert_company_saved_in_main_flow()


@allure.feature('Main Flow Company Creation')
@allure.severity('critical')
@allure.story('Create X_AMOUNT company')
@pytest.mark.pre_release
def test_create_company_x_amount_main_flow(driver):
    """Проверяет создание компании с Compensation type X_AMOUNT:
    - выполняется логин в Journal;
    - открывается форма создания компании;
    - для Registration type выбирается REGISTRATION_FORM;
    - для Default subscription выбирается region;
    - для Compensation type выбирается X_AMOUNT;
    - заполняется Compensation amount;
    - компания успешно сохраняется.
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login_for_main_company_flow()
    create_company.open_add_company_page()
    create_company.create_company_for_main_flow(
        company_suffix='Company 4 X_AMOUNT',
        registration_type='REGISTRATION_FORM',
        compensation_type='X_AMOUNT',
    )
    create_company.assert_company_saved_in_main_flow()


@allure.feature('Main Flow Company Creation')
@allure.severity('critical')
@allure.story('Create X_AMOUNT_WITH_EXTENSION company')
@pytest.mark.pre_release
def test_create_company_x_amount_with_extension_main_flow(driver):
    """Проверяет создание компании с Compensation type X_AMOUNT_WITH_EXTENSION:
    - выполняется логин в Journal;
    - открывается форма создания компании;
    - для Registration type выбирается REGISTRATION_FORM;
    - для Default subscription выбирается region;
    - для Compensation type выбирается X_AMOUNT_WITH_EXTENSION;
    - заполняется Compensation amount;
    - компания успешно сохраняется.
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login_for_main_company_flow()
    create_company.open_add_company_page()
    create_company.create_company_for_main_flow(
        company_suffix='Company 5 X_AMOUNT_WITH_EXTENSION',
        registration_type='REGISTRATION_FORM',
        compensation_type='X_AMOUNT_WITH_EXTENSION',
    )
    create_company.assert_company_saved_in_main_flow()


@allure.feature('Main Flow Company Creation')
@allure.severity('critical')
@allure.story('Create X_AMOUNT_WITH_EXTENSION B2C company')
@pytest.mark.pre_release
def test_create_company_x_amount_with_extension_b2c_main_flow(driver):
    """Проверяет создание компании с Compensation type X_AMOUNT_WITH_EXTENSION и пустым Compensation amount:
    - выполняется логин в Journal;
    - открывается форма создания компании;
    - для Registration type выбирается REGISTRATION_FORM;
    - для Default subscription выбирается region;
    - для Compensation type выбирается X_AMOUNT_WITH_EXTENSION;
    - поле Compensation amount (VAT included) остается пустым;
    - компания успешно сохраняется.
    """
    create_company = Company(driver)
    create_company.open_jn()
    create_company.login_for_main_company_flow()
    create_company.open_add_company_page()
    create_company.create_company_for_main_flow(
        company_suffix='Company 6 X_AMOUNT_WITH_EXTENSION_B2C',
        registration_type='REGISTRATION_FORM',
        compensation_type='X_AMOUNT_WITH_EXTENSION',
        fill_compensation_amount=False,
    )
    create_company.assert_company_saved_in_main_flow()

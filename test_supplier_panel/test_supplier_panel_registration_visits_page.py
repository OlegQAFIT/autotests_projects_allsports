import os

import allure
import pytest
import requests
from pages.supplier_panel.registration_visits_page import SupplierPanelRegistrationVisits

SUPPLIER_VISITS_CHECK_URL = (
    "https://xn--80ann.xn--k1aahcehedi.xn--90ais/api/supplier/1.0.0/visits/check"
)

EXPECTED_WAITING_VISITS = [
    {
        "phone": "375440000100",
        "user_name": "Test AVT visit VIP",
        "level": "vip",
        "attraction_id": 17008,
        "attraction_name": "Водный мотоцикл",
        "status": "waiting",
    },
    {
        "phone": "375440000101",
        "user_name": "Test AVT visit PREMIUM",
        "level": "premium",
        "attraction_id": 16837,
        "attraction_name": "Кизомба",
        "status": "waiting",
    },
    {
        "phone": "375440000102",
        "user_name": "Test AVT visit classic",
        "level": "classic",
        "attraction_id": 17007,
        "attraction_name": "Водные лыжи",
        "status": "waiting",
    },
    {
        "phone": "375440000103",
        "user_name": "Test AVT visit LITE",
        "level": "lite",
        "attraction_id": 16838,
        "attraction_name": "Баня",
        "status": "waiting",
    },
    {
        "phone": "375440000104",
        "user_name": "Test AVT visit REGIN",
        "level": "region",
        "attraction_id": 17006,
        "attraction_name": "Пренатальная йога",
        "status": "waiting",
    },
]


def _normalize_bearer_token(token):
    normalized = str(token or "").strip()
    if normalized.lower().startswith("bearer "):
        return normalized
    return f"Bearer {normalized}" if normalized else ""


def _get_supplier_visits_check_response():
    token = _normalize_bearer_token(os.getenv("SUPPLIER_VISITS_CHECK_BEARER_TOKEN"))
    assert token, (
        "Укажите SUPPLIER_VISITS_CHECK_BEARER_TOKEN в Environment variables "
        "для проверки ожидаемых waiting-визитов в supplier panel."
    )

    response = requests.get(
        SUPPLIER_VISITS_CHECK_URL,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Authorization": token,
            "X-Localization": "ru",
        },
        timeout=30,
    )
    assert response.status_code == 200, (
        f"SUPPLIER VISITS CHECK API failed. status={response.status_code}, body={response.text}"
    )
    body = response.json()
    visits = body.get("visits")
    assert isinstance(visits, list), f"Response has no visits list: {body}"
    return visits


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Проверка элементов на панели поставщика')
@pytest.mark.parametrize("role", ["reception", "finance"])
def test_checking_elements_supplier_panel_ru(driver, role):
    """
    Тест для проверки элементов на панели поставщика на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel(role=role)
    registration_visits_supplier_panel.clear_pending_visits_if_any()
    registration_visits_supplier_panel.assert_found_elements_on_registrarion_visitspage_ru(role=role)


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Checking Elements on Supplier Panel')
@pytest.mark.parametrize("role", ["reception", "finance"])
def test_checking_elements_supplier_panel_en(driver, role):
    """
    Test to check elements on the Supplier Panel in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_supplier_panel(role=role)
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.clear_pending_visits_if_any()
    registration_visits_supplier_panel.assert_found_elements_on_registrarion_visitspage_en(role=role)


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Expected waiting visits arrived in supplier panel')
def test_expected_waiting_visits_arrived_in_supplier_panel_api():
    visits = _get_supplier_visits_check_response()

    actual_entries = {
        (
            visit.get("user", {}).get("name"),
            visit.get("user", {}).get("level"),
            visit.get("attraction", {}).get("id"),
            visit.get("attraction", {}).get("name"),
            visit.get("status"),
        )
        for visit in visits
        if isinstance(visit, dict)
    }

    missing_visits = []
    for expected in EXPECTED_WAITING_VISITS:
        expected_entry = (
            expected["user_name"],
            expected["level"],
            expected["attraction_id"],
            expected["attraction_name"],
            expected["status"],
        )
        if expected_entry not in actual_entries:
            missing_visits.append(
                f"{expected['phone']} / {expected['user_name']} / "
                f"{expected['level']} / attraction_id={expected['attraction_id']}"
            )

    assert not missing_visits, (
        "Не найдены ожидаемые waiting-визиты в supplier panel API: "
        + "; ".join(missing_visits)
    )


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Elements with Visit in Russian')
def test_elements_with_visit_ru(driver):
    """
    Тест элементов с визитом на панели поставщика на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.assert_found_elements_with_wisit_page_ru()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Elements with Visit in English')
def test_elements_with_visit_en(driver):
    """
    Test elements with a visit on the Supplier Panel in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.assert_found_elements_with_wisit_page_en()


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Элементы при отмене визита на русском')
def test_elements_when_cancel_visit_ru(driver):
    """
    Тест проверки элементов при отмене визита на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.click_reject_visit()
    registration_visits_supplier_panel.assert_found_elements_modal_reject_visit_page_ru()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Elements when canceling a visit in English')
def test_elements_when_cancel_visit_en(driver):
    """
    Test elements when canceling a visit in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit(
        phone_number="+375330000088",
        sms_code="4290",
        gym_token=None,
        attraction_id=16835,
        holder_id=41232,
        admin_token=os.getenv("SUPPLIER_JRNL_ADMIN_TOKEN"),
        supplier_id=5003,
        lat=53.90450845,
        lng=27.56395822,
    )
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.click_reject_visit_en()
    registration_visits_supplier_panel.assert_found_elements_modal_reject_visit_page_en()


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Отклонение визита на русском')
def test_reject_visit_ru(driver):
    """
    Тест отклонения визита на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.click_reject_visit()
    registration_visits_supplier_panel.enter_reason_visit()
    registration_visits_supplier_panel.click_save_reject_visit()
    registration_visits_supplier_panel.assert_registration_page_opened_after_reject(language="ru")


@allure.feature('Панель поставщика')
@allure.severity('critical')
@allure.story('Подтверждение визита на русском')
def test_confirm_visit_elements_ru(driver):
    """
    Тест элементов при подтверждении визита на русском языке.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.click_confirm_visit_ru()
    registration_visits_supplier_panel.assert_found_elements_on_confirm_visit_modal()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Confirming a visit in English')
def test_confirm_visit_elements_en(driver):
    """
    Test confirming a visit in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.click_confirm_visit_en()
    registration_visits_supplier_panel.assert_found_elements_on_confirm_visit_modal_en()


@allure.feature('Supplier Panel')
@allure.severity('critical')
@allure.story('Rejecting a visit in English')
def test_reject_visit_en(driver):
    """
    Test rejecting a visit in English.
    """
    registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
    registration_visits_supplier_panel.open_sp()
    registration_visits_supplier_panel.login_and_create_visit()
    registration_visits_supplier_panel.login_supplier_panel()
    registration_visits_supplier_panel.select_language()
    registration_visits_supplier_panel.click_reject_visit_en()
    registration_visits_supplier_panel.enter_reason_visit()
    registration_visits_supplier_panel.click_save_reject_visit_en()
    registration_visits_supplier_panel.assert_registration_page_opened_after_reject(language="en")


# @allure.feature('')
# @allure.severity('')
# @allure.story('')
# def test_confirm_visit_elements_without_foto_ru(driver):
#     """
#
#     """
#     registration_visits_supplier_panel = SupplierPanelRegistrationVisits(driver)
#     registration_visits_supplier_panel.open_sp()
#     registration_visits_supplier_panel.login_supplier_panel()
#     registration_visits_supplier_panel.test_login_and_create_visit_without_foto()
#     registration_visits_supplier_panel.click_confirm_visit_ru()
#     registration_visits_supplier_panel.assert_found_elements_on_confirm_visit_modal_en()

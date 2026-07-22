import os
import re
import time
import uuid
from datetime import datetime
from pathlib import Path

import allure
import pytest
import requests
from dotenv import load_dotenv
from pages.supplier_panel.registration_visits_page import SupplierPanelRegistrationVisits


load_dotenv()
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
SUPPLIER_PANEL_BASE_URL = "https://xn--80ann.xn--k1aahcehedi.xn--90ais"
MOBILE_API_PREFIX = "/api/holder/2.0.0"
CSRF_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/csrf-token"
REQUEST_SMS_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/request-sms"
CONFIRM_SMS_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/confirm-sms-code"
CREATE_VISIT_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/suppliers/visit"
ADMIN_LOGIN_URL = f"{BASE_URL}/api/admin_login"
SUPPLIER_VISITS_CHECK_URL = f"{SUPPLIER_PANEL_BASE_URL}/api/supplier/1.0.0/visits/check"
SUPPLIER_ACCEPTED_VISITS_URL = f"{SUPPLIER_PANEL_BASE_URL}/api/supplier/1.0.0/visits"
JOURNAL_VISITS_URL = f"{BASE_URL}/api/journal/"

SMS_CODE = os.getenv("CREATE_VISIT_SMS_CODE", "").strip()
ADMIN_TOKEN = os.getenv("SUPPLIER_JRNL_ADMIN_TOKEN", "").strip()
ADMIN_EMAIL = os.getenv("SUPPLIER_JRNL_EMAIL", "").strip() or "oleg.fit@gmail.com"
ADMIN_PASSWORD = os.getenv("SUPPLIER_JRNL_PASSWORD", "").strip() or "9efbee942864"
CY_SUPPLIER_LOGIN = os.getenv("CY_SUPPLIER_CONFIRM_LOGIN", "").strip() or "snsaggcddh@gmail.com"
CY_SUPPLIER_PASSWORD = os.getenv("CY_SUPPLIER_CONFIRM_PASSWORD", "").strip() or "12345678"
CY_JOURNAL_COUNTRY = os.getenv("CY_JOURNAL_COUNTRY", "cy").strip() or "cy"
CY_SUPPLIER_VISITS_CHECK_BEARER_TOKEN = os.getenv(
    "CY_SUPPLIER_VISITS_CHECK_BEARER_TOKEN", ""
).strip()

VISIT_PROFILES = {
    "vip": {
        "phone": "35796000101",
        "user_name": "Test AVT visit VIP CY",
        "request_body": {
            "supplier_id": 5010,
            "attraction_id": 16985,
            "lat": 34.69323610,
            "lng": 33.03418616,
            "geo_mocked": False,
        },
    },
    "platinum": {
        "phone": "35796000102",
        "user_name": "Test AVT visit PLATINUM CY",
        "request_body": {
            "supplier_id": 5010,
            "attraction_id": 16985,
            "lat": 34.69323610,
            "lng": 33.03418616,
            "geo_mocked": False,
        },
    },
    "gold": {
        "phone": "35796000103",
        "user_name": "Test AVT visit GOLD CY",
        "request_body": {
            "supplier_id": 5010,
            "attraction_id": 16985,
            "lat": 34.69323610,
            "lng": 33.03418616,
            "geo_mocked": False,
        },
    },
    "silver": {
        "phone": "35796000104",
        "user_name": "Test AVT visit SILVER CY",
        "request_body": {
            "supplier_id": 5010,
            "attraction_id": 16985,
            "lat": 34.69323610,
            "lng": 33.03418616,
            "geo_mocked": False,
        },
    },
    "vip_no_limit": {
        "phone": "35796000105",
        "user_name": "Test AVT visit VIP CY(no limit)",
        "request_body": {
            "supplier_id": 5010,
            "attraction_id": 16984,
            "lat": 53.904963940824274,
            "lng": 27.561529701524286,
            "geo_mocked": False,
        },
    },
}

EXPECTED_VISITS_IN_SUPPLIER_PANEL = [
    {
        "phone": "3579600010",
        "phone": "35796000101",
        "user_name": "Test AVT visit VIP CY",
        "attraction_name": "Swimm",
        "attraction_id": 16985,
        "status": "waiting",
    },
    {
        "phone": "35796000102",
        "user_name": "Test AVT visit PLATINUM CY",
        "attraction_name": "Swimm",
        "attraction_id": 16985,
        "status": "waiting",
    },
    {
        "phone": "35796000103",
        "user_name": "Test AVT visit GOLD CY",
        "attraction_name": "Swimm",
        "attraction_id": 16985,
        "status": "waiting",
    },
    {
        "phone": "35796000104",
        "user_name": "Test AVT visit SILVER CY",
        "attraction_name": "Swimm",
        "attraction_id": 16985,
        "status": "waiting",
    },
    {
        "phone": "35796000105",
        "user_name": "Test AVT visit VIP CY(no limit)",
        "attraction_name": "Gym",
        "attraction_id": 16984,
        "status": "waiting",
    },
]

LIMIT_TRACKED_PHONES = {
    "vip_limited": "35796000101",
    "vip_no_limit": "35796000105",
}

SUPPLIER_CONFIRM_REASON = "autotest cleanup"
EXPECTED_JOURNAL_COMPANY = os.getenv("CY_EXPECTED_JOURNAL_COMPANY", "").strip()
EXPECTED_JOURNAL_SUPPLIER = os.getenv("CY_EXPECTED_JOURNAL_SUPPLIER", "").strip()
VISIT_REJECT_REASON = "manually_rejected_broken_scan"
VISIT_REJECT_STATUS = "supplier_reject_wrong_id"


def _normalize_token(token):
    normalized = str(token or "").strip()
    if normalized.lower().startswith("bearer "):
        return normalized[7:].strip()
    return normalized


def _normalize_bearer_token(token):
    normalized = str(token or "").strip()
    if normalized.lower().startswith("bearer "):
        return normalized
    return f"Bearer {normalized}" if normalized else ""


def _normalize_holder_name(name):
    normalized = str(name or "").strip()
    if "[!!!" in normalized:
        normalized = normalized.split("[!!!", 1)[0].strip()
    return normalized


def _format_confirm_phone(phone):
    normalized = str(phone or "").strip()
    digits_only = normalized.replace("+", "")
    if CY_JOURNAL_COUNTRY.lower() == "cy":
        return f"+{digits_only}"
    return digits_only


def _admin_headers(admin_token):
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {admin_token}",
        "X-Country": CY_JOURNAL_COUNTRY,
        "X-Localization": "ru",
    }


def _resolve_admin_token():
    token = _normalize_token(ADMIN_TOKEN)
    if token:
        probe = requests.get(
            f"{BASE_URL}/api/helpdesk/card/1",
            headers=_admin_headers(token),
            timeout=30,
        )
        if probe.status_code == 200:
            return token

    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        return ""

    response = requests.post(
        ADMIN_LOGIN_URL,
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        timeout=30,
    )
    assert response.status_code == 200, (
        f"ADMIN LOGIN failed. status={response.status_code}, body={response.text}"
    )
    body = response.json()
    token = body.get("access_token")
    assert token, f"access_token not found in admin login response: {body}"
    return str(token)


def _find_holder_id(phone, admin_token):
    response = requests.get(
        f"{BASE_URL}/api/helpdesk/load_holder_by",
        headers=_admin_headers(admin_token),
        params={"card_id": "", "holder": phone},
        timeout=30,
    )
    assert response.status_code == 200, (
        f"LOAD HOLDER failed. status={response.status_code}, body={response.text}"
    )

    body = response.json()
    items = body.get("data")
    assert isinstance(items, list), f"Holder search response has no data list: {body}"

    requested_phone = re.sub(r"\D", "", str(phone))
    exact_matches = [
        item
        for item in items
        if isinstance(item, dict)
        and re.sub(r"\D", "", str(item.get("phone_number", ""))) == requested_phone
    ]
    assert len(exact_matches) == 1, (
        f"Expected exactly one holder for phone {phone}, found {len(exact_matches)}: {body}"
    )

    holder_id = exact_matches[0].get("id")
    assert holder_id, f"Holder id not found for phone {phone}: {exact_matches[0]}"
    return int(holder_id)


def _get_sms_token_v2(holder_id, admin_token):
    response = requests.get(
        f"{BASE_URL}/api/helpdesk/card/{holder_id}",
        headers=_admin_headers(admin_token),
        timeout=30,
    )
    assert response.status_code == 200, (
        f"GET HOLDER CARD failed. status={response.status_code}, body={response.text}"
    )

    body = response.json()
    card = body.get("card", {}) if isinstance(body, dict) else {}
    holder = body.get("holder", {}) if isinstance(body, dict) else {}
    sms_token = (
        card.get("sms_token_v2")
        or card.get("sms_token")
        or holder.get("sms_token_v2")
        or holder.get("sms_token")
    )
    assert sms_token, f"sms_token_v2 not found in holder card response: {body}"
    return str(sms_token)


def _get_holder_card(holder_id, admin_token):
    response = requests.get(
        f"{BASE_URL}/api/helpdesk/card/{holder_id}",
        headers=_admin_headers(admin_token),
        timeout=30,
    )
    assert response.status_code == 200, (
        f"GET HOLDER CARD failed. status={response.status_code}, body={response.text}"
    )

    body = response.json()
    assert isinstance(body, dict), f"Holder card response is invalid: {body}"
    return body


def _get_limited_visits_remaining(phone, admin_token):
    holder_id = _find_holder_id(phone, admin_token)
    body = _get_holder_card(holder_id, admin_token)
    holder = body.get("holder", {})
    remaining = holder.get("limited_visits_remaining")
    assert isinstance(remaining, int), (
        f"limited_visits_remaining is invalid for phone {phone}: {body}"
    )
    print(f"limited_visits_remaining for {phone}: {remaining}")
    return {
        "holder_id": holder_id,
        "remaining": remaining,
        "holder_name": holder.get("holder"),
        "is_unlimited": holder.get("is_unlimited"),
    }


def _reset_installs(holder_id, admin_token):
    response = requests.post(
        f"{BASE_URL}/api/jrnl/admin/holders/{holder_id}/reset/installs",
        headers=_admin_headers(admin_token),
        timeout=30,
    )
    assert response.status_code in (200, 204), (
        f"RESET INSTALLS failed. status={response.status_code}, body={response.text}"
    )


def _reset_visit_limit(holder_id, admin_token):
    response = requests.post(
        f"{BASE_URL}/api/jrnl/admin/holders/{holder_id}/reset/visit",
        headers=_admin_headers(admin_token),
        timeout=30,
    )
    assert response.status_code in (200, 204), (
        f"RESET VISIT LIMIT failed. status={response.status_code}, body={response.text}"
    )


def _mobile_headers(instance_id, csrf_token=None, language="ru_RU", connection="close"):
    headers = {
        "Accept": "application/json",
        "X-INSTANCE-ID": instance_id,
        "Host": "xn--d1aey.xn--k1aahcehedi.xn--90ais",
        "Connection": connection,
        "X-Country": CY_JOURNAL_COUNTRY,
        "X-Localization": "ru",
        "Content-Language": language,
        "User-Agent": "android-MB",
    }
    if csrf_token:
        headers["X-CSRF-TOKEN"] = csrf_token
    return headers


def _get_csrf_token(instance_id):
    response = requests.get(
        CSRF_URL,
        headers={
            **_mobile_headers(instance_id, language="ru_RU", connection="keep-alive"),
            "Accept": "*/*",
            "User-Agent": "PostmanRuntime/7.54.0",
        },
        timeout=30,
    )
    assert response.status_code == 200, (
        f"CSRF API failed. status={response.status_code}, body={response.text}"
    )
    body = response.json()
    csrf_token = body.get("csrf-token") or body.get("csrf_token")
    assert csrf_token, f"csrf-token not found in response: {body}"
    return csrf_token


def _request_sms(phone, instance_id, csrf_token):
    response = requests.post(
        REQUEST_SMS_URL,
        headers={
            **_mobile_headers(instance_id, csrf_token, language="ru_RU"),
            "Content-Type": "application/json",
        },
        json={
            "phone": str(phone).replace("+", ""),
            "csrf_token": csrf_token,
        },
        timeout=30,
    )
    if response.status_code == 200:
        return {"status": "requested"}

    try:
        body = response.json()
    except ValueError:
        body = {}

    if response.status_code == 422 and body.get("state") == "no_access":
        return {"status": "no_access", "body": body}

    raise AssertionError(
        f"REQUEST SMS API failed. status={response.status_code}, body={response.text}"
    )


def _confirm_sms(phone, sms_code, instance_id):
    csrf_token = _get_csrf_token(instance_id)
    confirm_language = "ru_RU" if CY_JOURNAL_COUNTRY.lower() == "cy" else "ru_BY"
    response = requests.post(
        CONFIRM_SMS_URL,
        headers={
            **_mobile_headers(instance_id, csrf_token, language=confirm_language),
            "Content-Type": "application/json",
        },
        json={
            "phone": _format_confirm_phone(phone),
            "sms_code": str(sms_code),
            "csrf_token": csrf_token,
        },
        timeout=30,
    )
    assert response.status_code == 200, (
        f"CONFIRM SMS API failed. status={response.status_code}, body={response.text}"
    )

    body = response.json()
    oauth_token = body.get("oauth-token") or body.get("oauth_token")
    assert oauth_token, f"oauth-token not found in confirm response: {body}"
    return str(oauth_token)


def _create_visit(oauth_token, request_body, holder_id=None, admin_token=None):
    def _make_request():
        return requests.post(
            CREATE_VISIT_URL,
            headers={
                "Authorization": f"Bearer {oauth_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=request_body,
            timeout=30,
        )

    def _extract_status_and_id(response):
        try:
            payload = response.json()
        except ValueError:
            payload = {}

        response_status = payload.get("status") if isinstance(payload, dict) else None
        response_id = payload.get("id") if isinstance(payload, dict) else None
        return response_status, response_id, payload if isinstance(payload, dict) else {}

    response = _make_request()
    if response.status_code in (200, 201):
        body = response.json()
        if "id" in body:
            assert isinstance(body.get("id"), int), f"Field id is invalid: {body}"
        if "status" in body:
            assert body.get("status") in ("wait", "limit"), f"Unexpected status: {body}"
        return

    response_status, response_id, body = _extract_status_and_id(response)
    if response.status_code == 403 and response_status == "wait" and response_id:
        return

    if response.status_code == 403 and response_status == "limit" and holder_id and admin_token:
        _reset_visit_limit(holder_id, admin_token)
        response = _make_request()
        if response.status_code in (200, 201):
            body = response.json()
            if "id" in body:
                assert isinstance(body.get("id"), int), f"Field id is invalid: {body}"
            if "status" in body:
                assert body.get("status") in ("wait", "limit"), f"Unexpected status: {body}"
            return
        response_status, response_id, body = _extract_status_and_id(response)
        if response.status_code == 403 and response_status == "wait" and response_id:
            return

    assert response.status_code in (200, 201), (
        f"CREATE VISIT API failed. status={response.status_code}, body={response.text}"
    )

    if "id" in body:
        assert isinstance(body.get("id"), int), f"Field id is invalid: {body}"
    if "status" in body:
        assert body.get("status") in ("wait", "limit"), f"Unexpected status: {body}"


def _login_and_create_visit(phone, request_body):
    admin_token = _resolve_admin_token()
    sms_code = SMS_CODE or None

    if admin_token:
        holder_id = _find_holder_id(phone, admin_token)
        _reset_installs(holder_id, admin_token)
        _reset_visit_limit(holder_id, admin_token)
        instance_id = str(uuid.uuid4())
        request_csrf_token = _get_csrf_token(instance_id)
        request_sms_result = _request_sms(phone, instance_id, request_csrf_token)
        sms_code = _get_sms_token_v2(holder_id, admin_token)
        if request_sms_result["status"] == "no_access":
            print(
                f"Cyprus request-sms returned no_access for {phone}; "
                "continuing with sms_token_v2 from helpdesk card."
            )
    else:
        if not sms_code:
            pytest.skip(
                "Set CREATE_VISIT_SMS_CODE or SUPPLIER_JRNL_EMAIL/SUPPLIER_JRNL_PASSWORD "
                "to run mobile holder visit creation tests."
            )
        instance_id = str(uuid.uuid4())

    oauth_token = _confirm_sms(phone, sms_code, instance_id)
    _create_visit(oauth_token, request_body, holder_id=holder_id if admin_token else None, admin_token=admin_token)


def _get_supplier_visits():
    bearer_token = _normalize_bearer_token(CY_SUPPLIER_VISITS_CHECK_BEARER_TOKEN)
    if not bearer_token:
        pytest.skip(
            "Укажите CY_SUPPLIER_VISITS_CHECK_BEARER_TOKEN в Environment variables "
            "для проверки визитов в supplier panel."
        )

    response = requests.get(
        SUPPLIER_VISITS_CHECK_URL,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Authorization": bearer_token,
            "X-Country": CY_JOURNAL_COUNTRY,
            "X-Localization": "ru",
        },
        timeout=30,
    )
    assert response.status_code == 200, (
        f"SUPPLIER VISITS CHECK API failed. status={response.status_code}, body={response.text}"
    )

    body = response.json()
    visits = body.get("visits") if isinstance(body, dict) else None
    assert isinstance(visits, list), f"Response has no visits list: {body}"
    return visits


def _get_supplier_accepted_visits_for_month(month_value):
    bearer_token = _normalize_bearer_token(CY_SUPPLIER_VISITS_CHECK_BEARER_TOKEN)
    if not bearer_token:
        pytest.skip(
            "Укажите CY_SUPPLIER_VISITS_CHECK_BEARER_TOKEN в Environment variables "
            "для проверки accepted-визитов в supplier panel."
        )

    response = requests.get(
        SUPPLIER_ACCEPTED_VISITS_URL,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Authorization": bearer_token,
            "X-Country": CY_JOURNAL_COUNTRY,
            "X-Localization": "ru",
        },
        params={"month": month_value, "status": "accepted"},
        timeout=30,
    )
    assert response.status_code == 200, (
        f"SUPPLIER ACCEPTED VISITS API failed. status={response.status_code}, body={response.text}"
    )
    body = response.json()
    assert isinstance(body, list), f"Accepted visits response is invalid: {body}"
    return body


def _get_journal_rows_for_period(date_from, date_finish, admin_token):
    response = requests.get(
        JOURNAL_VISITS_URL,
        headers={
            **_admin_headers(admin_token),
            "X-Country": CY_JOURNAL_COUNTRY,
            "X-Localization": "ru",
        },
        params={
            "page": 1,
            "row_count": 100,
            "date": date_from,
            "date_finish": date_finish,
        },
        timeout=30,
    )
    assert response.status_code == 200, (
        f"JOURNAL API failed. status={response.status_code}, body={response.text}"
    )
    body = response.json()
    headers = body.get("headers")
    data = body.get("data")
    assert isinstance(headers, list) and isinstance(data, list), (
        f"Journal response has invalid structure: {body}"
    )
    rows = []
    for raw_row in data:
        if isinstance(raw_row, list) and len(raw_row) == len(headers):
            rows.append(dict(zip(headers, raw_row)))
    return rows


def _reject_visit_in_journal(visit_id, attraction_id, admin_token):
    response = requests.patch(
        f"{BASE_URL}/api/helpdesk/manually_update_visit",
        headers={
            **_admin_headers(admin_token),
            "X-Country": CY_JOURNAL_COUNTRY,
            "X-Localization": "ru",
        },
        params={
            "id": visit_id,
            "status": VISIT_REJECT_STATUS,
            "reason": VISIT_REJECT_REASON,
            "attraction_id": attraction_id,
            "force": 1,
        },
        timeout=30,
    )
    assert response.status_code == 200, (
        f"REJECT VISIT API failed. id={visit_id}, "
        f"status={response.status_code}, body={response.text}"
    )
    print(
        f"Реджект визита выполнен: id={visit_id}, attraction_id={attraction_id}, "
        f"reason={VISIT_REJECT_REASON}, status_code={response.status_code}"
    )
    return response


def _iter_supplier_panel_accounts():
    assert CY_SUPPLIER_LOGIN and CY_SUPPLIER_PASSWORD, (
        "Для Cyprus supplier panel укажите CY_SUPPLIER_CONFIRM_LOGIN и "
        "CY_SUPPLIER_CONFIRM_PASSWORD."
    )
    yield {"login": CY_SUPPLIER_LOGIN, "password": CY_SUPPLIER_PASSWORD, "label": "cyprus"}


def _reset_supplier_panel_session(driver):
    driver.delete_all_cookies()
    driver.get(SUPPLIER_PANEL_BASE_URL + "/login")
    try:
        driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    except Exception:
        pass
    driver.delete_all_cookies()


def _open_pending_visits_if_present(page):
    if page.is_element_visible(page.BUTTON_NEW_VISITS_LOCATOR):
        page.hard_click(page.BUTTON_NEW_VISITS_LOCATOR)
        return True
    if page.is_element_visible(page.BUTTON_NEW_VISITS_LOCATOR_EN):
        page.hard_click(page.BUTTON_NEW_VISITS_LOCATOR_EN)
        return True
    return False


def _current_visit_card(page):
    return {
        "user_name": page.find_element_text(page.NAME_USER_LOCATOR).strip(),
        "user_level": page.find_element_text(page.LEVEL_USER_LOCATOR).strip(),
        "attraction": page.find_element_text(page.ATTRACTION_USER_LOCATOR).strip(),
    }


def _confirm_photo_if_present(page):
    if page.is_element_visible(page.BUTTON_LOOKS_LIKE_LOCATOR_EN):
        page.hard_click(page.BUTTON_LOOKS_LIKE_LOCATOR_EN)
        return True
    if page.is_element_visible(page.BUTTON_LOOKS_LIKE_LOCATOR):
        page.hard_click(page.BUTTON_LOOKS_LIKE_LOCATOR)
        return True
    return False


def _confirm_visit_card(page, card_info):
    if page.is_element_visible(page.ACCEPT_BUTTON_LOCATOR_EN):
        page.hard_click(page.ACCEPT_BUTTON_LOCATOR_EN)
    elif page.is_element_visible(page.ACCEPT_BUTTON_LOCATOR):
        page.hard_click(page.ACCEPT_BUTTON_LOCATOR)
    else:
        raise AssertionError(f"Кнопка Accept не найдена для визита: {card_info}")

    photo_check = _confirm_photo_if_present(page)
    result = {
        **card_info,
        "action": "confirmed",
        "photo_check": photo_check,
        "status_code": 200,
    }
    print(
        "Подтвержден визит:",
        result["user_name"],
        result["user_level"],
        result["attraction"],
        f"status_code={result['status_code']}",
    )
    return result


def _reject_visit_card(page, card_info):
    if page.is_element_visible(page.DECLINE_BUTTON_LOCATOR_EN):
        page.hard_click(page.DECLINE_BUTTON_LOCATOR_EN)
    elif page.is_element_visible(page.DECLINE_BUTTON_LOCATOR):
        page.hard_click(page.DECLINE_BUTTON_LOCATOR)
    else:
        raise AssertionError(f"Кнопка Decline не найдена для визита: {card_info}")

    page.fill(page.INPUT_REASON_REJECT_LOCATOR, SUPPLIER_CONFIRM_REASON)
    if page.is_element_visible(page.CLICK_BUTTON_SAVE_EN):
        page.hard_click(page.CLICK_BUTTON_SAVE_EN)
    elif page.is_element_visible(page.CLICK_BUTTON_SAVE):
        page.hard_click(page.CLICK_BUTTON_SAVE)
    else:
        raise AssertionError(f"Кнопка Save не найдена для отклонения визита: {card_info}")

    result = {
        **card_info,
        "action": "rejected",
        "reason": SUPPLIER_CONFIRM_REASON,
        "status_code": 200,
    }
    print(
        "Отклонен визит:",
        result["user_name"],
        result["user_level"],
        result["attraction"],
        f"status_code={result['status_code']}",
    )
    return result


def _process_expected_visits_in_supplier_panel(driver, expected_actions, max_iterations=12):
    results = []
    processed_names_total = set()

    for account in _iter_supplier_panel_accounts():
        _reset_supplier_panel_session(driver)
        page = SupplierPanelRegistrationVisits(driver)
        page.open_sp()
        if account.get("login") and account.get("password"):
            page.login_supplier_panel(login=account["login"], password=account["password"])
        else:
            page.login_supplier_panel(role=account["role"])

        processed = []
        processed_names_account = set()
        stop_reason = None
        duplicate_streak = 0

        for _ in range(max_iterations):
            has_actions = page.is_element_visible(page.ACCEPT_BUTTON_LOCATOR) or page.is_element_visible(
                page.ACCEPT_BUTTON_LOCATOR_EN
            )
            if not has_actions:
                _open_pending_visits_if_present(page)
                has_actions = page.is_element_visible(page.ACCEPT_BUTTON_LOCATOR) or page.is_element_visible(
                    page.ACCEPT_BUTTON_LOCATOR_EN
                )
            if not has_actions:
                stop_reason = "accept button not found"
                break

            card_info = _current_visit_card(page)
            user_name = card_info["user_name"]
            expected_action = expected_actions.get(user_name)

            if expected_action is None:
                stop_reason = f"encountered non-test visit: {user_name}"
                break

            if user_name in processed_names_total or user_name in processed_names_account:
                duplicate_streak += 1
                time.sleep(1)
                _open_pending_visits_if_present(page)
                if duplicate_streak >= 3:
                    page.driver.refresh()
                    time.sleep(2)
                if duplicate_streak >= 5:
                    stop_reason = f"duplicate visit card encountered repeatedly: {user_name}"
                    break
                continue

            duplicate_streak = 0

            if expected_action == "confirm":
                processed.append(_confirm_visit_card(page, card_info))
            else:
                processed.append(_reject_visit_card(page, card_info))
            processed_names_account.add(user_name)
            processed_names_total.add(user_name)

            if processed_names_total == set(expected_actions):
                stop_reason = "all expected visits processed"
                break

            has_next_actions = page.is_element_visible(page.ACCEPT_BUTTON_LOCATOR) or page.is_element_visible(
                page.ACCEPT_BUTTON_LOCATOR_EN
            )
            if not has_next_actions:
                _open_pending_visits_if_present(page)

        results.append(
            {
                "account": account["label"],
                "processed": processed,
                "stop_reason": stop_reason,
            }
        )

        if processed_names_total == set(expected_actions):
            return results

    return results


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create VIP visit via mobile login flow")
def test_create_visit_vip():
    profile = VISIT_PROFILES["vip"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create premium visit via mobile login flow")
def test_create_visit_platinum():
    profile = VISIT_PROFILES["platinum"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create classic visit via mobile login flow")
def test_create_visit_gold():
    profile = VISIT_PROFILES["gold"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create lite visit via mobile login flow")
def test_create_visit_silver():
    profile = VISIT_PROFILES["silver"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create region visit via mobile login flow")
def test_create_visit_vip_no_limit():
    profile = VISIT_PROFILES["vip_no_limit"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Check created visits arrived in supplier panel")
def test_check_created_visits_arrived_in_supplier_panel():
    visits = _get_supplier_visits()

    actual_entries = {
        (
            _normalize_holder_name(visit.get("user", {}).get("name")),
            visit.get("attraction", {}).get("id"),
            visit.get("attraction", {}).get("name"),
            visit.get("status"),
        )
        for visit in visits
        if isinstance(visit, dict)
    }

    missing_visits = []
    for expected in EXPECTED_VISITS_IN_SUPPLIER_PANEL:
        expected_entry = (
            expected["user_name"],
            expected["attraction_id"],
            expected["attraction_name"],
            expected["status"],
        )
        if expected_entry not in actual_entries:
            missing_visits.append(
                f"{expected['phone']} / {expected['user_name']} / "
                f"attraction_id={expected['attraction_id']}"
            )

    assert not missing_visits, (
        "Не найдены ожидаемые визиты в supplier panel: " + "; ".join(missing_visits)
    )


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Confirm Cyprus visits and verify limited visits counters")
@pytest.mark.live_api
def test_confirm_target_visits_and_check_limit_counters_cy(driver):
    admin_token = _resolve_admin_token()
    assert admin_token, "Не удалось получить admin token для проверки лимитов."

    vip_before = _get_limited_visits_remaining(LIMIT_TRACKED_PHONES["vip_limited"], admin_token)
    vip_no_limit_before = _get_limited_visits_remaining(
        LIMIT_TRACKED_PHONES["vip_no_limit"], admin_token
    )

    expected_actions = {
        profile["user_name"]: "confirm"
        for profile in VISIT_PROFILES.values()
    }

    results = _process_expected_visits_in_supplier_panel(driver, expected_actions)
    print(f"supplier panel processing results: {results}")

    processed_names = {
        item["user_name"]
        for account_result in results
        for item in account_result["processed"]
    }
    missing_names = sorted(set(expected_actions) - processed_names)
    assert not missing_names, (
        "Не удалось обработать все ожидаемые визиты в supplier panel. "
        f"Не обработаны: {missing_names}. Результаты: {results}"
    )

    vip_after = _get_limited_visits_remaining(LIMIT_TRACKED_PHONES["vip_limited"], admin_token)
    vip_no_limit_after = _get_limited_visits_remaining(
        LIMIT_TRACKED_PHONES["vip_no_limit"], admin_token
    )

    print(
        f"{LIMIT_TRACKED_PHONES['vip_limited']} before={vip_before['remaining']} "
        f"after={vip_after['remaining']}"
    )
    print(
        f"{LIMIT_TRACKED_PHONES['vip_no_limit']} before={vip_no_limit_before['remaining']} "
        f"after={vip_no_limit_after['remaining']}"
    )

    assert vip_after["remaining"] == vip_before["remaining"] - 1, (
        "Лимит для 35796000101 изменился неверно. "
        f"before={vip_before['remaining']}, after={vip_after['remaining']}"
    )
    assert vip_no_limit_after["remaining"] == vip_no_limit_before["remaining"], (
        "Лимит для 35796000105 не должен измениться. "
        f"before={vip_no_limit_before['remaining']}, after={vip_no_limit_after['remaining']}"
    )


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Check accepted visits in supplier panel and journal")
def test_check_accepted_visits_in_supplier_panel_and_journal_cy():
    today = datetime.now().date()
    today_iso = today.isoformat()
    month_value = today.strftime("%Y-%m")
    admin_token = _resolve_admin_token()
    assert admin_token, "Не удалось получить admin token для проверки journal."

    supplier_visits = _get_supplier_accepted_visits_for_month(month_value)
    journal_rows = _get_journal_rows_for_period(
        date_from=today.replace(day=1).isoformat(),
        date_finish=today_iso,
        admin_token=admin_token,
    )

    expected_today_visits = {
        "Test AVT visit VIP CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit PLATINUM CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit GOLD CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit SILVER CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit VIP CY(no limit)": {"attraction_id": 16984, "attraction_name": "Gym"},
    }

    supplier_today_rows = []
    for visit in supplier_visits:
        if not isinstance(visit, dict):
            continue
        created_at = str(visit.get("created_at", ""))
        if not created_at.startswith(today_iso):
            continue
        user = visit.get("user", {}) if isinstance(visit.get("user"), dict) else {}
        attraction = visit.get("attraction", {}) if isinstance(visit.get("attraction"), dict) else {}
        user_name = _normalize_holder_name(user.get("name"))
        if user_name in expected_today_visits:
            supplier_today_rows.append(visit)

    supplier_by_name = {}
    for visit in supplier_today_rows:
        user_name = _normalize_holder_name(visit["user"]["name"])
        supplier_by_name[user_name] = visit

    missing_in_supplier = sorted(set(expected_today_visits) - set(supplier_by_name))
    assert not missing_in_supplier, (
        "Не найдены accepted-визиты за сегодня в supplier panel: "
        f"{missing_in_supplier}"
    )

    journal_by_id = {row.get("id"): row for row in journal_rows}

    for user_name, expected in expected_today_visits.items():
        supplier_visit = supplier_by_name[user_name]
        supplier_visit_id = supplier_visit.get("id")
        supplier_status = supplier_visit.get("status")
        supplier_attraction = supplier_visit.get("attraction", {})
        supplier_attraction_id = supplier_attraction.get("id")
        supplier_attraction_name = supplier_attraction.get("name")
        supplier_level = supplier_visit.get("user", {}).get("level")

        assert supplier_status == "accepted", (
            f"В supplier panel у визита {user_name} неверный status: {supplier_visit}"
        )
        assert supplier_attraction_id == expected["attraction_id"], (
            f"В supplier panel у визита {user_name} неверный attraction_id: {supplier_visit}"
        )
        assert supplier_attraction_name == expected["attraction_name"], (
            f"В supplier panel у визита {user_name} неверная услуга: {supplier_visit}"
        )

        journal_row = journal_by_id.get(supplier_visit_id)
        assert journal_row, (
            f"В journal не найден визит с id={supplier_visit_id} для пользователя {user_name}"
        )

        print(
            f"САПЛАЕР ПАНЕЛЬ: id={supplier_visit_id}, пользователь={user_name}, "
            f"уровень={supplier_level}, услуга={supplier_attraction_name}, "
            f"attraction_id={supplier_attraction_id}, статус={supplier_status}"
        )

        assert _normalize_holder_name(journal_row.get("holder")) == user_name, (
            f"В journal у id={supplier_visit_id} неверный holder: {journal_row}"
        )
        assert journal_row.get("status") == "app_holder_passed", (
            f"В journal у id={supplier_visit_id} неверный status: {journal_row}"
        )
        if EXPECTED_JOURNAL_COMPANY:
            assert journal_row.get("company_name") == EXPECTED_JOURNAL_COMPANY, (
                f"В journal у id={supplier_visit_id} неверная company_name: {journal_row}"
            )
        if EXPECTED_JOURNAL_SUPPLIER:
            assert journal_row.get("sup_name") == EXPECTED_JOURNAL_SUPPLIER, (
                f"В journal у id={supplier_visit_id} неверный supplier: {journal_row}"
            )

        print(
            f"ЖУРНАЛ: id={journal_row.get('id')}, пользователь={journal_row.get('holder')}, "
            f"статус={journal_row.get('status')}, компания={journal_row.get('company_name')}, "
            f"поставщик={journal_row.get('sup_name')}"
        )
        print(
            f"ПРОВЕРЕНО: данные в саплаер панели и журнале совпадают для id={supplier_visit_id}, "
            f"пользователь={user_name}, attraction_id={expected['attraction_id']}"
        )


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Reject accepted visits and verify journal status")
def test_reject_accepted_visits_and_check_journal_status_cy():
    today = datetime.now().date()
    today_iso = today.isoformat()
    month_value = today.strftime("%Y-%m")
    admin_token = _resolve_admin_token()
    assert admin_token, "Не удалось получить admin token для реджекта визитов."

    supplier_visits = _get_supplier_accepted_visits_for_month(month_value)
    expected_today_visits = {
        "Test AVT visit VIP CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit PLATINUM CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit GOLD CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit SILVER CY": {"attraction_id": 16985, "attraction_name": "Swimm"},
        "Test AVT visit VIP CY(no limit)": {"attraction_id": 16984, "attraction_name": "Gym"},
    }

    supplier_today_rows = []
    for visit in supplier_visits:
        if not isinstance(visit, dict):
            continue
        created_at = str(visit.get("created_at", ""))
        user = visit.get("user", {}) if isinstance(visit.get("user"), dict) else {}
        user_name = _normalize_holder_name(user.get("name"))
        if created_at.startswith(today_iso) and user_name in expected_today_visits:
            supplier_today_rows.append(visit)

    supplier_by_name = {
        _normalize_holder_name(visit["user"]["name"]): visit
        for visit in supplier_today_rows
        if isinstance(visit.get("user"), dict) and visit["user"].get("name")
    }
    missing_in_supplier = sorted(set(expected_today_visits) - set(supplier_by_name))
    assert not missing_in_supplier, (
        "Не найдены accepted-визиты за сегодня перед реджектом: "
        f"{missing_in_supplier}"
    )

    for user_name, expected in expected_today_visits.items():
        supplier_visit = supplier_by_name[user_name]
        visit_id = supplier_visit.get("id")
        _reject_visit_in_journal(
            visit_id=visit_id,
            attraction_id=expected["attraction_id"],
            admin_token=admin_token,
        )

    journal_rows = _get_journal_rows_for_period(
        date_from=today.replace(day=1).isoformat(),
        date_finish=today_iso,
        admin_token=admin_token,
    )
    journal_by_id = {row.get("id"): row for row in journal_rows}

    for user_name, expected in expected_today_visits.items():
        visit_id = supplier_by_name[user_name]["id"]
        journal_row = journal_by_id.get(visit_id)
        assert journal_row, (
            f"В journal не найден визит после реджекта: id={visit_id}, user={user_name}"
        )
        assert _normalize_holder_name(journal_row.get("holder")) == user_name, (
            f"В journal после реджекта у id={visit_id} неверный holder: {journal_row}"
        )
        assert journal_row.get("status") == "app_holder_reject", (
            f"В journal после реджекта у id={visit_id} неверный status: {journal_row}"
        )
        if EXPECTED_JOURNAL_COMPANY:
            assert journal_row.get("company_name") == EXPECTED_JOURNAL_COMPANY, (
                f"В journal после реджекта у id={visit_id} неверная company_name: {journal_row}"
            )
        if EXPECTED_JOURNAL_SUPPLIER:
            assert journal_row.get("sup_name") == EXPECTED_JOURNAL_SUPPLIER, (
                f"В journal после реджекта у id={visit_id} неверный supplier: {journal_row}"
            )
        print(
            f"РЕДЖЕКТ ПРОВЕРЕН: id={visit_id}, пользователь={user_name}, "
            f"attraction_id={expected['attraction_id']}, статус journal=app_holder_reject"
        )

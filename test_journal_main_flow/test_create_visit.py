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
SUPPLIER_VISITS_CHECK_BEARER_TOKEN = os.getenv(
    "SUPPLIER_VISITS_CHECK_BEARER_TOKEN", ""
).strip()

VISIT_PROFILES = {
    "vip": {
        "phone": "375440000100",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 17008,
            "lat": 53.904963940824274,
            "lng": 27.561529701524286,
            "geo_mocked": False,
        },
    },
    "premium": {
        "phone": "375440000101",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 16837,
            "lat": 53.9006,
            "lng": 27.5590,
            "geo_mocked": False,
        },
    },
    "classic": {
        "phone": "375440000102",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 17007,
            "lat": 53.9006,
            "lng": 27.5590,
            "geo_mocked": False,
        },
    },
    "lite": {
        "phone": "375440000103",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 16838,
            "lat": 53.9006,
            "lng": 27.5590,
            "geo_mocked": False,
        },
    },
    "region": {
        "phone": "375440000104",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 17006,
            "lat": 53.9006,
            "lng": 27.5590,
            "geo_mocked": False,
        },
    },
    "vip_no_limit": {
        "phone": "375440000105",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 17006,
            "lat": 53.9006,
            "lng": 27.5590,
            "geo_mocked": False,
        },
    },
}

EXPECTED_VISITS_IN_SUPPLIER_PANEL = [
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
    {
        "phone": "375440000105",
        "user_name": "Test AVT visit VIP(no limit)",
        "level": "vip",
        "attraction_id": 17006,
        "attraction_name": "Пренатальная йога",
        "status": "waiting",
    },
]

LIMIT_TRACKED_PHONES = {
    "vip_limited": "375440000100",
    "vip_no_limit": "375440000105",
}

SUPPLIER_CONFIRM_REASON = "autotest cleanup"
EXPECTED_JOURNAL_COMPANY = "!!!НЕ ТРОГАТЬ!!! AT Main Flow ZP26PW07 Company 1 B2B"
EXPECTED_JOURNAL_SUPPLIER = "Gym НЕ УДАЛЯТЬ НЕ ИЗМЕНЯТЬ НИЧЕГО, НЕ ШУТКА"
VISIT_REJECT_REASON = "manually_rejected_broken_scan"
VISIT_REJECT_STATUS = "supplier_reject_wrong_id"
SUPPLIER_VISITS_SYNC_TIMEOUT = 90
SUPPLIER_VISITS_SYNC_POLL_INTERVAL = 5


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


def _admin_headers(admin_token):
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {admin_token}",
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


def _mobile_headers(instance_id, csrf_token=None):
    headers = {
        "Accept": "application/json",
        "X-INSTANCE-ID": instance_id,
        "User-Agent": "PostmanRuntime/7.54.0",
    }
    if csrf_token:
        headers["X-CSRF-TOKEN"] = csrf_token
    return headers


def _get_csrf_token(instance_id):
    response = requests.get(
        CSRF_URL,
        headers=_mobile_headers(instance_id),
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
            **_mobile_headers(instance_id, csrf_token),
            "Content-Type": "application/json",
        },
        json={
            "phone": str(phone).replace("+", ""),
            "csrf_token": csrf_token,
        },
        timeout=30,
    )
    assert response.status_code == 200, (
        f"REQUEST SMS API failed. status={response.status_code}, body={response.text}"
    )


def _confirm_sms(phone, sms_code, instance_id):
    csrf_token = _get_csrf_token(instance_id)
    response = requests.post(
        CONFIRM_SMS_URL,
        headers={
            **_mobile_headers(instance_id, csrf_token),
            "Content-Type": "application/json",
        },
        json={
            "phone": str(phone).replace("+", ""),
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
    if response.status_code == 201:
        body = response.json()
        assert isinstance(body.get("id"), int), f"Field id is invalid: {body}"
        assert body.get("status") == "wait", f"Expected status=wait, got: {body}"
        assert body.get("timeout_at"), f"Field timeout_at is missing: {body}"
        assert "content" in body, f"Field content is missing: {body}"
        return

    response_status, response_id, body = _extract_status_and_id(response)
    if response.status_code == 403 and response_status == "wait" and response_id:
        return

    if response.status_code == 403 and response_status == "limit" and holder_id and admin_token:
        _reset_visit_limit(holder_id, admin_token)
        response = _make_request()
        if response.status_code == 201:
            body = response.json()
            assert isinstance(body.get("id"), int), f"Field id is invalid: {body}"
            assert body.get("status") == "wait", f"Expected status=wait, got: {body}"
            assert body.get("timeout_at"), f"Field timeout_at is missing: {body}"
            assert "content" in body, f"Field content is missing: {body}"
            return
        response_status, response_id, body = _extract_status_and_id(response)
        if response.status_code == 403 and response_status == "wait" and response_id:
            return

    assert response.status_code == 201, (
        f"CREATE VISIT API failed. status={response.status_code}, body={response.text}"
    )

    assert isinstance(body.get("id"), int), f"Field id is invalid: {body}"
    assert body.get("status") == "wait", f"Expected status=wait, got: {body}"
    assert body.get("timeout_at"), f"Field timeout_at is missing: {body}"
    assert "content" in body, f"Field content is missing: {body}"


def _login_and_create_visit(phone, request_body):
    admin_token = _resolve_admin_token()
    sms_code = SMS_CODE or None

    if admin_token:
        holder_id = _find_holder_id(phone, admin_token)
        _reset_installs(holder_id, admin_token)
        _reset_visit_limit(holder_id, admin_token)
        instance_id = str(uuid.uuid4())
        request_csrf_token = _get_csrf_token(instance_id)
        _request_sms(phone, instance_id, request_csrf_token)
        sms_code = _get_sms_token_v2(holder_id, admin_token)
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
    bearer_token = _normalize_bearer_token(SUPPLIER_VISITS_CHECK_BEARER_TOKEN)
    assert bearer_token, (
        "Укажите SUPPLIER_VISITS_CHECK_BEARER_TOKEN в Environment variables "
        "для проверки визитов в supplier panel."
    )

    response = requests.get(
        SUPPLIER_VISITS_CHECK_URL,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Authorization": bearer_token,
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
    bearer_token = _normalize_bearer_token(SUPPLIER_VISITS_CHECK_BEARER_TOKEN)
    assert bearer_token, (
        "Укажите SUPPLIER_VISITS_CHECK_BEARER_TOKEN в Environment variables "
        "для проверки accepted-визитов в supplier panel."
    )

    response = requests.get(
        SUPPLIER_ACCEPTED_VISITS_URL,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Authorization": bearer_token,
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


def _wait_for_expected_waiting_visits(expected_visits):
    """Wait until all newly created visits are visible in the supplier queue."""
    expected_entries = {
        (
            visit["user_name"],
            visit["level"],
            visit["attraction_id"],
            visit["attraction_name"],
            visit["status"],
        )
        for visit in expected_visits
    }
    deadline = time.monotonic() + SUPPLIER_VISITS_SYNC_TIMEOUT

    while True:
        actual_entries = {
            (
                visit.get("user", {}).get("name"),
                visit.get("user", {}).get("level"),
                visit.get("attraction", {}).get("id"),
                visit.get("attraction", {}).get("name"),
                visit.get("status"),
            )
            for visit in _get_supplier_visits()
            if isinstance(visit, dict)
        }
        missing_entries = expected_entries - actual_entries
        if not missing_entries:
            return
        if time.monotonic() >= deadline:
            raise AssertionError(
                "Не дождались появления waiting-визитов в supplier panel за "
                f"{SUPPLIER_VISITS_SYNC_TIMEOUT} сек.: {sorted(missing_entries)}"
            )
        time.sleep(SUPPLIER_VISITS_SYNC_POLL_INTERVAL)


def _wait_for_today_accepted_visits(month_value, today_iso, expected_visits):
    """Wait until supplier panel API reflects visits confirmed through the UI."""
    deadline = time.monotonic() + SUPPLIER_VISITS_SYNC_TIMEOUT
    supplier_by_name = {}

    while True:
        supplier_by_name = {}
        for visit in _get_supplier_accepted_visits_for_month(month_value):
            if not isinstance(visit, dict):
                continue
            if not str(visit.get("created_at", "")).startswith(today_iso):
                continue

            user = visit.get("user", {})
            user_name = user.get("name") if isinstance(user, dict) else None
            if user_name in expected_visits:
                supplier_by_name[user_name] = visit

        missing_names = sorted(set(expected_visits) - set(supplier_by_name))
        if not missing_names:
            return supplier_by_name
        if time.monotonic() >= deadline:
            raise AssertionError(
                "Не дождались accepted-визитов в supplier panel за "
                f"{SUPPLIER_VISITS_SYNC_TIMEOUT} сек.: {missing_names}"
            )
        time.sleep(SUPPLIER_VISITS_SYNC_POLL_INTERVAL)


def _get_journal_rows_for_period(date_from, date_finish, admin_token):
    response = requests.get(
        JOURNAL_VISITS_URL,
        headers={
            **_admin_headers(admin_token),
            "X-Country": "by",
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
            "X-Country": "by",
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
    env_login = os.getenv("SUPPLIER_CONFIRM_LOGIN", "").strip()
    env_password = os.getenv("SUPPLIER_CONFIRM_PASSWORD", "").strip()
    if env_login and env_password:
        yield {"login": env_login, "password": env_password, "label": "env"}

    yield {"role": "finance", "label": "finance"}
    yield {"role": "reception", "label": "reception"}


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
        foreign_card_streak = 0

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
                # Do not accept or reject somebody else's visit. Refreshing and opening
                # the queue again allows the supplier panel to return another card.
                foreign_card_streak += 1
                page.driver.refresh()
                time.sleep(2)
                _open_pending_visits_if_present(page)
                if foreign_card_streak >= 5:
                    stop_reason = (
                        "foreign visit blocks the queue repeatedly: "
                        f"{user_name}"
                    )
                    break
                continue

            foreign_card_streak = 0
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
def test_create_visit_premium():
    profile = VISIT_PROFILES["premium"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create classic visit via mobile login flow")
def test_create_visit_classic():
    profile = VISIT_PROFILES["classic"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create lite visit via mobile login flow")
def test_create_visit_lite():
    profile = VISIT_PROFILES["lite"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create region visit via mobile login flow")
def test_create_visit_region():
    profile = VISIT_PROFILES["region"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create VIP no limit visit via mobile login flow")
def test_create_visit_vip_no_limit():
    profile = VISIT_PROFILES["vip_no_limit"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Check created visits arrived in supplier panel")
def test_check_created_visits_arrived_in_supplier_panel():
    _wait_for_expected_waiting_visits(EXPECTED_VISITS_IN_SUPPLIER_PANEL)


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Confirm all 6 visits and verify limited visits counters")
@pytest.mark.live_api
def test_confirm_target_visits_and_check_limit_counters(driver):
    admin_token = _resolve_admin_token()
    assert admin_token, "Не удалось получить admin token для проверки лимитов."

    vip_before = _get_limited_visits_remaining(LIMIT_TRACKED_PHONES["vip_limited"], admin_token)
    vip_no_limit_before = _get_limited_visits_remaining(
        LIMIT_TRACKED_PHONES["vip_no_limit"], admin_token
    )

    expected_actions = {
        "Test AVT visit VIP": "confirm",
        "Test AVT visit PREMIUM": "confirm",
        "Test AVT visit classic": "confirm",
        "Test AVT visit LITE": "confirm",
        "Test AVT visit REGIN": "confirm",
        "Test AVT visit VIP(no limit)": "confirm",
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
        "Лимит для 375440000100 изменился неверно. "
        f"before={vip_before['remaining']}, after={vip_after['remaining']}"
    )
    assert vip_no_limit_after["remaining"] == vip_no_limit_before["remaining"], (
        "Лимит для 375440000105 не должен измениться. "
        f"before={vip_no_limit_before['remaining']}, after={vip_no_limit_after['remaining']}"
    )


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Check accepted visits in supplier panel and journal")
def test_check_accepted_visits_in_supplier_panel_and_journal():
    today = datetime.now().date()
    today_iso = today.isoformat()
    month_value = today.strftime("%Y-%m")
    admin_token = _resolve_admin_token()
    assert admin_token, "Не удалось получить admin token для проверки journal."

    expected_today_visits = {
        "Test AVT visit VIP": {"attraction_id": 17008, "attraction_name": "Водный мотоцикл"},
        "Test AVT visit PREMIUM": {"attraction_id": 16837, "attraction_name": "Кизомба"},
        "Test AVT visit classic": {"attraction_id": 17007, "attraction_name": "Водные лыжи"},
        "Test AVT visit LITE": {"attraction_id": 16838, "attraction_name": "Баня"},
        "Test AVT visit REGIN": {"attraction_id": 17006, "attraction_name": "Пренатальная йога"},
        "Test AVT visit VIP(no limit)": {
            "attraction_id": 17006,
            "attraction_name": "Пренатальная йога",
        },
    }
    supplier_by_name = _wait_for_today_accepted_visits(
        month_value, today_iso, expected_today_visits
    )
    journal_rows = _get_journal_rows_for_period(
        date_from=today.replace(day=1).isoformat(),
        date_finish=today_iso,
        admin_token=admin_token,
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

        assert journal_row.get("holder") == user_name, (
            f"В journal у id={supplier_visit_id} неверный holder: {journal_row}"
        )
        assert journal_row.get("status") == "app_holder_passed", (
            f"В journal у id={supplier_visit_id} неверный status: {journal_row}"
        )
        assert journal_row.get("company_name") == EXPECTED_JOURNAL_COMPANY, (
            f"В journal у id={supplier_visit_id} неверная company_name: {journal_row}"
        )
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
            f"пользователь={user_name}, услуга={expected['attraction_name']}"
        )


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Reject accepted visits and verify journal status")
def test_reject_accepted_visits_and_check_journal_status():
    today = datetime.now().date()
    today_iso = today.isoformat()
    month_value = today.strftime("%Y-%m")
    admin_token = _resolve_admin_token()
    assert admin_token, "Не удалось получить admin token для реджекта визитов."

    expected_today_visits = {
        "Test AVT visit VIP": {"attraction_id": 17008, "attraction_name": "Водный мотоцикл"},
        "Test AVT visit PREMIUM": {"attraction_id": 16837, "attraction_name": "Кизомба"},
        "Test AVT visit classic": {"attraction_id": 17007, "attraction_name": "Водные лыжи"},
        "Test AVT visit LITE": {"attraction_id": 16838, "attraction_name": "Баня"},
        "Test AVT visit REGIN": {"attraction_id": 17006, "attraction_name": "Пренатальная йога"},
        "Test AVT visit VIP(no limit)": {
            "attraction_id": 17006,
            "attraction_name": "Пренатальная йога",
        },
    }
    supplier_by_name = _wait_for_today_accepted_visits(
        month_value, today_iso, expected_today_visits
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
        assert journal_row.get("holder") == user_name, (
            f"В journal после реджекта у id={visit_id} неверный holder: {journal_row}"
        )
        assert journal_row.get("status") == "app_holder_reject", (
            f"В journal после реджекта у id={visit_id} неверный status: {journal_row}"
        )
        assert journal_row.get("company_name") == EXPECTED_JOURNAL_COMPANY, (
            f"В journal после реджекта у id={visit_id} неверная company_name: {journal_row}"
        )
        assert journal_row.get("sup_name") == EXPECTED_JOURNAL_SUPPLIER, (
            f"В journal после реджекта у id={visit_id} неверный supplier: {journal_row}"
        )
        print(
            f"РЕДЖЕКТ ПРОВЕРЕН: id={visit_id}, пользователь={user_name}, "
            f"услуга={expected['attraction_name']}, статус journal=app_holder_reject"
        )

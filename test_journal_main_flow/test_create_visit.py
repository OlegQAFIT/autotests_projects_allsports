import os
import re
import uuid
from pathlib import Path

import allure
import pytest
import requests
from dotenv import load_dotenv


load_dotenv()
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
MOBILE_API_PREFIX = "/api/holder/2.0.0"
CSRF_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/csrf-token"
REQUEST_SMS_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/request-sms"
CONFIRM_SMS_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/confirm-sms-code"
CREATE_VISIT_URL = f"{BASE_URL}{MOBILE_API_PREFIX}/suppliers/visit"
ADMIN_LOGIN_URL = f"{BASE_URL}/api/admin_login"

SMS_CODE = os.getenv("CREATE_VISIT_SMS_CODE", "").strip()
ADMIN_TOKEN = os.getenv("SUPPLIER_JRNL_ADMIN_TOKEN", "").strip()
ADMIN_EMAIL = os.getenv("SUPPLIER_JRNL_EMAIL", "").strip() or "oleg.fit@gmail.com"
ADMIN_PASSWORD = os.getenv("SUPPLIER_JRNL_PASSWORD", "").strip() or "9efbee942864"

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
    "premium_alt": {
        "phone": "375440000103",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 16838,
            "lat": 53.9006,
            "lng": 27.5590,
            "geo_mocked": False,
        },
    },
    "classic_alt": {
        "phone": "375440000104",
        "request_body": {
            "supplier_id": 5003,
            "attraction_id": 17006,
            "lat": 53.9006,
            "lng": 27.5590,
            "geo_mocked": False,
        },
    },
}


def _normalize_token(token):
    normalized = str(token or "").strip()
    if normalized.lower().startswith("bearer "):
        return normalized[7:].strip()
    return normalized


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
@allure.story("Create premium alt visit via mobile login flow")
def test_create_visit_premium_alt():
    profile = VISIT_PROFILES["premium_alt"]
    _login_and_create_visit(profile["phone"], profile["request_body"])


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create classic alt visit via mobile login flow")
def test_create_visit_classic_alt():
    profile = VISIT_PROFILES["classic_alt"]
    _login_and_create_visit(profile["phone"], profile["request_body"])

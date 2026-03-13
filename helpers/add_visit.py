import requests
import json
import uuid
import base64
import os
import pytest

JRNL_BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
LOGIN_URL = f"{JRNL_BASE_URL}/api/v1/token"
CREATE_VISIT_URL = f"{JRNL_BASE_URL}/api/v1/visit"

PHONE_TO_HOLDER_ID = {
    "+375330000088": 41232,
    "+375290000999": 41255,
}


class VisitDailyLimitReachedError(AssertionError):
    pass


def _to_int_or_none(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_token(token):
    if not token:
        return ""
    token = str(token).strip()
    if token.lower().startswith("bearer "):
        return token[7:].strip()
    return token


def _resolve_admin_token(token=None):
    if token:
        return _normalize_token(token)
    return _normalize_token(os.getenv("SUPPLIER_JRNL_ADMIN_TOKEN", ""))


def _extract_key_recursive(payload, key):
    if isinstance(payload, dict):
        if key in payload:
            return payload[key]
        for value in payload.values():
            found = _extract_key_recursive(value, key)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for item in payload:
            found = _extract_key_recursive(item, key)
            if found is not None:
                return found
    return None


def _journal_headers(admin_token):
    return {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {admin_token}",
    }


def _reset_installs(holder_id, admin_token):
    if not holder_id or not admin_token:
        return

    response = requests.post(
        f"{JRNL_BASE_URL}/api/jrnl/admin/holders/{holder_id}/reset/installs",
        headers=_journal_headers(admin_token),
    )
    if response.status_code not in (200, 204):
        raise AssertionError(
            f"RESET INSTALLS failed for holder {holder_id}. "
            f"status={response.status_code}, response={response.text}"
        )


def _reset_visit_limit(holder_id, admin_token):
    if not holder_id or not admin_token:
        return

    response = requests.post(
        f"{JRNL_BASE_URL}/api/jrnl/admin/holders/{holder_id}/reset/visit",
        headers=_journal_headers(admin_token),
    )
    if response.status_code not in (200, 204):
        raise AssertionError(
            f"RESET VISIT LIMIT failed for holder {holder_id}. "
            f"status={response.status_code}, response={response.text}"
        )


def _get_sms_token_v2(holder_id, admin_token):
    if not holder_id or not admin_token:
        return None

    response = requests.get(
        f"{JRNL_BASE_URL}/api/helpdesk/card/{holder_id}",
        headers=_journal_headers(admin_token),
    )
    if response.status_code != 200:
        raise AssertionError(
            f"GET HOLDER CARD failed for holder {holder_id}. "
            f"status={response.status_code}, response={response.text}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"Failed to decode holder card JSON for holder {holder_id}: {response.text}"
        ) from exc

    sms_token = _extract_key_recursive(payload, "sms_token_v2")
    if sms_token is None:
        sms_token = _extract_key_recursive(payload, "sms_token")
    if sms_token is None:
        raise AssertionError(
            f"sms_token_v2 not found in holder card for holder {holder_id}. response={payload}"
        )

    return str(sms_token)


def _mobile_login(phone_number, sms_code):
    api_token = str(uuid.uuid4())
    base64_string = base64.b64encode(api_token.encode("utf-8")).decode("utf-8")

    payload = json.dumps(
        {
            "phone": phone_number,
            "sms_token": sms_code,
            "api_token": base64_string,
            "instance_id": base64_string,
        }
    )
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(LOGIN_URL, headers=headers, data=payload)
    return response, api_token


def _create_visit(api_token, gym_token, attraction_id, holder_id=None, admin_token=None):
    def _make_request():
        payload = json.dumps(
            {
                "token": gym_token,
                "attraction_id": attraction_id,
                "lat": 0,
                "lng": 0,
            }
        )
        headers = {
            "Authorization": "Bearer " + api_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        return requests.post(CREATE_VISIT_URL, headers=headers, data=payload)

    def _extract_status_and_id(response):
        try:
            response_payload = response.json()
        except ValueError:
            response_payload = {}

        response_data = response_payload.get("data") if isinstance(response_payload, dict) else {}
        response_status = response_data.get("status") if isinstance(response_data, dict) else None
        response_id = response_data.get("id") if isinstance(response_data, dict) else None
        return response_status, response_id

    response = _make_request()

    if response.status_code == 201:
        return

    response_status, response_id = _extract_status_and_id(response)

    # На проде API иногда возвращает 403 с уже созданным визитом (status=wait, id>0).
    if response.status_code == 403 and response_status == "wait" and response_id:
        return

    # На этом проекте лимит визита можно снять через admin endpoint reset/visit.
    if response.status_code == 403 and response_status == "limit" and holder_id and admin_token:
        _reset_visit_limit(holder_id, admin_token)
        response = _make_request()
        if response.status_code == 201:
            return
        response_status, response_id = _extract_status_and_id(response)
        if response.status_code == 403 and response_status == "wait" and response_id:
            return

    if response.status_code == 403 and response_status == "limit":
        raise VisitDailyLimitReachedError(
            f"Daily visit limit reached. response={response.text}"
        )

    raise AssertionError(
        f"CREATE VISIT API failed. status={response.status_code}, response={response.text}"
    )


def _load_profiles_from_env():
    profiles = []

    def _build(prefix="SUPPLIER_VISIT"):
        phone = os.getenv(f"{prefix}_PHONE")
        sms_code = os.getenv(f"{prefix}_SMS_CODE")
        gym_token = os.getenv(f"{prefix}_GYM_TOKEN")
        attraction_id = os.getenv(f"{prefix}_ATTRACTION_ID")
        holder_id = _to_int_or_none(os.getenv(f"{prefix}_HOLDER_ID"))
        if holder_id is None and phone:
            holder_id = PHONE_TO_HOLDER_ID.get(phone)
        if all([phone, sms_code, gym_token, attraction_id]):
            return {
                "phone_number": phone,
                "sms_code": sms_code,
                "gym_token": gym_token,
                "attraction_id": int(attraction_id),
                "holder_id": holder_id,
            }
        return None

    first = _build("SUPPLIER_VISIT")
    second = _build("SUPPLIER_VISIT_2")
    if first:
        profiles.append(first)
    if second:
        profiles.append(second)
    return profiles


DEFAULT_VISIT_PROFILES = [
    {
        "phone_number": "+375330000088",
        "sms_code": "5566",
        "gym_token": "https://holder.allsports.by/s/6143",
        "attraction_id": 16835,
        "holder_id": 41232,
    },
    {
        "phone_number": "+375290000999",
        "sms_code": "1734",
        "gym_token": "https://holder.allsports.by/s/6143",
        "attraction_id": 16835,
        "holder_id": 41255,
    },
]

def login_and_create_visit(
    phone_number,
    sms_code,
    gym_token,
    attraction_id,
    holder_id=None,
    admin_token=None,
):
    holder_id = holder_id or PHONE_TO_HOLDER_ID.get(phone_number)
    admin_token = _resolve_admin_token(admin_token)
    current_sms_code = sms_code

    # При наличии admin token автоматически сбрасываем попытки и берем свежий sms_token_v2.
    if holder_id and admin_token:
        _reset_installs(holder_id, admin_token)
        fresh_sms = _get_sms_token_v2(holder_id, admin_token)
        if fresh_sms:
            current_sms_code = fresh_sms
        _reset_visit_limit(holder_id, admin_token)

    response, api_token = _mobile_login(phone_number, current_sms_code)

    if response.status_code != 200 and holder_id and admin_token:
        # Ретрай после повторного reset + получения нового sms_token_v2.
        _reset_installs(holder_id, admin_token)
        current_sms_code = _get_sms_token_v2(holder_id, admin_token)
        response, api_token = _mobile_login(phone_number, current_sms_code)

    if response.status_code != 200:
        admin_hint = ""
        if not admin_token:
            admin_hint = (
                " Для автосброса попыток и получения свежего sms_token_v2 "
                "задайте SUPPLIER_JRNL_ADMIN_TOKEN."
            )
        raise AssertionError(
            f"LOGIN API failed. status={response.status_code}, response={response.text}.{admin_hint}"
        )

    _create_visit(
        api_token,
        gym_token,
        attraction_id,
        holder_id=holder_id,
        admin_token=admin_token,
    )


def create_test_visit(profiles=None):
    env_profiles = _load_profiles_from_env()
    profiles = profiles or (env_profiles + DEFAULT_VISIT_PROFILES)
    errors = []
    limit_errors = []

    for profile in profiles:
        try:
            login_and_create_visit(
                phone_number=profile["phone_number"],
                sms_code=profile["sms_code"],
                gym_token=profile["gym_token"],
                attraction_id=profile["attraction_id"],
                holder_id=profile.get("holder_id"),
            )
            return profile
        except VisitDailyLimitReachedError as exc:
            limit_errors.append(f"{profile['phone_number']}: {exc}")
        except AssertionError as exc:
            errors.append(f"{profile['phone_number']}: {exc}")

    if limit_errors:
        details = "; ".join(limit_errors)
        if errors:
            details = f"{details}; fallback errors: {'; '.join(errors)}"
        raise VisitDailyLimitReachedError(
            "Не удалось создать новый визит: достигнут дневной лимит. " + details
        )

    joined_errors = "; ".join(errors) if errors else "No profiles provided."
    raise AssertionError(
        "Не удалось создать визит ни по одному тестовому профилю. "
        f"{joined_errors}. "
        "Укажите актуальные данные через env: SUPPLIER_VISIT_PHONE, SUPPLIER_VISIT_SMS_CODE, "
        "SUPPLIER_VISIT_GYM_TOKEN, SUPPLIER_VISIT_ATTRACTION_ID, "
        "SUPPLIER_VISIT_HOLDER_ID и SUPPLIER_JRNL_ADMIN_TOKEN."
    )


def test_login_and_create_visit():
    try:
        create_test_visit()
    except VisitDailyLimitReachedError as exc:
        pytest.skip(str(exc))

def test_login_and_create_visit_without_foto():
    profile = DEFAULT_VISIT_PROFILES[1]
    try:
        login_and_create_visit(
            phone_number=profile["phone_number"],
            sms_code=profile["sms_code"],
            gym_token=profile["gym_token"],
            attraction_id=profile["attraction_id"],
            holder_id=profile["holder_id"],
        )
    except VisitDailyLimitReachedError as exc:
        pytest.skip(str(exc))

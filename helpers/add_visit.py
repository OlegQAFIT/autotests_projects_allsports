import requests
import json
import uuid
import base64
import os
import pytest

JRNL_BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
LOGIN_URL = f"{JRNL_BASE_URL}/api/v1/token"
CREATE_VISIT_URL = f"{JRNL_BASE_URL}/api/v1/visit"
MOBILE_V2_CSRF_URL = f"{JRNL_BASE_URL}/api/holder/2.0.0/csrf-token"
MOBILE_V2_REQUEST_SMS_URL = f"{JRNL_BASE_URL}/api/holder/2.0.0/request-sms"
MOBILE_V2_CONFIRM_SMS_URL = f"{JRNL_BASE_URL}/api/holder/2.0.0/confirm-sms-code"
MOBILE_V2_CREATE_VISIT_URL = f"{JRNL_BASE_URL}/api/holder/2.0.0/suppliers/visit"
ADMIN_LOGIN_URL = f"{JRNL_BASE_URL}/api/admin_login"

PHONE_TO_HOLDER_ID = {
    "+375330000088": 41232,
    "+375290000999": 41255,
}


class VisitDailyLimitReachedError(AssertionError):
    pass


class VisitNoInstallsError(AssertionError):
    pass


def _to_int_or_none(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_str_or_none(value):
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


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


def _resolve_admin_credentials(email=None, password=None):
    resolved_email = email or os.getenv("SUPPLIER_JRNL_EMAIL", "")
    resolved_password = password or os.getenv("SUPPLIER_JRNL_PASSWORD", "")
    return resolved_email.strip(), resolved_password.strip()


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


def _get_admin_token_from_credentials(email=None, password=None):
    email, password = _resolve_admin_credentials(email, password)
    if not email or not password:
        return None

    response = requests.post(
        ADMIN_LOGIN_URL,
        json={"email": email, "password": password},
    )
    if response.status_code != 200:
        raise AssertionError(
            f"ADMIN LOGIN failed. status={response.status_code}, response={response.text}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"Failed to decode admin login JSON: {response.text}"
        ) from exc

    access_token = payload.get("access_token")
    if not access_token:
        raise AssertionError(f"access_token not found in admin login response: {payload}")
    return str(access_token)


def _get_working_admin_token(admin_token=None, email=None, password=None):
    token = _resolve_admin_token(admin_token)
    if token:
        probe = requests.get(
            f"{JRNL_BASE_URL}/api/helpdesk/card/1",
            headers=_journal_headers(token),
        )
        if probe.status_code == 200:
            return token
    try:
        return _get_admin_token_from_credentials(email=email, password=password)
    except AssertionError:
        return None


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


def _find_holder_id_by_phone(phone_number, admin_token):
    normalized_phone = str(phone_number or "").strip()
    if not normalized_phone or not admin_token:
        return None

    response = requests.get(
        f"{JRNL_BASE_URL}/api/helpdesk/load_holder_by",
        headers=_journal_headers(admin_token),
        params={"card_id": "", "holder": normalized_phone},
    )
    if response.status_code in (401, 403):
        return None
    if response.status_code != 200:
        raise AssertionError(
            f"LOAD HOLDER BY PHONE failed for {normalized_phone}. "
            f"status={response.status_code}, response={response.text}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"Failed to decode holder search JSON for phone {normalized_phone}: {response.text}"
        ) from exc

    items = payload.get("data", []) if isinstance(payload, dict) else []
    requested_phone = "".join(ch for ch in normalized_phone if ch.isdigit())
    exact_matches = [
        item
        for item in items
        if isinstance(item, dict)
        and "".join(ch for ch in str(item.get("phone_number", "")) if ch.isdigit()) == requested_phone
    ]
    if len(exact_matches) != 1:
        return None

    holder_id = exact_matches[0].get("id")
    if not holder_id:
        return None
    return int(holder_id)


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


def _mobile_v2_headers(instance_id, csrf_token=None, language="ru_RU"):
    headers = {
        "Accept": "application/json",
        "X-INSTANCE-ID": instance_id,
        "host": "xn--d1aey.xn--k1aahcehedi.xn--90ais",
        "connection": "close",
        "content-language": language,
        "User-Agent": "android-MB",
    }
    if csrf_token:
        headers["X-CSRF-TOKEN"] = csrf_token
    return headers


def _get_mobile_v2_csrf_token(instance_id):
    response = requests.get(
        MOBILE_V2_CSRF_URL,
        headers={
            "Accept": "*/*",
            "X-INSTANCE-ID": instance_id,
            "Host": "xn--d1aey.xn--k1aahcehedi.xn--90ais",
            "Connection": "keep-alive",
            "User-Agent": "PostmanRuntime/7.54.0",
        },
    )
    if response.status_code != 200:
        raise AssertionError(
            f"CSRF API failed. status={response.status_code}, response={response.text}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"Failed to decode csrf JSON: {response.text}"
        ) from exc

    csrf_token = payload.get("csrf-token") or payload.get("csrf_token")
    if not csrf_token:
        raise AssertionError(f"csrf-token not found in response: {payload}")
    return str(csrf_token)


def _request_sms_v2(phone_number, instance_id, csrf_token):
    response = requests.post(
        MOBILE_V2_REQUEST_SMS_URL,
        headers={
            **_mobile_v2_headers(instance_id, csrf_token=csrf_token, language="ru_RU"),
            "Content-Type": "application/json",
        },
        json={
            "phone": str(phone_number).replace("+", ""),
            "csrf_token": csrf_token,
        },
    )
    if response.status_code != 200:
        raise AssertionError(
            f"REQUEST SMS API failed. status={response.status_code}, response={response.text}"
        )


def _confirm_sms_v2(phone_number, sms_code, instance_id, csrf_token):
    response = requests.post(
        MOBILE_V2_CONFIRM_SMS_URL,
        headers={
            **_mobile_v2_headers(instance_id, csrf_token=csrf_token, language="ru_BY"),
            "Content-Type": "application/json",
        },
        json={
            "phone": str(phone_number).replace("+", ""),
            "sms_code": str(sms_code),
            "csrf_token": csrf_token,
        },
    )
    if response.status_code != 200:
        raise AssertionError(
            f"CONFIRM SMS API failed. status={response.status_code}, response={response.text}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"Failed to decode confirm sms JSON: {response.text}"
        ) from exc

    oauth_token = payload.get("oauth-token") or payload.get("oauth_token")
    if not oauth_token:
        if payload.get("state") == "no_installs":
            raise VisitNoInstallsError(f"oauth-token not found in confirm sms response: {payload}")
        raise AssertionError(f"oauth-token not found in confirm sms response: {payload}")
    return str(oauth_token)


def _get_holder_level(holder_id, admin_token):
    response = requests.get(
        f"{JRNL_BASE_URL}/api/helpdesk/card/{holder_id}",
        headers=_journal_headers(admin_token),
    )
    if response.status_code != 200:
        raise AssertionError(
            f"GET HOLDER CARD failed for holder {holder_id}. "
            f"status={response.status_code}, response={response.text}"
        )
    payload = response.json()
    return str(payload.get("holder", {}).get("level") or "").strip()


def _get_supplier_attraction(supplier_id, attraction_id, admin_token):
    response = requests.get(
        f"{JRNL_BASE_URL}/api/suppliers/{supplier_id}/attractions",
        headers=_journal_headers(admin_token),
    )
    if response.status_code != 200:
        raise AssertionError(
            f"GET SUPPLIER ATTRACTIONS failed for supplier {supplier_id}. "
            f"status={response.status_code}, response={response.text}"
        )

    payload = response.json()
    attractions = payload.get("data", []) if isinstance(payload, dict) else []
    for attraction in attractions:
        if attraction.get("id") == attraction_id:
            return attraction
    raise AssertionError(
        f"Attraction {attraction_id} not found for supplier {supplier_id}. response={payload}"
    )


def _normalize_holder_level_codes(level_value):
    normalized = str(level_value or "").strip().lower()
    aliases = {
        "red": {"R"},
        "silver": {"S"},
        "gold": {"G"},
        "platinum": {"P"},
        "lite": {"L"},
        "classic": {"C"},
        "medium": {"M"},
        "vip": {"V"},
    }
    if normalized in aliases:
        return aliases[normalized]
    if not normalized:
        return set()
    return {normalized.upper()}


def _normalize_allowed_level_codes(raw_levels):
    codes = set()
    for raw_level in raw_levels:
        level = str(raw_level or "").strip().upper()
        if not level:
            continue
        if level.endswith("+") and len(level) == 2 and level[0].isalpha():
            codes.add(level[0])
        if len(level) > 1 and "+" not in level and "," not in level:
            codes.update(level)
            continue
        codes.add(level)
    return codes


def _assert_holder_can_use_attraction(holder_id, supplier_id, attraction_id, admin_token):
    if not holder_id or not admin_token or not supplier_id or not attraction_id:
        return

    holder_level = _get_holder_level(holder_id, admin_token)
    attraction = _get_supplier_attraction(supplier_id, attraction_id, admin_token)
    allowed_levels = [
        level.strip()
        for level in (
            f"{attraction.get('levels', '')},{attraction.get('limited_levels', '')}"
        ).split(",")
        if level.strip()
    ]
    holder_codes = _normalize_holder_level_codes(holder_level)
    allowed_codes = _normalize_allowed_level_codes(allowed_levels)
    if allowed_codes and holder_codes and not (holder_codes & allowed_codes):
        raise AssertionError(
            f"Holder {holder_id} has level '{holder_level}', but attraction {attraction_id} "
            f"for supplier {supplier_id} allows only {sorted(allowed_codes)}. "
            f"Current mobile API returns backend error for this incompatible combination."
        )


def _create_visit_v2(oauth_token, supplier_id, attraction_id, lat, lng, holder_id=None, admin_token=None):
    def _make_request():
        return requests.post(
            MOBILE_V2_CREATE_VISIT_URL,
            headers={
                "Authorization": f"Bearer {oauth_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "supplier_id": supplier_id,
                "attraction_id": attraction_id,
                "lat": lat,
                "lng": lng,
                "geo_mocked": False,
            },
        )

    response = _make_request()

    if response.status_code in (200, 201):
        return

    try:
        payload = response.json()
    except ValueError:
        payload = {}

    response_status = payload.get("status") if isinstance(payload, dict) else None
    response_data = payload.get("data") if isinstance(payload, dict) else {}
    if response_status is None and isinstance(response_data, dict):
        response_status = response_data.get("status")

    if response.status_code == 403 and response_status == "limit" and holder_id and admin_token:
        _reset_visit_limit(holder_id, admin_token)
        response = _make_request()
        if response.status_code in (200, 201):
            return

        try:
            payload = response.json()
        except ValueError:
            payload = {}
        response_status = payload.get("status") if isinstance(payload, dict) else None
        response_data = payload.get("data") if isinstance(payload, dict) else {}
        if response_status is None and isinstance(response_data, dict):
            response_status = response_data.get("status")

    if response.status_code == 403 and response_status == "limit":
        raise VisitDailyLimitReachedError(
            f"Daily visit limit reached. response={response.text}"
        )

    raise AssertionError(
        f"CREATE VISIT V2 API failed. status={response.status_code}, response={response.text}"
    )


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
        phone = _to_str_or_none(os.getenv(f"{prefix}_PHONE"))
        sms_code = _to_str_or_none(os.getenv(f"{prefix}_SMS_CODE"))
        gym_token = _to_str_or_none(os.getenv(f"{prefix}_GYM_TOKEN"))
        attraction_id = _to_str_or_none(os.getenv(f"{prefix}_ATTRACTION_ID"))
        holder_id = _to_int_or_none(os.getenv(f"{prefix}_HOLDER_ID"))
        supplier_id = _to_int_or_none(os.getenv(f"{prefix}_SUPPLIER_ID"))
        lat = _to_str_or_none(os.getenv(f"{prefix}_LAT"))
        lng = _to_str_or_none(os.getenv(f"{prefix}_LNG"))
        if holder_id is None and phone:
            holder_id = PHONE_TO_HOLDER_ID.get(phone)
        has_legacy_profile = all([phone, sms_code, gym_token, attraction_id])
        has_mobile_v2_profile = all([phone, attraction_id, supplier_id, lat, lng])
        if not has_legacy_profile and not has_mobile_v2_profile:
            return None

        profile = {
                "phone_number": phone,
                "sms_code": sms_code,
                "gym_token": gym_token,
                "attraction_id": int(attraction_id),
                "holder_id": holder_id,
            }
        if supplier_id is not None:
            profile["supplier_id"] = supplier_id
        if lat is not None:
            profile["lat"] = float(lat)
        if lng is not None:
            profile["lng"] = float(lng)
        return profile

    first = _build("SUPPLIER_VISIT")
    second = _build("SUPPLIER_VISIT_2")
    if first:
        profiles.append(first)
    if second:
        profiles.append(second)

    unique_profiles = []
    seen = set()
    for profile in profiles:
        key = (
            profile.get("phone_number"),
            profile.get("sms_code"),
            profile.get("gym_token"),
            profile.get("attraction_id"),
            profile.get("holder_id"),
            profile.get("supplier_id"),
            profile.get("lat"),
            profile.get("lng"),
        )
        if key in seen:
            continue
        seen.add(key)
        unique_profiles.append(profile)
    return unique_profiles


def _deduplicate_profiles(profiles):
    unique_profiles = []
    seen = set()
    for profile in profiles:
        key = (
            profile.get("phone_number"),
            profile.get("sms_code"),
            profile.get("gym_token"),
            profile.get("attraction_id"),
            profile.get("holder_id"),
            profile.get("supplier_id"),
            profile.get("lat"),
            profile.get("lng"),
        )
        if key in seen:
            continue
        seen.add(key)
        unique_profiles.append(profile)
    return unique_profiles


DEFAULT_VISIT_PROFILES = [
    {
        "phone_number": "+375440000105",
        "sms_code": None,
        "gym_token": None,
        "attraction_id": 16835,
        "holder_id": None,
        "supplier_id": 5003,
        "lat": 53.90450845,
        "lng": 27.56395822,
    },
    {
        "phone_number": "375440000100",
        "sms_code": None,
        "gym_token": None,
        "attraction_id": 17008,
        "holder_id": None,
        "supplier_id": 5003,
        "lat": 53.904963940824274,
        "lng": 27.561529701524286,
    },
    {
        "phone_number": "375440000101",
        "sms_code": None,
        "gym_token": None,
        "attraction_id": 16837,
        "holder_id": None,
        "supplier_id": 5003,
        "lat": 53.9006,
        "lng": 27.5590,
    },
    {
        "phone_number": "375440000102",
        "sms_code": None,
        "gym_token": None,
        "attraction_id": 17007,
        "holder_id": None,
        "supplier_id": 5003,
        "lat": 53.9006,
        "lng": 27.5590,
    },
    {
        "phone_number": "375440000103",
        "sms_code": None,
        "gym_token": None,
        "attraction_id": 16838,
        "holder_id": None,
        "supplier_id": 5003,
        "lat": 53.9006,
        "lng": 27.5590,
    },
    {
        "phone_number": "375440000104",
        "sms_code": None,
        "gym_token": None,
        "attraction_id": 17006,
        "holder_id": None,
        "supplier_id": 5003,
        "lat": 53.9006,
        "lng": 27.5590,
    },
]

def login_and_create_visit(
    phone_number,
    sms_code,
    gym_token,
    attraction_id,
    holder_id=None,
    admin_token=None,
    supplier_id=None,
    lat=None,
    lng=None,
):
    if supplier_id is not None and lat is not None and lng is not None:
        working_admin_token = _get_working_admin_token(admin_token=admin_token)
        if holder_id is None and working_admin_token:
            holder_id = _find_holder_id_by_phone(phone_number, working_admin_token)
        instance_id = str(uuid.uuid4())
        csrf_token = _get_mobile_v2_csrf_token(instance_id)
        effective_sms_code = sms_code

        if working_admin_token:
            _assert_holder_can_use_attraction(
                holder_id=holder_id,
                supplier_id=supplier_id,
                attraction_id=attraction_id,
                admin_token=working_admin_token,
            )
            if holder_id:
                _reset_installs(holder_id, working_admin_token)
            _request_sms_v2(phone_number, instance_id, csrf_token)
            fresh_sms_code = _get_sms_token_v2(holder_id, working_admin_token) if holder_id else sms_code
            if fresh_sms_code:
                effective_sms_code = fresh_sms_code

        effective_sms_code = _to_str_or_none(effective_sms_code)
        if effective_sms_code is None:
            raise AssertionError(
                "Не удалось получить актуальный sms_code для mobile API 2.0. "
                "Передайте рабочий sms_code вручную или задайте SUPPLIER_JRNL_EMAIL / "
                "SUPPLIER_JRNL_PASSWORD, чтобы helper смог автоматически получить новый код."
            )

        try:
            oauth_token = _confirm_sms_v2(phone_number, effective_sms_code, instance_id, csrf_token)
        except VisitNoInstallsError:
            if not (working_admin_token and holder_id):
                raise
            _reset_installs(holder_id, working_admin_token)
            _request_sms_v2(phone_number, instance_id, csrf_token)
            refreshed_sms_code = _get_sms_token_v2(holder_id, working_admin_token)
            oauth_token = _confirm_sms_v2(phone_number, refreshed_sms_code, instance_id, csrf_token)
        _create_visit_v2(
            oauth_token,
            supplier_id,
            attraction_id,
            lat,
            lng,
            holder_id=holder_id,
            admin_token=working_admin_token,
        )
        return

    holder_id = holder_id or PHONE_TO_HOLDER_ID.get(phone_number)
    admin_token = _resolve_admin_token(admin_token)
    current_sms_code = sms_code

    # При наличии admin token пытаемся сбросить попытки и взять свежий sms_token_v2.
    # Если token протух, не блокируем сценарий и пробуем исходный sms_code.
    if holder_id and admin_token:
        try:
            _reset_installs(holder_id, admin_token)
            fresh_sms = _get_sms_token_v2(holder_id, admin_token)
            if fresh_sms:
                current_sms_code = fresh_sms
            _reset_visit_limit(holder_id, admin_token)
        except AssertionError:
            pass

    response, api_token = _mobile_login(phone_number, current_sms_code)

    if response.status_code != 200 and holder_id and admin_token:
        # Ретрай после повторного reset + получения нового sms_token_v2.
        try:
            _reset_installs(holder_id, admin_token)
            current_sms_code = _get_sms_token_v2(holder_id, admin_token)
            response, api_token = _mobile_login(phone_number, current_sms_code)
        except AssertionError:
            pass

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
    if profiles is None:
        profiles = _deduplicate_profiles(DEFAULT_VISIT_PROFILES + env_profiles)
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
                admin_token=profile.get("admin_token"),
                supplier_id=profile.get("supplier_id"),
                lat=profile.get("lat"),
                lng=profile.get("lng"),
            )
            return profile
        except VisitDailyLimitReachedError as exc:
            limit_errors.append(f"{profile['phone_number']}: {exc}")
        except AssertionError as exc:
            if (
                profile.get("supplier_id") is not None
                and _to_str_or_none(profile.get("sms_code")) is None
                and "Не удалось получить актуальный sms_code" in str(exc)
            ):
                errors.append(
                    f"{profile['phone_number']}: {exc} "
                    "Проверьте SUPPLIER_JRNL_EMAIL / SUPPLIER_JRNL_PASSWORD "
                    "или обновите SUPPLIER_JRNL_ADMIN_TOKEN."
                )
                continue
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
        "Укажите актуальные данные через env: SUPPLIER_VISIT_PHONE, SUPPLIER_VISIT_ATTRACTION_ID, "
        "SUPPLIER_VISIT_HOLDER_ID и либо SUPPLIER_VISIT_GYM_TOKEN, либо "
        "SUPPLIER_VISIT_SUPPLIER_ID вместе с SUPPLIER_VISIT_LAT/SUPPLIER_VISIT_LNG. "
        "Для автоматического получения свежего sms кода задайте "
        "SUPPLIER_JRNL_EMAIL / SUPPLIER_JRNL_PASSWORD или рабочий SUPPLIER_JRNL_ADMIN_TOKEN."
    )


def test_login_and_create_visit():
    try:
        create_test_visit()
    except VisitDailyLimitReachedError as exc:
        pytest.skip(str(exc))

def test_login_and_create_visit_without_foto():
    profile = DEFAULT_VISIT_PROFILES[0]
    try:
        login_and_create_visit(
            phone_number=profile["phone_number"],
            sms_code=profile["sms_code"],
            gym_token=profile["gym_token"],
            attraction_id=profile["attraction_id"],
            holder_id=profile["holder_id"],
            supplier_id=profile.get("supplier_id"),
            lat=profile.get("lat"),
            lng=profile.get("lng"),
        )
    except VisitDailyLimitReachedError as exc:
        pytest.skip(str(exc))

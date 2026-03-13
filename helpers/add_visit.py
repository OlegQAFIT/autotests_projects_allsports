import requests
import json
import uuid
import base64
import os


def _load_profiles_from_env():
    profiles = []

    def _build(prefix="SUPPLIER_VISIT"):
        phone = os.getenv(f"{prefix}_PHONE")
        sms_code = os.getenv(f"{prefix}_SMS_CODE")
        gym_token = os.getenv(f"{prefix}_GYM_TOKEN")
        attraction_id = os.getenv(f"{prefix}_ATTRACTION_ID")
        if all([phone, sms_code, gym_token, attraction_id]):
            return {
                "phone_number": phone,
                "sms_code": sms_code,
                "gym_token": gym_token,
                "attraction_id": int(attraction_id),
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
    },
    {
        "phone_number": "+375290000999",
        "sms_code": "1734",
        "gym_token": "https://holder.allsports.by/s/6143",
        "attraction_id": 16835,
    },
]

def login_and_create_visit(phone_number, sms_code, gym_token, attraction_id):
    LOGIN_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais/api/v1/token"
    CREATE_VISIT_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais/api/v1/visit"

    api_token = str(uuid.uuid4())
    uuid_bytes = api_token.encode('utf-8')
    base64_encoded = base64.b64encode(uuid_bytes)
    base64_string = base64_encoded.decode('utf-8')

    payload = json.dumps({
        "phone": phone_number,
        "sms_token": sms_code,
        "api_token": base64_string,
        "instance_id": base64_string
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(LOGIN_URL, headers=headers, data=payload)

    assert response.status_code == 200, (
        f"LOGIN API failed. status={response.status_code}, response={response.text}"
    )

    payload = json.dumps({
      "token": gym_token,
      "attraction_id": attraction_id,
      "lat": 0,
      "lng": 0
    })
    headers = {
      'Authorization': 'Bearer ' + api_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

    response = requests.post(CREATE_VISIT_URL, headers=headers, data=payload)

    if response.status_code == 201:
        return

    try:
        response_payload = response.json()
    except ValueError:
        response_payload = {}

    response_data = response_payload.get("data") if isinstance(response_payload, dict) else {}
    response_status = response_data.get("status") if isinstance(response_data, dict) else None
    response_id = response_data.get("id") if isinstance(response_data, dict) else None

    # На проде API иногда возвращает 403 с уже созданным визитом (status=wait, id>0).
    if response.status_code == 403 and response_status == "wait" and response_id:
        return

    raise AssertionError(
        f"CREATE VISIT API failed. status={response.status_code}, response={response.text}"
    )


def create_test_visit(profiles=None):
    env_profiles = _load_profiles_from_env()
    profiles = profiles or (env_profiles + DEFAULT_VISIT_PROFILES)
    errors = []

    for profile in profiles:
        try:
            login_and_create_visit(
                phone_number=profile["phone_number"],
                sms_code=profile["sms_code"],
                gym_token=profile["gym_token"],
                attraction_id=profile["attraction_id"],
            )
            return profile
        except AssertionError as exc:
            errors.append(f"{profile['phone_number']}: {exc}")

    joined_errors = "; ".join(errors) if errors else "No profiles provided."
    raise AssertionError(
        "Не удалось создать визит ни по одному тестовому профилю. "
        f"{joined_errors}. "
        "Укажите актуальные данные через env: SUPPLIER_VISIT_PHONE, SUPPLIER_VISIT_SMS_CODE, "
        "SUPPLIER_VISIT_GYM_TOKEN, SUPPLIER_VISIT_ATTRACTION_ID."
    )


def test_login_and_create_visit():
    create_test_visit()

def test_login_and_create_visit_without_foto():
    profile = DEFAULT_VISIT_PROFILES[1]
    login_and_create_visit(
        phone_number=profile["phone_number"],
        sms_code=profile["sms_code"],
        gym_token=profile["gym_token"],
        attraction_id=profile["attraction_id"],
    )

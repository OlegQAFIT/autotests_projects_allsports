import allure
import requests


BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
CREATE_VISIT_URL = f"{BASE_URL}/api/holder/2.0.0/suppliers/visit"

VIP_HOLDER_BEARER_TOKEN = "7198|fYRr621CX1pGoLkCOhPqz76yJTkWAFTXdZ5Xe9o9"
VIP_REQUEST_BODY = {
    "supplier_id": 5003,
    "attraction_id": 17008,
    "lat": 53.904963940824274,
    "lng": 27.561529701524286,
    "geo_mocked": False,
}

PREMIUM_HOLDER_BEARER_TOKEN = "7197|BCSggRswAypG5Z8QhPYCRFdxiiW2A8JWA5TD6Wrj"
PREMIUM_REQUEST_BODY = {
    "supplier_id": 5003,
    "attraction_id": 16837,
    "lat": 53.9006,
    "lng": 27.5590,
    "geo_mocked": False,
}

CLASSIC_HOLDER_BEARER_TOKEN = "7200|Ow2un01rJelboXOlquG6C99imcWkzfkvlbkPBiWf"
CLASSIC_REQUEST_BODY = {
    "supplier_id": 5003,
    "attraction_id": 17007,
    "lat": 53.9006,
    "lng": 27.5590,
    "geo_mocked": False,
}


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create supplier VIP visit on limit")
def test_create_visit_holder_vip_on_limit():
    response = requests.post(
        CREATE_VISIT_URL,
        headers={
            "Authorization": f"Bearer {VIP_HOLDER_BEARER_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=VIP_REQUEST_BODY,
        timeout=30,
    )

    assert response.status_code == 201, (
        "Не удалось создать визит через holder API. "
        f"status={response.status_code}, body={response.text}"
    )

    body = response.json()
    assert isinstance(body.get("id"), int), f"Поле id отсутствует или некорректно: {body}"
    assert body.get("status") == "wait", f"Ожидался статус wait, получено: {body}"
    assert body.get("timeout_at"), f"Поле timeout_at отсутствует: {body}"
    assert "content" in body, f"Поле content отсутствует: {body}"


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create supplier premium visit on limit")
def test_create_visit_holder_premium_on_limit():
    response = requests.post(
        CREATE_VISIT_URL,
        headers={
            "Authorization": f"Bearer {PREMIUM_HOLDER_BEARER_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=PREMIUM_REQUEST_BODY,
        timeout=30,
    )

    assert response.status_code == 201, (
        "Не удалось создать визит через holder API. "
        f"status={response.status_code}, body={response.text}"
    )

    body = response.json()
    assert isinstance(body.get("id"), int), f"Поле id отсутствует или некорректно: {body}"
    assert body.get("status") == "wait", f"Ожидался статус wait, получено: {body}"
    assert body.get("timeout_at"), f"Поле timeout_at отсутствует: {body}"
    assert "content" in body, f"Поле content отсутствует: {body}"


@allure.feature("Holder API")
@allure.severity("critical")
@allure.story("Create supplier classic visit")
def test_create_visit_holder_classic():
    response = requests.post(
        CREATE_VISIT_URL,
        headers={
            "Authorization": f"Bearer {CLASSIC_HOLDER_BEARER_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=CLASSIC_REQUEST_BODY,
        timeout=30,
    )

    assert response.status_code == 201, (
        "Не удалось создать визит через holder API. "
        f"status={response.status_code}, body={response.text}"
    )

    body = response.json()
    assert isinstance(body.get("id"), int), f"Поле id отсутствует или некорректно: {body}"
    assert body.get("status") == "wait", f"Ожидался статус wait, получено: {body}"
    assert body.get("timeout_at"), f"Поле timeout_at отсутствует: {body}"
    assert "content" in body, f"Поле content отсутствует: {body}"

# -*- coding: utf-8 -*-
import time
from urllib.parse import urlparse

import allure
import pytest
import requests


pytestmark = [pytest.mark.live_api]


CONTACT_ENDPOINTS = [
    "/api/www/2.0.0/contact/get_offer",
    "/api/www/2.0.0/contact/become_partner",
    "/api/www/2.0.0/contact/ask_question",
]


def _require_staging_host(request):
    base_url = request.config.getoption("--base-url")
    parsed = urlparse(base_url)
    host = (parsed.netloc or "").lower()

    # Safety guard: never run live contact POST contract on production.
    if "sportbenefit" not in host or "staging" not in host:
        pytest.skip(
            "Live SB POST contract is allowed only on staging SportBenefit hosts. "
            f"Current --base-url host: {host or '<empty>'}"
        )

    return f"{parsed.scheme}://{parsed.netloc}".rstrip("/")


def _payload_for(endpoint_path: str):
    stamp = int(time.time())
    phone = "35799112233"

    if endpoint_path.endswith("/ask_question"):
        return {
            "name": f"QA Contract {stamp}",
            "email": f"qa.contract.{stamp}@example.com",
            "phone": phone,
            "processPersonalData": True,
            "country": "cy",
            "question": "Staging contract check from autotests",
        }

    return {
        "name": f"QA Contract {stamp}",
        "email": f"qa.contract.{stamp}@example.com",
        "phone": phone,
        "processPersonalData": True,
        "country": "cy",
        "companyName": f"QA Contract Company {stamp}",
        "location": "Nicosia",
    }


@allure.feature("SB Live API Contract")
@allure.severity("Critical")
@pytest.mark.parametrize("endpoint_path", CONTACT_ENDPOINTS)
def test_contact_post_contract_live_staging_sb(request, endpoint_path):
    """Проверка live POST-контракта контактных API на staging окружении."""
    api_base = _require_staging_host(request)
    url = f"{api_base}{endpoint_path}"

    payload = _payload_for(endpoint_path)
    response = requests.post(url, json=payload, timeout=25)

    assert response.status_code in (200, 201, 202, 204), (
        f"Live POST contract failed for {url}. "
        f"status={response.status_code}, body={(response.text or '')[:300]}"
    )

    if response.status_code == 200:
        content_type = (response.headers.get("Content-Type") or "").lower()
        assert "text/html" not in content_type, (
            f"POST to {url} returned HTML page instead of API response. "
            f"content-type={content_type}, body={(response.text or '')[:300]}"
        )

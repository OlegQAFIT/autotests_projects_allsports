# -*- coding: utf-8 -*-
import hashlib
import json
import os
import time
from pathlib import Path

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.new_web_site_sb.base_page_sb import BasePageSb


BASELINE_DIR = Path(__file__).resolve().parent / "visual_baseline_sb"
BASELINE_HASHES_FILE = BASELINE_DIR / "hashes.json"
CURRENT_DIR = BASELINE_DIR / "current"
UPDATE_BASELINE = os.getenv("SB_VISUAL_UPDATE", "").strip() == "1"


VISUAL_CASES = [
    {"key": "home_desktop", "url": "https://www.sportbenefit.eu/en-cy", "viewport": (1440, 900)},
    {"key": "home_mobile", "url": "https://www.sportbenefit.eu/en-cy", "viewport": (390, 844)},
    {"key": "facilities_table_desktop", "url": "https://www.sportbenefit.eu/en-cy/facilities-table", "viewport": (1440, 900)},
    {"key": "companies_desktop", "url": "https://www.sportbenefit.eu/en-cy/companies", "viewport": (1440, 900)},
    {"key": "app_desktop", "url": "https://www.sportbenefit.eu/en-cy/app", "viewport": (1440, 900)},
]


def _load_baseline_hashes():
    if not BASELINE_HASHES_FILE.exists():
        return {}
    try:
        return json.loads(BASELINE_HASHES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_baseline_hashes(data):
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    BASELINE_HASHES_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _hash_bytes(raw_bytes: bytes) -> str:
    return hashlib.sha256(raw_bytes).hexdigest()


def _prepare_stable_visual_state(driver):
    driver.execute_script(
        """
        const hideSelectors = [
          '.cookie-primary-modal',
          '.cookie-secondary-modal',
          '.mapboxgl-control-container',
          '.mapboxgl-canvas-container',
          '.mapboxgl-canvas',
          'video',
          'iframe[src*="youtube"]',
          '[class*="spinner"]',
          '[class*="loader"]'
        ];
        hideSelectors.forEach((selector) => {
          document.querySelectorAll(selector).forEach((el) => {
            el.style.visibility = 'hidden';
          });
        });
        """
    )
    time.sleep(0.6)


@allure.feature("SB Visual Regression")
@allure.severity("Normal")
@pytest.mark.pre_release
@pytest.mark.visual_regression
def test_visual_baseline_hashes_sb(driver):
    """Проверка визуальной регрессии по hash-бейзлайну ключевых страниц."""
    page = BasePageSb(driver)
    baseline = _load_baseline_hashes()
    CURRENT_DIR.mkdir(parents=True, exist_ok=True)

    current_hashes = {}
    mismatches = []
    missing = []

    for case in VISUAL_CASES:
        width, height = case["viewport"]
        key = case["key"]
        url = case["url"]

        driver.set_window_size(width, height)
        page.open_url(url)
        page.accept_cookie_consent()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        _prepare_stable_visual_state(driver)

        image = driver.get_screenshot_as_png()
        current_hash = _hash_bytes(image)
        current_hashes[key] = current_hash
        (CURRENT_DIR / f"{key}.png").write_bytes(image)

        if UPDATE_BASELINE:
            continue

        expected_hash = baseline.get(key)
        if not expected_hash:
            missing.append(key)
            continue
        if current_hash != expected_hash:
            mismatches.append(
                f"{key}: expected={expected_hash[:16]}..., actual={current_hash[:16]}..., url={url}, viewport={width}x{height}"
            )

    if UPDATE_BASELINE:
        _save_baseline_hashes(current_hashes)
        pytest.skip("Visual baseline hashes updated via SB_VISUAL_UPDATE=1")

    assert not missing, (
        "Visual baseline keys are missing. Run with SB_VISUAL_UPDATE=1 to record baseline. Missing keys: "
        + ", ".join(missing)
    )
    assert not mismatches, "Visual regression hash mismatches found:\n" + "\n".join(mismatches)

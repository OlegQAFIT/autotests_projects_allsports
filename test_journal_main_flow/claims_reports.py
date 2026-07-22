import os
import tempfile
import time
from datetime import date, timedelta
from pathlib import Path

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.journal.company import Company


BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
CLAIMS_FILTER_INPUT = (By.ID, "stat_filter_at")
CLAIMS_REPORT_BUTTONS = [
    {
        "name": "Card Types Statistics by Month",
        "xpath": "/html/body/div/div/div/div[2]/button[1]",
    },
    {
        "name": "Summary Statistics by Month",
        "xpath": "/html/body/div/div/div/div[2]/button[2]",
    },
    {
        "name": "Marginality Report",
        "xpath": "/html/body/div/div/div/div[2]/button[3]",
    },
    {
        "name": "B2B Statistics by Month",
        "xpath": "/html/body/div/div/div/div[2]/button[4]",
    },
    {
        "name": "B2С Statistics by Month",
        "xpath": "/html/body/div/div/div/div[2]/button[5]",
    },
    {
        "name": "Copay Statistics by Month",
        "xpath": "/html/body/div/div/div/div[2]/button[6]",
    },
    {
        "name": "Visit Statistics by Month",
        "xpath": "/html/body/div/div/div/div[2]/button[7]",
    },
]

JOURNAL_LOGIN = os.getenv("JOURNAL_COMPANY_LOGIN", "oleg.fit@gmail.com")
JOURNAL_PASSWORD = os.getenv("JOURNAL_COMPANY_PASSWORD", "9efbee942864")


def _get_previous_month_value(reference_date=None):
    current_date = reference_date or date.today()
    first_day_of_current_month = current_date.replace(day=1)
    previous_month_last_day = first_day_of_current_month - timedelta(days=1)
    return previous_month_last_day.strftime("%Y-%m")


def _claims_page_url(month_value):
    return f"{BASE_URL}/claims/list/{month_value}"


def _configure_download_dir(driver):
    download_dir = Path(tempfile.mkdtemp(prefix="claims_reports_"))
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {"behavior": "allow", "downloadPath": str(download_dir)},
    )
    return download_dir


def _install_claims_network_probe(driver):
    # The claims page triggers report downloads through XHR requests.
    driver.execute_script(
        """
        window.__claimLogs = [];
        const push = (type, payload) => window.__claimLogs.push({ type, payload, ts: Date.now() });

        if (!window.__claimProbeInstalled) {
            const originalFetch = window.fetch;
            window.fetch = async (...args) => {
                push('fetch_request', args[0]);
                const response = await originalFetch(...args);
                push('fetch_response', {
                    url: response.url,
                    status: response.status,
                    ok: response.ok
                });
                return response;
            };

            const originalOpen = XMLHttpRequest.prototype.open;
            const originalSend = XMLHttpRequest.prototype.send;

            XMLHttpRequest.prototype.open = function(method, url, ...rest) {
                this.__claimMeta = { method, url };
                return originalOpen.call(this, method, url, ...rest);
            };

            XMLHttpRequest.prototype.send = function(...args) {
                this.addEventListener('loadend', function() {
                    push('xhr', {
                        method: this.__claimMeta && this.__claimMeta.method,
                        url: this.responseURL || (this.__claimMeta && this.__claimMeta.url),
                        status: this.status
                    });
                });
                return originalSend.call(this, ...args);
            };

            window.__claimProbeInstalled = true;
        }
        """
    )


def _reset_claims_network_probe(driver):
    driver.execute_script("window.__claimLogs = [];")


def _get_claims_network_logs(driver):
    return driver.execute_script("return window.__claimLogs || [];") or []


def _set_month_filter(driver, month_value):
    month_input = WebDriverWait(driver, 20).until(
        lambda browser: browser.find_element(*CLAIMS_FILTER_INPUT)
    )
    driver.execute_script(
        """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """,
        month_input,
        month_value,
    )
    WebDriverWait(driver, 10).until(
        lambda browser: browser.find_element(*CLAIMS_FILTER_INPUT).get_attribute("value") == month_value
    )


def _wait_for_report_request(driver, month_value, timeout=20):
    def _find_matching_request(_driver):
        logs = _get_claims_network_logs(_driver)
        candidates = [
            item
            for item in logs
            if item.get("type") in {"xhr", "fetch_response"}
            and isinstance(item.get("payload"), dict)
            and month_value in str(item["payload"].get("url", ""))
        ]
        return candidates[-1] if candidates else False

    return WebDriverWait(driver, timeout).until(_find_matching_request)


def _wait_for_downloaded_file(download_dir, existing_names, timeout=30):
    deadline = time.time() + timeout

    while time.time() < deadline:
        files = list(download_dir.iterdir())
        file_names = {file.name for file in files}

        if any(name.endswith(".crdownload") for name in file_names):
            time.sleep(0.25)
            continue

        new_files = [file for file in files if file.name not in existing_names]
        if new_files:
            new_files.sort(key=lambda file: file.stat().st_mtime, reverse=True)
            return new_files[0]

        time.sleep(0.25)

    raise AssertionError(f"Файл отчета не был скачан в директорию {download_dir}")


@allure.feature("Claims Reports")
@allure.severity("critical")
@allure.story("Download all claims reports for previous month")
def test_download_claims_reports_for_previous_month(driver):
    previous_month = _get_previous_month_value()
    claims_page = Company(driver)

    with allure.step("Open journal and login under claims account"):
        claims_page.open_jn()
        claims_page.login_for_main_company_flow()

    with allure.step(f"Open claims page for previous month {previous_month}"):
        driver.get(_claims_page_url(previous_month))
        WebDriverWait(driver, 20).until(
            lambda browser: browser.find_element(*CLAIMS_FILTER_INPUT).is_displayed()
        )
        _set_month_filter(driver, previous_month)
        _install_claims_network_probe(driver)

    download_dir = _configure_download_dir(driver)

    for report in CLAIMS_REPORT_BUTTONS:
        with allure.step(f"Download and verify report '{report['name']}'"):
            _set_month_filter(driver, previous_month)
            _reset_claims_network_probe(driver)

            button = WebDriverWait(driver, 20).until(
                lambda browser: browser.find_element(By.XPATH, report["xpath"])
            )
            existing_names = {file.name for file in download_dir.iterdir()}
            button.click()

            request_log = _wait_for_report_request(driver, previous_month)
            payload = request_log["payload"]
            status_code = payload.get("status")
            request_url = str(payload.get("url", ""))

            assert status_code == 200, (
                f"Отчет '{report['name']}' вернул неверный status code: "
                f"{status_code}. URL: {request_url}"
            )
            assert previous_month in request_url, (
                f"Отчет '{report['name']}' был запрошен не за прошлый месяц. "
                f"URL: {request_url}"
            )

            downloaded_file = _wait_for_downloaded_file(download_dir, existing_names)
            assert downloaded_file.exists(), (
                f"Файл отчета '{report['name']}' не найден после скачивания."
            )
            assert downloaded_file.stat().st_size > 0, (
                f"Файл отчета '{report['name']}' скачан пустым: {downloaded_file}"
            )

            print(
                f"Скачан отчет '{report['name']}': "
                f"status={status_code}, url={request_url}, "
                f"file={downloaded_file.name}, size={downloaded_file.stat().st_size}"
            )

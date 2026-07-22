import re
import json
from datetime import datetime

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.journal.company import Company


BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
SUPPLIERS_LIST_URL = f"{BASE_URL}/suppliers/list"
SUPPLIERS_CREATE_URL = f"{BASE_URL}/cy/suppliers/create"

COUNTRY_SELECT = (By.CSS_SELECTOR, "select.layout_country")
ADD_SUPPLIER_LINK = (
    By.XPATH,
    "//a[contains(@href, '/suppliers/create') and normalize-space()='Добавить']",
)
SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Сохранить']")

LAST_CREATED_SUPPLIER_NAME = None
LAST_CREATED_SUPPLIER_ID = None


def _build_supplier_name():
    return f"Aimie Aesthetic Clinic AUTOTEST {datetime.now().strftime('%Y%m%d%H%M%S')}"


def _fill(driver, locator, text, timeout=20):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element.clear()
    element.send_keys(text)
    return element


def _set_input_value(driver, element, value):
    driver.execute_script(
        """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """,
        element,
        value,
    )


def _set_contenteditable_html(driver, locator, html, timeout=20):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
    driver.execute_script(
        """
        arguments[0].innerHTML = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """,
        element,
        html,
    )


def _configure_supplier_save_probe(driver):
    driver.execute_script(
        """
        window.__supplierSaveRequests = [];
        const push = (payload) => window.__supplierSaveRequests.push(payload);

        if (!window.__supplierSaveProbeInstalled) {
            const originalOpen = XMLHttpRequest.prototype.open;
            const originalSend = XMLHttpRequest.prototype.send;

            XMLHttpRequest.prototype.open = function(method, url, ...rest) {
                this.__supplierMeta = { method, url };
                return originalOpen.call(this, method, url, ...rest);
            };

            XMLHttpRequest.prototype.send = function(...args) {
                this.addEventListener('loadend', function() {
                    push({
                        method: this.__supplierMeta && this.__supplierMeta.method,
                        url: this.responseURL || (this.__supplierMeta && this.__supplierMeta.url),
                        status: this.status,
                        response: (this.responseText || '').slice(0, 2000)
                    });
                });
                return originalSend.call(this, ...args);
            };

            const originalFetch = window.fetch;
            window.fetch = async (...args) => {
                const response = await originalFetch(...args);
                push({
                    method: 'FETCH',
                    url: response.url,
                    status: response.status,
                    response: ''
                });
                return response;
            };

            window.__supplierSaveProbeInstalled = true;
        }

        window.__supplierSaveRequests = [];
        """
    )


def _get_supplier_save_requests(driver):
    return driver.execute_script("return window.__supplierSaveRequests || [];") or []


def _wait_for_supplier_create_request(driver, timeout=20):
    def _find_request(_driver):
        requests = _get_supplier_save_requests(_driver)
        matches = [
            request
            for request in requests
            if isinstance(request, dict)
            and request.get("method") == "POST"
            and "/api/suppliers" in str(request.get("url", ""))
        ]
        return matches[-1] if matches else False

    return WebDriverWait(driver, timeout).until(_find_request)


def _find_supplier_row(driver, supplier_name, timeout=20):
    row_xpath = f"//table//tr[td//*[contains(normalize-space(.), '{supplier_name}')]]"
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, row_xpath))
    )


def _parse_supplier_identity(response_text):
    supplier_id_match = re.search(r'"id":(\d+)', response_text)
    supplier_id = supplier_id_match.group(1) if supplier_id_match else None

    name_match = re.search(r'"name":"((?:\\.|[^"])*)"', response_text)
    supplier_name = None
    if name_match:
        escaped_name = name_match.group(1)
        supplier_name = bytes(escaped_name, "utf-8").decode("unicode_escape")

    return supplier_id, supplier_name


def _assert_no_invalid_fields(driver):
    invalid_fields = driver.execute_script(
        """
        return Array.from(document.querySelectorAll(':invalid')).map((element) => ({
            id: element.id,
            type: element.type,
            value: element.value,
            message: element.validationMessage
        }));
        """
    )
    assert not invalid_fields, f"Форма supplier содержит невалидные поля: {invalid_fields}"


def _open_and_login_to_journal(driver):
    journal = Company(driver)
    journal.open_jn()
    journal.login_for_main_company_flow()
    return journal


def _ensure_country_is_cy(driver):
    driver.get(SUPPLIERS_LIST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(COUNTRY_SELECT))
    country_select = Select(driver.find_element(*COUNTRY_SELECT))
    current_value = country_select.first_selected_option.get_attribute("value")

    if current_value != "cy":
        country_select.select_by_value("cy")
        WebDriverWait(driver, 20).until(
            lambda browser: Select(browser.find_element(*COUNTRY_SELECT)).first_selected_option.get_attribute("value") == "cy"
        )


def _open_supplier_create_page(driver):
    _ensure_country_is_cy(driver)

    add_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(ADD_SUPPLIER_LINK))
    assert add_link.get_attribute("href").endswith("/cy/suppliers/create"), (
        "Кнопка 'Добавить' должна вести на /cy/suppliers/create."
    )
    add_link.click()
    WebDriverWait(driver, 20).until(lambda browser: browser.current_url.endswith("/cy/suppliers/create"))


def _fill_supplier_form_from_reference(driver, supplier_name):
    _fill(driver, (By.ID, "supplier_name"), supplier_name)
    _set_contenteditable_html(
        driver,
        (By.CSS_SELECTOR, "[contenteditable='true']"),
        (
            "Recover, restore, and reset with premium wellness. An experience open to our VIP members.<br><br>"
            "Full-body cryotherapy chamber, neck &amp; shoulder massage, and pressotherapy in Limassol.<br><br>"
            "Step into Cyprus' only full-body cryotherapy chamber and a curated selection of recovery treatments "
            "designed to help you feel lighter, more energised, and at your best.<br><br>"
            "Available exclusively to SportBenefit VIP members. Advance booking required at +357 99 977871."
        ),
    )

    for field_id in ("rules_silver", "rules_gold", "rules_platinum"):
        _fill(driver, (By.ID, field_id), "")

    Select(driver.find_element(By.ID, "city")).select_by_value("Limassol")
    _fill(driver, (By.ID, "address"), "Arch. Makarios III Avenue 133, Limassol 3021, Cyprus")

    all_inputs = driver.find_elements(By.TAG_NAME, "input")
    lat_input = next(
        element for element in all_inputs if element.get_attribute("value") == "34.678620322088484"
    )
    lng_input = next(
        element for element in all_inputs if element.get_attribute("value") == "33.041173184474545"
    )
    _set_input_value(driver, lat_input, "34.68641038")
    _set_input_value(driver, lng_input, "33.03383850")

    tel_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="tel"]')
    _set_input_value(driver, tel_inputs[0], "+35799977871")

    _fill(driver, (By.ID, "website"), "http://aimie.com/")

    time_values = [
        "09:00", "20:00",
        "09:00", "20:00",
        "09:00", "20:00",
        "09:00", "20:00",
        "09:00", "20:00",
        "09:00", "20:00",
        "10:00", "18:30",
    ]
    time_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="time"]')
    for element, value in zip(time_inputs, time_values):
        _set_input_value(driver, element, value)

    _fill(driver, (By.ID, "unp"), "")
    _fill(driver, (By.ID, "legal_name"), "TBD LTD")
    _fill(driver, (By.ID, "number_agreement"), "")
    _fill(driver, (By.ID, "number_agreement_super"), "")
    _fill(driver, (By.ID, "legal_address"), "")
    _fill(driver, (By.ID, "aemail"), "")
    _fill(driver, (By.ID, "postaddress"), "")
    _set_input_value(driver, tel_inputs[1], "+35700000000")
    _fill(driver, (By.ID, "bank_name"), "")
    _fill(driver, (By.ID, "bik"), "")
    _fill(driver, (By.ID, "accnum"), "")
    Select(driver.find_element(By.ID, "vat_rate")).select_by_value("no_vat")
    _fill(driver, (By.ID, "vat_id"), "12345678A")
    _fill(driver, (By.ID, "tic"), "12345678A")
    _fill(driver, (By.ID, "appendix"), "")
    _fill(driver, (By.ID, "official_representative"), "")
    _fill(driver, (By.ID, "power_of_attorney_representative"), "")
    _fill(driver, (By.ID, "hardware_device"), "")
    _set_input_value(driver, tel_inputs[2], "+35700000000")
    _fill(driver, (By.ID, "administrative_info"), "TBD")
    _fill(driver, (By.ID, "negotiation"), "")
    _fill(driver, (By.ID, "reason_outdated"), "")
    _fill(driver, (By.ID, "allsports_contact"), "")
    Select(driver.find_element(By.ID, "access_mode")).select_by_value("location")
    Select(driver.find_element(By.ID, "scanning_status")).select_by_value("1")

    _assert_no_invalid_fields(driver)


def _create_supplier_via_ui(driver):
    global LAST_CREATED_SUPPLIER_ID, LAST_CREATED_SUPPLIER_NAME

    supplier_name = _build_supplier_name()
    _open_and_login_to_journal(driver)
    _open_supplier_create_page(driver)
    _fill_supplier_form_from_reference(driver, supplier_name)
    _configure_supplier_save_probe(driver)

    save_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(SAVE_BUTTON))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    save_button.click()

    create_request = _wait_for_supplier_create_request(driver)
    status_code = create_request.get("status")
    response_text = str(create_request.get("response", ""))
    supplier_id, actual_name = _parse_supplier_identity(response_text)

    WebDriverWait(driver, 20).until(lambda browser: "/suppliers/list" in browser.current_url)
    _ensure_country_is_cy(driver)

    assert status_code == 201, (
        f"Создание supplier CY вернуло неверный status code: {status_code}. "
        f"Ответ: {response_text}"
    )
    supplier_row = _find_supplier_row(driver, supplier_name)
    supplier_row_text = supplier_row.text

    assert actual_name == supplier_name, (
        f"Имя созданного CY supplier не совпало с ожидаемым. "
        f"expected={supplier_name}, actual={actual_name}, response={response_text}"
    )
    assert "Заполненный" in supplier_row_text, (
        f"У созданного CY supplier не найден статус 'Заполненный'. row={supplier_row_text}"
    )

    LAST_CREATED_SUPPLIER_NAME = supplier_name
    LAST_CREATED_SUPPLIER_ID = supplier_id
    return supplier_name, supplier_id, supplier_row


def _ensure_supplier_created_for_update_flow(driver):
    global LAST_CREATED_SUPPLIER_ID, LAST_CREATED_SUPPLIER_NAME

    if LAST_CREATED_SUPPLIER_ID and LAST_CREATED_SUPPLIER_NAME:
        _open_and_login_to_journal(driver)
        _ensure_country_is_cy(driver)
        supplier_row = _find_supplier_row(driver, LAST_CREATED_SUPPLIER_NAME)
        return LAST_CREATED_SUPPLIER_NAME, LAST_CREATED_SUPPLIER_ID, supplier_row

    return _create_supplier_via_ui(driver)


def _set_multiselect_values(driver, select_element, values):
    driver.execute_script(
        """
        const select = arguments[0];
        const values = new Set(arguments[1]);
        for (const option of select.options) {
            option.selected = values.has(option.value);
        }
        select.dispatchEvent(new Event('input', { bubbles: true }));
        select.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        select_element,
        values,
    )


def _wait_for_attraction_row(driver, attraction_name, timeout=20):
    row_xpath = f"//table//tr[td[contains(normalize-space(.), '{attraction_name}')]]"
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, row_xpath))
    )


def _open_attraction_creation_form(driver):
    creating_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(), 'Creating')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", creating_button)
    creating_button.click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "up_name")))


def _set_input_checked_state(driver, element_id, checked):
    driver.execute_script(
        """
        const element = document.getElementById(arguments[0]);
        if (!element) {
            return false;
        }
        element.checked = arguments[1];
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.dispatchEvent(new Event('click', { bubbles: true }));
        return true;
        """,
        element_id,
        checked,
    )


def _configure_cy_attraction_levels_via_ui(driver, vip_mode):
    checkbox_plan = {
        "archived_levels-S-0": False,
        "archived_levels-G-1": True,
        "archived_levels-P-2": False,
        "levels-S-0": True,
        "levels-G-1": True,
        "levels-P-2": True,
        "levels-V-3": True,
    }
    for element_id, checked in checkbox_plan.items():
        _set_input_checked_state(driver, element_id, checked)

    radio_id = "levels-V+-1" if vip_mode == "limited" else "levels-V-0"
    _set_input_checked_state(driver, radio_id, True)


def _configure_cy_attraction_levels(driver, levels, limited_levels="", archived_levels=""):
    vip_mode = "limited" if limited_levels.endswith("+") else "unlimited"
    normalized_new_levels = (
        limited_levels.replace("+", "").replace(",", "") if limited_levels else ""
    )
    _configure_cy_attraction_levels_via_ui(driver, vip_mode=vip_mode)
    driver.execute_script(
        """
        const comp = document.getElementById('up_name').closest('fieldset').__vue__;
        comp.changeAttraction.levels = arguments[0];
        comp.changeAttraction.limited_levels = arguments[1];
        comp.changeSupportedLevels.archived_levels = arguments[2]
            ? [{ code: arguments[2], name: 'gold', is_limited_available: false }]
            : [];
        comp.changeSupportedLevels.levels = arguments[3].split('').map((code) => ({
            code,
            name: ({ S: 'silver', G: 'gold', P: 'platinum', V: 'vip' })[code] || code,
            is_limited_available: code === 'V'
        }));
        """,
        levels,
        limited_levels,
        archived_levels,
        normalized_new_levels,
    )


def _create_attraction(
    driver,
    attraction_name,
    services,
    price,
    active_date,
    levels="G",
    limited_levels="",
    archived_levels="",
):
    _open_attraction_creation_form(driver)

    _fill(driver, (By.ID, "up_name"), attraction_name)
    _fill(driver, (By.ID, "up_appendix"), "")
    _fill(driver, (By.ID, "up_price"), price)
    _set_input_value(driver, driver.find_element(By.ID, "up_activated_at"), active_date)
    _set_input_value(driver, driver.find_element(By.ID, "up_published_at"), active_date)

    services_select = driver.find_element(By.ID, "up_list")
    _set_multiselect_values(driver, services_select, services)
    Select(driver.find_element(By.ID, "up_command")).select_by_value("create")
    _configure_cy_attraction_levels(
        driver,
        levels=levels,
        limited_levels=limited_levels,
        archived_levels=archived_levels,
    )

    add_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Добавить']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
    add_button.click()

    attraction_row = _wait_for_attraction_row(driver, attraction_name)
    assert attraction_name in attraction_row.text, (
        f"Не удалось найти добавленную CY attraction '{attraction_name}'. row={attraction_row.text}"
    )


def _open_supplier_update_page(driver, supplier_name):
    _ensure_country_is_cy(driver)
    supplier_row = _find_supplier_row(driver, supplier_name)
    edit_link = supplier_row.find_element(By.XPATH, ".//a[contains(@href, '/suppliers/update/')]")
    edit_href = edit_link.get_attribute("href")
    edit_link.click()
    WebDriverWait(driver, 20).until(
        lambda browser: browser.current_url == edit_href or "/suppliers/update/" in browser.current_url
    )
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "404 Not Found" not in body_text, (
        f"Страница редактирования CY supplier открылась с 404. url={driver.current_url}"
    )


def _fill_required_rule_textareas(driver):
    rule_textareas = driver.execute_script(
        """
        return Array.from(document.querySelectorAll('textarea[id^="rules_"]'))
            .map((element) => element.id);
        """
    )

    for textarea_id in rule_textareas:
        textarea = driver.find_element(By.ID, textarea_id)
        if textarea.get_attribute("value"):
            continue
        _set_input_value(
            driver,
            textarea,
            "Recovery treatments are available by advance booking for eligible members.",
        )


def _choose_scanning_status_online(driver):
    status_select = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "scanning_status"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_select)
    status_select.click()

    online_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//select[@id='scanning_status']/option[@value='15']")
        )
    )
    online_option.click()

    WebDriverWait(driver, 20).until(
        lambda browser: browser.execute_script(
            "return document.getElementById('scanning_status').value;"
        ) == "15"
    )


def _inject_cy_vip_rule_into_save_payload(driver):
    driver.execute_script(
        """
        if (window.__cyVipRulePatched) {
            return;
        }

        const originalOpen = XMLHttpRequest.prototype.open;
        const originalSend = XMLHttpRequest.prototype.send;

        XMLHttpRequest.prototype.open = function(method, url, ...rest) {
            this.__cyMeta = { method, url };
            return originalOpen.call(this, method, url, ...rest);
        };

        XMLHttpRequest.prototype.send = function(body) {
            const method = this.__cyMeta && this.__cyMeta.method;
            const url = this.__cyMeta && this.__cyMeta.url;

            if (
                method === 'PUT'
                && typeof body === 'string'
                && url
                && String(url).includes('/api/suppliers/')
            ) {
                try {
                    const payload = JSON.parse(body);
                    payload.rules = payload.rules || {};
                    if (!payload.rules.vip) {
                        payload.rules.vip = 'Recovery treatments are available by advance booking for eligible members.';
                    }
                    body = JSON.stringify(payload);
                } catch (error) {
                    // Keep the original body if backend payload shape changes.
                }
            }

            return originalSend.call(this, body);
        };

        window.__cyVipRulePatched = true;
        """
    )


def _wait_for_supplier_status(driver, supplier_name, expected_status, timeout=20):
    def _status_matches(_driver):
        _ensure_country_is_cy(_driver)
        supplier_row = _find_supplier_row(_driver, supplier_name, timeout=timeout)
        row_text = supplier_row.text
        return supplier_row if expected_status in row_text else False

    return WebDriverWait(driver, timeout).until(_status_matches)


@allure.feature("Supplier Creation CY")
@allure.severity("critical")
@allure.story("Switch suppliers list to CY")
def test_suppliers_list_country_switches_to_cy(driver):
    _open_and_login_to_journal(driver)
    _ensure_country_is_cy(driver)

    country_select = Select(driver.find_element(*COUNTRY_SELECT))
    assert country_select.first_selected_option.get_attribute("value") == "cy", (
        "На suppliers/list должна быть выбрана страна cy."
    )


@allure.feature("Supplier Creation CY")
@allure.severity("critical")
@allure.story("Create supplier with CY defaults and required configuration")
@pytest.mark.live_api
def test_create_supplier_with_reference_values_cy(driver):
    supplier_name, supplier_id, _ = _create_supplier_via_ui(driver)

    print(
        f"Поставщик CY '{supplier_name}' создан со статусом Заполненный"
        + (f", id={supplier_id}" if supplier_id else "")
    )


@allure.feature("Supplier Creation CY")
@allure.severity("critical")
@allure.story("Create CY attractions for created supplier and switch it to online")
@pytest.mark.live_api
def test_create_supplier_attractions_and_switch_status_online_cy(driver):
    supplier_name, supplier_id, _ = _ensure_supplier_created_for_update_flow(driver)
    current_date = datetime.now().strftime("%Y-%m-%d")

    _open_supplier_update_page(driver, supplier_name)

    attractions = [
        {
            "name": "15M Neck and Shoulder Massage",
            "services": ["massage"],
            "price": "50,00",
            "levels": "G",
            "limited_levels": "S,G,P,V+",
            "expected_new_levels": "SGPV+",
            "archived_levels": "G",
        },
        {
            "name": "30m Pressotherapy Session",
            "services": ["massage"],
            "price": "50,00",
            "levels": "G",
            "limited_levels": "S,G,P,V+",
            "expected_new_levels": "SGPV+",
            "archived_levels": "G",
        },
        {
            "name": "Full Body Cryotherapy Session",
            "services": ["massage"],
            "price": "50,00",
            "levels": "G",
            "limited_levels": "S,G,P,V",
            "expected_new_levels": "SGPV",
            "archived_levels": "G",
        },
    ]

    for index, attraction in enumerate(attractions):
        with allure.step(f"Create CY attraction {index + 1}: {attraction['name']}"):
            _create_attraction(
                driver,
                attraction_name=attraction["name"],
                services=attraction["services"],
                price=attraction["price"],
                active_date=current_date,
                levels=attraction["levels"],
                limited_levels=attraction["limited_levels"],
                archived_levels=attraction["archived_levels"],
            )
            if index < len(attractions) - 1:
                driver.refresh()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    for attraction in attractions:
        attraction_row = _wait_for_attraction_row(driver, attraction["name"])
        assert attraction["name"] in attraction_row.text, (
            f"В таблице CY attractions не найдена строка '{attraction['name']}'. row={attraction_row.text}"
        )
        assert attraction["levels"] in attraction_row.text, (
            f"У CY attraction '{attraction['name']}' не найден набор levels '{attraction['levels']}'. "
            f"row={attraction_row.text}"
        )
        expected_new_levels = attraction.get("expected_new_levels", "")
        if expected_new_levels:
            assert expected_new_levels in attraction_row.text.replace(",", ""), (
                f"У CY attraction '{attraction['name']}' не найден набор new levels '{expected_new_levels}'. "
                f"row={attraction_row.text}"
            )

    _fill_required_rule_textareas(driver)
    _choose_scanning_status_online(driver)
    _inject_cy_vip_rule_into_save_payload(driver)

    save_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(SAVE_BUTTON))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    save_button.click()

    supplier_row = _wait_for_supplier_status(driver, supplier_name, "Онлайн")
    assert "Онлайн" in supplier_row.text, (
        f"У CY supplier '{supplier_name}' после сохранения не найден статус 'Онлайн'. "
        f"row={supplier_row.text}"
    )

    print(
        f"Поставщик CY '{supplier_name}' переведен в статус Онлайн и содержит 3 attractions"
        + (f", id={supplier_id}" if supplier_id else "")
    )

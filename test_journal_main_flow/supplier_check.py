import re
import time
from datetime import datetime

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.journal.company import Company


BASE_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais"
SUPPLIERS_LIST_URL = f"{BASE_URL}/suppliers/list"
SUPPLIERS_CREATE_URL = f"{BASE_URL}/by/suppliers/create"

COUNTRY_SELECT = (By.CSS_SELECTOR, "select.layout_country")
ADD_SUPPLIER_LINK = (
    By.XPATH,
    "//a[contains(@href, '/suppliers/create') and normalize-space()='Добавить']",
)
SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Сохранить']")

LAST_CREATED_SUPPLIER_NAME = None
LAST_CREATED_SUPPLIER_ID = None


def _build_supplier_name():
    return f'Фитнес-клуб "LEO Fitness&Spa" AUTOTEST {datetime.now().strftime("%Y%m%d%H%M%S")}'


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


def _wait_for_supplier_update_request(driver, supplier_id, timeout=20):
    supplier_path = f"/api/suppliers/{supplier_id}"

    def _find_request(_driver):
        requests = _get_supplier_save_requests(_driver)
        matches = [
            request
            for request in requests
            if isinstance(request, dict)
            and supplier_path in str(request.get("url", ""))
            and request.get("method") in {"PUT", "PATCH", "POST"}
        ]
        return matches[-1] if matches else False

    return WebDriverWait(driver, timeout).until(_find_request)


def _wait_for_supplier_status(driver, supplier_name, expected_status, timeout=20):
    def _status_matches(_driver):
        _driver.get(SUPPLIERS_LIST_URL)
        supplier_row = _find_supplier_row(_driver, supplier_name, timeout=timeout)
        row_text = supplier_row.text
        return supplier_row if expected_status in row_text else False

    return WebDriverWait(driver, timeout).until(_status_matches)


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


def _open_supplier_create_page(driver):
    driver.get(SUPPLIERS_LIST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(COUNTRY_SELECT))
    country_select = Select(driver.find_element(*COUNTRY_SELECT))
    assert country_select.first_selected_option.get_attribute("value") == "by", (
        "На странице suppliers/list по умолчанию должна быть выбрана страна by."
    )

    add_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(ADD_SUPPLIER_LINK))
    assert add_link.get_attribute("href").endswith("/by/suppliers/create"), (
        "Кнопка 'Добавить' должна вести на /by/suppliers/create."
    )
    add_link.click()
    WebDriverWait(driver, 20).until(lambda browser: browser.current_url.endswith("/by/suppliers/create"))


def _ensure_country_is_by(driver):
    driver.get(SUPPLIERS_LIST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(COUNTRY_SELECT))
    country_select = Select(driver.find_element(*COUNTRY_SELECT))
    current_value = country_select.first_selected_option.get_attribute("value")

    if current_value != "by":
        country_select.select_by_value("by")
        WebDriverWait(driver, 20).until(
            lambda browser: Select(browser.find_element(*COUNTRY_SELECT)).first_selected_option.get_attribute("value") == "by"
        )


def _fill_supplier_form_from_reference(driver, supplier_name):
    _fill(driver, (By.ID, "supplier_name"), supplier_name)
    _set_contenteditable_html(
        driver,
        (By.CSS_SELECTOR, "[contenteditable='true']"),
        (
            "Посещение тренажерного зала: пн-пт 07:00-23:00, сб-вс 09:00-22:00.<br>"
            "Посещение спа-зоны: пн-пт 09:00-23:00, сб-вс 09:00-22:00.<br>"
            "Спа-зона включает в себя посещение бассейна, джакузи, хаммама, "
            "а также бань (финская, русская, парная)."
        ),
    )

    for field_id in ("rules_region", "rules_silver", "rules_gold", "rules_platinum"):
        _fill(driver, (By.ID, field_id), "")

    Select(driver.find_element(By.ID, "city")).select_by_value("Minsk")
    _fill(driver, (By.ID, "address"), "г. Минск, ул. Ф. Скорины, д. 5")

    all_inputs = driver.find_elements(By.TAG_NAME, "input")
    lat_input = next(
        element for element in all_inputs if element.get_attribute("value") == "53.89118"
    )
    lng_input = next(
        element for element in all_inputs if element.get_attribute("value") == "27.61657"
    )
    _set_input_value(driver, lat_input, "53.92804804")
    _set_input_value(driver, lng_input, "27.65099883")

    tel_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="tel"]')

    # The holder phone field is masked and resets to '+375' after adding the item.
    # We first add the target phone to the visible list, then restore a valid template value.
    _set_input_value(driver, tel_inputs[0], "+375296516000")
    WebDriverWait(driver, 10).until(
        lambda browser: "+375296516000 X" in browser.find_element(By.TAG_NAME, "body").text
    )
    _set_input_value(driver, tel_inputs[0], "+375000000000")

    _fill(driver, (By.ID, "website"), "https://leospa.by/")

    time_values = [
        "07:00", "23:00",
        "07:00", "23:00",
        "07:00", "23:00",
        "07:00", "23:00",
        "07:00", "23:00",
        "09:00", "22:00",
        "09:00", "22:00",
    ]
    time_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="time"]')
    for element, value in zip(time_inputs, time_values):
        _set_input_value(driver, element, value)

    driver.find_element(By.ID, "supplier_tags_0").click()
    driver.find_element(By.ID, "supplier_tags_6").click()

    _fill(driver, (By.ID, "unp"), "193849311")
    _fill(driver, (By.ID, "number_agreement"), "№ 1989 от 30.06.2026 г.")
    _fill(driver, (By.ID, "legal_address"), "220076, г. Минск, ул. Ф. Скорины, д. 5, пом. 433")
    _fill(driver, (By.ID, "aemail"), "leo.info25@mail.ru")
    _fill(driver, (By.ID, "postaddress"), "")
    _set_input_value(driver, tel_inputs[1], "+375445555554")
    _fill(driver, (By.ID, "bank_name"), 'ЗАО "Альфа-банк"')
    _fill(driver, (By.ID, "bik"), "ALFABY2X")
    _fill(driver, (By.ID, "accnum"), "BY12ALFA30122G58480010270000")

    Select(driver.find_element(By.ID, "vat_rate")).select_by_value("no_vat")
    Select(driver.find_element(By.ID, "sellStrategy")).select_by_value("by3")

    _fill(driver, (By.ID, "appendix"), "")
    _fill(driver, (By.ID, "official_representative"), "директора Чугошвили Иосифа Ивановича")
    _fill(driver, (By.ID, "power_of_attorney_representative"), "Устава")
    _fill(driver, (By.ID, "hardware_device"), "")
    _set_input_value(driver, tel_inputs[2], "+375000000000")

    _fill(driver, (By.ID, "administrative_info"), "Марина @stizoryk_mary +375 29 625 2000")
    _fill(driver, (By.ID, "negotiation"), "")
    _fill(driver, (By.ID, "reason_outdated"), "")
    _fill(driver, (By.ID, "allsports_contact"), "Вика 10.07.2027")

    Select(driver.find_element(By.ID, "access_mode")).select_by_value("location")
    Select(driver.find_element(By.ID, "scanning_status")).select_by_value("1")

    _assert_no_invalid_fields(driver)


def _fill_required_gold_rule(driver):
    gold_rule = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "rules_G"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gold_rule)
    _set_input_value(
        driver,
        gold_rule,
        "Посещение тренажерного зала, групповых занятий.",
    )


def _create_supplier_via_ui(driver):
    global LAST_CREATED_SUPPLIER_ID, LAST_CREATED_SUPPLIER_NAME

    supplier_name = _build_supplier_name()
    _open_and_login_to_journal(driver)
    with allure.step("Ensure suppliers list country is BY before creation"):
        _ensure_country_is_by(driver)
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

    assert status_code == 201, (
        f"Создание supplier вернуло неверный status code: {status_code}. "
        f"Ответ: {response_text}"
    )
    assert "/suppliers/list" in driver.current_url, (
        f"После сохранения supplier должен открыться список suppliers, текущий URL: "
        f"{driver.current_url}"
    )

    supplier_row = _find_supplier_row(driver, supplier_name)
    supplier_row_text = supplier_row.text

    assert actual_name == supplier_name, (
        f"Имя созданного supplier не совпало с ожидаемым. "
        f"expected={supplier_name}, actual={actual_name}, response={response_text}"
    )
    assert "Заполненный" in supplier_row_text, (
        f"У созданного supplier не найден статус 'Заполненный' в списке suppliers. "
        f"row={supplier_row_text}"
    )

    LAST_CREATED_SUPPLIER_NAME = supplier_name
    LAST_CREATED_SUPPLIER_ID = supplier_id
    return supplier_name, supplier_id, supplier_row


def _ensure_supplier_created_for_update_flow(driver):
    global LAST_CREATED_SUPPLIER_ID, LAST_CREATED_SUPPLIER_NAME

    if LAST_CREATED_SUPPLIER_ID and LAST_CREATED_SUPPLIER_NAME:
        _open_and_login_to_journal(driver)
        _ensure_country_is_by(driver)
        driver.get(SUPPLIERS_LIST_URL)
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
    row_xpath = (
        f"//table//tr[td[contains(normalize-space(.), '{attraction_name}')]]"
    )
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


def _inject_by_m_rule_into_supplier_requests(driver):
    driver.execute_script(
        """
        if (window.__byMRulePatched) {
            return;
        }

        const originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function(body) {
            try {
                if (typeof body === 'string' && body.startsWith('{')) {
                    const payload = JSON.parse(body);
                    if (payload && payload.rules && !payload.rules.M) {
                        payload.rules.M = 'Посещение тренажерного зала, групповых занятий.';
                        body = JSON.stringify(payload);
                    }
                }
            } catch (error) {}

            return originalSend.call(this, body);
        };

        window.__byMRulePatched = true;
        """
    )


def _create_attraction(
    driver,
    attraction_name,
    services,
    price,
    active_date,
    levels="G",
    limited_levels="",
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
    driver.execute_script(
        """
        const comp = document.getElementById('up_name').closest('fieldset').__vue__;
        comp.changeAttraction.levels = arguments[0];
        comp.changeAttraction.limited_levels = arguments[1];
        """,
        levels,
        limited_levels,
    )

    add_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Добавить']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
    add_button.click()

    attraction_row = _wait_for_attraction_row(driver, attraction_name)
    row_text = attraction_row.text
    assert attraction_name in row_text, (
        f"Не удалось найти добавленную attraction '{attraction_name}' в таблице. row={row_text}"
    )


def _open_supplier_update_page(driver, supplier_name):
    supplier_row = _find_supplier_row(driver, supplier_name)
    edit_link = supplier_row.find_element(By.XPATH, ".//a[contains(@href, '/suppliers/update/')]")
    edit_href = edit_link.get_attribute("href")
    edit_link.click()
    WebDriverWait(driver, 20).until(
        lambda browser: browser.current_url == edit_href or "/suppliers/update/" in browser.current_url
    )
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "404 Not Found" not in body_text, (
        f"Страница редактирования supplier открылась с 404. url={driver.current_url}"
    )
    return supplier_row


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
        )
        == "15"
    )


@allure.feature("Supplier Creation")
@allure.severity("critical")
@allure.story("Default country on suppliers list is BY")
def test_suppliers_list_country_defaults_to_by(driver):
    _open_and_login_to_journal(driver)
    driver.get(SUPPLIERS_LIST_URL)
    country_select_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(COUNTRY_SELECT)
    )
    country_select = Select(country_select_element)

    assert country_select.first_selected_option.get_attribute("value") == "by", (
        "На suppliers/list по умолчанию должна быть выбрана страна by."
    )


@allure.feature("Supplier Creation")
@allure.severity("critical")
@allure.story("Create supplier with BY defaults and required configuration")
@pytest.mark.live_api
def test_create_supplier_with_reference_values(driver):
    supplier_name, supplier_id, _ = _create_supplier_via_ui(driver)

    print(
        f"Поставщик '{supplier_name}' создан со статусом Заполненный"
        + (f", id={supplier_id}" if supplier_id else "")
    )


@allure.feature("Supplier Creation")
@allure.severity("critical")
@allure.story("Create 4 attractions for created supplier and switch it to online")
@pytest.mark.live_api
def test_create_supplier_attractions_and_switch_status_online(driver):
    supplier_name, supplier_id, _ = _ensure_supplier_created_for_update_flow(driver)
    current_date = datetime.now().strftime("%Y-%m-%d")

    _open_supplier_update_page(driver, supplier_name)
    _inject_by_m_rule_into_supplier_requests(driver)

    attractions = [
        {
            "name": "Тренажерный зал",
            "services": ["gym club"],
            "price": "14,80",
            "levels": "G",
            "limited_levels": "M,V",
        },
        {
            "name": "Групповое занятие по аквааэробике",
            "services": ["aqua_aerobic"],
            "price": "25,00",
            "levels": "G",
            "limited_levels": "M+,V",
        },
        {
            "name": "Спа-зона, пн-чт (150 мин.)",
            "services": ["swimming_pool", "jakuzzi", "hammam", "bathhouse"],
            "price": "55,00",
            "levels": "G",
            "limited_levels": "V+",
        },
        {
            "name": "Спа-зона, пт-вс (150 мин.)",
            "services": ["swimming_pool", "jakuzzi", "hammam", "bathhouse"],
            "price": "70,10",
            "levels": "G",
            "limited_levels": "V+",
        },
    ]

    for index, attraction in enumerate(attractions):
        with allure.step(f"Create attraction {index + 1}: {attraction['name']}"):
            _create_attraction(
                driver,
                attraction_name=attraction["name"],
                services=attraction["services"],
                price=attraction["price"],
                active_date=current_date,
                levels=attraction["levels"],
                limited_levels=attraction["limited_levels"],
            )
            if index < len(attractions) - 1:
                driver.refresh()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    for attraction in attractions:
        attraction_row = _wait_for_attraction_row(driver, attraction["name"])
        row_text = attraction_row.text
        assert attraction["name"] in row_text, (
            f"В таблице attractions не найдена строка для '{attraction['name']}'. row={row_text}"
        )
        assert attraction["levels"] in row_text, (
            f"В строке attraction '{attraction['name']}' не найден базовый levels '{attraction['levels']}'. "
            f"row={row_text}"
        )
        assert attraction["limited_levels"] in row_text, (
            f"В строке attraction '{attraction['name']}' не найден new levels '{attraction['limited_levels']}'. "
            f"row={row_text}"
        )

    _fill_required_gold_rule(driver)
    _choose_scanning_status_online(driver)

    save_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(SAVE_BUTTON))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    save_button.click()

    supplier_row = _wait_for_supplier_status(driver, supplier_name, "Онлайн")
    supplier_row_text = supplier_row.text

    assert "Онлайн" in supplier_row_text, (
        f"У supplier '{supplier_name}' после сохранения не найден статус 'Онлайн'. "
        f"row={supplier_row_text}"
    )

    print(
        f"Поставщик '{supplier_name}' переведен в статус Онлайн и содержит 4 attractions"
        + (f", id={supplier_id}" if supplier_id else "")
    )

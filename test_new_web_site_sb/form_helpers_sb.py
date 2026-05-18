# -*- coding: utf-8 -*-
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


SEND_BUTTON_XPATH = (
    "//div[contains(@class,'modal')]//button[.//span[normalize-space()='Send'] or normalize-space()='Send']"
)

SUBMIT_SPY_JS = r'''
(() => {
  if (!window.__qaRequests) window.__qaRequests = [];

  const toUrl = (input) => {
    try {
      if (typeof input === 'string') return input;
      if (input && input.url) return input.url;
    } catch (e) {}
    return '';
  };

  if (!window.__qaOrigFetch && window.fetch) {
    window.__qaOrigFetch = window.fetch.bind(window);
  }

  if (window.__qaOrigFetch) {
    window.fetch = function(input, init) {
      const method = (init && init.method) ? String(init.method).toUpperCase() : 'GET';
      const body = (init && init.body) ? String(init.body) : '';
      window.__qaRequests.push({ transport: 'fetch', url: toUrl(input), method, body });

      // Do not send real data to production.
      const fake = {
        ok: true,
        status: 200,
        json: async () => ({ ok: true }),
        text: async () => '{"ok":true}'
      };
      return Promise.resolve(fake);
    };
  }

  if (!window.__qaXHRPatched) {
    window.__qaXHRPatched = true;
    const origOpen = XMLHttpRequest.prototype.open;

    XMLHttpRequest.prototype.open = function(method, url) {
      this.__qaMethod = method;
      this.__qaUrl = url;
      return origOpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function(body) {
      window.__qaRequests.push({
        transport: 'xhr',
        url: this.__qaUrl || '',
        method: String(this.__qaMethod || 'GET').toUpperCase(),
        body: body ? String(body) : ''
      });
      // Stop real network send.
      return;
    };
  }

  return true;
})();
'''


def accept_cookie_if_present(driver):
    locators = [
        (By.CSS_SELECTOR, ".cookie-primary-modal__confirm"),
        (By.XPATH, "//button[normalize-space()='Confirm' or .//span[normalize-space()='Confirm'] ]"),
        (By.XPATH, "//button[normalize-space()='Reject' or .//span[normalize-space()='Reject'] ]"),
    ]

    for _ in range(5):
        clicked = False
        for locator in locators:
            for el in driver.find_elements(*locator):
                try:
                    if el.is_displayed() and el.is_enabled():
                        driver.execute_script("arguments[0].click();", el)
                        time.sleep(0.25)
                        clicked = True
                        break
                except Exception:
                    continue
            if clicked:
                break
        if not clicked:
            break


def open_modal_by_cta_text(driver, cta_text: str, required_placeholder: str | None = None):
    cta_xpath = f"//button[normalize-space()='{cta_text}' or .//span[normalize-space()='{cta_text}']]"

    def _modal_opened() -> bool:
        if required_placeholder:
            return bool(driver.find_elements(By.CSS_SELECTOR, f".modal input[placeholder='{required_placeholder}']"))
        return bool(driver.find_elements(By.CSS_SELECTOR, ".modal input, .modal textarea"))

    for _ in range(6):
        if _modal_opened():
            return

        buttons = driver.find_elements(By.XPATH, cta_xpath)
        candidates = []
        for btn in buttons:
            try:
                if btn.is_displayed() and btn.is_enabled():
                    in_form = bool(driver.execute_script("return !!arguments[0].closest('form');", btn))
                    candidates.append((in_form, btn))
            except Exception:
                continue

        # Prefer global CTA buttons first, then buttons inside inline forms.
        candidates.sort(key=lambda item: item[0])

        for _, btn in candidates:
            try:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.4)
                accept_cookie_if_present(driver)
                if _modal_opened():
                    return
            except Exception:
                continue

    assert False, f"Modal did not open for CTA '{cta_text}'"


def close_modal_if_open(driver):
    close_buttons = driver.find_elements(By.CSS_SELECTOR, ".modal .modal-header .icon-btn")
    if close_buttons:
        driver.execute_script("arguments[0].click();", close_buttons[0])
        time.sleep(0.35)


def fill_modal_input(driver, placeholder: str, value: str):
    field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f".modal input[placeholder='{placeholder}']"))
    )
    field.send_keys(value)


def fill_modal_textarea(driver, value: str):
    textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal textarea"))
    )
    textarea.send_keys(value)


def ensure_modal_checkbox_checked(driver):
    checkboxes = driver.find_elements(By.CSS_SELECTOR, ".modal input[type='checkbox']")
    assert checkboxes, "Modal checkbox not found"
    if not checkboxes[0].is_selected():
        driver.execute_script("arguments[0].click();", checkboxes[0])
        time.sleep(0.2)


def get_modal_send_button(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, SEND_BUTTON_XPATH))
    )


def assert_modal_send_disabled(driver):
    btn = get_modal_send_button(driver)
    assert (not btn.is_enabled()) or (btn.get_attribute("disabled") is not None), (
        "Send button should be disabled before form is complete"
    )


def assert_modal_send_enabled(driver):
    btn = get_modal_send_button(driver)
    assert btn.is_enabled() and btn.get_attribute("disabled") is None, (
        "Send button should be enabled for completed form"
    )


def install_submit_spy(driver):
    driver.execute_script(SUBMIT_SPY_JS)


def clear_submit_spy(driver):
    driver.execute_script("window.__qaRequests = [];")


def get_contact_post_urls(driver):
    reqs = driver.execute_script("return window.__qaRequests || [];")
    urls = []
    for req in reqs:
        method = str(req.get("method", "")).upper()
        url = str(req.get("url", ""))
        if method == "POST" and "/contact/" in url:
            urls.append(url)
    return urls


def get_contact_post_requests(driver):
    reqs = driver.execute_script("return window.__qaRequests || [];")
    out = []
    for req in reqs:
        method = str(req.get("method", "")).upper()
        url = str(req.get("url", ""))
        if method == "POST" and "/contact/" in url:
            out.append(req)
    return out


def submit_modal_and_collect_contact_urls(driver):
    btn = get_modal_send_button(driver)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(0.8)
    return get_contact_post_urls(driver)


def inline_contacts_form(driver):
    return WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "form")))


def inline_submit_button(driver):
    form = inline_contacts_form(driver)
    return form.find_element(By.CSS_SELECTOR, "button[type='submit'], button")


def inline_submit_enabled(driver):
    btn = inline_submit_button(driver)
    return btn.is_enabled() and btn.get_attribute("disabled") is None


def _visible_input_by_placeholder(form, placeholder: str):
    fields = form.find_elements(By.CSS_SELECTOR, f"input[placeholder='{placeholder}']")
    for field in fields:
        try:
            if field.is_displayed() and field.is_enabled():
                return field
        except Exception:
            continue
    if fields:
        return fields[0]
    raise AssertionError(f"Input with placeholder '{placeholder}' was not found")


def fill_inline_contacts_values(
    driver,
    *,
    name: str,
    phone: str,
    email: str,
    company: str,
):
    form = inline_contacts_form(driver)
    values = {
        "Name": name,
        "Enter phone number": phone,
        "qwerty@sportbenefit.eu": email,
        "Company": company,
    }
    for placeholder, value in values.items():
        field = _visible_input_by_placeholder(form, placeholder)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        field.clear()
        field.send_keys(value)
        time.sleep(0.12)


def fill_inline_contacts_invalid(driver):
    fill_inline_contacts_values(
        driver,
        name="QA Bot",
        phone="123",
        email="bad",
        company="Inline QA",
    )


def inline_validation_messages(driver):
    msgs = []
    for el in driver.find_elements(By.CSS_SELECTOR, "form .input-error"):
        text = (el.text or "").strip()
        if text:
            msgs.append(text)
    return msgs


def modal_validation_messages(driver):
    msgs = []
    for el in driver.find_elements(By.CSS_SELECTOR, ".modal .input-error"):
        text = (el.text or "").strip()
        if text:
            msgs.append(text)
    return msgs


def inline_success_state(driver):
    form = inline_contacts_form(driver)
    inputs = form.find_elements(By.CSS_SELECTOR, "input")
    values = [(el.get_attribute("value") or "").strip() for el in inputs]
    cleared_inputs = sum(1 for value in values if not value)
    disabled_after_submit = not inline_submit_enabled(driver)

    # Different builds show success differently. We accept either post-submit reset
    # or disabled state after send as an observable completion signal.
    return disabled_after_submit or cleared_inputs >= 2

# -*- coding: utf-8 -*-
import time
from urllib.parse import urlparse

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.new_web_site_sb.base_page_sb import BasePageSb


class ContactFormsSb(BasePageSb):
    SEND_BUTTON_XPATH = (
        "//div[contains(@class,'modal')]//button[.//span[normalize-space()='Send'] or normalize-space()='Send']"
    )

    SUBMIT_SPY_JS = r"""
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
      return;
    };
  }

  return true;
})();
"""

    REAL_NETWORK_PROBE_JS = r"""
(() => {
  if (!window.__qaRealNet) window.__qaRealNet = [];
  const push = (item) => {
    try {
      window.__qaRealNet.push(Object.assign({ ts: Date.now() }, item || {}));
    } catch (e) {}
  };

  const toUrl = (input) => {
    try {
      if (typeof input === 'string') return input;
      if (input && input.url) return String(input.url);
    } catch (e) {}
    return '';
  };

  if (!window.__qaOrigFetchReal && window.fetch) {
    window.__qaOrigFetchReal = window.fetch.bind(window);
    window.fetch = async function(input, init) {
      const method = (init && init.method) ? String(init.method).toUpperCase() : 'GET';
      const url = toUrl(input);
      let body = '';
      try { body = (init && init.body) ? String(init.body) : ''; } catch (e) {}

      const started = Date.now();
      try {
        const response = await window.__qaOrigFetchReal(input, init);
        let responseText = '';
        try {
          responseText = await response.clone().text();
        } catch (e) {}
        push({
          transport: 'fetch',
          method,
          url,
          status: Number(response.status || 0),
          ok: !!response.ok,
          body: body.slice(0, 1000),
          responseText: String(responseText || '').slice(0, 1000),
          durationMs: Date.now() - started,
        });
        return response;
      } catch (error) {
        push({
          transport: 'fetch',
          method,
          url,
          status: 0,
          ok: false,
          body: body.slice(0, 1000),
          error: String(error),
          durationMs: Date.now() - started,
        });
        throw error;
      }
    };
  }

  if (!window.__qaXhrRealPatched) {
    window.__qaXhrRealPatched = true;
    const origOpen = XMLHttpRequest.prototype.open;
    const origSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function(method, url) {
      this.__qaMethod = String(method || 'GET').toUpperCase();
      this.__qaUrl = String(url || '');
      return origOpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function(body) {
      const xhr = this;
      const started = Date.now();
      xhr.addEventListener('loadend', function() {
        let responseText = '';
        try { responseText = String(xhr.responseText || '').slice(0, 1000); } catch (e) {}
        push({
          transport: 'xhr',
          method: String(xhr.__qaMethod || 'GET').toUpperCase(),
          url: String(xhr.__qaUrl || ''),
          status: Number(xhr.status || 0),
          ok: Number(xhr.status || 0) >= 200 && Number(xhr.status || 0) < 300,
          body: body ? String(body).slice(0, 1000) : '',
          responseText: responseText,
          durationMs: Date.now() - started,
        });
      }, { once: true });
      return origSend.apply(this, arguments);
    };
  }
  return true;
})();
"""

    NETWORK_FAILURE_STUB_JS = r"""
((statusCode) => {
  window.__qaFailNet = [];
  const push = (item) => {
    try {
      window.__qaFailNet.push(Object.assign({ ts: Date.now() }, item || {}));
    } catch (e) {}
  };

  const normalizedStatus = Number(statusCode || 500);

  if (window.fetch) {
    window.fetch = function(input, init) {
      const method = (init && init.method) ? String(init.method).toUpperCase() : 'GET';
      const url = (typeof input === 'string') ? input : (input && input.url ? String(input.url) : '');
      const body = (init && init.body) ? String(init.body) : '';
      push({ transport: 'fetch', method, url, status: normalizedStatus, ok: false, body: body.slice(0, 1000) });

      const payload = JSON.stringify({ error: 'qa simulated failure', status: normalizedStatus });
      if (typeof Response !== 'undefined') {
        return Promise.resolve(new Response(payload, {
          status: normalizedStatus,
          headers: { 'Content-Type': 'application/json' },
        }));
      }
      return Promise.resolve({
        ok: false,
        status: normalizedStatus,
        json: async () => ({ error: 'qa simulated failure', status: normalizedStatus }),
        text: async () => payload,
      });
    };
  }

  if (!window.__qaXhrFailurePatched) {
    window.__qaXhrFailurePatched = true;
    XMLHttpRequest.prototype.open = function(method, url) {
      this.__qaMethod = String(method || 'GET').toUpperCase();
      this.__qaUrl = String(url || '');
    };
    XMLHttpRequest.prototype.send = function(body) {
      const xhr = this;
      push({
        transport: 'xhr',
        method: String(xhr.__qaMethod || 'GET').toUpperCase(),
        url: String(xhr.__qaUrl || ''),
        status: normalizedStatus,
        ok: false,
        body: body ? String(body).slice(0, 1000) : '',
      });

      setTimeout(() => {
        try {
          if (typeof xhr.onerror === 'function') xhr.onerror(new Event('error'));
          xhr.dispatchEvent(new Event('error'));
          xhr.dispatchEvent(new Event('loadend'));
        } catch (e) {}
      }, 0);
    };
  }

  return true;
})
"""

    def accept_cookie_if_present(self):
        self.accept_cookie_consent()

    def open_modal_by_cta_text(self, cta_text: str, required_placeholder: str | None = None):
        cta_xpath = f"//button[normalize-space()='{cta_text}' or .//span[normalize-space()='{cta_text}']]"

        def modal_opened() -> bool:
            if required_placeholder:
                selector = f".modal input[placeholder='{required_placeholder}']"
                return bool(self.driver.find_elements(By.CSS_SELECTOR, selector))
            return bool(self.driver.find_elements(By.CSS_SELECTOR, ".modal input, .modal textarea"))

        for _ in range(6):
            if modal_opened():
                return

            buttons = self.driver.find_elements(By.XPATH, cta_xpath)
            candidates = []
            for btn in buttons:
                try:
                    if btn.is_displayed() and btn.is_enabled():
                        in_form = bool(self.driver.execute_script("return !!arguments[0].closest('form');", btn))
                        candidates.append((in_form, btn))
                except Exception:
                    continue

            candidates.sort(key=lambda item: item[0])

            for _, btn in candidates:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.4)
                    self.accept_cookie_if_present()
                    if modal_opened():
                        return
                except Exception:
                    continue

        assert False, f"Modal did not open for CTA '{cta_text}'"

    def close_modal_if_open(self):
        close_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".modal .modal-header .icon-btn")
        if close_buttons:
            self.driver.execute_script("arguments[0].click();", close_buttons[0])
            time.sleep(0.35)

    def fill_modal_input(self, placeholder: str, value: str):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f".modal input[placeholder='{placeholder}']"))
        )
        field.clear()
        field.send_keys(value)

    def fill_modal_textarea(self, value: str):
        textarea = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal textarea"))
        )
        textarea.clear()
        textarea.send_keys(value)

    def ensure_modal_checkbox_checked(self):
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, ".modal input[type='checkbox']")
        assert checkboxes, "Modal checkbox not found"
        if not checkboxes[0].is_selected():
            self.driver.execute_script("arguments[0].click();", checkboxes[0])
            time.sleep(0.2)

    def get_modal_send_button(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.SEND_BUTTON_XPATH))
        )

    def assert_modal_send_disabled(self):
        btn = self.get_modal_send_button()
        assert (not btn.is_enabled()) or (btn.get_attribute("disabled") is not None), (
            "Send button should be disabled before form is complete"
        )

    def assert_modal_send_enabled(self):
        btn = self.get_modal_send_button()
        assert btn.is_enabled() and btn.get_attribute("disabled") is None, (
            "Send button should be enabled for completed form"
        )

    def click_modal_send(self):
        self.driver.execute_script("arguments[0].click();", self.get_modal_send_button())

    def modal_is_open(self):
        return bool(self.driver.find_elements(By.XPATH, self.SEND_BUTTON_XPATH))

    def modal_send_disabled(self):
        if not self.modal_is_open():
            return False
        btn = self.get_modal_send_button()
        return (not btn.is_enabled()) or (btn.get_attribute("disabled") is not None)

    def install_submit_spy(self):
        self.driver.execute_script(self.SUBMIT_SPY_JS)

    def clear_submit_spy(self):
        self.driver.execute_script("window.__qaRequests = [];")

    def get_contact_post_urls(self):
        reqs = self.driver.execute_script("return window.__qaRequests || [];")
        urls = []
        for req in reqs:
            method = str(req.get("method", "")).upper()
            url = str(req.get("url", ""))
            if method == "POST" and "/contact/" in url:
                urls.append(url)
        return urls

    def submit_modal_and_collect_contact_urls(self):
        self.click_modal_send()
        time.sleep(0.8)
        return self.get_contact_post_urls()

    def install_real_network_probe(self):
        self.driver.execute_script(self.REAL_NETWORK_PROBE_JS)

    def clear_real_network_probe(self):
        self.driver.execute_script("window.__qaRealNet = [];")

    def get_real_network_events(self):
        return self.driver.execute_script("return window.__qaRealNet || [];")

    def wait_for_contact_network_events(self, endpoint_substring: str, timeout: float = 20.0):
        end_at = time.time() + timeout
        endpoint_substring = endpoint_substring or "/contact/"

        while time.time() < end_at:
            events = self.get_real_network_events()
            matched = []
            for event in events:
                method = str(event.get("method", "")).upper()
                url = str(event.get("url", ""))
                if method == "POST" and endpoint_substring in url:
                    matched.append(event)
            if matched:
                return matched
            time.sleep(0.35)
        return []

    def install_network_failure_stub(self, status_code: int = 500):
        self.driver.execute_script(self.NETWORK_FAILURE_STUB_JS, int(status_code))

    def clear_failure_stub_events(self):
        self.driver.execute_script("window.__qaFailNet = [];")

    def get_failure_stub_events(self):
        return self.driver.execute_script("return window.__qaFailNet || [];")

    def inline_contacts_form(self):
        return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "form")))

    def inline_submit_button(self):
        form = self.inline_contacts_form()
        return form.find_element(By.CSS_SELECTOR, "button[type='submit'], button")

    def inline_submit_enabled(self):
        btn = self.inline_submit_button()
        return btn.is_enabled() and btn.get_attribute("disabled") is None

    def visible_input_by_placeholder(self, form, placeholder: str):
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

    def fill_inline_contacts_values(self, *, name: str, phone: str, email: str, company: str):
        form = self.inline_contacts_form()
        values = {
            "Name": name,
            "Enter phone number": phone,
            "qwerty@sportbenefit.eu": email,
            "Company": company,
        }
        for placeholder, value in values.items():
            field = self.visible_input_by_placeholder(form, placeholder)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
            field.clear()
            field.send_keys(value)
            time.sleep(0.12)

    def fill_inline_contacts_invalid(self):
        self.fill_inline_contacts_values(
            name="QA Bot",
            phone="123",
            email="bad",
            company="Inline QA",
        )

    def click_inline_submit(self):
        submit = self.inline_submit_button()
        self.driver.execute_script("arguments[0].click();", submit)

    def inline_validation_messages(self):
        msgs = []
        for el in self.driver.find_elements(By.CSS_SELECTOR, "form .input-error"):
            text = (el.text or "").strip()
            if text:
                msgs.append(text)
        return msgs

    def modal_validation_messages(self):
        msgs = []
        for el in self.driver.find_elements(By.CSS_SELECTOR, ".modal .input-error"):
            text = (el.text or "").strip()
            if text:
                msgs.append(text)
        return msgs

    def inline_success_state(self):
        form = self.inline_contacts_form()
        inputs = form.find_elements(By.CSS_SELECTOR, "input")
        values = [(el.get_attribute("value") or "").strip() for el in inputs]
        cleared_inputs = sum(1 for value in values if not value)
        disabled_after_submit = not self.inline_submit_enabled()
        return disabled_after_submit or cleared_inputs >= 2

    def wait_for_modal_submit_feedback(self, timeout: float = 12.0):
        end_at = time.time() + timeout
        while time.time() < end_at:
            send_buttons = self.driver.find_elements(By.XPATH, self.SEND_BUTTON_XPATH)
            if not send_buttons:
                return {"closed": True, "disabled": False, "messages": self.modal_validation_messages()}

            btn = send_buttons[0]
            disabled = (not btn.is_enabled()) or (btn.get_attribute("disabled") is not None)
            messages = self.modal_validation_messages()
            if disabled or messages:
                return {"closed": False, "disabled": disabled, "messages": messages}
            time.sleep(0.3)

        send_buttons = self.driver.find_elements(By.XPATH, self.SEND_BUTTON_XPATH)
        if not send_buttons:
            return {"closed": True, "disabled": False, "messages": self.modal_validation_messages()}
        btn = send_buttons[0]
        disabled = (not btn.is_enabled()) or (btn.get_attribute("disabled") is not None)
        return {"closed": False, "disabled": disabled, "messages": self.modal_validation_messages()}

    def fill_valid_modal_form(self, kind: str, suffix: str):
        self.fill_modal_input("Name", f"QA UX {suffix}")
        self.fill_modal_input("Enter phone number", "+357 99 11 22 55")

        if kind == "ask_question":
            self.fill_modal_input("qwerty@allsports.by", f"qa.ux.ask.{suffix}@example.com")
            self.fill_modal_textarea(f"UX question {suffix}")
        elif kind == "become_partner":
            self.fill_modal_input("qwerty@sportbenefit.eu", f"qa.ux.partner.{suffix}@example.com")
            self.fill_modal_input("Facility name", f"QA UX Facility {suffix}")
            self.fill_modal_input("Enter the city", "Larnaca")
        else:
            self.fill_modal_input("qwerty@sportbenefit.eu", f"qa.ux.offer.{suffix}@example.com")
            self.fill_modal_input("Company", f"QA UX Company {suffix}")
            self.fill_modal_input("Enter the city", "Limassol")

        self.ensure_modal_checkbox_checked()
        self.assert_modal_send_enabled()

    def fill_modal_form_for_validation(self, form_kind: str, invalid_case: str):
        email = "qa.matrix@example.com"
        phone = "+357 99 11 22 33"

        if invalid_case == "invalid_email":
            email = "bad"
        if invalid_case == "invalid_phone":
            phone = "123"

        self.fill_modal_input("Name", "QA Matrix")
        self.fill_modal_input("Enter phone number", phone)

        if form_kind == "ask_question":
            self.fill_modal_input("qwerty@allsports.by", email)
            self.fill_modal_textarea("Validation matrix question")
        elif form_kind == "become_partner":
            self.fill_modal_input("qwerty@sportbenefit.eu", email)
            self.fill_modal_input("Facility name", "QA Matrix Facility")
            self.fill_modal_input("Enter the city", "Nicosia")
        else:
            self.fill_modal_input("qwerty@sportbenefit.eu", email)
            self.fill_modal_input("Company", "QA Matrix Company")
            self.fill_modal_input("Enter the city", "Limassol")

        if invalid_case != "without_consent":
            self.ensure_modal_checkbox_checked()

    def fill_modal_form_for_live_case(self, case_kind: str, suffix: str):
        self.assert_modal_send_disabled()

        self.fill_modal_input("Name", f"QA Live {suffix}")
        self.fill_modal_input("Enter phone number", "+357 99 11 22 33")

        if case_kind == "ask_question":
            self.fill_modal_input("qwerty@allsports.by", f"qa.live.ask.{suffix}@example.com")
            self.fill_modal_textarea(f"Live ask-question check {suffix}")
        elif case_kind == "become_partner":
            self.fill_modal_input("qwerty@sportbenefit.eu", f"qa.live.partner.{suffix}@example.com")
            self.fill_modal_input("Facility name", f"QA Facility {suffix}")
            self.fill_modal_input("Enter the city", "Nicosia")
        else:
            self.fill_modal_input("qwerty@sportbenefit.eu", f"qa.live.offer.{suffix}@example.com")
            self.fill_modal_input("Company", f"QA Company {suffix}")
            self.fill_modal_input("Enter the city", "Limassol")

        self.ensure_modal_checkbox_checked()
        self.assert_modal_send_enabled()

    @staticmethod
    def require_staging_base_for_live_forms(request):
        base_url = request.config.getoption("--base-url").rstrip("/")
        parsed = urlparse(base_url)
        host = (parsed.netloc or "").lower()

        if "sportbenefit" not in host or "staging" not in host:
            pytest.skip(
                "UI live form E2E is allowed only on staging SportBenefit hosts. "
                f"Current --base-url host: {host or '<empty>'}"
            )

        return f"{parsed.scheme}://{parsed.netloc}".rstrip("/")

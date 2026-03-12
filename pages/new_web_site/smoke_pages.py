# -*- coding: utf-8 -*-
import allure

from locators.elements_for_new_web_site.for_smoke_pages import SmokeLocators as L
from pages.new_web_site.regression_pages import RegressionPages


class SmokePages(RegressionPages):
    """Smoke-проверки после релиза в Page Object формате."""

    def _build_failure(self, page_key, url, reason):
        return {
            'page': page_key,
            'url': self._resolve_url(url),
            'reason': str(reason),
        }

    def _attach_smoke_summary(self, name, failures):
        if failures:
            lines = [f'{name}: FAILED']
            for idx, item in enumerate(failures, 1):
                lines.append(
                    f"{idx}. page={item['page']} | url={item['url']} | reason={item['reason']}"
                )
        else:
            lines = [f'{name}: PASSED', 'FAILED_ITEMS: none']

        summary = '\n'.join(lines)
        print(summary)
        allure.attach(summary, name=name, attachment_type=allure.attachment_type.TEXT)
        return summary

    def _collect_ui_failures(self):
        failures = []
        for page_key in L.UI_PAGE_KEYS:
            data = L.get_page_data(page_key)
            url = data['url']
            locators = data.get('locators', [])

            with allure.step(f'Smoke UI: {page_key} -> {url}'):
                try:
                    if not locators:
                        raise AssertionError(f'Для страницы {page_key} не заданы локаторы')

                    self.check_http_status(url)
                    self.open_page(url)
                    self.accept_cookie_consent()
                    self.check_element_visible(locators[0])
                except Exception as e:
                    failures.append(self._build_failure(page_key, url, e))

        return failures

    def _collect_http_failures(self):
        failures = []
        for page_key in L.HTTP_PAGE_KEYS:
            data = L.get_page_data(page_key)
            url = data['url']

            with allure.step(f'Smoke HTTP: {page_key} -> {url}'):
                try:
                    self.check_http_status(url)
                except Exception as e:
                    failures.append(self._build_failure(page_key, url, e))

        return failures

    @allure.step('Выполнить post-release smoke: ключевые UI страницы')
    def run_post_release_smoke_ui(self):
        failures = self._collect_ui_failures()
        summary = self._attach_smoke_summary('smoke-post-release-ui', failures)
        assert not failures, summary

    @allure.step('Выполнить post-release smoke: доступность критичных служебных страниц')
    def run_post_release_smoke_http(self):
        failures = self._collect_http_failures()
        summary = self._attach_smoke_summary('smoke-post-release-http', failures)
        assert not failures, summary

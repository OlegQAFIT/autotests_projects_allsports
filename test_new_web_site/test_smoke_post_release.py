# -*- coding: utf-8 -*-
import allure
from pages.new_web_site.regression_pages import RegressionPages
from locators.elements_for_new_web_site.regression_pages_locators import RegressionLocators as L


SMOKE_UI_PAGE_KEYS = (
    'main',
    'facilities',
    'levels',
    'companies',
    'partners',
    'contacts',
)

SMOKE_HTTP_PAGE_KEYS = (
    'license',
    'user_agreement',
    'policy',
    'license_doc',
    'individual_license',
    'rule',
    'cookie_policy',
    'facilities_table',
)


def _attach_smoke_summary(name, failures):
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


@allure.feature('Smoke')
@allure.story('Post-release: ключевые UI страницы')
@allure.severity('Blocker')
def test_post_release_smoke_ui(driver):
    page = RegressionPages(driver)
    failures = []

    for page_key in SMOKE_UI_PAGE_KEYS:
        data = L.PAGES[page_key]
        url = data['url']
        locator = data['locators'][0]

        with allure.step(f'Smoke UI: {page_key} -> {url}'):
            try:
                page.check_http_status(url)
                page.open_page(url)
                page.accept_cookie_consent()
                page.check_element_visible(locator)
            except Exception as e:
                failures.append(
                    {
                        'page': page_key,
                        'url': page._resolve_url(url),
                        'reason': str(e),
                    }
                )

    summary = _attach_smoke_summary('smoke-post-release-ui', failures)
    assert not failures, summary


@allure.feature('Smoke')
@allure.story('Post-release: доступность критичных служебных страниц')
@allure.severity('Critical')
def test_post_release_smoke_http(driver):
    page = RegressionPages(driver)
    failures = []

    for page_key in SMOKE_HTTP_PAGE_KEYS:
        data = L.PAGES[page_key]
        url = data['url']

        with allure.step(f'Smoke HTTP: {page_key} -> {url}'):
            try:
                page.check_http_status(url)
            except Exception as e:
                failures.append(
                    {
                        'page': page_key,
                        'url': page._resolve_url(url),
                        'reason': str(e),
                    }
                )

    summary = _attach_smoke_summary('smoke-post-release-http', failures)
    assert not failures, summary

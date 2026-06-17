# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.document_integrity_sb import DocumentIntegritySb


@allure.feature("SB Documents Integrity")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.docs_integrity
@pytest.mark.parametrize(
    "case",
    DocumentIntegritySb.DOC_CASES,
    ids=[c["url"].split("/en-cy/")[-1] for c in DocumentIntegritySb.DOC_CASES],
)
def test_documents_html_language_content_and_links_sb(case):
    page = DocumentIntegritySb()
    page.check_document_html_language_content_and_links(case)

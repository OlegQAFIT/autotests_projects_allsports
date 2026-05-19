# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin, urlparse, urlunparse

import allure
import pytest
import requests


DOC_CASES = [
    {
        "url": "https://www.sportbenefit.eu/en-cy/license",
        "keywords": ["license", "rights", "terms", "agreement"],
        "require_version_signal": False,
    },
    {
        "url": "https://www.sportbenefit.eu/en-cy/user-agreements",
        "keywords": ["user", "agreement", "terms", "conditions"],
        "require_version_signal": False,
    },
    {
        "url": "https://www.sportbenefit.eu/en-cy/policy/260407_processing_personal_data",
        "keywords": ["personal data", "processing", "privacy", "policy"],
        "require_version_signal": True,
    },
    {
        "url": "https://www.sportbenefit.eu/en-cy/rule/250811_rule",
        "keywords": ["rule", "membership", "benefit", "conditions"],
        "require_version_signal": True,
    },
    {
        "url": "https://www.sportbenefit.eu/en-cy/cookie/cookie-policy",
        "keywords": ["cookie", "policy", "tracking", "browser"],
        "require_version_signal": True,
    },
]

CYRILLIC_RE = re.compile(r"[А-Яа-яЁёІіЇїЄєЎў]+")
YEAR_RE = re.compile(r"\b20\d{2}\b")


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))


def _extract_canonical(html: str):
    match = re.search(
        r"<link[^>]+rel\s*=\s*['\"][^'\"]*canonical[^'\"]*['\"][^>]*href\s*=\s*['\"]([^'\"]+)['\"]",
        html,
        flags=re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()
    return None


def _strip_html_text(html: str) -> str:
    without_scripts = re.sub(r"<script.*?>.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    without_styles = re.sub(r"<style.*?>.*?</style>", " ", without_scripts, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", without_styles)
    return re.sub(r"\s+", " ", text).strip()


def _extract_headings(html: str):
    headings = re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html, flags=re.IGNORECASE | re.DOTALL)
    cleaned = []
    for heading in headings:
        plain = re.sub(r"<[^>]+>", " ", heading)
        plain = re.sub(r"\s+", " ", plain).strip()
        if plain:
            cleaned.append(plain)
    return cleaned


def _extract_internal_legal_links(base_url: str, html: str):
    links = set()
    for href in re.findall(r"href=['\"]([^'\"]+)['\"]", html, flags=re.IGNORECASE):
        absolute = urljoin(base_url, href.strip())
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc.lower() not in {"www.sportbenefit.eu", "sportbenefit.eu"}:
            continue
        path = (parsed.path or "").lower()
        if any(token in path for token in ("/license", "/user-agreements", "/policy/", "/rule/", "/cookie/")):
            links.add(_normalize_url(absolute))
    return sorted(links)


@allure.feature("SB Documents Integrity")
@allure.severity("Critical")
@pytest.mark.pre_release
@pytest.mark.docs_integrity
@pytest.mark.parametrize("case", DOC_CASES, ids=[c["url"].split("/en-cy/")[-1] for c in DOC_CASES])
def test_documents_html_language_content_and_links_sb(case):
    """Проверка legal-документов: язык, canonical, контент и внутренние ссылки."""
    response = requests.get(case["url"], timeout=25, allow_redirects=True)
    assert response.status_code == 200, f"{case['url']} returned {response.status_code}"

    content_type = (response.headers.get("Content-Type") or "").lower()
    assert "text/html" in content_type, f"{case['url']} is not HTML content-type: {content_type}"

    html = response.text or ""
    assert len(html) > 800, f"Document HTML is unexpectedly short: {case['url']}"

    lang_match = re.search(r"<html[^>]*lang=['\"]([^'\"]+)['\"]", html, flags=re.IGNORECASE)
    assert lang_match, f"HTML lang attribute is missing on {case['url']}"
    lang_value = (lang_match.group(1) or "").lower()
    assert lang_value.startswith("en"), f"Unexpected document lang on {case['url']}: {lang_value}"

    canonical = _extract_canonical(html)
    assert canonical, f"Canonical link is missing on {case['url']}"
    canonical_url = _normalize_url(urljoin(response.url, canonical))
    final_url = _normalize_url(response.url)
    assert canonical_url == final_url, (
        f"Canonical mismatch on {case['url']}: canonical={canonical_url}, final={final_url}"
    )

    text = _strip_html_text(html)
    assert len(text) > 300, f"Document text is too short: {case['url']}"
    assert not CYRILLIC_RE.findall(text), f"Cyrillic words detected in document: {case['url']}"

    text_lower = text.lower()
    assert any(keyword in text_lower for keyword in case["keywords"]), (
        f"Expected legal keywords are missing on {case['url']}. Keywords={case['keywords']}"
    )

    headings = _extract_headings(html)
    assert headings, f"No headings found in document: {case['url']}"

    has_version_signal = bool(YEAR_RE.search(text_lower)) or any(
        token in text_lower for token in ("updated", "effective", "version", "revision", "last updated")
    )
    if case.get("require_version_signal", True):
        assert has_version_signal, f"No version/date signal found in document: {case['url']}"

    internal_legal_links = _extract_internal_legal_links(response.url, html)
    assert internal_legal_links, f"No internal legal links found in document: {case['url']}"

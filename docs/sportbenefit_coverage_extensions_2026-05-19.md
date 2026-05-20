# SportBenefit Coverage Extensions (2026-05-19)

## Added suites

- Unified UI forms suite (modal/inline forms, validation, submit endpoints, post-submit UX, live E2E, mobile form checks): `test_new_web_site_sb/test_forms_sb.py`
- Click-through all key pages (links/buttons/tabs): `test_new_web_site_sb/test_clickthrough_all_pages_sb.py`
- Mobile facilities regression (3 viewports): `test_new_web_site_sb/test_mobile_functional_regression_sb.py`
- Strict console gate: `test_new_web_site_sb/test_console_strict_sb.py`
- Legal documents integrity depth checks: `test_new_web_site_sb/test_documents_integrity_sb.py`
- Visual regression baseline hashes: `test_new_web_site_sb/test_visual_regression_sb.py`

## New pytest markers

- `console_strict`
- `docs_integrity`
- `visual_regression`

## Run examples

```bash
# Strict console
pytest test_new_web_site_sb -m console_strict --headless --b chrome

# Documents integrity
pytest test_new_web_site_sb -m docs_integrity --headless --b chrome

# Mobile functional regression
pytest test_new_web_site_sb/test_mobile_functional_regression_sb.py --headless --b chrome

# Live UI E2E forms (staging only)
pytest test_new_web_site_sb/test_forms_sb.py -m live_api --live-api --base-url https://staging.sportbenefit.eu --headless --b chrome

# Visual regression compare
pytest test_new_web_site_sb -m visual_regression --headless --b chrome

# Visual baseline update
SB_VISUAL_UPDATE=1 pytest test_new_web_site_sb/test_visual_regression_sb.py --headless --b chrome
```

## CI browser matrix

Workflow: `.github/workflows/sb_browser_matrix.yml`

Matrix:
- `ubuntu-latest` + `chrome`
- `ubuntu-latest` + `ff`
- `windows-latest` + `edge`

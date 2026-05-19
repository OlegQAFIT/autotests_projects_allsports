# SportBenefit Coverage Extensions (2026-05-19)

## Added suites

- Live UI form E2E (staging only): `test_new_web_site_sb/test_live_ui_forms_e2e_sb.py`
- Post-submit UX (success + backend 4xx/5xx simulation): `test_new_web_site_sb/test_form_post_submit_ux_sb.py`
- Click-through all key pages (links/buttons/tabs): `test_new_web_site_sb/test_clickthrough_all_pages_sb.py`
- Mobile functional regression (3 viewports): `test_new_web_site_sb/test_mobile_functional_regression_sb.py`
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
pytest test_new_web_site_sb/test_live_ui_forms_e2e_sb.py --live-api --base-url https://staging.sportbenefit.eu --headless --b chrome

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

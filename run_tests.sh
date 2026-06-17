#!/bin/bash
set -euo pipefail

echo "Cron запустил run_tests.sh в $(date)" >> /Users/olega/cron_test.log

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# ===== НАСТРОЙКИ =====
PROJECT_PATH="${PROJECT_PATH:-/Users/olega/PycharmProjects/autotests_projects_allsports}"
VENV_PATH="${VENV_PATH:-/Users/olega/myproject/venv}"

# ВАЖНО: задаются только через переменные окружения (без хранения в файле)
BOT_TOKEN="${BOT_TOKEN:-}"
CHAT_ID="${CHAT_ID:-}"

PYTEST="$VENV_PATH/bin/pytest"
ALLURE="${ALLURE:-/opt/homebrew/bin/allure}"
CURL="/usr/bin/curl"
ZIP="/usr/bin/zip"

source "$VENV_PATH/bin/activate"
cd "$PROJECT_PATH"

NOW=$(date +'%Y-%m-%d_%H-%M')
LOG_FILE="pytest_${NOW}.log"
REPORT_ZIP="allure_report_${NOW}.zip"

# ===== ЗАПУСК ТЕСТОВ =====
TEST_EXIT=0
set +e
"$PYTEST" \
    test_new_web_site/test_smoke_post_release.py \
    -m "smoke and release_gate" \
    --json-report \
    --json-report-file=pytest-report.json \
    --alluredir=allure-results \
    > "$LOG_FILE" 2>&1
TEST_EXIT=$?
set -e

# ===== ALLURE =====
if [ -x "$ALLURE" ]; then
    "$ALLURE" generate allure-results --clean -o allure-report || true
    "$ZIP" -r "$REPORT_ZIP" allure-report >/dev/null || true
fi

# ===== ПОДСЧЁТ РЕЗУЛЬТАТОВ ИЗ JSON-ОТЧЁТА =====
TOTAL=0
PASSED=0
FAILED=0

if [ -f "pytest-report.json" ]; then
    TOTAL=$("$VENV_PATH/bin/python" - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("pytest-report.json").read_text(encoding="utf-8"))
print((data.get("summary") or {}).get("total", 0))
PY
)
    PASSED=$("$VENV_PATH/bin/python" - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("pytest-report.json").read_text(encoding="utf-8"))
print((data.get("summary") or {}).get("passed", 0))
PY
)
    FAILED=$("$VENV_PATH/bin/python" - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("pytest-report.json").read_text(encoding="utf-8"))
summary = data.get("summary") or {}
failed = sum(summary.get(key, 0) for key in ("failed", "error"))
print(failed)
PY
)
fi

TOTAL=${TOTAL:-0}
PASSED=${PASSED:-0}
FAILED=${FAILED:-0}

if [ "$FAILED" -gt 0 ]; then
    TEST_EXIT=1
fi

SUMMARY="🏁 *Результаты тестов (${NOW})*
✔️ Успешно: $PASSED
❌ Провалено: $FAILED
📊 Всего проверок: $TOTAL"

if [ "$FAILED" -gt 0 ]; then
    FAILED_DETAILS=$("$VENV_PATH/bin/python" - <<'PY'
import json
from pathlib import Path

report = Path("pytest-report.json")
if not report.exists():
    print("pytest-report.json not found")
    raise SystemExit(0)

data = json.loads(report.read_text(encoding="utf-8"))
tests = data.get("tests") or []
failed = []
for test in tests:
    outcome = test.get("outcome")
    if outcome not in {"failed", "error"}:
        continue
    nodeid = test.get("nodeid", "<unknown>")
    message = ""
    call = test.get("call") or {}
    crash = call.get("crash") or {}
    message = crash.get("message") or ""
    failed.append(f"{nodeid}\n{message}".strip())

print("\n\n".join(failed[:20]))
PY
)
    SUMMARY="$SUMMARY\n\n*📌 Упавшие проверки:*\n\`\`\`$FAILED_DETAILS\`\`\`"
fi

# ===== ОТПРАВКА В TELEGRAM (если заданы секреты) =====
if [ -n "$BOT_TOKEN" ] && [ -n "$CHAT_ID" ]; then
    "$CURL" -s -X POST \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\":\"$CHAT_ID\", \"text\":\"$SUMMARY\", \"parse_mode\":\"Markdown\"}" \
        "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" >/dev/null || true

    "$CURL" -F "chat_id=$CHAT_ID" \
        -F "caption=Лог тестов" \
        -F "document=@${LOG_FILE}" \
        "https://api.telegram.org/bot$BOT_TOKEN/sendDocument" >/dev/null || true

    if [ -f "$REPORT_ZIP" ]; then
        "$CURL" -F "chat_id=$CHAT_ID" \
            -F "caption=Allure отчёт" \
            -F "document=@${REPORT_ZIP}" \
            "https://api.telegram.org/bot$BOT_TOKEN/sendDocument" >/dev/null || true
    fi
fi

exit "$TEST_EXIT"

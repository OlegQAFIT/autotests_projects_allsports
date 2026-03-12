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
if ! "$PYTEST" \
    test_new_web_site/test_regression_pages.py \
    -m schedule \
    --alluredir=allure-results \
    > "$LOG_FILE" 2>&1; then
    TEST_EXIT=$?
fi

# ===== ALLURE =====
if [ -x "$ALLURE" ]; then
    "$ALLURE" generate allure-results --clean -o allure-report || true
    "$ZIP" -r "$REPORT_ZIP" allure-report >/dev/null || true
fi

# ===== ПОДСЧЁТ ПРОВЕРОК ИЗ ЛОГА =====
TOTAL=$(grep -Eo 'CHECKS_TOTAL=[0-9]+' "$LOG_FILE" | tail -1 | cut -d'=' -f2 || true)
PASSED=$(grep -Eo 'CHECKS_PASSED=[0-9]+' "$LOG_FILE" | tail -1 | cut -d'=' -f2 || true)
FAILED=$(grep -Eo 'CHECKS_FAILED=[0-9]+' "$LOG_FILE" | tail -1 | cut -d'=' -f2 || true)

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
    FAILED_DETAILS=$(awk 'found{print} /^FAILED_ITEMS:/{found=1}' "$LOG_FILE" | tail -40)
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

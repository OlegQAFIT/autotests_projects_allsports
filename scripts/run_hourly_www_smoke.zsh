#!/bin/zsh

# Ежечасовая smoke-проверка публичных сайтов.
# Скрипт вызывается LaunchAgent-ом macOS и показывает уведомление только
# если pytest завершился с ошибкой.

setopt pipefail

PROJECT_DIRECTORY="/Users/olega/PycharmProjects/autotests_projects_allsports"
PYTHON_EXECUTABLE="/Users/olega/myproject/venv/bin/python"
LOG_DIRECTORY="$PROJECT_DIRECTORY/logs/www_smoke"
RUN_TIMESTAMP="$(date '+%Y-%m-%d_%H-%M-%S')"
LOG_FILE="$LOG_DIRECTORY/www_smoke_$RUN_TIMESTAMP.log"

mkdir -p "$LOG_DIRECTORY"

{
    print "========================================"
    print "WWW smoke started: $(date '+%Y-%m-%d %H:%M:%S')"
    print "========================================"
} | tee -a "$LOG_FILE"

cd "$PROJECT_DIRECTORY" || exit 1

"$PYTHON_EXECUTABLE" -m pytest -q -s -p no:allure_pytest -o addopts='' \
    test_journal_main_flow --headless --live-api 2>&1 | tee -a "$LOG_FILE"
TEST_EXIT_CODE=${pipestatus[1]}

print "Finished: $(date '+%Y-%m-%d %H:%M:%S'); exit code: $TEST_EXIT_CODE" | tee -a "$LOG_FILE"

if (( TEST_EXIT_CODE != 0 )); then
    FAILED_TEST_NAMES="$(
        /usr/bin/grep '^FAILED ' "$LOG_FILE" \
            | /usr/bin/sed -E 's/^FAILED //' \
            | /usr/bin/tr '\n' ' '
    )"
    FAILED_TEST_NAMES="${FAILED_TEST_NAMES% }"
    if [[ -z "$FAILED_TEST_NAMES" ]]; then
        FAILED_TEST_NAMES="Pytest завершился с ошибкой; подробности — в logs/www_smoke."
    fi
    /usr/bin/osascript \
        -e 'on run argv' \
        -e 'display notification (item 1 of argv) with title "Allsports: упали тесты" sound name "Basso"' \
        -e 'end run' \
        "$FAILED_TEST_NAMES"
fi

exit "$TEST_EXIT_CODE"

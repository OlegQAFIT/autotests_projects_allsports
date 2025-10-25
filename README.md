# 🧪 autotests_projects_allsports

## 📘 Описание
**Allsports** — это единый проект автоматизации тестирования, объединяющий все автотесты для экосистемы Allsports:  
веб-сайт, Supplier Panel (SP V2), Journal и HR-портал.  
Основная цель — обеспечить полное покрытие тестами всех пользовательских сценариев, интеграций и интерфейсов, минимизировать ручное тестирование и ускорить релизы.

## 🎯 Цели проекта
- Автоматизация тестирования всех модулей Allsports.  
- Повышение стабильности релизов и скорости QA-процессов.  
- Сокращение времени на регрессию.  
- Формирование отчётности через **Allure** и интеграцию в CI/CD.  
- Возможность локального и удалённого запуска.

## ⚙️ Основной функционал
- UI и API автотесты для всех направлений Allsports.  
- Проверка форм, кнопок, навигации, валидаций и бизнес-логики.  
- Smoke, Regression, Validation и Integration тесты.  
- Отчётность через **Allure**.  
- Поддержка headless-режима и CI-интеграции (GitHub Actions, Jenkins, GitLab CI).  

## 🧩 Поддерживаемые подсистемы
- **Web Site** — проверка публичного сайта: форм, валидации, навигации, контента, карт, футеров, мета-тегов, ссылок.  
- **Supplier Panel (SP V2)** — тесты личного кабинета поставщиков: логин, создание и редактирование визитов, работа с расписанием, проверка данных объектов.  
- **Journal** — автотесты для журнала заявок: фильтры, статусы, экспорт данных, интеграция с другими системами.  
- **HR Portal** — тесты управления персоналом: списки, фильтры, импорт/экспорт, добавление и редактирование сотрудников.  

## 🧠 Структура проекта
autotests_projects_allsports/  
├── helpers/ — вспомогательные утилиты и методы  
├── locators/ — локаторы элементов  
│   ├── elements_for_new_web_site/  
│   ├── journal/  
│   ├── web_site_old/  
│   └── sp_v2/  
├── pages/ — Page Object модели  
│   ├── new_web_site/  
│   ├── supplier_panel/  
│   ├── journal/  
│   └── hr_portal/  
├── test_new_web_site/ — тесты для нового веб-сайта  
├── test_supplier_panel/ — тесты Supplier Panel (SP V2)  
├── tests_journal/ — тесты Journal  
├── tests_hr_portal/ — тесты HR-портала  
├── requirements.txt — список зависимостей  
└── README.md — инструкция по проекту  

## 🧩 Требования
Перед запуском убедитесь, что установлены:
- **Python 3.10+**
- **pip** (идёт вместе с Python)
- **Google Chrome** и **chromedriver**
- **Git**
- **Allure Commandline** (для генерации отчётов)

---

## 🛠 Установка и настройка окружения

1. Клонирование проекта  
   `git clone https://github.com/OlegQAFIT/autotests_projects_allsports.git`  
   `cd autotests_projects_allsports`

2. Создание виртуального окружения  
   `python -m venv venv`  
   `source venv/bin/activate` (macOS / Linux)  
   `venv\Scripts\activate` (Windows)

3. Установка зависимостей  
   `pip install -r requirements.txt`

4. Проверка установки  
   `python --version`  
   `pip --version`

---

## 🚀 Запуск тестов

**Запустить все тесты:**  
`pytest`

**Запустить только Smoke тесты:**  
`pytest -m smoke`

**Запустить конкретный модуль:**  
- Web site: `pytest test_new_web_site/`  
- Supplier Panel: `pytest test_supplier_panel/`  
- Journal: `pytest tests_journal/`  
- HR Portal: `pytest tests_hr_portal/`

**Подробный вывод шагов:**  
`pytest -v`

**Headless-режим (без открытия браузера):**  
`pytest --headless`

**С сохранением результатов для Allure:**  
`pytest --alluredir=allure-results`

---

## 📊 Отчёты Allure

**Установка Allure**  
macOS: `brew install allure`  
Windows: скачайте [Allure Commandline](https://github.com/allure-framework/allure2/releases) и добавьте путь к `bin` в PATH.  

**Генерация отчёта:**  
`allure generate allure-results -o allure-report --clean`

**Открытие отчёта:**  
`allure open allure-report`

---

## ⚒️ Полезные команды
`pytest -v` — подробный вывод шагов  
`pytest -k "contacts"` — запуск тестов, содержащих слово `contacts`  
`pytest --maxfail=1` — остановка при первом падении  
`pytest --tb=short` — короткий формат логов  
`git pull origin main` — получение последних изменений  
`git push origin main` — отправка изменений в репозиторий  
`allure open allure-report` — открыть Allure-отчёт локально  

---

## 🧾 Примеры запуска
**Пример 1 — smoke-тест веб-сайта:**  
`pytest -m smoke test_new_web_site/test_contacts_page.py --alluredir=allure-results`

**Пример 2 — тесты Supplier Panel:**  
`pytest test_supplier_panel/ --alluredir=allure-results`

**Пример 3 — полная регрессия со сбором отчёта:**  
`pytest -v --alluredir=allure-results && allure generate allure-results -o allure-report --clean && allure open allure-report`

---

## 🧩 Настройка GitHub и CI/CD
1. Проект связан с GitHub: [OlegQAFIT/autotests_projects_allsports](https://github.com/OlegQAFIT/autotests_projects_allsports)  
2. Все коммиты автоматически запускают тесты через GitHub Actions (можно подключить workflow `.github/workflows/tests.yml`).  
3. Отчёты Allure можно хранить как артефакты или публиковать в GitHub Pages.

---

## 👥 Авторы
- **Олег А.** — QA Automation Engineer  
  Автор и поддерживающий проекта **Allsports Autotests Framework**.

---

## 📬 Контакты
📧 Email: [oleg.a.allsports.fit@gmail.com](mailto:oleg.a.allsports.fit@gmail.com)  
🐙 GitHub: [OlegQAFIT](https://github.com/OlegQAFIT)

---

## 📜 Лицензия
Проект распространяется под лицензией **MIT**.  
Свободно используйте и модифицируйте код с указанием автора.

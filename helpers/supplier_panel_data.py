import os
from typing import Optional


def _as_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


SUPPLIER_ACCOUNTS = {
    "reception": {
        "login": os.getenv("SUPPLIER_RECEPTION_LOGIN", "auttest1@gmail.com"),
        "password": os.getenv("SUPPLIER_RECEPTION_PASSWORD", "secret"),
    },
    "finance": {
        "login": os.getenv("SUPPLIER_FINANCE_LOGIN", "auttest1@gmail.com"),
        "password": os.getenv("SUPPLIER_FINANCE_PASSWORD", "secret"),
    },
}


ROLE_DOCUMENTS_ACCESS = {
    "reception": _as_bool(os.getenv("SUPPLIER_RECEPTION_HAS_DOCUMENTS"), True),
    "finance": _as_bool(os.getenv("SUPPLIER_FINANCE_HAS_DOCUMENTS"), True),
}


FACILITY_DETAILS_EXACT_TEXT = {
    "reception": {
        "name": os.getenv(
            "SUPPLIER_RECEPTION_FACILITY_NAME",
            "Gym1 НЕ УДАЛЯТЬ НЕ ИЗМЕНЯТЬ НИЧЕГО",
        ),
        "description": os.getenv(
            "SUPPLIER_RECEPTION_FACILITY_DESCRIPTION",
            (
                "Предварительная запись обязательна через приложение объекта или по телефону. "
                "При отмене записи необходимо предупредить администратора студии за 4 часа до начала занятия. "
                "Полностью укомплектованная студия пилатеса и фитнеса. "
                "С актуальными направлениями можно ознакомиться в инстаграм студии. "
                "Тест XXX wedfwdwed n23e23e23n23e 23e 4444 qwd 555 "
                "wedwedqwdqdqd qdwqwd 333 444 цувцув 55 77"
            ),
        ),
        "address": os.getenv(
            "SUPPLIER_RECEPTION_FACILITY_ADDRESS",
            "г. Минск, ул. Рыбалко, д.16А г. Минск, ул. Рыбалко, д.16А г. Минск, ул. Рыбалко, д.16А",
        ),
        "phone": os.getenv(
            "SUPPLIER_RECEPTION_FACILITY_PHONE",
            "+375000000000;+375123456789",
        ),
        "website": os.getenv(
            "SUPPLIER_RECEPTION_FACILITY_WEBSITE",
            "https://mayert.com/nihil-sed-pariatur-eos-et-reprehenderit-ut.html",
        ),
    },
    "finance": {
        "name": os.getenv(
            "SUPPLIER_FINANCE_FACILITY_NAME",
            "Gym НЕ УДАЛЯТЬ НЕ ИЗМЕНЯТЬ НИЧЕГО, НЕ ШУТКА",
        ),
        "description": os.getenv(
            "SUPPLIER_FINANCE_FACILITY_DESCRIPTION",
            (
                "Предварительная запись обязательна через приложение объекта или по телефону. "
                "При отмене записи необходимо предупредить администратора студии за 4 часа до начала занятия. "
                "Полностью укомплектованная студия пилатеса и фитнеса. "
                "С актуальными направлениями можно ознакомиться в инстаграм студии. Тест XXX"
            ),
        ),
        "address": os.getenv(
            "SUPPLIER_FINANCE_FACILITY_ADDRESS",
            "г. Минск, ул. ИНТЕРНАЦИОНАЛЬНАЯ 36",
        ),
        "phone": os.getenv(
            "SUPPLIER_FINANCE_FACILITY_PHONE",
            "+375000000000;+375123456789",
        ),
        "website": os.getenv(
            "SUPPLIER_FINANCE_FACILITY_WEBSITE",
            "https://mayert.com/nihil-sed-pariatur-eos-et-reprehenderit-ut.html",
        ),
    },
}


CONTACTS_EXPECTED = {
    "phone": os.getenv("SUPPLIER_SUPPORT_PHONE", "+374 91 777 931"),
    "email": os.getenv("SUPPLIER_SUPPORT_EMAIL", "info@allsports.am"),
    "hours_ru": os.getenv(
        "SUPPLIER_SUPPORT_HOURS_RU",
        "Пн-Пт: 09:00-21:00, Сб-Вс: 09:00-19:00",
    ),
    "hours_en": os.getenv(
        "SUPPLIER_SUPPORT_HOURS_EN",
        "Mon-Fri: 09:00-21:00, Sat-Sun: 09:00-19:00",
    ),
}


def get_role_credentials(role: str) -> tuple[str, str]:
    account = SUPPLIER_ACCOUNTS.get(role)
    if account is None:
        raise ValueError(f"Unsupported supplier role: {role}")
    return account["login"], account["password"]


def role_has_documents(role: str) -> bool:
    return ROLE_DOCUMENTS_ACCESS.get(role, False)


def get_expected_facility_text(role: str) -> dict:
    expected = FACILITY_DETAILS_EXACT_TEXT.get(role)
    if expected is None:
        raise ValueError(f"Unsupported supplier role: {role}")
    return expected


def get_expected_contacts_text() -> dict:
    return CONTACTS_EXPECTED

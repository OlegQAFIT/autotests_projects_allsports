class LocatorsFromPagesLinks():
    domain_production = "https://www.allsports.fit/by"
    domain_production_new = "https://www.allsports.by/ru-by"
    domain_test = "https://оллспортс.бел/by"
    domain_test_new = "https://сайт.оллспортс.бел/ru-by"


    stay_links = [
        "/skidki/",
        "/price/220418_price/",
        "/price/230301_price/",
        "/price/201217_price/",
        "/price/210615_price/",
        "/affiliates-update/",
        "/affiliates-table/",
        # "/price/",
        "/faq-template/",# выдает 404
        "/faq_partner",
        "/android-policy",
        "/политика-конфиденциальности",
        "/faq/220822_geo_location/",
        "/faq/230801_faq/",
        "/faq/bioid/",
        "/faq/210615_faq/",
        "/hr_portal_rule/230301_rule/"
    ]

    pages_links = [
        "/user-agreements",
        "/license/",
        "/license/240415_license/",
        "/license/220701_licence/",
        "/license/230306_license/",
        "/license/210615_license/",
        "/license/220418_license/",
        "/license/210401_license/",
        "/license/240327_license/",
        "/license/201217_license/",
        "/license/201009_license/",
        "/license/201214_license/",
        "/blog/",
        "/blog/20201014-decrease-stress/",
        "/rule/240415_rule/",
        "/rule/230801_rule/",
        "/rule/230306_rule/",
        "/rule/210615_rule/",
        "/rule/210401_rule/",
        "/rule/201207_rule/",
        "/individual_license/240415_license/",
        "/individual_license/220316_license/",
        "/policy/211115_policy/",
        "/policy/220127_processing_personal_data/",
        "/policy/220218_processing_personal_data/",
        "/policy/230911_processing_personal_data/",
        "/policy/231109_processing_personal_data/"
    ]

    paths_and_redirects = [
        {
            "path": "/s/df34",
            "expected_redirect_test": "https://сайт.оллспортс.бел/ru-by/app",
            "expected_redirect_prod": "https://www.allsports.by/ru-by/app"
        },
        {
            "path": "/prices/",
            "expected_redirect_test": "https://сайт.оллспортс.бел/ru-by/levels",
            "expected_redirect_prod": "https://www.allsports.by/ru-by/levels"
        },
        {
            "path": "/prices/#objects",
            "expected_redirect_test": "https://сайт.оллспортс.бел/ru-by/levels#objects",
            "expected_redirect_prod": "https://www.allsports.by/ru-by/levels#objects"
        },
        {
            "path": "/objects/",
            "expected_redirect_test": "https://сайт.оллспортс.бел/ru-by/facilities",
            "expected_redirect_prod": "https://www.allsports.by/ru-by/facilities"
        },
        {
            "path": "/contact/",
            "expected_redirect_test": "https://сайт.оллспортс.бел/ru-by/contacts",
            "expected_redirect_prod": "https://www.allsports.by/ru-by/contacts"
        },
        {
            "path": "/affiliates/",
            "expected_redirect_test": "https://сайт.оллспортс.бел/ru-by/partners",
            "expected_redirect_prod": "https://www.allsports.by/ru-by/partners"
        },
        {
            "path": "/payment_service_rules/providing_payment_service_rules/",
            "expected_redirect_test": "https://сайт.оллспортс.бел/ru-by/providing-payment-service-rules",
            "expected_redirect_prod": "https://www.allsports.by/ru-by/providing-payment-service-rules"
        }
    ]




    pages_lincs_four = [
        "/holder-app-license-agreement",
        "/by/holder-app-license-agreement",
        "/holder-app-legal_license-agreement",
        "/by/holder-app-legal_license-agreement",
        "/holder_app_rules",
        "/by/holder_app_rules",
        "/holder-app-rules",
        "/holder-app-rules",
        "/user-agreements",
        "/by/user-agreements",
        "/program-rules-allsports-super",
        "/program-rules-allsports-super",
        "/card_rules",
        "/card_rules",
        "/holder-app-faq",
        "/by/holder-app-faq",
        "/ru/holder-app-faq",
        "/am/holder-app-faq",
        "/faq",
        "/ru/companies/",
        "/by/companies/",
        "/am/companies/",
        "/en_am/companies/",
        "/политика-конфиденциальности",
        "/android-policy",
        "/by/processing-personal-data",
        "/faq_partner",
        "/holder-app-policy",
        "/am/holder-app-policy",
        "/holder-app-policy",
        "/am/holder-app-rules",
        "/en_am/holder-app-rules",
        "/holder-app-rules",
        "/ru/holder-app-rules"
    ]

    expected_parts = [
        "/ru-by/individual_license/240415_license",
        "/ru-by/individual_license/240415_license/",
        "/ru-by/license/240415_license",
        "/ru-by/license/240415_license/",
        "/ru-by/rule/240415_rule/",
        "/ru-by/rule/240415_rule/",
        "/ru-by/rule/240415_rule/",
        "/ru-by/rule/240415_rule/",
        "/ru-by/user-agreements/",
        "/ru-by/user-agreements/",
        "/ru-by/rule/230801_rule/",
        "/ru-by/rule/230801_rule/",
        "/ru-by/rule/240415_rule/",
        "/ru-by/rule/240415_rule/",
        "/by/faq/230801_faq/",
        "/by/faq/230801_faq/",
        "/by/faq/230801_faq/",
        "/am/faq/210615_faq/",
        "/ru-by/facilities",
        "/ru/",
        "/ru-by/",
        "/am/",
        "/am/",
        "/%D0%BF%D0%BE%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0-%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B4%D0%B5%D0%BD%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D0%B8",
        "/android-policy/",
        "/ru-by/policy/231109_processing_personal_data/",
        "/faq_partner/",
        "/ru-by/policy/231109_processing_personal_data/",
        "/am/policy/190615_policy/",
        "/ru-by/policy/231109_processing_personal_data/",
        "/am/rule/210615_rule/",
        "/am/rule/210615_rule/",
        "/ru-by/rule/240415_rule/",
        "/ru/rule/210615_rule/"
    ]






    links = [
        "https://www.allsports.by/contact/",
        "http://www.allsports.by/objects",
        "http://allsports.by/affiliates",
        "https://www.allsports.by/политика-конфиденциальности",
        "https://www.allsports.by/program-rules-allsports-super",
        "https://www.allsports.by/holder-app-license-agreement/",
        "https://allsports.by/price/220418_price/",
        "https://allsports.by/holder-app-rules",
        "https://www.allsports.by/android-policy",
        "https://www.allsports.by/price/210615_price/"
    ]









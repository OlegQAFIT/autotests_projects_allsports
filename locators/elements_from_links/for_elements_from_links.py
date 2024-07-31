class LocatorsFromPagesLinks():
    domain_production = "https://www.allsports.fit/by"
    domain_production_new = "https://www.allsports.by/ru-by"
    # domain_test = "https://www.allsports.fit/by"
    # domain_test_new = "https://www.allsports.by/ru-by"
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

    pages_lincs_three = [
        "/s/df34",
        "/prices/",
        "/prices/#objects",
        "/objects/",
        "/contact/",
        "/affiliates/",
        "/payment_service_rules/providing_payment_service_rules/",
    ]

    mappings = {
        "/s/df34": "https://сайт.оллспортс.бел/ru-by/app",
        "/prices/": "https://сайт.оллспортс.бел/ru-by/levels",
        "/prices/#objects": "https://сайт.оллспортс.бел/ru-by/levels#objects",
        "/objects/": "https://сайт.оллспортс.бел/ru-by/facilities",
        "/contact/": "https://сайт.оллспортс.бел/ru-by/contacts",
        "/affiliates/": "https://сайт.оллспортс.бел/ru-by/partners",
        "/payment_service_rules/providing_payment_service_rules/": "https://сайт.оллспортс.бел/ru-by/providing-payment-service-rules"
    }
    redirects_to_pages = {
        "https://оллспортс.бел/by/app/",
        "https://сайт.оллспортс.бел/ru-by/levels",
        "https://сайт.оллспортс.бел/ru-by/prices/#objects",
        "https://сайт.оллспортс.бел/ru-by/facilities",
        "https://сайт.оллспортс.бел/ru-by/contacts",
        "https://сайт.оллспортс.бел/ru-by/partners",
        "https://сайт.оллспортс.бел/ru-by/providing-payment-service-rules"
    }
    # mappings_prod = {
    #     "/s/df34": "https://www.allsports.fit/by/app",
    #     "/prices/": "https://www.allsports.fit/by/levels",
    #     "/prices/#objects": "https://www.allsports.fit/by/levels#objects",
    #     "/objects/": "https://www.allsports.fit/by/facilities",
    #     "/contact/": "https://www.allsports.fit/by/contacts",
    #     "/affiliates/": "https://www.allsports.fit/by/partners",
    #     "/payment_service_rules/providing_payment_service_rules/": "https://www.allsports.fit/by/providing-payment-service-rules"
    # }
    # redirects_to_pages_prod = {
    #     "https://www.allsports.fit/by/app",
    #     "https://www.allsports.fit/by/levels",
    #     "https://www.allsports.fit/by/levels#objects",
    #     "https://www.allsports.fit/by/facilities",
    #     "https://www.allsports.fit/by/contacts",
    #     "https://www.allsports.fit/by/partners",
    #     "https://www.allsports.fit/by/providing-payment-service-rules"
    # }




    pages_lincs_four = [
        "https://оллспортс.бел/holder-app-license-agreement",
        "https://оллспортс.бел/by/holder-app-license-agreement",
        "https://оллспортс.бел/holder-app-legal_license-agreement",
        "https://оллспортс.бел/by/holder-app-legal_license-agreement",
        "https://оллспортс.бел/holder_app_rules",
        "https://оллспортс.бел/by/holder_app_rules",
        "https://оллспортс.бел/holder-app-rules",
        "https://оллспортс.бел/holder-app-rules",
        "https://оллспортс.бел/user-agreements",
        "https://оллспортс.бел/by/user-agreements",
        "https://оллспортс.бел/program-rules-allsports-super",
        "https://оллспортс.бел/program-rules-allsports-super",
        "https://оллспортс.бел/card_rules",
        "https://оллспортс.бел/card_rules",
        "https://оллспортс.бел/holder-app-faq",
        "https://оллспортс.бел/by/holder-app-faq",
        "https://оллспортс.бел/ru/holder-app-faq",
        "https://оллспортс.бел/am/holder-app-faq",
        "https://оллспортс.бел/faq",
        "https://оллспортс.бел/ru/companies/",
        "https://оллспортс.бел/by/companies/",
        "https://оллспортс.бел/am/companies/",
        "https://оллспортс.бел/en_am/companies/",
        "https://оллспортс.бел/политика-конфиденциальности",
        "https://оллспортс.бел/android-policy",
        "https://оллспортс.бел/by/processing-personal-data",
        "https://оллспортс.бел/faq_partner",
        "https://оллспортс.бел/holder-app-policy",
        "https://оллспортс.бел/am/holder-app-policy",
        "https://оллспортс.бел/holder-app-policy",
        "https://оллспортс.бел/am/holder-app-rules",
        "https://оллспортс.бел/en_am/holder-app-rules",
        "https://оллспортс.бел/holder-app-rules",
        "https://оллспортс.бел/ru/holder-app-rules"
    ]
    # pages_lincs_prod_four = [
    #     "https://www.allsports.fit/by/holder-app-license-agreement",
    #     "https://www.allsports.fit/by/holder-app-license-agreement",
    #     "https://www.allsports.fit/by/holder-app-legal_license-agreement",
    #     "https://www.allsports.fit/by/holder-app-legal_license-agreement",
    #     "https://www.allsports.fit/by/holder_app_rules",
    #     "https://www.allsports.fit/by/holder_app_rules",
    #     "https://www.allsports.fit/by/holder-app-rules",
    #     "https://www.allsports.fit/by/holder-app-rules",
    #     "https://www.allsports.fit/by/user-agreements",
    #     "https://www.allsports.fit/by/user-agreements",
    #     "https://www.allsports.fit/by/program-rules-allsports-super",
    #     "https://www.allsports.fit/by/program-rules-allsports-super",
    #     "https://www.allsports.fit/by/card_rules",
    #     "https://www.allsports.fit/by/card_rules",
    #     "https://www.allsports.fit/by/holder-app-faq",
    #     "https://www.allsports.fit/by/holder-app-faq",
    #     "https://www.allsports.fit/by/holder-app-faq",
    #     "https://www.allsports.fit/by/holder-app-faq",
    #     "https://www.allsports.fit/by/faq",
    #     "https://www.allsports.fit/ru/companies/",
    #     "https://www.allsports.fit/by/companies/",
    #     "https://www.allsports.fit/am/companies/",
    #     "https://www.allsports.fit/en_am/companies/",
    #     "https://www.allsports.fit/by/политика-конфиденциальности",
    #     "https://www.allsports.fit/by/android-policy",
    #     "https://www.allsports.fit/by/processing-personal-data",
    #     "https://www.allsports.fit/by/faq_partner",
    #     "https://www.allsports.fit/by/holder-app-policy",
    #     "https://www.allsports.fit/am/holder-app-policy",
    #     "https://www.allsports.fit/by/holder-app-policy",
    #     "https://www.allsports.fit/am/holder-app-rules",
    #     "https://www.allsports.fit/en_am/holder-app-rules",
    #     "https://www.allsports.fit/by/holder-app-rules",
    #     "https://www.allsports.fit/ru/holder-app-rules"
    # ]

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
        "https://www.allsports.by/ru-by/affiliates-table/",
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









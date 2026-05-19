# -*- coding: utf-8 -*-


class RegressionPagesLocatorsSb:
    LEGAL_PAGES = [
        "https://www.sportbenefit.eu/en-cy/license",
        "https://www.sportbenefit.eu/en-cy/user-agreements",
        "https://www.sportbenefit.eu/en-cy/policy/260407_processing_personal_data",
        "https://www.sportbenefit.eu/en-cy/rule/250811_rule",
        "https://www.sportbenefit.eu/en-cy/cookie/cookie-policy",
        "https://www.sportbenefit.eu/en-cy/license/260407_license",
        "https://www.sportbenefit.eu/en-cy/individual_license/260407_license",
    ]

    MOBILE_VIEWPORTS = [
        (390, 844),
        (768, 1024),
    ]

    COPYWRITING_VIEWPORTS = [
        (360, 800),
        (390, 844),
        (768, 1024),
        (1024, 768),
        (1280, 800),
        (1440, 900),
    ]

    CYRILLIC_GATE_VIEWPORTS = [
        (390, 844),
        (1280, 800),
    ]

    KEY_PAGES = [
        "https://www.sportbenefit.eu/en-cy",
        "https://www.sportbenefit.eu/en-cy/facilities",
        "https://www.sportbenefit.eu/en-cy/facilities-table",
        "https://www.sportbenefit.eu/en-cy/levels",
        "https://www.sportbenefit.eu/en-cy/companies",
        "https://www.sportbenefit.eu/en-cy/partners",
        "https://www.sportbenefit.eu/en-cy/contacts",
        "https://www.sportbenefit.eu/en-cy/app",
    ]

    FACILITIES_PAGE = "https://www.sportbenefit.eu/en-cy/facilities"
    FACILITIES_TABLE_PAGE = "https://www.sportbenefit.eu/en-cy/facilities-table"

    ALL_CHECK_PAGES = KEY_PAGES + LEGAL_PAGES

    PAGES_WITHOUT_FOOTER = {
        "https://www.sportbenefit.eu/en-cy/facilities",
    }

    LOGO_SELECTOR = (
        "header img[alt*='sportbenefit' i], "
        "header a[href='/en-cy'] img, "
        "header a[href='/en-cy/'] img, "
        "header a[href='https://www.sportbenefit.eu/en-cy'] img"
    )

    TABLE_FILTER_BUTTON_CSS = "button.facilities-table-filter__button"
    GENERIC_FILTER_BUTTON_XPATH = "//button[contains(.,'Filter') or .//span[contains(.,'Filter')]]"
    FILTER_MODAL_ROOT_CSS = ".modal-container.map-filter-modal"
    FILTER_MODAL_APPLY_XPATH = (
        "//div[contains(@class,'map-filter-modal')]"
        "//button[.//span[normalize-space()='Apply'] or normalize-space()='Apply']"
    )

    INTERNAL_IMAGE_HOSTS = {
        "www.sportbenefit.eu",
        "sportbenefit.eu",
    }

    INTERNAL_PAGE_HOSTS = INTERNAL_IMAGE_HOSTS
    INTERNAL_PAGE_PATH_PREFIX = "/en-cy"
    SKIP_HREF_PREFIXES = ("mailto:", "tel:", "javascript:", "#")
    SKIP_PATH_PARTS = ("/_nuxt/",)
    SKIP_EXTENSIONS = (
        ".js",
        ".css",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".svg",
        ".ico",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".map",
        ".xml",
        ".pdf",
        ".zip",
    )

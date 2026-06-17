# -*- coding: utf-8 -*-
import allure
import pytest

from pages.new_web_site_sb.live_api_contract_sb import LiveApiContractSb


pytestmark = [pytest.mark.live_api]


@allure.feature("SB Live API Contract")
@allure.severity("Critical")
@pytest.mark.parametrize("endpoint_path", LiveApiContractSb.CONTACT_ENDPOINTS)
def test_contact_post_contract_live_staging_sb(request, endpoint_path):
    page = LiveApiContractSb()
    page.check_contact_post_contract_live_staging(request, endpoint_path)

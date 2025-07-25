import pytest
from src.base_scraper import BASE_URL

import requests

session = requests.Session()


@pytest.mark.integration
def test_scraper_request():
    response = session.get(BASE_URL)

    assert response.status_code == 200

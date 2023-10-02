from typing import Optional
from contextlib import nullcontext as does_not_raise

import pytest
from unittest.mock import Mock
import requests

from src.base.scraping import BaseScraper

from exceptions import InvalidResponse




class TestBaseScraper:

    status_200_url = 'https://www.google.com/'
    status_404_url = 'https://www.google.com/some/strange/route'
    invalid_url = 'https://a123123sdasd.com/'
    
    @pytest.mark.parametrize(
        "request_url, with_session, expection, headers",
        [
            (status_200_url, False, does_not_raise(), None),
            (status_200_url, True, does_not_raise(), {'user-agent': 'something'}),

            (12345, False, pytest.raises(TypeError), None),
            ([status_200_url], False, pytest.raises(TypeError), None),

            (status_200_url, False, pytest.raises(TypeError), 12345),
            (status_200_url, False, pytest.raises(TypeError), '123545'),
            (status_200_url, False, pytest.raises(TypeError), [{'user-agent': 'something'}]),

            (invalid_url, False, pytest.raises(requests.exceptions.ConnectionError), None),
            (status_404_url, False, pytest.raises(InvalidResponse), None),


        ]
    )
    def test_get_response(self, scraper, request_url: str, with_session: bool, expection, headers:Optional[dict]) -> requests.Response:
        with expection:
            result = scraper._get_response(request_url, with_session, headers)
            assert isinstance(result, requests.Response)
            assert result.status_code == 200

    def test_get_response_text(self, scraper):
        result = scraper._get_response_text(
            self.status_200_url, False
        )
        assert isinstance(result, str)

    def test_get_categories(self, scraper, monkeypatch, categories):
        monkeypatch.setattr(scraper, '_get_response_text', lambda url: '<html>...<html>')
        assert scraper.get_categories() == categories



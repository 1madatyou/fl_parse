import pytest
from unittest.mock import Mock
import time

import bs4

from src.base.items import Category
from src.base.scraping import BaseScraper


@pytest.fixture
def categories():
    categories = [
        Category("IT", "www.test.com/it"),
        Category("Management", "www.test.com/management"),
        Category("3D", "www.test.com/3d"),
    ]
    return categories


@pytest.fixture
def parser(monkeypatch, categories):
    mock_parser = Mock()
    monkeypatch.setattr(mock_parser, "parse_categories", lambda self: categories)
    return mock_parser


@pytest.fixture()
def scraper(parser):
    scraper = BaseScraper(parser)
    scraper.base_url = "http://www.example.com/"
    scraper.category_route = "/category"
    return scraper


@pytest.fixture
def raw_html():
    raw_html = """

    <html>
        <div class="item_list">
            <div class="item">
                <ul>
                    <li class="name"></li>
                    <li class="description"></li>
                    <li class="something"></li>
                </ul>
            </div>
            <div class="item">
                <ul>
                    <li class="name"></li>
                    <li class="description"></li>
                    <li class="something"></li>
                </ul>
            </div>
            <div class="item">
                <ul>
                    <li class="name"></li>
                    <li class="description"></li>
                    <li class="something"></li>
                </ul>
            </div>
            <div class="item">
                <ul>
                    <li class="name"></li>
                    <li class="description"></li>
                    <li class="something"></li>
                </ul>
            </div>
        </div>
    </html>
"""
    return raw_html


@pytest.fixture
def soup(raw_html):
    soup = bs4.BeautifulSoup(raw_html, "html.parser")
    return soup


@pytest.fixture
def bs4_tag_list(soup):
    tag_list = soup.find_all("div", {"class": "item"})
    return tag_list


@pytest.fixture
def bs4_tag(bs4_tag_list):
    return bs4_tag_list[0]

from contextlib import nullcontext as does_not_raise
from typing import List

import pytest
import bs4

from src.base.parsing import (
    BaseItemParser,
    BaseItemFieldParser,
    BaseHTMLParser

)

@pytest.fixture
def raw_html():
    raw_html = '''

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
'''
    return raw_html

@pytest.fixture
def soup(raw_html):
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    return soup

@pytest.fixture
def bs4_tag_list(soup):
    tag_list = soup.find_all('div', {'class': 'item'})
    return tag_list

@pytest.fixture
def bs4_tag(bs4_tag_list):
    return bs4_tag_list[0]

@pytest.fixture
def item_parser():
    item_parser = BaseItemParser()
    item_parser.name = ItemFieldName()
    item_parser.description = ItemFieldDescription()
    return item_parser

# Pseudo classes for nest inside BaseItemParser
class ItemFieldName(BaseItemFieldParser):
    def parse(self) -> str:
        return "Parsed name"

class ItemFieldDescription(BaseItemFieldParser):
    def parse(self) -> str:
        return "Parsed description"
    
class HTMLParser(BaseHTMLParser):
    
    def _get_order_list(self) -> List:
        pass
    
    def parse_categories():
        pass

class TestBaseItemParser:

    @pytest.mark.parametrize(
        'item, expectation',
        [
            ('bs4_tag', does_not_raise()),
            (1234, pytest.raises(TypeError)),
            ('asdf', pytest.raises(TypeError)),
        ]
    )
    def test_set_item(self, item, expectation, item_parser, request):
        with expectation:
            if item in ('bs4_tag'):
                item = request.getfixturevalue(item)

            assert item_parser.set_item(item) == None
            assert item_parser.item == item
        
    def test_parse_item(self, item_parser, bs4_tag):
        item_parser.set_item(bs4_tag)
        parsed_item = item_parser.parse_item()
        assert isinstance(parsed_item, dict)
        if len(parsed_item):
            assert all(isinstance(key, str) for key in parsed_item.keys())

class TestBaseHTMLParser():

    @pytest.fixture
    def parser(self, item_parser):
        parser = HTMLParser(item_parser)
        return parser
        
    ### TESTS




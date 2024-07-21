from contextlib import nullcontext as does_not_raise
from typing import List

import pytest
import bs4

from src.base.parsing import BaseItemParser, BaseItemFieldParser, BaseHTMLParser

from exceptions import EmptyPageException


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


# HTMLParser Implementation
class HTMLParser(BaseHTMLParser):

    def _get_order_list(self) -> List:
        pass

    def parse_categories():
        pass


class TestBaseItemParser:

    @pytest.mark.parametrize(
        "item, expectation",
        [
            ("bs4_tag", does_not_raise()),
            (1234, pytest.raises(TypeError)),
            ("asdf", pytest.raises(TypeError)),
        ],
    )
    def test_set_item(self, item, expectation, item_parser, request):
        with expectation:
            if item in ("bs4_tag"):
                item = request.getfixturevalue(item)

            assert item_parser.set_item(item) == None
            assert item_parser.item == item

    def test_parse_item(self, item_parser, bs4_tag):
        item_parser.set_item(bs4_tag)
        parsed_item = item_parser.parse_item()
        assert isinstance(parsed_item, dict)
        if len(parsed_item):
            assert all(isinstance(key, str) for key in parsed_item.keys())


class TestBaseHTMLParser:

    @pytest.fixture
    def parser(self, item_parser):
        parser = HTMLParser(item_parser)
        return parser

    @pytest.mark.parametrize(
        "order_list, expectation",
        [
            ("bs4_tag_list", does_not_raise()),
            ("test_string", pytest.raises(TypeError)),
            (12345, pytest.raises(TypeError)),
            (None, pytest.raises(TypeError)),
            ([], pytest.raises(EmptyPageException)),
        ],
    )
    def test_parse(self, order_list, expectation, monkeypatch, parser, request):
        with expectation:
            if order_list in ("bs4_tag_list",):
                order_list = request.getfixturevalue(order_list)
            monkeypatch.setattr(parser, "_get_order_list", lambda: order_list)

            for item in parser.parse():
                assert isinstance(item, dict)

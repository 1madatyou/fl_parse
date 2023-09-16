import unittest
from unittest.mock import MagicMock

from bs4 import BeautifulSoup


from freelance_services.weblancer.parsing import (
    WeblancerItemParser,
    WeblancerPageParser
) 
from freelance_services.weblancer import URL


class TestWeblancerItemParser(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:

        html = '<div><span class="title"><a href="/freelance/test">Test Order</a></span><div class="text-rich"><p>Description paragraph 1</p><p>Description paragraph 2</p></div></div>'
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('div')
        self.parser = WeblancerItemParser(item)

        super().__init__(methodName)

    def test_parse_item_returns_dict(self):
        expected_result = {'name': 'Test Order', 'description': 'Description paragraph 1 Description paragraph 2', 'href': URL + '/freelance/test'}

        result = self.parser.parsed_item

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
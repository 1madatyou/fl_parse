import pytest

from src.base.processing import BaseDataProcessor
from src.base.items import Category

@pytest.fixture
def data_processor(scraper):
    return BaseDataProcessor(scraper)

class TestBaseDataProcessor:

    @pytest.mark.parametrize(
        'category, page_num',
        [
            (Category('SomeCat', '/route'), 10),
        ]
    )
    def test_assemble_url(self, category, page_num, data_processor):
        res = data_processor._assemble_url(category, page_num)
        assert isinstance(res, str)

        parts = (data_processor.scraper.base_url, category.route, page_num)
        assert [str(part) in res for part in parts]
    

    # @pytest.mark.parametrize(
    #     'category, count_of_orders',
    #     [
    #         (Category('SomeCat', 'www.example.com'), 20),

    #     ]
    # )
    # def test_get_data_by_category(self, category, count_of_orders, data_processor, monkeypatch, raw_html):
    #     monkeypatch.setattr(data_processor.scraper, '_get_response_text', lambda: raw_html)
    #     monkeypatch.setattr(data_processor.scraper.parser, 'parse', lambda: {'name': 1} )
    #     result = data_processor._get_data_by_category(category, count_of_orders)
    #     assert isinstance(result, list)


        
        
        



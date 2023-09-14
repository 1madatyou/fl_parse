import unittest
from base import BaseScraper
from exceptions import InvalidStatusCode


class TestBaseScraperMethods(unittest.TestCase):

    

    def test_get_response_text_return_str(self):
        request_url = 'https://example.com'

        result = BaseScraper._get_response_text(request_url)

        self.assertEqual(type(result), str)
    
    def test_get_response_raises_invalid_status_code_error(self):
        request_url = 'https://example.com/404'

        self.assertRaises(InvalidStatusCode, BaseScraper._get_response_text, request_url)

    def test_get_response_raises_value_error(self):
        self.assertRaises(ValueError, BaseScraper._get_response_text, [])
        self.assertRaises(ValueError, BaseScraper._get_response_text, (1,))
        self.assertRaises(ValueError, BaseScraper._get_response_text, 1)
        self.assertRaises(ValueError, BaseScraper._get_response_text, 1.1234)
                          



if __name__ == '__main__':
    unittest.main()



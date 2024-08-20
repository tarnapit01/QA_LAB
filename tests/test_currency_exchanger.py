import unittest

import os,sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from unittest.mock import patch
from util import get_mock_currency_api_response
from source.currency_exchanger import CurrencyExchanger

class TestCurrency (unittest.TestCase):
    
    def setUp(self):
        self.crex = CurrencyExchanger(base_currency="THB", target_currency="KRW")
        self.mock_api_response = get_mock_currency_api_response()
        
    def tearDown(self):
        print("\nTearDown Called...\n")
        
    @patch("source.currency_exchanger.requests")
    def test_get_currency_rate(self, mock_request):
        print("test_get_currency Called...\n")
        mock_request.get.return_value = get_mock_currency_api_response()
        
        self.crex.get_currency_rate()
        
        mock_request.get.assert_called_once()
        
        mock_request.get.assert_called_with("https://coc-kku-bank.com/foreign-exchange",
            params={'from': 'THB', 'to': 'KRW'})
        
        self.assertIsNotNone(self.crex.api_response)
        self.assertEqual(self.crex.api_response,self.mock_api_response.json())

    @patch("source.currency_exchanger.requests")
    def test_currency_exchange(self, mock_request):
        print("test_currency_exchange Called...\n")
        mock_request.get.return_value = get_mock_currency_api_response()

        result = self.crex.currency_exchange(100)
        
        mock_request.get.assert_called_once()
        
        mock_request.get.assert_called_with("https://coc-kku-bank.com/foreign-exchange",
            params={'from': 'THB', 'to': 'KRW'})
        
        self.assertIsNotNone(self.crex.api_response)
        self.assertEqual(self.crex.api_response,self.mock_api_response.json())
        self.assertEqual(result,3869.0)  
        
if __name__ == '__main__':
    unittest.main()
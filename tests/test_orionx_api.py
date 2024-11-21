import unittest

from unittest.mock import patch, MagicMock
from src.apis.orionx_api import OrionxAPI

class TestOrionxAPI(unittest.TestCase):

    def setUp(self):
        self.api_key = "fake_api_key"
        self.api_secret = "fake_api_secret"
        self.orionx_api = OrionxAPI(self.api_key, self.api_secret)

    def test_instance_creation(self):
        self.assertEqual(self.orionx_api.api_key, self.api_key)
        self.assertEqual(self.orionx_api.api_secret, self.api_secret)

    def test_set_headers(self):
        body = '{"query": "fake_query"}'
        with patch("src.apis.orionx_api.OrionxAPI.hmac_sha512", return_value="fake_signature"):
            headers = self.orionx_api.set_headers(body)
            self.assertIn("Content-Type", headers)
            self.assertIn("X-ORIONX-TIMESTAMP", headers)
            self.assertIn("X-ORIONX-APIKEY", headers)
            self.assertIn("X-ORIONX-SIGNATURE", headers)
            self.assertEqual(headers["X-ORIONX-APIKEY"], self.api_key)

    @patch("src.apis.orionx_api.requests.post")
    def test_get_currency_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        {
            "data": {
                "_id": "wallet123",
                "balance": "0.5",
                "availableBalance": "0.3",
                "unconfirmedBalance": "0.2"
            }
        }'''
        mock_post.return_value = mock_response

        result = self.orionx_api.get_currency("BTC")

        self.assertIsInstance(result, dict)
        self.assertIn("data", result)
        self.assertEqual(result["data"]["_id"], 'wallet123')
        self.assertEqual(result["data"]["balance"], "0.5")
        self.assertEqual(result["data"]["availableBalance"], "0.3")
        self.assertEqual(result["data"]["unconfirmedBalance"], "0.2")

    @patch("src.apis.orionx_api.requests.post")
    def test_get_currency_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = '{"error": "Unauthorized"}'
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.orionx_api.get_currency("BTC")

        self.assertIn("Error: 401", str(context.exception))

    @patch("src.apis.orionx_api.requests.post")
    def test_get_currencyTransformFactor_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        {
            "data": {
                "factor": 1000
            }
        }'''
        mock_post.return_value = mock_response

        result = self.orionx_api.get_currencyTransformFactor("BTC", "CLP")

        self.assertIsInstance(result, dict)
        self.assertIn("data", result)
        self.assertEqual(result["data"]["factor"], 1000)

if __name__ == "__main__":
    unittest.main()
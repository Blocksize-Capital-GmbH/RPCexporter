import unittest

from exporter.jsonRPCRequest import JsonRPCRequest


class TestJsonRPCConstructURL(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://rpc-mainnet.supra.com/rpc/v1"

    def test_construct_url_block_height_1(self):
        """Test URL construction for block height 1."""
        method = "block/height/{height}"
        params = {"height": 1, "with_finalized_transactions": "false"}
        expected_url = "https://rpc-mainnet.supra.com/rpc/v1/block/height/1?with_finalized_transactions=false"
        constructed_url = JsonRPCRequest.construct_url(self.base_url, method, params)
        self.assertEqual(constructed_url, expected_url)

    def test_construct_url_block_height_2(self):
        """Test URL construction for block height 2."""
        method = "block/height/{height}"
        params = {"height": 2, "with_finalized_transactions": "false"}
        expected_url = "https://rpc-mainnet.supra.com/rpc/v1/block/height/2?with_finalized_transactions=false"
        constructed_url = JsonRPCRequest.construct_url(self.base_url, method, params)
        self.assertEqual(constructed_url, expected_url)


if __name__ == "__main__":
    unittest.main()

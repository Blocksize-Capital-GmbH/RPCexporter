import unittest

from exporter.jsonRPCRequest import JsonRPCRequest


class TestJsonRPCIntegrationSupra(unittest.TestCase):
    rpc_url = "https://rpc-mainnet.supra.com/rpc/v1"

    def test_integration_get_request(self):
        """Test a single GET request for the Supra RPC."""
        request = JsonRPCRequest(
            method="block/height/{height}",
            params={"height": 1, "with_finalized_transactions": "false"},
            use_get=True,
        )
        response = JsonRPCRequest.send(
            rpc_url=self.rpc_url,
            rpc_requests=request,
        )

        self.assertEqual(len(response), 1)
        self.assertTrue(response[0].is_successful())
        self.assertIsInstance(response[0].result, dict)

        # Access the nested 'height' key inside 'header'
        self.assertIn("header", response[0].result)
        self.assertIn("height", response[0].result["header"])
        self.assertEqual(response[0].result["header"]["height"], 1)

    def test_integration_get_batch_request(self):
        """Test a batch GET request for multiple block heights."""
        requests = [
            JsonRPCRequest(
                method="block/height/{height}",
                params={"height": 1, "with_finalized_transactions": "false"},
                use_get=True,
            ),
            JsonRPCRequest(
                method="block/height/{height}",
                params={"height": 2, "with_finalized_transactions": "false"},
                use_get=True,
            ),
        ]
        responses = JsonRPCRequest.send(
            rpc_url=self.rpc_url,
            rpc_requests=requests,
        )

        print(f"Raw Batch GET Responses: {responses}")

        self.assertEqual(len(responses), 2)

        # Validate first GET response
        self.assertTrue(responses[0].is_successful())
        self.assertIsInstance(responses[0].result, dict)
        self.assertIn("header", responses[0].result)
        self.assertIn("height", responses[0].result["header"])
        self.assertEqual(responses[0].result["header"]["height"], 1)

        # Validate second GET response
        self.assertTrue(responses[1].is_successful())
        self.assertIsInstance(responses[1].result, dict)
        self.assertIn("header", responses[1].result)
        self.assertIn("height", responses[1].result["header"])
        self.assertEqual(responses[1].result["header"]["height"], 2)


if __name__ == "__main__":
    unittest.main()

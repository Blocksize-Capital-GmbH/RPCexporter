import unittest
from typing import List
from unittest.mock import MagicMock, patch

from exporter.jsonRPCRequest import JsonRPCRequest
from exporter.jsonRPCResponse import JsonRPCResponse


class TestJsonRPCRequestStandardizeResponse(unittest.TestCase):
    @patch("requests.post")
    def test_standardize_response_batch(self, mock_post):
        """Test batch mode handling with two block requests."""
        # Mock response from the Supra public RPC
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [
            {"result": {"height": 12345}},
            {"result": {"height": 12346}},
        ]

        # Create batch requests
        requests: list[JsonRPCRequest] = [
            JsonRPCRequest(method="block", params={"height": 12345}),
            JsonRPCRequest(method="block", params={"height": 12346}),
        ]

        # Execute the batched RPC call
        responses: List[JsonRPCResponse] = JsonRPCRequest.send(
            rpc_url="https://rpc-testnet.supra.com/rpc/v1",
            rpc_requests=requests,
        )

        # Assertions
        self.assertEqual(len(responses), 2)
        self.assertTrue(responses[0].is_successful())
        self.assertEqual(responses[0].result["height"], 12345)
        self.assertTrue(responses[1].is_successful())
        self.assertEqual(responses[1].result["height"], 12346)

    @patch("requests.post")
    def test_standardize_response_serial(self, mock_post):
        """Test serial mode handling with two block requests."""
        # Mock response for the first request
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {"result": {"height": 12345}}),
            MagicMock(status_code=200, json=lambda: {"result": {"height": 12346}}),
        ]

        # Create individual requests
        request1 = JsonRPCRequest(method="block", params={"height": 12345})
        request2 = JsonRPCRequest(method="block", params={"height": 12346})

        # Execute the requests serially
        response1 = JsonRPCRequest.send(
            rpc_url="https://rpc-testnet.supra.com/rpc/v1",
            rpc_requests=request1,
        )
        response2 = JsonRPCRequest.send(
            rpc_url="https://rpc-testnet.supra.com/rpc/v1",
            rpc_requests=request2,
        )

        # Assertions for the first request
        self.assertEqual(len(response1), 1)
        self.assertTrue(response1[0].is_successful())
        self.assertEqual(response1[0].result["height"], 12345)

        # Assertions for the second request
        self.assertEqual(len(response2), 1)
        self.assertTrue(response2[0].is_successful())
        self.assertEqual(response2[0].result["height"], 12346)

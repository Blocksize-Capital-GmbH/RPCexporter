import unittest
from unittest.mock import patch

from exporter.jsonRPCRequest import JsonRPCRequest


class TestJsonRPCRequest(unittest.TestCase):
    @patch("requests.post")
    def test_post_single_request(self, mock_post):
        """Test a single POST request."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"result": 42}

        request = JsonRPCRequest(method="getBalance", params=["address"], use_get=False)
        responses = JsonRPCRequest.send(
            rpc_url="http://94.75.194.166:27000/rpc/v1",
            rpc_requests=request,
        )

        self.assertEqual(len(responses), 1)
        self.assertTrue(responses[0].is_successful())
        self.assertEqual(responses[0].result, 42)

    @patch("requests.post")
    def test_post_request_failure(self, mock_post):
        """Test POST request handling of failure."""
        mock_post.return_value.status_code = 500
        mock_post.return_value.reason = "Internal Server Error"  # Explicitly set the reason
        mock_post.return_value.json.return_value = {
            "error": {"code": -32000, "message": "Internal server error"}
        }

        request = JsonRPCRequest(method="getBalance", params=["address"], use_get=False)
        responses = JsonRPCRequest.send(
            rpc_url="http://example.com/rpc/v1", rpc_requests=request
        )

        self.assertEqual(len(responses), 1)
        self.assertFalse(responses[0].is_successful())
        self.assertEqual(
            responses[0].error,
            {"code": 500, "message": "Internal Server Error"},  # Match HTTP error details
        )

    @patch("requests.get")
    def test_get_request_failure(self, mock_get):
        """Test GET request handling of failure."""
        mock_get.return_value.status_code = 404
        mock_get.return_value.reason = "Not Found"
        mock_get.return_value.json.return_value = {
            "error": {"code": -32601, "message": "Method not found"}
        }

        request = JsonRPCRequest(method="block", params={"height": 12345}, use_get=True)
        responses = JsonRPCRequest.send("http://example.com/rpc/v1", request)

        self.assertEqual(len(responses), 1)
        self.assertFalse(responses[0].is_successful())
        self.assertEqual(
            responses[0].error,
            {"code": 404, "message": "Not Found"},  # Match the HTTP error details
        )

    @patch("requests.get")
    def test_get_single_request(self, mock_get):
        """Test a single GET request."""
        # Mock the GET request response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"block": "data"}

        # Create a request and send it
        request = JsonRPCRequest(method="block", params={"height": 12345}, use_get=True)
        responses = JsonRPCRequest.send(
            rpc_url="http://94.75.194.166:27000/rpc/v1",
            rpc_requests=request,
        )

        # Assertions
        self.assertEqual(len(responses), 1)
        self.assertTrue(responses[0].is_successful())
        self.assertEqual(responses[0].result, {"block": "data"})

    @patch("requests.post")
    def test_send_single(self, mock_post):
        """Test sending a single JSON-RPC POST request."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"result": 42}

        request = JsonRPCRequest(method="getSlot")
        responses = JsonRPCRequest.send("http://example.com/rpc/v1", request)

        self.assertEqual(len(responses), 1)
        self.assertTrue(responses[0].is_successful())
        self.assertEqual(responses[0].result, 42)

    @patch("requests.post")
    def test_send_batch(self, mock_post):
        """Test sending a batch JSON-RPC POST request."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [
            {"result": 42},
            {"error": {"code": -32601, "message": "Method not found"}},
        ]

        request1 = JsonRPCRequest(method="getSlot")
        request2 = JsonRPCRequest(method="invalidMethod")
        responses = JsonRPCRequest.send("http://example.com/rpc/v1", [request1, request2])

        self.assertEqual(len(responses), 2)
        self.assertTrue(responses[0].is_successful())
        self.assertEqual(responses[0].result, 42)
        self.assertFalse(responses[1].is_successful())
        self.assertEqual(responses[1].error, {"code": -32601, "message": "Method not found"})


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch

from exporter.jsonRPCRequest import JsonRPCRequest
from exporter.jsonRPCResponse import JsonRPCResponse
from exporter.rpcExporter import RPCExporter
from exporter.rpcExporterConfig import ExporterConfig


class TestRPCExporter(unittest.TestCase):
    @patch.dict(
        "os.environ",
        {
            "SOLANA_RPC_URL": "http://localhost:8899",
            "SOLANA_PUBLIC_RPC_URL": "https://api.testnet.solana.com",
            "EXPORTER_PORT": "7896",
            "POLL_INTERVAL": "10",
            "VOTE_PUBKEY": "6jJK69aeuLbVnM6nUKnmMMwyQG2rNjKNFrfM459kfAdL",
            "VALIDATOR_PUBKEY": "4EKxPYXmBha7ADnZphFFC13RaKNYLZCiQPKuSV8YWRZc",
            "STAKE_ACCOUNT_PUBKEY": "J1XibEzMT4pAhu6yBFs2EdsK8nSrVcCao3Ut4eYytzmw",
            "VERSION": "0.1.0",
            "LABEL": "test",
        },
    )
    @patch("exporter.jsonRPCRequest.JsonRPCRequest.send")
    def test_rpc_call(self, mock_send):
        mock_send.return_value = [JsonRPCResponse(result=42)]
        exporter = RPCExporter("solana", "fromEnv")
        response = exporter._rpc_call(JsonRPCRequest("getSlot"))
        self.assertEqual(response[0].result, 42)


class TestJsonRPCResponse(unittest.TestCase):
    def test_is_successful(self):
        response = JsonRPCResponse(result=42)
        self.assertTrue(response.is_successful())

    def test_log_error(self):
        logger = MagicMock()
        response = JsonRPCResponse(error={"message": "An error occurred"})
        response.log_error(logger, "getSlot")
        logger.error.assert_called_with(
            "RPC call to getSlot failed: {'message': 'An error occurred'}"
        )


class TestJsonRPCRequest(unittest.TestCase):
    @patch("requests.post")
    def test_send_single(self, mock_post):
        """Test sending a single JSON-RPC request."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [
            {"result": 42}
        ]  # Use a list for batch response

        request = JsonRPCRequest("getSlot")
        response = JsonRPCRequest.send("http://localhost:8899", request)

        self.assertIsInstance(response[0], JsonRPCResponse)
        self.assertEqual(response[0].result, 42)


class TestExporterConfig(unittest.TestCase):
    def test_init(self):
        config = ExporterConfig.init(
            {
                "rpc_url": "SOLANA_RPC_URL",
                "exporter_port": "EXPORTER_PORT",
                "poll_interval": "POLL_INTERVAL",
            }
        )
        self.assertIn("rpc_url", config._config)
        self.assertIsNone(config.rpc_url)

    def test_load_from_env(self):
        with patch.dict(
            "os.environ",
            {
                "SOLANA_RPC_URL": "http://localhost:8899",
                "EXPORTER_PORT": "7896",
                "POLL_INTERVAL": "10",
            },
        ):
            config = ExporterConfig.init(
                {
                    "rpc_url": "SOLANA_RPC_URL",
                    "exporter_port": "EXPORTER_PORT",
                    "poll_interval": "POLL_INTERVAL",
                }
            )
            config.load(
                "fromEnv",
                {
                    "rpc_url": "SOLANA_RPC_URL",
                    "exporter_port": "EXPORTER_PORT",
                    "poll_interval": "POLL_INTERVAL",
                },
            )
            self.assertEqual(config.rpc_url, "http://localhost:8899")
            self.assertEqual(config.exporter_port, "7896")
            self.assertEqual(config.poll_interval, "10")

    def test_load_from_file(self):
        mock_file_content = """
        SOLANA_RPC_URL=http://localhost:8899
        EXPORTER_PORT=7896
        POLL_INTERVAL=10
        """
        with patch("builtins.open", unittest.mock.mock_open(read_data=mock_file_content)):
            config = ExporterConfig.init(
                {
                    "rpc_url": "SOLANA_RPC_URL",
                    "exporter_port": "EXPORTER_PORT",
                    "poll_interval": "POLL_INTERVAL",
                }
            )
            config.load(
                "fromFile",
                {
                    "rpc_url": "SOLANA_RPC_URL",
                    "exporter_port": "EXPORTER_PORT",
                    "poll_interval": "POLL_INTERVAL",
                },
                "dummy_path",
            )
            self.assertEqual(config.rpc_url, "http://localhost:8899")
            self.assertEqual(config.exporter_port, "7896")
            self.assertEqual(config.poll_interval, "10")

    def test_validate(self):
        config = ExporterConfig.init(
            {
                "rpc_url": "SOLANA_RPC_URL",
                "exporter_port": "EXPORTER_PORT",
                "poll_interval": "POLL_INTERVAL",
            }
        )
        with self.assertRaises(ValueError):
            config.validate(
                {
                    "rpc_url": "SOLANA_RPC_URL",
                    "exporter_port": "EXPORTER_PORT",
                    "poll_interval": "POLL_INTERVAL",
                }
            )

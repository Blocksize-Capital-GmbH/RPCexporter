import logging
from unittest.mock import patch

from exporter.jsonRPCResponse import JsonRPCResponse


def test_response_validity():
    valid_response = JsonRPCResponse(result={"value": 42})
    invalid_response = JsonRPCResponse()

    assert valid_response.is_valid()
    assert not invalid_response.is_valid()


def test_response_success():
    successful_response = JsonRPCResponse(result={"value": 42})
    failed_response = JsonRPCResponse(error={"code": -32601, "message": "Method not found"})

    assert successful_response.is_successful()
    assert not failed_response.is_successful()


@patch("logging.Logger.error")
def test_log_error(mock_logger_error):
    logger = logging.getLogger("test_logger")
    response = JsonRPCResponse(error={"code": -32601, "message": "Method not found"})
    response.log_error(logger, "getBalance")

    mock_logger_error.assert_called_once_with(
        "RPC call to getBalance failed: {'code': -32601, 'message': 'Method not found'}"
    )

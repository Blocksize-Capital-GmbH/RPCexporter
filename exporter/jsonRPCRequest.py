import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode

import requests

from exporter.jsonRPCResponse import JsonRPCResponse


@dataclass
class JsonRPCRequest:
    def __init__(
        self, method: str, params: Optional[Union[List, Dict]] = None, use_get: bool = False
    ) -> None:
        self.method: str = method
        self.params = params
        self.use_get: bool = use_get

    def to_json(self) -> dict:
        """
        Convert the JsonRPCRequest instance to a dictionary suitable for JSON serialization.
        """
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "method": self.method,
            "params": (
                self.params if self.params is not None else []
            ),  # Ensure params is always a list
        }

    @staticmethod
    def construct_url(base_url: str, method: str, params: Optional[dict]) -> str:
        """
        Construct a URL for a GET request with path-based and query parameters.

        :param base_url: The base URL of the RPC endpoint.
        :param method: The RPC method to call.
        :param params: Parameters for the method (if any).
        :return: The constructed URL.
        """
        # Start with the base URL and method
        url = f"{base_url.rstrip('/')}/{method}"

        if params:
            # Replace placeholders in the method with actual values
            for key, value in params.items():
                placeholder = f"{{{key}}}"
                if placeholder in url:
                    url = url.replace(placeholder, str(value))

            # Add any remaining parameters as query parameters
            query_params = {k: v for k, v in params.items() if f"{{{k}}}" not in method}
            if query_params:
                url += "?" + urlencode(query_params)

        return url

    @staticmethod
    def send(
        rpc_url: str,
        rpc_requests: Union["JsonRPCRequest", List["JsonRPCRequest"]],
        logger: Optional[logging.Logger] = None,
    ) -> List["JsonRPCResponse"]:
        """
        Send a JSON-RPC request using either POST or GET.

        :param rpc_url: Base URL for the RPC server.
        :param rpc_requests: Single or list of JsonRPCRequest instances.
        :param logger: Logger instance for logging errors.
        :return: List of JsonRPCResponse objects.
        """
        is_single: bool = isinstance(rpc_requests, JsonRPCRequest)
        requests_list: List[JsonRPCRequest] = [rpc_requests] if is_single else rpc_requests
        responses = []

        try:
            if any(req.use_get for req in requests_list):
                # Handle GET requests individually
                for req in requests_list:
                    if req.use_get:
                        constructed_url = JsonRPCRequest.construct_url(
                            rpc_url, req.method, req.params
                        )
                        response = requests.get(constructed_url, timeout=15)
                        if response.status_code == 200:
                            responses.append(
                                JsonRPCResponse(result=response.json(), error=None)
                            )
                        else:
                            responses.append(
                                JsonRPCResponse(
                                    result=None,
                                    error={
                                        "code": response.status_code,
                                        "message": response.reason,
                                    },
                                )
                            )
                    else:
                        raise ValueError("Batched GET requests are not supported.")
            else:
                # Handle POST requests in batch mode
                print(f"requests_list: {[req.params for req in requests_list]}")
                batch_requests = [req.to_json() for req in requests_list]
                print(f"processed batched requests: {batch_requests}")
                response: requests.Response = requests.post(
                    rpc_url, json=batch_requests, timeout=15
                )

                if response.status_code == 200:
                    raw_responses = response.json()
                    responses.extend(JsonRPCRequest.standardize_response(raw_responses))
                else:
                    error_response = {"code": response.status_code, "message": response.reason}
                    responses.extend(
                        JsonRPCResponse(result=None, error=error_response)
                        for _ in requests_list
                    )

        except requests.RequestException as e:
            if logger:
                logger.error(f"Failed to send JSON-RPC request: {e}")
            responses.extend(
                JsonRPCResponse(result=None, error={"message": str(e)}) for _ in requests_list
            )

        return responses

    @staticmethod
    def standardize_response(raw_responses) -> List["JsonRPCResponse"]:
        """
        Standardize the output of raw JSON-RPC responses to always be a list of JsonRPCResponse.

        :param raw_responses: Raw responses from the JSON-RPC server (dict or list of dicts).
        :return: List of standardized JsonRPCResponse objects.
        """
        if isinstance(raw_responses, dict):
            # Single response case
            return [
                JsonRPCResponse(
                    result=raw_responses.get(
                        "result", raw_responses
                    ),  # Use raw response if no "result"
                    error=raw_responses.get("error"),
                )
            ]
        elif isinstance(raw_responses, list):
            # Batch response case
            return [
                JsonRPCResponse(
                    result=response.get("result", response),  # Use raw response if no "result"
                    error=response.get("error"),
                )
                for response in raw_responses
            ]
        else:
            # Unexpected response format
            raise ValueError(f"Unexpected raw response format: {type(raw_responses)}")

import logging
from typing import List

from prometheus_client import CollectorRegistry

from exporter.jsonRPCRequest import JsonRPCRequest
from exporter.jsonRPCResponse import JsonRPCResponse
from exporter.rpcExporterConfig import ExporterConfig
from exporter.rpcExporterDefaults import CONFIG_KEYS


class RPCExporter:
    """Base class for exporting metrics from an RPC-compatible network."""

    def __init__(self, network: str, config_source: str, config_file: str = None):
        self.network: str = network.lower()
        self.config: ExporterConfig = ExporterConfig.init(CONFIG_KEYS[self.network])
        self.config.load(config_source, CONFIG_KEYS[self.network], file_path=config_file)

        self.rpc_url: str | None = self.config.rpc_url or self._raise_config_error(
            key="rpc_url"
        )
        self.public_rpc_url: str | None = (
            self.config.public_rpc_url or self._raise_config_error(key="public_rpc_url")
        )

        self.poll_interval = int(
            self.config.poll_interval or self._raise_config_error("poll_interval")
        )
        self.exporter_port = int(
            self.config.exporter_port or self._raise_config_error("exporter_port")
        )

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        self.registry = CollectorRegistry()

    def _raise_config_error(self, key: str) -> None:
        """Raise a configuration error for a missing key."""
        raise ValueError(f"Missing configuration key: {key}")

    def _rpc_call(self, request: JsonRPCRequest) -> List[JsonRPCResponse]:
        """Make an individual JSON-RPC call."""
        return JsonRPCRequest.send(
            rpc_url=self.rpc_url, rpc_requests=request, logger=self.logger
        )

    def _batched_rpc_call(self, requests: List[JsonRPCRequest]) -> List[JsonRPCResponse]:
        """Make a batched JSON-RPC call."""
        return JsonRPCRequest.send(
            rpc_url=self.rpc_url, rpc_requests=requests, logger=self.logger
        )

    def setup_metrics(self) -> None:
        """Initialize Prometheus metrics. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement setup_metrics.")

    def collect_metrics(self) -> None:
        """Collect metrics from the node. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement collect_metrics.")

    def start_exporter(self) -> None:
        """Start the Prometheus metrics exporter."""
        import time

        from prometheus_client import start_http_server

        start_http_server(self.exporter_port, registry=self.registry)
        while True:
            self.collect_metrics()
            time.sleep(self.poll_interval)

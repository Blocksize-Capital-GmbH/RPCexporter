import logging
import warnings
from typing import Dict, List, Optional

from prometheus_client import CollectorRegistry

from exporter.jsonRPCRequest import JsonRPCRequest
from exporter.jsonRPCResponse import JsonRPCResponse
from exporter.rpcExporterConfig import ExporterConfig


class RPCExporter:
    """Base class for exporting metrics from an RPC-compatible network.
    
    This class can be initialized in two ways:
    1. Legacy mode: Pass 'network' parameter (deprecated, uses centralized CONFIG_KEYS)
    2. Preferred mode: Pass 'config_keys' and optionally 'required_keys' parameters
    """

    def __init__(
        self,
        config_source: str,
        config_file: Optional[str] = None,
        network: Optional[str] = None,
        config_keys: Optional[Dict[str, str]] = None,
        required_keys: Optional[Dict[str, str]] = None,
    ):
        """Initialize the RPC Exporter.
        
        Args:
            config_source: Configuration source ('fromEnv' or 'fromFile')
            config_file: Path to configuration file (required if config_source='fromFile')
            network: Network name (deprecated, use config_keys instead)
            config_keys: Dictionary mapping config key names to environment variable names
            required_keys: Dictionary of required configuration keys (subset of config_keys)
        
        Example (preferred):
            exporter = RPCExporter(
                config_source="fromEnv",
                config_keys={"rpc_url": "SOLANA_RPC_URL", ...},
                required_keys={"rpc_url": "SOLANA_RPC_URL", ...}
            )
        
        Example (legacy, deprecated):
            exporter = RPCExporter(network="solana", config_source="fromEnv")
        """
        # Handle legacy network parameter
        if network is not None and config_keys is None:
            warnings.warn(
                "Passing 'network' parameter is deprecated. "
                "Please pass 'config_keys' and 'required_keys' instead.",
                DeprecationWarning,
                stacklevel=2
            )
            from exporter.rpcExporterDefaults import CONFIG_KEYS
            self.network = network.lower()
            config_keys = CONFIG_KEYS[self.network]
            # In legacy mode, all keys are required
            required_keys = config_keys
        elif config_keys is None:
            raise ValueError(
                "Either 'network' (deprecated) or 'config_keys' must be provided"
            )
        
        self.config: ExporterConfig = ExporterConfig.init(config_keys)
        self.config.load(config_source, config_keys, file_path=config_file, required_keys=required_keys)

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

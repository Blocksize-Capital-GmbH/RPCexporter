"""Default key definitions for different json RPC implementations.

DEPRECATED: This module is deprecated and maintained only for backward compatibility.
New exporters should define their own configuration keys and pass them directly
to RPCExporter using the config_keys parameter.

Example:
    # Old way (deprecated):
    exporter = RPCExporter(network="solana", config_source="fromEnv")

    # New way (preferred):
    from myexporter.config import ALL_CONFIG_KEYS, REQUIRED_CONFIG_KEYS
    exporter = RPCExporter(
        config_source="fromEnv",
        config_keys=ALL_CONFIG_KEYS,
        required_keys=REQUIRED_CONFIG_KEYS
    )
"""

import warnings

warnings.warn(
    "rpcExporterDefaults.CONFIG_KEYS is deprecated. "
    "Define configuration keys in your exporter implementation instead.",
    DeprecationWarning,
    stacklevel=2
)

# Legacy CONFIG_KEYS kept for backward compatibility
# Note: double_zero_fees_address removed from solana defaults as it should be optional
CONFIG_KEYS: dict[str, dict[str, str]] = {
    "solana": {
        "rpc_url": "SOLANA_RPC_URL",
        "public_rpc_url": "SOLANA_PUBLIC_RPC_URL",
        "exporter_port": "EXPORTER_PORT",
        "poll_interval": "POLL_INTERVAL",
        "vote_pubkey": "VOTE_PUBKEY",
        "validator_pubkey": "VALIDATOR_PUBKEY",
        "version": "VERSION",
        "label": "LABEL",
    },
    "supra": {
        "rpc_url": "SUPRA_RPC_URL",
        "public_rpc_url": "SUPRA_PUBLIC_RPC_URL",
        "validator_log_file": "VALIDATOR_LOG_FILE",
        "exporter_port": "EXPORTER_PORT",
        "poll_interval": "POLL_INTERVAL",
        "smr_validator_pubkey": "SMR_VALIDATOR_PUBKEY",
        "smr_validator_account_pubkey": "SMR_VALIDATOR_ACCOUNT_PUBKEY",
        "network_pubkey": "NETWORK_PUBKEY",
        "consensus_pubkey": "CONSENSUS_PUBKEY",
        "dkg_cg_pubkey": "DKG_CG_PUBKEY",
    },
}

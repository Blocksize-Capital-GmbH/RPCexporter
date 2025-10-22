"""Default key definitions for different json RPC implementations."""

CONFIG_KEYS: dict[str, dict[str, str]] = {
    "solana": {
        "rpc_url": "SOLANA_RPC_URL",
        "public_rpc_url": "SOLANA_PUBLIC_RPC_URL",
        "exporter_port": "EXPORTER_PORT",
        "poll_interval": "POLL_INTERVAL",
        "vote_pubkey": "VOTE_PUBKEY",
        "validator_pubkey": "VALIDATOR_PUBKEY",
        "double_zero_fees_address": "DOUBLE_ZERO_FEES_ADDRESS",
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

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Configurable configuration keys per exporter instance via `config_keys` and `required_keys` parameters
- Support for optional configuration keys (keys that don't need to be validated as required)
- Comprehensive backward compatibility for legacy `network` parameter API
- Automatic detection of legacy positional arguments (`RPCExporter(network, config_source)`)
- Enhanced error messages with context when configuration is missing
- CI pipeline now runs on feature branches matching `feature/**` pattern
- Automatic whitespace fixing in CI pipeline before linting

### Changed
- **Breaking (with deprecation)**: Configuration defaults moved from `RPCExporter` base class to individual exporter implementations
  - Old way: `RPCExporter(network="solana", config_source="fromEnv")`
  - New way: `RPCExporter(config_source="fromEnv", config_keys=ALL_CONFIG_KEYS, required_keys=REQUIRED_CONFIG_KEYS)`
- `RPCExporter.__init__()` signature updated to accept `config_keys` and `required_keys` as primary configuration method
- `ExporterConfig.load()` now accepts optional `required_keys` parameter for validation
- `rpcExporterDefaults.CONFIG_KEYS` marked as deprecated (maintained for backward compatibility)

### Deprecated
- `network` parameter in `RPCExporter.__init__()` (will be removed in future version)
- `rpcExporterDefaults.CONFIG_KEYS` dictionary (define configuration in your exporter instead)
- Legacy positional argument API: `RPCExporter(network, config_source)` (use keyword arguments)

### Fixed
- Trailing whitespace in `rpcExporterDefaults.py`
- Black formatting issues
- All CI linting and testing now passes

### Migration Guide

#### For Exporter Developers
If you're creating a new exporter or updating an existing one:

**Before:**
```python
from exporter.rpcExporter import RPCExporter

class MyExporter(RPCExporter):
    def __init__(self, config_source: str, config_file: Optional[str] = None):
        super().__init__(
            network="mynetwork",  # Deprecated
            config_source=config_source,
            config_file=config_file
        )
```

**After:**
```python
from exporter.rpcExporter import RPCExporter

# Define your configuration keys
REQUIRED_CONFIG_KEYS = {
    "rpc_url": "MY_RPC_URL",
    "exporter_port": "EXPORTER_PORT",
    # ... other required keys
}

OPTIONAL_CONFIG_KEYS = {
    "optional_param": "MY_OPTIONAL_PARAM",
}

ALL_CONFIG_KEYS = {**REQUIRED_CONFIG_KEYS, **OPTIONAL_CONFIG_KEYS}

class MyExporter(RPCExporter):
    def __init__(self, config_source: str, config_file: Optional[str] = None):
        super().__init__(
            config_source=config_source,
            config_file=config_file,
            config_keys=ALL_CONFIG_KEYS,
            required_keys=REQUIRED_CONFIG_KEYS
        )
```

#### For Exporter Users
Your existing code will continue to work with deprecation warnings:

```python
# This still works but shows a deprecation warning
exporter = RPCExporter("solana", "fromEnv")
exporter = RPCExporter(network="solana", config_source="fromEnv")
```

For new code, use the updated API provided by your specific exporter implementation (e.g., `SolanaExporter`, `SupraExporter`).

## [Previous Versions]

_(Add previous version history here if available)_


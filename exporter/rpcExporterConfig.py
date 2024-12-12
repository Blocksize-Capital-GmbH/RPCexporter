import os
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ExporterConfig:
    _config: Dict[str, Optional[str]] = field(default_factory=dict)

    @classmethod
    def init(cls, keys: Dict[str, str]) -> "ExporterConfig":
        """
        Initialize the configuration with keys from CONFIG_KEYS and values set to None.
        """
        return cls(_config={key: None for key in keys})

    def load(self, source: str, keys: Dict[str, str], file_path: Optional[str] = None) -> None:
        """
        Load configuration values from either environment variables or a file.
        """
        if source == "fromEnv":
            self._load_from_env(keys)
        elif source == "fromFile":
            if not file_path:
                raise ValueError("file_path must be provided when source is 'fromFile'")
            self._load_from_file(file_path, keys)
        else:
            raise ValueError("Invalid source. Use 'fromEnv' or 'fromFile'.")
        self.validate(keys)

    def _load_from_env(self, keys: Dict[str, str]) -> None:
        """Load values from environment variables."""
        for key, env_var in keys.items():
            self._config[key] = os.getenv(env_var, self._config.get(key))

    def _load_from_file(self, file_path: str, keys: Dict[str, str]) -> None:
        """Load values from a configuration file."""
        file_values = {}
        with open(file_path) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    file_values[key.strip()] = value.strip()

        for key, env_var in keys.items():
            if env_var in file_values:
                self._config[key] = file_values[env_var]

    def validate(self, keys: Dict[str, str]) -> None:
        """
        Ensure all required keys have been populated in the configuration.
        """
        missing_keys: list[str] = [key for key in keys if self._config.get(key) is None]
        if missing_keys:
            raise ValueError(f"Configuration is missing required keys: {missing_keys}")

    def __getattr__(self, name: str) -> Optional[str]:
        """
        Allow attribute-style access to configuration values.
        """
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"'ExporterConfig' object has no attribute '{name}'")

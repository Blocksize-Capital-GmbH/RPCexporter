import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class JsonRPCResponse:
    """Represents a JSON-RPC response."""

    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

    def is_valid(self) -> bool:
        """Check if the response is valid."""
        return self.result is not None or self.error is not None

    def is_successful(self) -> bool:
        """Check if the RPC response was successful."""
        return self.error is None

    def log_error(self, logger: logging.Logger, method: str) -> None:
        """Log the error if present."""
        if self.error:
            logger.error(f"RPC call to {method} failed: {self.error}")

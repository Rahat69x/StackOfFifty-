"""
Centralized structured logger for AegisCore platform and modules.
"""
import logging
import os
import sys
from datetime import datetime, timezone
from typing import List, Dict, Any
from collections import deque

# Global memory buffer for recent platform logs (max 1000 entries)
_LOG_BUFFER: deque = deque(maxlen=1000)

class BufferHandler(logging.Handler):
    """Custom logging handler to retain recent logs in memory for API querying."""
    def emit(self, record):
        try:
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "name": record.name,
                "message": self.format(record),
                "module": getattr(record, "module_name", record.name)
            }
            _LOG_BUFFER.append(log_entry)
        except Exception:
            self.handleError(record)

class AegisLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter providing module-specific metadata and retrieval helper."""
    def __init__(self, logger: logging.Logger, module_name: str):
        super().__init__(logger, {"module_name": module_name})
        self.module_name = module_name

    def get_recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Return the most recent logs for this module or all modules if empty."""
        logs = list(_LOG_BUFFER)
        if self.module_name and self.module_name != "aegiscore":
            filtered = [entry for entry in logs if entry.get("module") == self.module_name]
            return filtered[-limit:]
        return logs[-limit:]

def get_logger(name: str = "aegiscore") -> AegisLoggerAdapter:
    """Obtain or initialize a structured logger with console, file, and buffer outputs."""
    raw_logger = logging.getLogger(name)
    raw_logger.setLevel(logging.INFO)

    if not raw_logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        raw_logger.addHandler(console_handler)

        # Memory Buffer Handler
        buf_handler = BufferHandler()
        buf_handler.setFormatter(formatter)
        raw_logger.addHandler(buf_handler)

        # File Handler (logs/aegiscore.log)
        try:
            log_dir = os.path.abspath("./logs")
            os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.FileHandler(os.path.join(log_dir, "aegiscore.log"), encoding="utf-8")
            file_handler.setFormatter(formatter)
            raw_logger.addHandler(file_handler)
        except Exception:
            pass

    return AegisLoggerAdapter(raw_logger, name)

def get_all_recent_logs(limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch recent system-wide logs from the in-memory circular buffer."""
    return list(_LOG_BUFFER)[-limit:]

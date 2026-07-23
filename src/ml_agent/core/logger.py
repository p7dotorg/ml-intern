# src/ml_agent/core/logger.py
import logging
import structlog
from pathlib import Path
from typing import Optional

def setup_logging(
    level: str = "INFO",
    log_dir: Path = None,
    format: str = "json"
):
    """Configure structlog and standard logging."""

    # Standard library config
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level),
    )

    # structlog config
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
            if format == "json"
            else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # File handler if log_dir provided
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / "ml-agent.log"
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(file_handler)

def get_logger(name: str = __name__):
    """Get configured logger instance."""
    return structlog.get_logger(name)

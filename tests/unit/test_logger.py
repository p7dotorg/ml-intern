# tests/unit/test_logger.py
import logging
from ml_agent.core.logger import setup_logging, get_logger

def test_setup_logging():
    """Test logging setup."""
    setup_logging(level="DEBUG")
    logger = get_logger("test")
    assert logger is not None

def test_get_logger():
    """Test getting logger instance."""
    setup_logging()
    logger = get_logger("test_module")
    assert logger is not None
    # Should not raise
    logger.info("test message")

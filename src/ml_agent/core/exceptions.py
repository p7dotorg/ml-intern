# src/ml_agent/core/exceptions.py
"""Custom exceptions for ML Agent Framework."""

class MLAgentException(Exception):
    """Base exception for ML Agent."""
    pass

class ProviderException(MLAgentException):
    """Provider-related errors."""
    pass

class AuthenticationError(ProviderException):
    """Authentication/authorization errors."""
    pass

class RateLimitError(ProviderException):
    """Rate limit exceeded."""
    pass

class WorkflowException(MLAgentException):
    """Workflow execution errors."""
    pass

class ConfigurationError(MLAgentException):
    """Configuration errors."""
    pass

class ValidationError(MLAgentException):
    """Data validation errors."""
    pass

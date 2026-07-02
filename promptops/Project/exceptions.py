"""
PromptOps CLI — Module 3 contribution (1/2)

Defines the project's custom exception hierarchy.
All PromptOps-specific errors extend PromptOpsError, so callers can catch
broadly (PromptOpsError) or narrowly (InvalidPromptError, ModelCallError, etc).
"""


class PromptOpsError(Exception):
    """Base exception for all PromptOps-specific errors."""
    pass


class InvalidPromptError(PromptOpsError):
    """Raised when a prompt template is malformed or missing required variables."""

    def __init__(self, prompt_name, reason):
        self.prompt_name = prompt_name
        self.reason = reason
        super().__init__(f"Invalid prompt {prompt_name!r}: {reason}")


class ModelCallError(PromptOpsError):
    """Raised when the underlying model API call fails."""

    def __init__(self, model, status_code, detail=""):
        self.model = model
        self.status_code = status_code
        message = f"Model {model!r} call failed with status {status_code}"
        if detail:
            message += f" ({detail})"
        super().__init__(message)


class ConfigError(PromptOpsError):
    """Raised when PromptOps configuration (e.g. env vars, config files) is invalid."""

    def __init__(self, missing_key):
        self.missing_key = missing_key
        super().__init__(f"Missing or invalid configuration: {missing_key!r}")

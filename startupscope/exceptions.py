# exceptions.py

class StartupScopeError(Exception):
    """Base exception for StartupScope AI."""
    pass

class APIKeyMissingError(StartupScopeError):
    """Raised when an API key is required but not provided or found."""
    pass

class PromptParsingError(StartupScopeError):
    """Raised when the LLM response cannot be parsed into a valid JSON/Pydantic model."""
    pass

class ReportGenerationError(StartupScopeError):
    """Raised when the export process fails (e.g. PDF or DOCX generation error)."""
    pass

class DatabaseConnectionError(StartupScopeError):
    """Raised when there is an issue connecting to or querying the SQLite database."""
    pass

class InvalidExportFormatError(StartupScopeError):
    """Raised when an unsupported export format is requested."""
    pass

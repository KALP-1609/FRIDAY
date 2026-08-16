class FridayError(Exception):
    """Base exception for FRIDAY."""
    pass


class ToolError(FridayError):
    """Raised when a tool fails."""
    pass


class FileToolError(ToolError):
    """Raised when a file operation fails."""
    pass


class MemoryToolError(ToolError):
    """Raised when a memory operation fails."""
    pass


class WebSearchError(ToolError):
    """Raised when a web search fails."""
    pass
class RateLimitError(Exception):
    """Custom exception raised when a rate limit is exceeded."""

    def __init__(self):
        """Initializes a RateLimitError with a default message."""
        super().__init__("Rate limit exceeded")

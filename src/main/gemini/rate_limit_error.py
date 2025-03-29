class RateLimitError(Exception):
    def __init__(self):
        super().__init__("Rate limit exceeded")

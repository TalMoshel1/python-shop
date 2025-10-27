class BusinessError(Exception):
    """
    Custom domain-level exception used for predictable business logic errors.
    Example: Not enough stock, invalid coupon, duplicate order, etc.
    """
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

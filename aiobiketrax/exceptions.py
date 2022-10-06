class BikeTraxError(Exception):
    """Base error."""


class ApiError(BikeTraxError):
    """API error."""


class AuthenticationError(BikeTraxError):
    """Authentication error."""

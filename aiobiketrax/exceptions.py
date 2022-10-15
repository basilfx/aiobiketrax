class BikeTraxError(Exception):
    """Base error."""


class ApiError(BikeTraxError):
    """API error.

    For example, incorrect or unexpected responses.
    """


class AuthenticationError(BikeTraxError):
    """Authentication error.

    For example, incorrect login credentials.
    """


class ConnectionError(BikeTraxError):
    """Connection error.

    For example, connection-related errors.
    """

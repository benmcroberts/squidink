"""Exceptions raised by squidink."""


class SquidinkError(Exception):
    """Base class for all errors raised by squidink."""


class SquidinkAPIError(SquidinkError):
    """An error occurred while communicating with the Octopus API.

    Raised when Octopus returns an error response or cannot be reached. The
    originating library error is preserved as ``__cause__``.
    """

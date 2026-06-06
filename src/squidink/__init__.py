"""squidink: A Python client for the Octopus Energy API."""

from squidink.client import BaseClient, Client
from squidink.exceptions import SquidinkAPIError, SquidinkError
from squidink.models import Consumption

__version__ = "0.0.1"

__all__ = [
    "BaseClient",
    "Client",
    "Consumption",
    "SquidinkAPIError",
    "SquidinkError",
    "__version__",
]

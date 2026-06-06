"""The squidink client and its API selector."""

from enum import StrEnum, auto

from squidink.credentials import Credentials


class ApiKind(StrEnum):
    """
    Octopus exposes two APIs:

    - ``REST`` — resource-oriented HTTP endpoints, using HTTP Basic auth.
    - ``GRAPHQL`` — a single GraphQL endpoint, using token (JWT) auth.
    """

    REST = auto()
    GRAPHQL = auto()


class Client:
    """A client for the Octopus Energy API."""

    def __init__(self, api_key: str, *, api_kind: ApiKind = ApiKind.REST) -> None:
        if api_kind is ApiKind.GRAPHQL:
            raise NotImplementedError("The GraphQL API is not yet implemented; use ApiKind.REST.")
        self._credentials = Credentials(api_key=api_key)
        self._api_kind = api_kind

    @property
    def api_kind(self) -> ApiKind:
        """The Octopus Energy API this client talks to."""
        return self._api_kind

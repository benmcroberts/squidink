"""Credentials for authenticating with the Octopus Energy API."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Credentials:
    """The secret needed to authenticate with the Octopus Energy API."""

    api_key: str

    def __repr__(self) -> str:
        # Never expose the key in logs, tracebacks, or the REPL.
        return "Credentials(api_key='***')"

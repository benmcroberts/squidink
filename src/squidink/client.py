"""The squidink client."""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Any, Self

import httpx

from squidink.credentials import Credentials
from squidink.enums import Granularity
from squidink.exceptions import SquidinkAPIError
from squidink.models import ConsumptionReading

if TYPE_CHECKING:
    import pandas as pd

OCTOPUS_REST_BASE_URL = "https://api.octopus.energy"

# Largest page Octopus will return; used internally to minimise round-trips.
_MAX_PAGE_SIZE = 25000


class BaseClient(ABC):
    """Base class for Octopus Energy API clients.

    Subclasses talk to a specific Octopus API (REST, GraphQL) but expose the
    same operations, so callers do not care which one they hold.
    """

    def __init__(self, api_key: str) -> None:
        self._credentials = Credentials(api_key=api_key)

    @abstractmethod
    def get_consumption_readings(
        self,
        mpan: str,
        serial_number: str,
        *,
        granularity: Granularity = Granularity.HALF_HOURLY,
        period_from: datetime | None = None,
        period_to: datetime | None = None,
    ) -> list[ConsumptionReading]:
        """Return electricity consumption readings for a meter, oldest first.

        ``granularity`` controls aggregation (default: raw half-hourly).
        ``period_from`` and ``period_to`` bound the window (inclusive of
        ``period_from``, exclusive of ``period_to``); pass timezone-aware
        datetimes. ``period_to`` requires ``period_from``.
        """

    def get_consumption_series(
        self,
        mpan: str,
        serial_number: str,
        *,
        period_from: datetime | None = None,
        period_to: datetime | None = None,
        granularity: Granularity = Granularity.HALF_HOURLY,
    ) -> "pd.Series":
        """Return consumption as a pandas Series indexed by interval start.

        Requires the optional ``pandas`` dependency:
        ``pip install 'squidink[pandas]'``.
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "get_consumption_series requires pandas. "
                "Install it with: pip install 'squidink[pandas]'"
            ) from exc

        readings = self.get_consumption_readings(
            mpan,
            serial_number,
            granularity=granularity,
            period_from=period_from,
            period_to=period_to,
        )
        # Readings are already Europe/London-aware, so pandas builds a
        # tz-aware DatetimeIndex directly.
        return pd.Series(
            data=[r.consumption for r in readings],
            index=[r.interval_start for r in readings],
            name="consumption",
        )

    @abstractmethod
    def close(self) -> None:
        """Release any network resources held by the client."""

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class Client(BaseClient):
    """Talks to the Octopus Energy REST API using HTTP Basic auth.

    The API key is sent as the Basic-auth username with a blank password.
    """

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key)
        self._http = httpx.Client(
            base_url=OCTOPUS_REST_BASE_URL,
            auth=(self._credentials.api_key, ""),
        )

    def get_consumption_readings(
        self,
        mpan: str,
        serial_number: str,
        *,
        granularity: Granularity = Granularity.HALF_HOURLY,
        period_from: datetime | None = None,
        period_to: datetime | None = None,
    ) -> list[ConsumptionReading]:
        path = f"/v1/electricity-meter-points/{mpan}/meters/{serial_number}/consumption/"
        params: dict[str, str] = {"page_size": str(_MAX_PAGE_SIZE)}
        if granularity is not Granularity.HALF_HOURLY:
            params["group_by"] = granularity.value
        if period_from is not None:
            params["period_from"] = period_from.isoformat()
        if period_to is not None:
            params["period_to"] = period_to.isoformat()
        results = self._get_paginated_results(path, params=params)
        readings = [ConsumptionReading.model_validate(item) for item in results]
        readings.sort(key=lambda r: r.interval_start)
        return readings

    def _get_json(self, path: str, *, params: Mapping[str, Any] | None = None) -> Any:
        """Send an authenticated GET request and return the parsed JSON body."""
        try:
            response = self._http.get(path, params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SquidinkAPIError(f"Octopus API request failed: {exc}") from exc
        return response.json()

    def _get_paginated_results(
        self, path: str, *, params: Mapping[str, Any] | None = None
    ) -> list[Any]:
        """Follow ``next`` links and return every result item across all pages."""
        data = self._get_json(path, params=params)
        items: list[Any] = list(data["results"])
        next_url = data.get("next")
        while next_url:
            data = self._get_json(next_url)
            items.extend(data["results"])
            next_url = data.get("next")
        return items

    def close(self) -> None:
        self._http.close()

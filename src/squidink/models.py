"""Typed models for Octopus Energy API responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from squidink.constants import TIMEZONE


class ConsumptionReading(BaseModel):
    """A single meter consumption reading over one interval."""

    model_config = ConfigDict(frozen=True)

    consumption: float
    interval_start: datetime
    interval_end: datetime

    @field_validator("interval_start", "interval_end")
    @classmethod
    def _as_london_time(cls, value: datetime) -> datetime:
        """Normalise to the Europe/London zone.

        Octopus returns UK local times with varying fixed offsets (GMT/BST);
        re-express them in the DST-aware Europe/London zone so every reading
        carries a consistent timezone.
        """
        return value.astimezone(TIMEZONE)

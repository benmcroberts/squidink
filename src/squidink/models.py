"""Typed models for Octopus Energy API responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Consumption(BaseModel):
    """A single meter consumption reading over a half-hour interval."""

    model_config = ConfigDict(frozen=True)

    consumption: float
    interval_start: datetime
    interval_end: datetime

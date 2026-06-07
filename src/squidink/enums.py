"""Enumerations used across squidink."""

from enum import StrEnum, auto


class Granularity(StrEnum):
    """How finely to aggregate consumption readings."""

    HALF_HOURLY = auto()  # raw readings (no aggregation)
    HOUR = auto()
    DAY = auto()
    WEEK = auto()
    MONTH = auto()
    QUARTER = auto()

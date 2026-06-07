from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from squidink.models import ConsumptionReading

LONDON = ZoneInfo("Europe/London")


def _reading(**overrides):
    data = {
        "consumption": 0.5,
        "interval_start": "2025-06-01T00:00:00+01:00",
        "interval_end": "2025-06-01T00:30:00+01:00",
    }
    data.update(overrides)
    return ConsumptionReading.model_validate(data)


def test_summer_offset_normalised_to_london_tz():
    reading = _reading()
    assert reading.interval_start.tzinfo == LONDON
    assert reading.interval_start.tzname() == "BST"
    assert reading.consumption == 0.5


def test_utc_input_converted_to_london_tz():
    # Midnight UTC in winter is the same wall-clock instant in London (GMT).
    reading = _reading(
        interval_start="2025-01-15T00:00:00Z",
        interval_end="2025-01-15T00:30:00Z",
    )
    assert reading.interval_start.tzname() == "GMT"
    assert reading.interval_start == datetime(2025, 1, 15, 0, 0, tzinfo=LONDON)


def test_reading_is_immutable():
    reading = _reading()
    with pytest.raises(ValidationError):
        reading.consumption = 9.9


def test_missing_field_is_rejected():
    with pytest.raises(ValidationError):
        ConsumptionReading.model_validate(
            {"consumption": 0.5, "interval_start": "2025-06-01T00:00:00+01:00"}
        )

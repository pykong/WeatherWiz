"""
https://brightsky.dev/docs/#/operations/getWeather#response-body
"""

from dataclasses import dataclass
from datetime import datetime

from .weather_condition import WeatherCondition


@dataclass(frozen=True)
class WeatherInfo:
    """Dataclass representing weather information."""

    timestamp: datetime
    source_id: int
    cloud_cover: float | None = None
    condition: WeatherCondition | None = None
    dew_point: float | None = None
    icon: str | None = None
    precipitation: float | None = None
    precipitation_probability: int | None = None
    precipitation_probability_6h: int | None = None
    pressure_msl: float | None = None
    relative_humidity: float | None = None
    solar: float | None = None
    sunshine: int | None = None
    temperature: float | None = None
    visibility: int | None = None
    wind_direction: int | None = None
    wind_speed: float | None = None
    wind_gust_direction: int | None = None
    wind_gust_speed: float | None = None
    fallback_source_ids: dict[str, int] | None = None

# https://open-meteo.com/en/docs
from datetime import datetime, timezone
from typing import Any

import requests

from .place_info import PlaceInfo
from .weather_info import WeatherCondition, WeatherInfo

FORE_CAST_URL = "https://api.brightsky.dev/weather"


def fetch_weather_data(date: datetime, place: PlaceInfo) -> dict[str, Any]:
    """
    Fetch weather data from the BrightSky API.

    Args:
        date (datetime): The date for which to fetch the weather data.
        place (PlaceInfo): The location information containing latitude and longitude.

    Returns:
        Dict: A dictionary containing the weather data.
    """

    params: dict[str, str | float] = {
        "date": date.strftime("%Y-%m-%d"),
        "lat": place.latitude,
        "lon": place.longitude,
        "units": "dwd",
    }
    headers: dict[str, str] = {"Accept": "application/json"}

    # TODO: Consider retry and caching
    response: requests.Response = requests.get(
        FORE_CAST_URL,
        params=params,
        headers=headers,
    )
    return response.json()  # type: ignore


def find_closest_weather_snapshot(
    response: dict[str, Any], target_date: datetime
) -> dict[str, Any] | None:
    """
    Find the closest hourly weather snapshot to the given date.

    Args:
        response (Dict): The API response containing hourly weather data.
        target_date (datetime): The target date and time.

    Returns:
        Optional[Dict]: The closest hourly weather data snapshot, or None if not found.
    """

    weather_data: list[dict[str, Any]] = response.get("weather", [])
    closest_snapshot = None
    min_time_diff = float("inf")

    for snapshot in weather_data:
        snapshot_time: datetime = datetime.fromisoformat(snapshot["timestamp"])
        # TODO: Properly handle time zone
        snapshot_time = snapshot_time.replace(tzinfo=timezone.utc)
        time_diff: float = abs((snapshot_time - target_date).total_seconds())

        if time_diff < min_time_diff:
            min_time_diff = time_diff
            closest_snapshot = snapshot

    return closest_snapshot


def parse_weather_snapshot(snapshot: dict[str, Any]) -> WeatherInfo | None:
    """
    Parse a weather snapshot dictionary into a WeatherInfo dataclass.

    Args:
        snapshot (dict): A dictionary representing a weather snapshot.

    Returns:
        WeatherInfo: An instance of WeatherInfo with the data from the snapshot.
    """
    snapshot["timestamp"] = datetime.fromisoformat(snapshot["timestamp"])
    if snapshot["condition"]:
        snapshot["condition"] = WeatherCondition(snapshot["condition"])
    return WeatherInfo(**snapshot)


def get_weather_info(date_: datetime, place: PlaceInfo) -> WeatherInfo | None:
    # TODO: Properly handle time zone
    date_ = date_.replace(tzinfo=timezone.utc)
    response = fetch_weather_data(date_, place)
    snapshot = find_closest_weather_snapshot(response, date_)
    return parse_weather_snapshot(snapshot) if snapshot else None

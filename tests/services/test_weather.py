from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from requests import Response

from actions.services.get_weather import (
    fetch_weather_data,
    find_closest_weather_snapshot,
    get_weather_info,
    parse_weather_snapshot,
)
from actions.services.place_info import PlaceInfo
from actions.services.weather_info import WeatherCondition, WeatherInfo


@pytest.fixture
def mock_weather_response() -> Response:
    response = Response()
    response.status_code = 200
    response._content = b"""
    {
        "weather": [
            {
                "timestamp": "2023-08-07T00:00:00+00:00",
                "source_id": 46586,
                "precipitation": 0,
                "pressure_msl": 1013.7,
                "sunshine": 0,
                "temperature": 12.2,
                "wind_direction": 250,
                "wind_speed": 27.4,
                "cloud_cover": 100,
                "dew_point": 6.8,
                "relative_humidity": 69,
                "visibility": 61020,
                "wind_gust_direction": 260,
                "wind_gust_speed": 52.6,
                "condition": null,
                "precipitation_probability": null,
                "precipitation_probability_6h": null,
                "solar": null,
                "icon": "cloudy"
            },
            {
                "timestamp": "2023-08-07T01:00:00+00:00",
                "source_id": 46586,
                "precipitation": 0.1,
                "pressure_msl": 1014.3,
                "sunshine": 0,
                "temperature": 11.1,
                "wind_direction": 260,
                "wind_speed": 29.5,
                "cloud_cover": 100,
                "dew_point": 7.5,
                "relative_humidity": 78,
                "visibility": 18400,
                "wind_gust_direction": 250,
                "wind_gust_speed": 60.1,
                "condition": "rain",
                "precipitation_probability": null,
                "precipitation_probability_6h": null,
                "solar": null,
                "icon": "cloudy"
            },
            {
                "timestamp": "2023-08-07T02:00:00+00:00",
                "source_id": 46586,
                "precipitation": 1.2,
                "pressure_msl": 1014.7,
                "sunshine": 0,
                "temperature": 10.2,
                "wind_direction": 250,
                "wind_speed": 26.6,
                "cloud_cover": 87,
                "dew_point": 8.1,
                "relative_humidity": 87,
                "visibility": 21530,
                "wind_gust_direction": 250,
                "wind_gust_speed": 56.9,
                "condition": "rain",
                "precipitation_probability": null,
                "precipitation_probability_6h": null,
                "solar": null,
                "icon": "rain"
            },
            {
                "timestamp": "2023-08-07T03:00:00+00:00",
                "source_id": 46586,
                "precipitation": 0.4,
                "pressure_msl": 1015.1,
                "sunshine": 0,
                "temperature": 10.3,
                "wind_direction": 250,
                "wind_speed": 24.5,
                "cloud_cover": 100,
                "dew_point": 7.9,
                "relative_humidity": 85,
                "visibility": 44370,
                "wind_gust_direction": 250
            }
        ]
    }
    """
    response.status_code = 200
    return response


@pytest.fixture
def mock_place_info() -> PlaceInfo:
    return PlaceInfo(latitude=48.137, longitude=11.575, city="Munich", region="Bavaria")


@patch("actions.services.get_weather.requests.get")
def test_fetch_weather_data(  # type:ignore
    mock_get, mock_place_info: PlaceInfo, mock_weather_response: Response
) -> None:
    mock_get.return_value = mock_weather_response
    resp = fetch_weather_data(datetime(2023, 8, 7), mock_place_info)
    assert resp is not None
    assert resp["weather"] is not None
    assert len(resp["weather"]) == 4
    assert resp["weather"][0]["source_id"] == 46586


def test_find_closest_weather_snapshot(
    mock_weather_response: Response,
) -> None:  # type:ignore
    timestamp = datetime(2023, 8, 7, 0, 0, 0).replace(tzinfo=timezone.utc)
    actual = find_closest_weather_snapshot(mock_weather_response.json(), timestamp)
    assert actual is not None
    assert timestamp == datetime.fromisoformat(actual["timestamp"])


def test_parse_weather_snapshot() -> None:
    # Test case 1: Valid weather snapshot
    snapshot = {
        "timestamp": "2023-08-07T00:00:00+00:00",
        "source_id": 123,
        "temperature": 25.5,
        "precipitation": 70,
        "condition": "clear-day",
    }
    expected = WeatherInfo(
        timestamp=datetime(2023, 8, 7, 0, 0, 0, tzinfo=timezone.utc),
        source_id=123,
        temperature=25.5,
        precipitation=70,
        condition=WeatherCondition.CLEAR_DAY,
    )
    assert parse_weather_snapshot(snapshot) == expected


@patch("actions.services.get_weather.fetch_weather_data")
# type:ignore
def test_get_weather_info(mock_fetch_weather_data, mock_place_info: PlaceInfo) -> None:
    # Mock the fetch_weather_data function to return a sample weather response
    mock_fetch_weather_data.return_value = {
        "weather": [
            {
                "timestamp": "2023-08-07T00:00:00+00:00",
                "source_id": 123,
                "temperature": 25.5,
                "precipitation": 70,
                "condition": "clear-day",
            }
        ]
    }

    # Define the expected WeatherInfo object
    expected = WeatherInfo(
        timestamp=datetime(2023, 8, 7, 0, 0, 0, tzinfo=timezone.utc),
        source_id=123,
        temperature=25.5,
        precipitation=70,
        condition=WeatherCondition.CLEAR_DAY,
    )

    # Call the get_weather_info function
    actual = get_weather_info(datetime(2023, 8, 7), mock_place_info)

    # Assert that the actual result matches the expected result
    assert actual == expected

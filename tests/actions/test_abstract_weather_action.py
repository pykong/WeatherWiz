from datetime import datetime

import pytest

from actions.abstract_weather_action import AbstractWeatherAction
from actions.services.weather_info import WeatherInfo


class DummyWeatherAction(AbstractWeatherAction):
    def name(self) -> str:
        return "dummy_weather_action"

    def format_weather_info(self, weather: WeatherInfo) -> str:
        return "dummy_weather_info"


@pytest.mark.parametrize(
    "date_string, expected_date",
    [
        ("2023-11-04 00", datetime(2023, 11, 4, 0, 0, 0)),
        ("2023-11-04 00:00:00", datetime(2023, 11, 4, 0, 0, 0)),
        ("2023-10-04 00:10:00", datetime(2023, 10, 4, 0, 0, 0)),
        ("2033-11-04 00:00:10", datetime(2033, 11, 4, 0, 0, 0)),
        ("2023-11-05 00:00:00.123456", datetime(2023, 11, 5, 0, 0, 0)),
        ("2023-11-07 00:00:00 invalid", datetime(2023, 11, 7, 0, 0, 0)),
    ],
)
def test_parse_date(date_string: str, expected_date: datetime) -> None:
    action = DummyWeatherAction()
    assert action.parse_date(date_string) == expected_date

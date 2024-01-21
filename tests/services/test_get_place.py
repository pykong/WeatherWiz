from unittest import mock

import pytest

from actions.services.get_place import get_place_info_via_lookup
from actions.services.place_info import PlaceInfo


def test_get_location_info_via_lookup_happy_path() -> None:
    # Mock the requests.get function
    with mock.patch("actions.services.get_place.requests.get") as mock_get:
        # Set up the mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = [
            {
                "name": "Berlin",
                # 'country': 'Germany',
                "lat": 52.5200,
                "lon": 13.4050,
            }
        ]
        mock_get.return_value = mock_response

        # Call the function under test
        place_info = get_place_info_via_lookup("Berlin")

        # Assert the expected results
        assert isinstance(place_info, PlaceInfo)
        assert place_info.city == "Berlin"
        # assert place_info.region == 'Germany'
        assert place_info.latitude == 52.5200
        assert place_info.longitude == 13.4050

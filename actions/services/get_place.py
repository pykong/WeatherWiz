"""

Also look at:
- http://ip-api.com/json/

"""
# TODO: Handle errors and edge cases; use defensive programming
# TODO: Consider caching and retry

from typing import Final

import requests
from loguru import logger

from .place_info import PlaceInfo

HEADERS: Final[dict[str, str]] = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
}


def get_place_info_via_lookup(city: str, country: str = "DE") -> PlaceInfo:
    """Get the place information via looking up city (and country) from nominatim API.

    Args:
        city (str): The city name.
        country (str, optional): The country query string. Defaults to "DE".

    Docs:
        https://nominatim.org/release-docs/develop/api/Search/
        https://nominatim.openstreetmap.org/search?addressdetails=1&city=Velbert&format=jsonv2&limit=1

    Returns:
        PlaceInfo: The place information.
    """
    url: Final[str] = "https://nominatim.openstreetmap.org/search"
    params: Final[dict[str, str | int]] = {
        "city": city,
        "country": country,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1,
    }

    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    logger.debug(response.url, response.status_code, response.headers, response.text)

    # TODO: properly handle multiple and no results, sort by place_rank
    data = response.json()[-1]
    return PlaceInfo(
        latitude=float(data["lat"]),
        longitude=float(data["lon"]),
        city=data["name"],
        region=None,
    )


def get_place_info_via_ip() -> PlaceInfo:
    """Get the place information by own IP address from ipinfo API.

    The assumption is that the user is accessing the application from the location they want to get the weather for.

    Returns:
        PlaceInfo: The place information.
    """
    response = requests.get("https://ipinfo.io/json")
    response.raise_for_status()
    logger.debug(response.url, response.status_code, response.headers, response.text)

    data = response.json()
    latitude, longitude = map(float, data["loc"].split(","))
    return PlaceInfo(
        latitude=latitude,
        longitude=longitude,
        city=data.get("city", None),
        region=data.get("region", None),
    )

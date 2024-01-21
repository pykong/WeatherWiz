from enum import Enum, unique


@unique
class WeatherCondition(Enum):
    UNKNOWN = "unknown"
    CLEAR_DAY = "clear-day"
    CLEAR_NIGHT = "clear-night"
    PARTLY_CLOUDY_DAY = "partly-cloudy-day"
    CLOUDY = "cloudy"
    FOG = "fog"
    DRY = "dry"
    WIND = "wind"
    RAIN = "rain"
    SLEET = "sleet"
    SNOW = "snow"
    HAIL = "hail"
    THUNDERSTORM = "thunderstorm"

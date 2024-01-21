# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from abstract_weather_action import AbstractWeatherAction
from services.weather_condition import WeatherCondition
from services.weather_info import WeatherInfo


class ActionProvideCondition(AbstractWeatherAction):  # type: ignore
    def name(self) -> str:
        return "action_provide_condition"

    def format_weather_info(self, weather: WeatherInfo) -> str:
        match weather.condition:
            case WeatherCondition.CLEAR_DAY:
                return "clear"
            case WeatherCondition.CLEAR_NIGHT:
                return "clear"
            case WeatherCondition.PARTLY_CLOUDY_DAY:
                return "partly cloudy"
            case WeatherCondition.CLOUDY:
                return "cloudy"
            case WeatherCondition.FOG:
                return "foggy"
            case WeatherCondition.DRY:
                return "dry"
            case WeatherCondition.WIND:
                return "windy"
            case WeatherCondition.RAIN:
                return "rainy"
            case WeatherCondition.SLEET:
                return "sleeting"
            case WeatherCondition.SNOW:
                return "snowy"
            case WeatherCondition.HAIL:
                return "hailing"
            case WeatherCondition.THUNDERSTORM:
                return "thunderstorming"
            case _:
                return "an unknown weather condition"


class ActionProvideTemperature(AbstractWeatherAction):  # type: ignore
    def name(self) -> str:
        return "action_provide_temperature"

    def format_weather_info(self, weather: WeatherInfo) -> str:
        temperature = weather.temperature or 0
        if temperature > 30:
            return f"hot at {temperature}°C"
        elif temperature < 10:
            return f"cold at {temperature}°C"
        elif temperature < 0:
            return f"freezing cold at {temperature}°C"
        elif temperature < 0:
            return f"arctic cold at {temperature}°C"
        else:
            return f"moderate at {temperature}°C"


class ActionProvideRain(AbstractWeatherAction):  # type: ignore
    def name(self) -> str:
        return "action_provide_rain"

    def format_weather_info(self, weather: WeatherInfo) -> str:
        precipitation = weather.precipitation or 0
        if precipitation < 1:
            return "dry"
        elif precipitation < 5:
            return "lightly raining"
        elif precipitation < 20:
            return "moderately raining"
        else:
            return "heavily raining"


class ActionProvideWind(AbstractWeatherAction):  # type: ignore
    def name(self) -> str:
        return "action_provide_wind"

    def format_weather_info(self, weather: WeatherInfo) -> str:
        wind_speed = weather.wind_speed or 0
        wind_direction = self.degree_to_compass(weather.wind_direction)
        # https://en.wikipedia.org/wiki/Beaufort_scale
        if wind_speed < 2:
            return "calm"
        elif wind_speed < 5:
            return f"light air from {wind_direction}"
        elif wind_speed < 11:
            return f"breezing lightly from {wind_direction}"
        elif wind_speed < 19:
            return f"breezing gently from {wind_direction}"
        elif wind_speed < 28:
            return f"breezing moderately from {wind_direction}"
        elif wind_speed < 38:
            return f"breezing freshly from {wind_direction}"
        elif wind_speed < 49:
            return f"breezing strongly from {wind_direction}"
        elif wind_speed < 61:
            return f"gale blowing from {wind_direction}"
        elif wind_speed < 74:
            return f"severe gale blowing from {wind_direction}"
        elif wind_speed < 102:
            return f"storming from {wind_direction}"
        elif wind_speed < 117:
            return f"violently storming from {wind_direction}"
        else:
            return f"blowing with hurricane force from {wind_direction}"

    def degree_to_compass(self, degree: int | None) -> str:
        if degree is None:
            return "an unknown direction"
        val = int((degree / 22.5) + 0.5)
        arr = [
            "North",
            "North-northeast",
            "Northeast",
            "East-northeast",
            "East",
            "East-southeast",
            "Southeast",
            "South-southeast",
            "South",
            "South-southwest",
            "Southwest",
            "West-southwest",
            "West",
            "West-northwest",
            "Northwest",
            "North-northwest",
        ]
        return 'the ' + arr[(val % 16)]

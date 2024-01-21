from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Final

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from services import (
    PlaceInfo,
    WeatherInfo,
    get_place_info_via_ip,
    get_place_info_via_lookup,
    get_weather_info,
)

DATE_FMT: Final[str] = "%Y-%m-%d %H"
MAX_DAYS_IN_FUTURE: Final[int] = 7
MIN_DATE: Final[datetime] = datetime(2010, 1, 1)


def validate_time(func):
    reset_time_slot = [SlotSet("datetime", None)]

    @wraps(func)
    # type: ignore
    def wrapper(self: "AbstractWeatherAction", *args, **kwargs):
        dispatcher = args[0]
        time_ = self.get_time(args[1])
        if time_ - self.get_now_date() > timedelta(days=MAX_DAYS_IN_FUTURE):
            dispatcher.utter_message(
                response="utter_time_in_future", horizon=MAX_DAYS_IN_FUTURE
            )
            return reset_time_slot
        elif time_ < MIN_DATE:
            dispatcher.utter_message(
                response="utter_time_in_past", horizon=str(MIN_DATE)
            )
            return reset_time_slot
        return func(self, *args, **kwargs)

    return wrapper


class AbstractWeatherAction(Action, ABC):  # type: ignore
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def format_weather_info(self, weather: WeatherInfo) -> str:
        raise NotImplementedError

    @validate_time
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[str, Any]
    ) -> Any:
        time_: datetime = self.get_time(tracker)
        place: PlaceInfo | None = self.get_place(tracker)

        if not place:
            dispatcher.utter_message(response="utter_place_missing")
        else:
            weather = get_weather_info(time_, place)
            if not weather:
                dispatcher.utter_message(response="utter_could_not_find")
            else:
                dispatcher.utter_message(
                    response=self.determine_template(time_),
                    info=self.format_weather_info(weather),
                    date=datetime.strftime(time_, "%d.%m.%Y, %-H o'clock"),
                    place=place.city,
                )

        events = [SlotSet("datetime", datetime.strftime(time_, DATE_FMT))]
        if place and place.city:
            events.append(SlotSet("place", place.city))

        return events

    def get_time(self, tracker: Tracker) -> datetime:
        slot_value: str | None = tracker.get_slot("datetime")
        if slot_value:
            return self.parse_date(slot_value)
        else:
            return self.get_now_date()

    def get_now_date(self) -> datetime:
        date_string = str(datetime.now())
        return self.parse_date(date_string)

    def parse_date(self, date_string: str) -> datetime:
        date_string = date_string[:13]  # slice string to '2023-11-04 00'
        return datetime.strptime(date_string, DATE_FMT)

    def get_place(self, tracker: Tracker) -> PlaceInfo | None:
        slot_value: str | None = tracker.get_slot("place")
        if slot_value:
            return get_place_info_via_lookup(slot_value)
        else:
            return get_place_info_via_ip()

    def determine_template(self, time_: datetime) -> str:
        now = self.get_now_date()
        if time_ < now:
            return "utter_weather_past"
        elif time_ > now:
            return "utter_weather_future"
        else:
            return "utter_weather_present"

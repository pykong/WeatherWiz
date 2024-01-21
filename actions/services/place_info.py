import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PlaceInfo:
    latitude: float
    longitude: float
    city: str | None
    region: str | None

    @classmethod
    def to_json(cls, place_info: "PlaceInfo") -> str:
        dic = asdict(place_info)
        return json.dumps(dic)

    @classmethod
    def from_json(cls, place_info_json: str) -> "PlaceInfo":
        dic = json.loads(place_info_json)
        return cls(**dic)

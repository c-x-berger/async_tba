from . import constants
from .alliance import Alliance


class Event():
    def __init__(self, key: str = None, name: str = None, event_code: str = None,
                 event_type: int = None, district: dict = None, city: str = None,
                 state_prov: str = None, country: str = None, start_date: str = None,
                 end_date: str = None, year: int = None, short_name: str = None,
                 event_type_string: str = None, week: int = None, address: str = None,
                 postal_code: str = None, gmaps_place_id: str = None, gmaps_url: str = None,
                 lat: float = None, lng: float = None, location_name: str = None, timezone: str = None,
                 website: str = None, first_event_id: str = None, first_event_code: str = None,
                 webcasts: list = None, division_keys: list = None, parent_event_key: str = None,
                 playoff_type: int = 0, playoff_type_string: str = None):
        self.key = key
        self.name, self.short_name = name, short_name
        self.event_code = event_code
        self.event_type = event_type
        self.district = district
        self.city, self.state_prov, self.country = city, state_prov, country
        self.start_date, self.end_date, self.year, self.week = start_date, end_date, year, week
        self.address, self.postal_code = address, postal_code
        self.gmaps_place_id, self.gmaps_url = gmaps_place_id, gmaps_url
        self.lat, self.lng = lat, lng
        self.location_name = location_name
        self.timezone = timezone
        self.website = website
        self.first_event_id, self.first_event_code = first_event_id, first_event_code
        self.webcasts = webcasts
        self.division_keys, self.parent_event_key = division_keys, parent_event_key
        self.playoff_type, self.playoff_type_string = playoff_type, playoff_type_string

    async def get_alliances(self, client):
        async with client.get(constants.API_BASE_URL + constants.API_EVENT_URL.format(self.key) + "/alliances") as resp:
            if resp.status == 200:
                a = await resp.json()
                return [Alliance(**alliance) for alliance in a]
                return await resp.json()

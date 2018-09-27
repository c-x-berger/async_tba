import aiohttp
from . import constants
from .conn_state import ConnectionState
from .model import Model
from .alliance import Alliance
from .team import Team
from .mini_models import Datacache


class Event(Model):
    def __init__(self, conn_state: ConnectionState, key: str = None, name: str = None, event_code: str = None,
                 event_type: int = None, district: dict = None, city: str = None,
                 state_prov: str = None, country: str = None, start_date: str = None,
                 end_date: str = None, year: int = None, short_name: str = None,
                 event_type_string: str = None, week: int = None, address: str = None,
                 postal_code: str = None, gmaps_place_id: str = None, gmaps_url: str = None,
                 lat: float = None, lng: float = None, location_name: str = None, timezone: str = None,
                 website: str = None, first_event_id: str = None, first_event_code: str = None,
                 webcasts: list = None, division_keys: list = None, parent_event_key: str = None,
                 playoff_type: int = 0, playoff_type_string: str = None):
        super().__init__(conn_state, key=key)

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

        self._alliances = Datacache([], "", None)
        self._teams = Datacache([], "", None)

    async def get_alliances(self):
        data = await self.connection.get_alliances(self.key, self._alliances.last_modified)
        if data is not None:
            alliances = [Alliance(self._session, **s) for s in data['data']]
            self._alliances = Datacache(alliances, data["Last-Modified"], None)
            return alliances
        else:
            return self._alliances.data

    async def get_teams(self):
        data = await self.connection.get_event_teams(self.key, self._teams.last_modified)
        if data is not None:
            teams = [Team(self._connection, **s) for s in data['data']]
            self._teams = Datacache(teams, data['Last-Modified'], None)
            return teams
        else:
            return self._teams.data

import aiohttp
from typing import List
from . import constants
from .conn_state import ConnectionState
from .model import Model
from .mini_models import Robot, Datacache


class Team(Model):
    def __init__(self, conn_state: ConnectionState, team_number: int, key: str = None, nickname: str = None,
                 name: str = None, city: str = None, state_prov: str = None,
                 country: str = None, address: str = None, postal_code: str = None,
                 gmaps_place_id: str = None, gmaps_url: str = None, lat: int = 0, lng: int = 0,
                 location_name: str = None, website: str = None, rookie_year: int = 0,
                 motto: str = None, home_championship: dict = {}):
        super().__init__(conn_state, key=key)

        self.team_number = team_number

        self.nickname = nickname
        self.name = name

        self.city, self.state_prov, self.country, self.address, self.postal_code = city, state_prov, country, address, postal_code
        self.gmaps_place_id, self.gmaps_url = gmaps_place_id, gmaps_url
        self.lat, self.lng = lat, lng
        self.location_name = location_name

        self.website = website

        self.rookie_year = rookie_year

        self.motto = motto

        self.home_championship = home_championship

        self._robots = Datacache([], "", None)

    async def get_robots(self) -> List[Robot]:
        data = await self.connection.get_robots(self.key, self._robots.last_modified)
        if data is not None:
            robots = [Robot(**s) for s in data['data']]
            self._robots = Datacache(robots, data['Last-Modified'], None)
            return robots
        else:
            return self._robots.data

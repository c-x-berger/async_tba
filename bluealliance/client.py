import asyncio
import aiohttp
from typing import Dict, Union
from . import constants
from .conn_state import ConnectionState
from .team import Team
from .event import Event
from .mini_models import Datacache


class Client():
    def __init__(self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop = None):
        self.status_last_modified = ""
        self.status = {}
        self._event_cache = {}  # key: Datacache(Event, str, str)
        self._team_cache = {}  # key: Datacache(Team, str, str)
        self._caches = {
            "teams": {},
            "event": {}
        }
        self._connection_state = ConnectionState(
            x_tba_auth_key, event_loop if event_loop is not None else asyncio.get_event_loop())

    async def get_status(self):
        async with self.session.get(constants.API_STATUS_URL, headers={'If-Modified-Since': self.status_last_modified}) as r:
            if r.status == 200:
                s = await r.json()
                self.status = s
                self.status_last_modified = r.headers['Last-Modified']
                return s
            elif r.status == 304:
                return self.status

    def get_cache(self, type_: str, key: str) -> Datacache:
        try:
            return self._caches[type_][key]
        except KeyError:
            return Datacache(None, "", None)

    def set_cache(self, type_: str, key: str, value: Datacache):
        self._caches[type_][key] = value

    async def get_team(self, team_number: int) -> Team:
        team_key = "frc" + str(team_number)
        teamcache = self.get_cache("teams", team_key)
        heads = {'If-Modified-Since': teamcache.last_modified}
        async with self.session.get(constants.API_BASE_URL + constants.API_TEAM_URL.format(team_key), headers=heads) as resp:
            if resp.status == 200:
                team = Team(self._connection_state, **(await resp.json()))
                # update cache
                self.set_cache("teams", team_key, Datacache(
                    team, resp.headers['Last-Modified'], None))
                return team
            elif resp.status == 304:
                return teamcache.data

    async def get_event(self, event_key: str) -> Event:
        eventcache = self.get_cache("event", event_key)
        heads = {'If-Modified-Since': eventcache.last_modified}
        async with self.session.get(constants.API_BASE_URL + constants.API_EVENT_URL.format(event_key), headers=heads) as resp:
            if resp.status == 200:
                event = Event(self._connection_state, **(await resp.json()))
                self.set_cache("event", event_key, Datacache(
                    event, resp.headers['Last-Modified'], None))
                return event
            elif resp.status == 304:
                return eventcache.data

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._connection_state.session

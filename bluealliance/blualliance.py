import asyncio
import aiohttp
from . import constants
from .team import Team
from .event import Event
from .mini_models import Datacache


class Blualliance():
    def __init__(self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop = None):
        self.auth_key = x_tba_auth_key
        heads = {'X-TBA-Auth-Key': x_tba_auth_key}
        self._session = aiohttp.ClientSession(
            headers=heads, loop=event_loop if event_loop is not None else asyncio.get_event_loop())
        self.status_last_modified = ""
        self.status = {}
        self._teams_cache = {}
        self._events_cache = {}

    async def get_status(self):
        async with self.session.get(constants.API_STATUS_URL, headers={'If-Modified-Since': self.status_last_modified}) as r:
            if r.status == 200:
                s = await r.json()
                self.status = s
                self.status_last_modified = r.headers['Last-Modified']
                return s
            elif r.status == 304:
                return self.status

    @staticmethod
    def get_data_from_cache(cache: dict, datakey) -> Datacache:
        try:
            return cache[datakey]
        except KeyError:
            return Datacache(None, "", None)

    async def get_team(self, team_number: int) -> Team:
        teamcache = Blualliance.get_data_from_cache(
            self._teams_cache, "frc" + str(team_number))
        head = {'If-Modified-Since': teamcache.last_modified}
        async with self.session.get(constants.API_BASE_URL + constants.API_TEAM_URL.format("frc" + str(team_number)), headers=head) as resp:
            print(resp.status)
            if resp.status == 200:
                team = Team(self.session, **(await resp.json()))
                self._teams_cache[team.key] = Datacache(
                    team, resp.headers['Last-Modified'], None)
                return team
            elif resp.status == 304:
                return teamcache.data

    async def get_event(self, event_key: str, last_modified: str = "") -> Event:
        eventcache = Blualliance.get_data_from_cache(
            self._events_cache, event_key)
        head = {'If-Modified-Since': eventcache.last_modified}
        async with self.session.get(constants.API_BASE_URL + constants.API_EVENT_URL.format(event_key), headers=head) as resp:
            if resp.status == 200:
                event = Event(self.session, **(await resp.json()))
                self._events_cache[event.key] = Datacache(
                    event, resp.headers['Last-Modified'], None)
                return event
            elif resp.status == 304:
                return eventcache.data

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

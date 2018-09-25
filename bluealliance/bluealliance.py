import asyncio
import aiohttp
from . import constants
from . import Team
from . import Event


class Blualliance():
    def __init__(self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop = None):
        self.auth_key = x_tba_auth_key
        heads = {'X-TBA-Auth-Key': x_tba_auth_key}
        self._session = aiohttp.ClientSession(
            headers=heads, loop=event_loop if event_loop is not None else asyncio.get_event_loop())
        self.status_last_modified = ""
        self.status = {}

    async def get_status(self):
        async with self.session.get(constants.API_STATUS_URL, headers={'If-Modified-Since': self.status_last_modified}) as r:
            if r.status == 200:
                s = await r.json()
                self.status = s
                self.status_last_modified = r.headers['Last-Modified']
                return s
            elif r.status == 304:
                return self.status

    async def get_team(self, team_number: int, last_modified: str = "") -> Team:
        async with self.session.get(constants.API_BASE_URL + constants.API_TEAM_URL.format("frc" + str(team_number)), headers={'If-Modified-Since': last_modified}) as resp:
            if resp.status == 200:
                s = await resp.json()
                return Team(**s)

    async def get_event(self, event_key: str, last_modified: str = "") -> Event:
        async with self.session.get(constants.API_BASE_URL + constants.API_EVENT_URL.format(event_key)) as resp:
            if resp.status == 200:
                s = await resp.json()
                return Event(**s)

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

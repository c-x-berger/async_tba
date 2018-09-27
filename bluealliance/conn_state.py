import asyncio
import aiohttp
from . import constants
from .mini_models import Datacache


class Route():
    def __init__(self, path: str):
        self.path = path
        self.url = constants.API_BASE_URL + path


def common_header(last_modified: str) -> dict:
    return {'If-Modified-Since': last_modified}


class ConnectionState():
    def __init__(self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop):
        self._session = aiohttp.ClientSession(
            headers={'X-TBA-Auth-Key': x_tba_auth_key},
            loop=event_loop if event_loop is not None else asyncio.get_event_loop()
        )

    async def request(self, route: Route, **kwargs):
        url = route.url
        async with self._session.get(url, **kwargs) as resp:
            data = await resp.json()
            if 300 > resp.status >= 200:
                # request OK
                return {"data": data, "Last-Modified": resp.headers['Last-Modified']}
            elif resp.status == 304:
                # TODO: Find a better way to indicate "use cached"
                print("Use the cache, Luke!")
                return None
            elif resp.status == 401:
                # somehow unauthorized..?
                raise PermissionError()

    def get_robots(self, team_key: str, last_modified: str = "") -> list:
        r = Route(constants.API_TEAM_URL.format(team_key) + "/robots")
        return self.request(r, headers=common_header(last_modified))

    def get_alliances(self, event_key: str, last_modified: str = "") -> list:
        r = Route(constants.API_EVENT_URL.format(event_key) + "/alliances")
        return self.request(r, headers=common_header(last_modified))

    def get_event_teams(self, event_key: str, last_modified: str = "") -> list:
        r = Route(constants.API_EVENT_URL.format(event_key) + "/teams")
        return self.request(r, headers=common_header(last_modified))

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

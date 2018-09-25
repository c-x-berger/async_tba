import asyncio
import aiohttp
from . import constants


class Blualliance():
    def __init__(self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop = None):
        self.auth_key = x_tba_auth_key
        heads = {'X-TBA-Auth-Key': x_tba_auth_key}
        self.session = aiohttp.ClientSession(
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

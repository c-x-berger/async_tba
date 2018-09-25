import asyncio
import aiohttp
from . import constants
from typing import Optional

class Blualliance():
    def __init__(self, x_tba_auth_key: str, event_loop: asyncio.base_events.BaseEventLoop = asyncio.get_event_loop()):
        self.auth_key = x_tba_auth_key
        heads = {'X-TBA-Auth-Key': x_tba_auth_key}
        self.session = aiohttp.ClientSession(headers=heads, loop=event_loop)
        self.status_last_modified = ""

    async def get_status(self):
        async with self.session as session:
            async with session.get(constants.API_STATUS_URL, headers={'If-Modified-Since': self.status_last_modified}) as r:
                status = await r.json()
                self.status_last_modified = r.headers['Last-Modified']
                return status

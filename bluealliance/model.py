import aiohttp
from typing import Optional


class Model():
    def __init__(self, session: aiohttp.ClientSession, key: Optional[str] = None):
        self._session = session
        if key is not None:
            self.key = key
        # else no key (e.g. alliances)
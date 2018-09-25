import aiohttp
from . import constants
from .team import Team
from typing import Dict, List, Union


class Alliance():
    def __init__(self, name: str = None, backup: Dict[str, str] = None, declines: List[str] = [], picks: List[str] = [],
                 status: Dict[str, Union[str, None, Dict[str, int]]] = None):
        self._name = name
        self._backup = backup
        self._declines = declines
        self._picks = picks
        # tourney status
        self._full_status = status
        self._level = status["level"]
        self._status = status["status"]
        self._record = status["record"]
        self._wins, self._losses, self._ties = self._record[
            'wins'], self._record['losses'], self._record['ties']

        self._current_level_record = status['current_level_record']
        self._current_level_wins, self._current_level_losses, self._current_level_ties = self._current_level_record[
            'wins'], self._current_level_record['losses'], self._current_level_record['ties']

    async def get_declining_teams(self, client: aiohttp.ClientSession) -> List[Team]:
        r = []
        for team in self._declines:
            async with client.get(constants.API_BASE_URL + constants.API_TEAM_URL.format(int(team[3:]))) as resp:
                if resp.status == 200:
                    t = await resp.json()
                    r.append(Team(**t))
        return r

    async def get_teams(self, client: aiohttp.ClientSession) ->List[Team]:
        r = []
        for team in self._picks:
            async with client.get(constants.API_BASE_URL + constants.API_TEAM_URL.format(int(team[3:]))) as resp:
                if resp.status == 200:
                    t = await resp.json()
                    r.append(Team(**t))
        return r

    @property
    def name(self) -> str:
        return self._name

    @property
    def backup(self) -> dict:
        return self._backup

    @property
    def status(self) -> str:
        return self._status

    @property
    def record(self) -> Dict[str, int]:
        return self._record

    @property
    def wins(self) -> int:
        return self._wins

    @property
    def losses(self) -> int:
        return self._losses

    @property
    def ties(self) -> int:
        return self._ties

    @property
    def current_level_record(self) -> Dict[str, int]:
        return self._current_level_record

    @property
    def current_level_wins(self) -> int:
        return self._current_level_wins

    @property
    def current_level_losses(self) -> int:
        return self._current_level_losses

    @property
    def current_level_ties(self) -> int:
        return self._current_level_ties

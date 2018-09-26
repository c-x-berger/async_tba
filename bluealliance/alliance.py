import aiohttp
from . import constants
from .model import Model
from .team import Team
from typing import Dict, List, Union


class Alliance(Model):
    def __init__(self, session: aiohttp.ClientSession, name: str = None, backup: Dict[str, str] = None,
                 declines: List[str] = [], picks: List[str] = [],
                 status: Dict[str, Union[str, None, Dict[str, int]]] = None):
        super().__init__(session)

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

    async def get_declining_teams(self) -> List[Team]:
        r = []
        for team in self._declines:
            async with self._session.get(constants.API_BASE_URL + constants.API_TEAM_URL.format(int(team[3:]))) as resp:
                if resp.status == 200:
                    t = await resp.json()
                    r.append(Team(self._session, **t))
        return r

    async def get_teams(self) -> List[Team]:
        r = []
        for team in self._picks:
            async with self._session.get(constants.API_BASE_URL + constants.API_TEAM_URL.format(int(team[3:]))) as resp:
                if resp.status == 200:
                    t = await resp.json()
                    r.append(Team(self._session, **t))
        return r

    @property
    def name(self) -> str:
        """The alliance's name (e.g. Alliance 1)"""
        return self._name

    @property
    def backup(self) -> dict:
        """
        Dict detailing backup bot use.
        out: Team key that was replaced by the backup team.
        in: Team key that was called in as the backup.
        """
        return self._backup

    @property
    def picks(self) -> List[str]:
        '''A list of team keys for the teams picked. Actual Team objects should be fetched with get_teams'''
        return self._picks

    @property
    def declines(self) -> List[str]:
        '''A list of team keys for the teams that declined. Actual Team objects should be fetched with get_declining_teams'''
        return self._declines

    @property
    def status(self) -> str:
        '''Playoff status (e.g. eliminated)'''
        return self._status

    @property
    def record(self) -> Dict[str, int]:
        '''Overall playoff w/l/t record.'''
        return self._record

    @property
    def wins(self) -> int:
        '''Number of playoff wins.'''
        return self._wins

    @property
    def losses(self) -> int:
        '''Number of playoff losses.'''
        return self._losses

    @property
    def ties(self) -> int:
        '''Number of playoff ties.'''
        return self._ties

    @property
    def current_level_record(self) -> Dict[str, int]:
        """w/l/t record for the alliance's current playoff round."""
        return self._current_level_record

    @property
    def current_level_wins(self) -> int:
        """Number of wins for the alliance's current playoff round."""
        return self._current_level_wins

    @property
    def current_level_losses(self) -> int:
        """Number of losses for the alliance's current playoff round."""
        return self._current_level_losses

    @property
    def current_level_ties(self) -> int:
        """Number of ties for the alliance's current playoff round."""
        return self._current_level_ties

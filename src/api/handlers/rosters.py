from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)


async def fetch_roster(
    client: NHLApiClient, team_abbr: str, season_id: int
) -> dict[str, Any]:
    """Fetch the roster for a team in a given season.

    season_id is in the form 20232024.
    """
    data = await client.get(NHLApiClient.WEB_BASE, f"/roster/{team_abbr}/{season_id}")
    logger.debug("fetched roster", team=team_abbr, season=season_id)
    return data


async def fetch_roster_season_list(
    client: NHLApiClient, team_abbr: str
) -> list[dict[str, Any]]:
    """Fetch list of seasons for which a team has roster data."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/roster-season/{team_abbr}")
    seasons: list[dict[str, Any]] = data if isinstance(data, list) else []
    return seasons

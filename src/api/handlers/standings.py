from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)


async def fetch_standings(client: NHLApiClient, date: str) -> dict[str, Any]:
    """Fetch standings for a specific date (YYYY-MM-DD)."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/standings/{date}")
    logger.debug("fetched standings", date=date)
    return data


async def fetch_standings_now(client: NHLApiClient) -> dict[str, Any]:
    """Fetch current standings."""
    data = await client.get(NHLApiClient.WEB_BASE, "/standings/now")
    return data


async def fetch_standings_season(
    client: NHLApiClient, season_id: int
) -> list[dict[str, Any]]:
    """Fetch all standings snapshots for a season using the season endpoint."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/standings-season")
    seasons: list[dict[str, Any]] = data.get("seasons", [])
    for season in seasons:
        if season.get("id") == season_id:
            return [season]
    return []

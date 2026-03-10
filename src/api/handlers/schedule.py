from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)


async def fetch_schedule_by_date(client: NHLApiClient, date: str) -> dict[str, Any]:
    """Fetch the NHL schedule for a given date (YYYY-MM-DD)."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/schedule/{date}")
    logger.debug("fetched schedule", date=date)
    return data


async def fetch_club_season_schedule(
    client: NHLApiClient, team_abbr: str
) -> dict[str, Any]:
    """Fetch the full season schedule for a given team abbreviation."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/club-schedule-season/{team_abbr}/now")
    logger.debug("fetched club season schedule", team=team_abbr)
    return data


async def fetch_schedule_week(
    client: NHLApiClient, date: str | None = None
) -> dict[str, Any]:
    """Fetch the weekly schedule. Uses today if date is None."""
    path = "/schedule/now" if date is None else f"/schedule/{date}"
    data = await client.get(NHLApiClient.WEB_BASE, path)
    return data

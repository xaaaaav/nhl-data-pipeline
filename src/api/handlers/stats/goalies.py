from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)

GOALIE_REPORT_TYPES: list[str] = [
    "summary",
    "advanced",
    "bios",
    "savesByStrength",
    "shootout",
    "startedVsRelieved",
]


async def fetch_goalie_stats(
    client: NHLApiClient,
    report_type: str,
    season_id: int,
    game_type_id: int,
    start: int = 0,
    limit: int = 100,
) -> dict[str, Any]:
    """Fetch a single page of goalie stats for a given report type."""
    cayenne_exp = f"seasonId={season_id} and gameTypeId={game_type_id}"
    params: dict[str, Any] = {
        "cayenneExp": cayenne_exp,
        "start": start,
        "limit": limit,
    }
    data = await client.get(NHLApiClient.STATS_BASE, f"/goalie/{report_type}", params=params)
    logger.debug(
        "fetched goalie stats",
        report=report_type,
        season=season_id,
        game_type=game_type_id,
        start=start,
    )
    return data


async def fetch_all_goalie_stats(
    client: NHLApiClient,
    report_type: str,
    season_id: int,
    game_type_id: int,
    page_size: int = 100,
) -> list[dict[str, Any]]:
    """Fetch all pages of goalie stats, handling pagination automatically."""
    all_records: list[dict[str, Any]] = []
    start = 0

    while True:
        page = await fetch_goalie_stats(
            client, report_type, season_id, game_type_id, start=start, limit=page_size
        )
        records: list[dict[str, Any]] = page.get("data", [])
        all_records.extend(records)

        total = page.get("total", 0)
        start += len(records)

        if start >= total or not records:
            break

    logger.info(
        "fetched all goalie stats",
        report=report_type,
        season=season_id,
        game_type=game_type_id,
        total=len(all_records),
    )
    return all_records

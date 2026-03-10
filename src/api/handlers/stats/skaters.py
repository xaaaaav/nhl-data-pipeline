from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)

SKATER_REPORT_TYPES: list[str] = [
    "summary",
    "bios",
    "faceoffpercentages",
    "faceoffwins",
    "goalsForAgainst",
    "penalties",
    "penaltykill",
    "penaltyShots",
    "powerplay",
    "puckPossessions",
    "realtime",
    "shootout",
    "shottype",
    "timeonice",
    "pointspergame",
]


async def fetch_skater_stats(
    client: NHLApiClient,
    report_type: str,
    season_id: int,
    game_type_id: int,
    start: int = 0,
    limit: int = 100,
) -> dict[str, Any]:
    """Fetch a single page of skater stats for a given report type.

    Args:
        client: NHL API client.
        report_type: One of the SKATER_REPORT_TYPES.
        season_id: Season in the form 20232024.
        game_type_id: 2 for regular season, 3 for playoffs.
        start: Pagination offset.
        limit: Page size (max 100).
    """
    cayenne_exp = f"seasonId={season_id} and gameTypeId={game_type_id}"
    params: dict[str, Any] = {
        "cayenneExp": cayenne_exp,
        "start": start,
        "limit": limit,
    }
    data = await client.get(NHLApiClient.STATS_BASE, f"/skater/{report_type}", params=params)
    logger.debug(
        "fetched skater stats",
        report=report_type,
        season=season_id,
        game_type=game_type_id,
        start=start,
    )
    return data


async def fetch_all_skater_stats(
    client: NHLApiClient,
    report_type: str,
    season_id: int,
    game_type_id: int,
    page_size: int = 100,
) -> list[dict[str, Any]]:
    """Fetch all pages of skater stats, handling pagination automatically."""
    all_records: list[dict[str, Any]] = []
    start = 0

    while True:
        page = await fetch_skater_stats(
            client, report_type, season_id, game_type_id, start=start, limit=page_size
        )
        records: list[dict[str, Any]] = page.get("data", [])
        all_records.extend(records)

        total = page.get("total", 0)
        start += len(records)

        if start >= total or not records:
            break

    logger.info(
        "fetched all skater stats",
        report=report_type,
        season=season_id,
        game_type=game_type_id,
        total=len(all_records),
    )
    return all_records

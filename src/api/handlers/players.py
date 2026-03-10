from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)


async def fetch_player(client: NHLApiClient, player_id: int) -> dict[str, Any]:
    """Fetch profile data for a single player."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/player/{player_id}/landing")
    logger.debug("fetched player", player_id=player_id)
    return data


async def fetch_player_game_log(
    client: NHLApiClient,
    player_id: int,
    season_id: int,
    game_type_id: int,
) -> dict[str, Any]:
    """Fetch game-by-game log for a player in a given season."""
    data = await client.get(
        NHLApiClient.WEB_BASE,
        f"/player/{player_id}/game-log/{season_id}/{game_type_id}",
    )
    return data


async def search_players(
    client: NHLApiClient, query: str, limit: int = 20
) -> list[dict[str, Any]]:
    """Search for players by name using the search API."""
    data = await client.get(
        NHLApiClient.SEARCH_BASE,
        "/search/player",
        params={"q": query, "limit": limit},
    )
    results: list[dict[str, Any]] = data if isinstance(data, list) else []
    return results

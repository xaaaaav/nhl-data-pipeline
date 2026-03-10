from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)


async def fetch_boxscore(client: NHLApiClient, game_id: int) -> dict[str, Any]:
    """Fetch boxscore for a game."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/gamecenter/{game_id}/boxscore")
    logger.debug("fetched boxscore", game_id=game_id)
    return data


async def fetch_play_by_play(client: NHLApiClient, game_id: int) -> dict[str, Any]:
    """Fetch play-by-play data for a game."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/gamecenter/{game_id}/play-by-play")
    logger.debug("fetched play-by-play", game_id=game_id)
    return data


async def fetch_game_story(client: NHLApiClient, game_id: int) -> dict[str, Any]:
    """Fetch the game landing / story page."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/gamecenter/{game_id}/landing")
    return data

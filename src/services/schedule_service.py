from datetime import date
from typing import Any

import structlog
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.game import Game

logger = structlog.get_logger(__name__)


def _parse_game(raw: dict[str, Any]) -> dict[str, Any]:
    """Parse a game dict from the schedule API response."""
    return {
        "game_id": raw["id"],
        "season_id": raw["season"],
        "game_type": raw.get("gameType", 2),
        "game_date": raw.get("gameDate", str(date.today())),
        "home_team_id": raw["homeTeam"]["id"],
        "away_team_id": raw["awayTeam"]["id"],
        "venue": raw.get("venue", {}).get("default"),
        "game_state": raw.get("gameState", "FUT"),
        "home_score": raw.get("homeTeam", {}).get("score"),
        "away_score": raw.get("awayTeam", {}).get("score"),
        "period": raw.get("period"),
    }


async def upsert_game_from_schedule(
    session: AsyncSession, raw: dict[str, Any]
) -> Game:
    """Upsert a game record parsed from schedule data."""
    parsed = _parse_game(raw)
    stmt = (
        pg_insert(Game)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["game_id"],
            set_={k: v for k, v in parsed.items() if k != "game_id"},
        )
        .returning(Game)
    )
    result = await session.execute(stmt)
    game = result.scalar_one()
    return game


async def process_schedule_response(
    session: AsyncSession, data: dict[str, Any]
) -> list[int]:
    """Process a full schedule API response and return all game IDs upserted."""
    game_ids: list[int] = []
    for game_week in data.get("gameWeek", []):
        for raw_game in game_week.get("games", []):
            game = await upsert_game_from_schedule(session, raw_game)
            game_ids.append(game.game_id)
    logger.info("processed schedule", game_count=len(game_ids))
    return game_ids

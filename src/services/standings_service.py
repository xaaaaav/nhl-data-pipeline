from typing import Any

import structlog
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.standings import StandingsSnapshot

logger = structlog.get_logger(__name__)


def _parse_standing(data: dict[str, Any], snapshot_date: str) -> dict[str, Any]:
    """Parse a single team standing entry."""
    streak = data.get("streakCode", "")
    streak_type: str | None = None
    streak_count: int | None = None
    if streak and len(streak) > 1:
        streak_type = streak[0]
        try:
            streak_count = int(streak[1:])
        except ValueError:
            pass

    return {
        "season_id": data["seasonId"],
        "date": snapshot_date,
        "team_id": data["teamAbbrev"]["default"] if isinstance(data.get("teamAbbrev"), dict) else data.get("teamId"),
        "points": data.get("points", 0),
        "wins": data.get("wins", 0),
        "losses": data.get("losses", 0),
        "ot_losses": data.get("otLosses", 0),
        "games_played": data.get("gamesPlayed", 0),
        "goals_for": data.get("goalFor"),
        "goals_against": data.get("goalAgainst"),
        "regulation_wins": data.get("regulationWins"),
        "streak_type": streak_type,
        "streak_count": streak_count,
    }


async def upsert_standing(
    session: AsyncSession,
    data: dict[str, Any],
    snapshot_date: str,
    team_id: int,
) -> StandingsSnapshot:
    """Upsert a standings snapshot for one team on one date."""
    streak = data.get("streakCode", "")
    streak_type: str | None = None
    streak_count: int | None = None
    if streak and len(streak) > 1:
        streak_type = streak[0]
        try:
            streak_count = int(streak[1:])
        except ValueError:
            pass

    parsed: dict[str, Any] = {
        "season_id": data["seasonId"],
        "date": snapshot_date,
        "team_id": team_id,
        "points": data.get("points", 0),
        "wins": data.get("wins", 0),
        "losses": data.get("losses", 0),
        "ot_losses": data.get("otLosses", 0),
        "games_played": data.get("gamesPlayed", 0),
        "goals_for": data.get("goalFor"),
        "goals_against": data.get("goalAgainst"),
        "regulation_wins": data.get("regulationWins"),
        "streak_type": streak_type,
        "streak_count": streak_count,
    }
    stmt = (
        pg_insert(StandingsSnapshot)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["season_id", "date", "team_id"],
            set_={k: v for k, v in parsed.items() if k not in ("season_id", "date", "team_id")},
        )
        .returning(StandingsSnapshot)
    )
    result = await session.execute(stmt)
    snapshot = result.scalar_one()
    logger.debug(
        "upserted standing", team_id=team_id, date=snapshot_date, points=parsed["points"]
    )
    return snapshot

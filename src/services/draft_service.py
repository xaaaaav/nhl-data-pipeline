from typing import Any

import structlog
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.draft import DraftPick

logger = structlog.get_logger(__name__)


async def upsert_draft_pick(
    session: AsyncSession, data: dict[str, Any]
) -> DraftPick:
    """Upsert a single draft pick from raw API data."""
    parsed: dict[str, Any] = {
        "draft_year": data.get("draftYear", data.get("year")),
        "round_number": data.get("round", data.get("roundNumber")),
        "pick_in_round": data.get("pickInRound", data.get("pick")),
        "overall_pick": data.get("overallPick"),
        "team_id": data.get("teamId"),
        "player_id": data.get("playerId"),
    }
    stmt = (
        pg_insert(DraftPick)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["draft_year", "round_number", "pick_in_round"],
            set_={k: v for k, v in parsed.items()
                  if k not in ("draft_year", "round_number", "pick_in_round")},
        )
        .returning(DraftPick)
    )
    result = await session.execute(stmt)
    pick = result.scalar_one()
    return pick


async def upsert_draft(
    session: AsyncSession, picks: list[dict[str, Any]]
) -> list[DraftPick]:
    """Upsert all draft picks for a draft year."""
    upserted: list[DraftPick] = []
    for pick_data in picks:
        pick = await upsert_draft_pick(session, pick_data)
        upserted.append(pick)
    logger.info("upserted draft picks", count=len(upserted))
    return upserted

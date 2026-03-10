from typing import Any

import structlog
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.game import Game, GameBoxscore
from src.models.play_by_play import (
    PlayByPlayEvent,
    PbpBlockedShot,
    PbpFaceoff,
    PbpGoal,
    PbpHit,
    PbpMissedShot,
    PbpPenalty,
    PbpPeriodEvent,
    PbpShot,
    PbpStoppage,
)

logger = structlog.get_logger(__name__)

_FINAL_STATES = frozenset({"FINAL", "OFF"})


async def upsert_game(session: AsyncSession, data: dict[str, Any]) -> Game:
    """Upsert a game from raw boxscore/game-center data."""
    parsed: dict[str, Any] = {
        "game_id": data["id"],
        "season_id": data["season"],
        "game_type": data.get("gameType", 2),
        "game_date": data.get("gameDate"),
        "home_team_id": data["homeTeam"]["id"],
        "away_team_id": data["awayTeam"]["id"],
        "venue": data.get("venue", {}).get("default"),
        "game_state": data.get("gameState", "FUT"),
        "home_score": data.get("homeTeam", {}).get("score"),
        "away_score": data.get("awayTeam", {}).get("score"),
        "period": data.get("period"),
    }
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
    return result.scalar_one()


async def upsert_boxscore(
    session: AsyncSession, game_id: int, data: dict[str, Any]
) -> GameBoxscore:
    """Upsert a game boxscore from raw API response."""
    home = data.get("homeTeam", {})
    away = data.get("awayTeam", {})

    parsed: dict[str, Any] = {
        "game_id": game_id,
        "home_shots": home.get("sog"),
        "home_hits": home.get("hits"),
        "home_blocked_shots": home.get("blockedShots"),
        "home_pp_goals": home.get("powerPlayGoals"),
        "home_pp_opportunities": home.get("powerPlayConversions"),
        "home_faceoff_pct": home.get("faceoffWinningPctg"),
        "home_giveaways": home.get("giveaways"),
        "home_takeaways": home.get("takeaways"),
        "home_pim": home.get("pim"),
        "away_shots": away.get("sog"),
        "away_hits": away.get("hits"),
        "away_blocked_shots": away.get("blockedShots"),
        "away_pp_goals": away.get("powerPlayGoals"),
        "away_pp_opportunities": away.get("powerPlayConversions"),
        "away_faceoff_pct": away.get("faceoffWinningPctg"),
        "away_giveaways": away.get("giveaways"),
        "away_takeaways": away.get("takeaways"),
        "away_pim": away.get("pim"),
        "raw": data,
    }
    stmt = (
        pg_insert(GameBoxscore)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["game_id"],
            set_={k: v for k, v in parsed.items() if k != "game_id"},
        )
        .returning(GameBoxscore)
    )
    result = await session.execute(stmt)
    boxscore = result.scalar_one()
    logger.debug("upserted boxscore", game_id=game_id)
    return boxscore


async def upsert_play_by_play(
    session: AsyncSession, game_id: int, events: list[dict[str, Any]]
) -> None:
    """Upsert all play-by-play events for a game, routing to detail tables."""
    for raw in events:
        event_type: str = raw.get("typeDescKey", "").lower()
        period_descriptor = raw.get("periodDescriptor", {})

        base_parsed: dict[str, Any] = {
            "game_id": game_id,
            "event_number": raw.get("eventId", 0),
            "period": period_descriptor.get("number", 0),
            "period_type": period_descriptor.get("periodType", "REG"),
            "time_in_period": raw.get("timeInPeriod", "00:00"),
            "time_remaining": raw.get("timeRemaining", "00:00"),
            "event_type": event_type,
            "team_id": raw.get("details", {}).get("eventOwnerTeamId"),
            "x_coord": raw.get("details", {}).get("xCoord"),
            "y_coord": raw.get("details", {}).get("yCoord"),
            "zone": raw.get("details", {}).get("zoneCode"),
        }

        event_stmt = pg_insert(PlayByPlayEvent).values(**base_parsed).returning(
            PlayByPlayEvent.event_id
        )
        # On conflict for the same game/event_number combo, update
        event_stmt = event_stmt.on_conflict_do_update(
            index_elements=["game_id", "event_number"],
            set_={k: v for k, v in base_parsed.items() if k not in ("game_id", "event_number")},
        )
        result = await session.execute(event_stmt)
        event_id: int = result.scalar_one()

        await _upsert_event_detail(session, event_id, event_type, raw.get("details", {}))

    logger.debug("upserted play-by-play events", game_id=game_id, count=len(events))


async def _upsert_event_detail(
    session: AsyncSession,
    event_id: int,
    event_type: str,
    details: dict[str, Any],
) -> None:
    """Route to the correct per-event-type detail table."""
    if event_type == "goal":
        await session.execute(
            pg_insert(PbpGoal)
            .values(
                event_id=event_id,
                scoring_player_id=details.get("scoringPlayerId"),
                assist1_player_id=details.get("assist1PlayerId"),
                assist2_player_id=details.get("assist2PlayerId"),
                goalie_id=details.get("goalieInNetId"),
                shot_type=details.get("shotType"),
                strength=details.get("strength"),
                empty_net=details.get("goalieInNetId") is None,
            )
            .on_conflict_do_update(
                index_elements=["event_id"],
                set_={
                    "scoring_player_id": details.get("scoringPlayerId"),
                    "shot_type": details.get("shotType"),
                    "strength": details.get("strength"),
                },
            )
        )
    elif event_type == "shot-on-goal":
        await session.execute(
            pg_insert(PbpShot)
            .values(
                event_id=event_id,
                shooting_player_id=details.get("shootingPlayerId"),
                goalie_id=details.get("goalieInNetId"),
                shot_type=details.get("shotType"),
            )
            .on_conflict_do_nothing(index_elements=["event_id"])
        )
    elif event_type == "missed-shot":
        await session.execute(
            pg_insert(PbpMissedShot)
            .values(
                event_id=event_id,
                shooting_player_id=details.get("shootingPlayerId"),
                goalie_id=details.get("goalieInNetId"),
                shot_type=details.get("shotType"),
                miss_reason=details.get("reason"),
            )
            .on_conflict_do_nothing(index_elements=["event_id"])
        )
    elif event_type == "blocked-shot":
        await session.execute(
            pg_insert(PbpBlockedShot)
            .values(
                event_id=event_id,
                shooter_player_id=details.get("shootingPlayerId"),
                blocking_player_id=details.get("blockingPlayerId"),
            )
            .on_conflict_do_nothing(index_elements=["event_id"])
        )
    elif event_type == "hit":
        await session.execute(
            pg_insert(PbpHit)
            .values(
                event_id=event_id,
                hitting_player_id=details.get("hittingPlayerId"),
                hittee_player_id=details.get("hitteePlayerId"),
            )
            .on_conflict_do_nothing(index_elements=["event_id"])
        )
    elif event_type == "faceoff":
        await session.execute(
            pg_insert(PbpFaceoff)
            .values(
                event_id=event_id,
                winning_player_id=details.get("winningPlayerId"),
                losing_player_id=details.get("losingPlayerId"),
            )
            .on_conflict_do_nothing(index_elements=["event_id"])
        )
    elif event_type == "penalty":
        await session.execute(
            pg_insert(PbpPenalty)
            .values(
                event_id=event_id,
                committed_by_player_id=details.get("committedByPlayerId"),
                drawn_by_player_id=details.get("drawnByPlayerId"),
                penalty_type=details.get("typeCode"),
                penalty_description=details.get("descKey"),
                duration_minutes=details.get("duration"),
            )
            .on_conflict_do_nothing(index_elements=["event_id"])
        )
    elif event_type == "stoppage":
        await session.execute(
            pg_insert(PbpStoppage)
            .values(event_id=event_id, reason=details.get("reason"))
            .on_conflict_do_nothing(index_elements=["event_id"])
        )
    elif event_type in ("period-start", "period-end", "game-end"):
        await session.execute(
            pg_insert(PbpPeriodEvent)
            .values(event_id=event_id, period_number=details.get("periodNumber"))
            .on_conflict_do_nothing(index_elements=["event_id"])
        )


async def get_game_ids_needing_fetch(session: AsyncSession) -> list[int]:
    """Return game IDs where the game is not final or boxscore is missing."""
    games_subq = (
        select(Game.game_id)
        .where(Game.game_state.notin_(list(_FINAL_STATES)))
    )
    boxscore_subq = select(GameBoxscore.game_id)

    # Games that are not final
    not_final = await session.execute(games_subq)
    not_final_ids = set(not_final.scalars().all())

    # Games that are final but missing a boxscore
    final_game_ids_result = await session.execute(
        select(Game.game_id).where(Game.game_state.in_(list(_FINAL_STATES)))
    )
    final_game_ids = set(final_game_ids_result.scalars().all())

    existing_boxscore_ids_result = await session.execute(boxscore_subq)
    existing_boxscore_ids = set(existing_boxscore_ids_result.scalars().all())

    missing_boxscore_ids = final_game_ids - existing_boxscore_ids

    all_ids = not_final_ids | missing_boxscore_ids
    return sorted(all_ids)

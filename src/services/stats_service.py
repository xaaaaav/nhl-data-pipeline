from typing import Any

import structlog
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.stats import (
    GoalieStatsAdvanced,
    GoalieStatsBios,
    GoalieStatsSavesByStrength,
    GoalieStatsShootout,
    GoalieStatsSummary,
    GoalieStatsStartedVsRelieved,
    SkaterStatsBios,
    SkaterStatsFaceoffPercentages,
    SkaterStatsFaceoffWins,
    SkaterStatsGoalsForAgainst,
    SkaterStatsPenalties,
    SkaterStatsPenaltyKill,
    SkaterStatsPenaltyShots,
    SkaterStatsPowerplay,
    SkaterStatsPuckPossessions,
    SkaterStatsRealtime,
    SkaterStatsShootout,
    SkaterStatsShottype,
    SkaterStatsSummary,
    SkaterStatsTimeOnIce,
    SkaterStatsPointsPerGame,
    TeamStatsFaceoffPercentages,
    TeamStatsFaceoffWins,
    TeamStatsGoalsAgainstByStrength,
    TeamStatsGoalsForByStrength,
    TeamStatsGoalsLeaders,
    TeamStatsPenalties,
    TeamStatsPenaltyKill,
    TeamStatsPenaltyShots,
    TeamStatsPercentages,
    TeamStatsPointsPerGame,
    TeamStatsPowerplay,
    TeamStatsRealtime,
    TeamStatsScoretrail,
    TeamStatsShootout,
    TeamStatsSummary,
)

logger = structlog.get_logger(__name__)

_SKATER_REPORT_MODEL_MAP: dict[str, Any] = {
    "summary": SkaterStatsSummary,
    "bios": SkaterStatsBios,
    "faceoffpercentages": SkaterStatsFaceoffPercentages,
    "faceoffwins": SkaterStatsFaceoffWins,
    "goalsforagainst": SkaterStatsGoalsForAgainst,
    "penalties": SkaterStatsPenalties,
    "penaltykill": SkaterStatsPenaltyKill,
    "penaltyshots": SkaterStatsPenaltyShots,
    "powerplay": SkaterStatsPowerplay,
    "puckpossessions": SkaterStatsPuckPossessions,
    "realtime": SkaterStatsRealtime,
    "shootout": SkaterStatsShootout,
    "shottype": SkaterStatsShottype,
    "timeonice": SkaterStatsTimeOnIce,
    "pointspergame": SkaterStatsPointsPerGame,
}

_GOALIE_REPORT_MODEL_MAP: dict[str, Any] = {
    "summary": GoalieStatsSummary,
    "advanced": GoalieStatsAdvanced,
    "bios": GoalieStatsBios,
    "savesbystrength": GoalieStatsSavesByStrength,
    "shootout": GoalieStatsShootout,
    "startedvsrelieved": GoalieStatsStartedVsRelieved,
}

_TEAM_REPORT_MODEL_MAP: dict[str, Any] = {
    "summary": TeamStatsSummary,
    "faceoffpercentages": TeamStatsFaceoffPercentages,
    "faceoffwins": TeamStatsFaceoffWins,
    "goalsagainstbystrength": TeamStatsGoalsAgainstByStrength,
    "goalsforbystrength": TeamStatsGoalsForByStrength,
    "goalsleaders": TeamStatsGoalsLeaders,
    "powerplay": TeamStatsPowerplay,
    "penaltykill": TeamStatsPenaltyKill,
    "realtime": TeamStatsRealtime,
    "penalties": TeamStatsPenalties,
    "penaltyshots": TeamStatsPenaltyShots,
    "pointspergame": TeamStatsPointsPerGame,
    "percentages": TeamStatsPercentages,
    "scoretrail": TeamStatsScoretrail,
    "shootout": TeamStatsShootout,
}


def _camel_to_snake(name: str) -> str:
    import re
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _map_api_record(
    record: dict[str, Any],
    season_id: int,
    game_type_id: int,
    entity_key: str,
) -> dict[str, Any]:
    """Flatten a raw API stats record to snake_case with required FK columns."""
    mapped: dict[str, Any] = {
        _camel_to_snake(k): v for k, v in record.items()
    }
    mapped["season_id"] = season_id
    mapped["game_type_id"] = game_type_id
    mapped[entity_key] = record.get("playerId", record.get("teamId"))
    return mapped


async def upsert_skater_stats(
    session: AsyncSession,
    report_type: str,
    season_id: int,
    game_type_id: int,
    records: list[dict[str, Any]],
) -> int:
    """Upsert a batch of skater stats records for a given report type."""
    model = _SKATER_REPORT_MODEL_MAP.get(report_type.lower())
    if model is None:
        logger.warning("unknown skater report type", report_type=report_type)
        return 0

    upserted = 0
    for record in records:
        mapped = _map_api_record(record, season_id, game_type_id, "player_id")
        stmt = (
            pg_insert(model)
            .values(**{k: v for k, v in mapped.items() if hasattr(model, k)})
            .on_conflict_do_update(
                index_elements=["player_id", "season_id", "team_id", "game_type_id"],
                set_={
                    k: v
                    for k, v in mapped.items()
                    if k not in ("player_id", "season_id", "team_id", "game_type_id", "id")
                    and hasattr(model, k)
                },
            )
        )
        await session.execute(stmt)
        upserted += 1

    logger.debug(
        "upserted skater stats",
        report=report_type,
        season=season_id,
        game_type=game_type_id,
        count=upserted,
    )
    return upserted


async def upsert_goalie_stats(
    session: AsyncSession,
    report_type: str,
    season_id: int,
    game_type_id: int,
    records: list[dict[str, Any]],
) -> int:
    """Upsert a batch of goalie stats records for a given report type."""
    model = _GOALIE_REPORT_MODEL_MAP.get(report_type.lower())
    if model is None:
        logger.warning("unknown goalie report type", report_type=report_type)
        return 0

    upserted = 0
    for record in records:
        mapped = _map_api_record(record, season_id, game_type_id, "player_id")
        stmt = (
            pg_insert(model)
            .values(**{k: v for k, v in mapped.items() if hasattr(model, k)})
            .on_conflict_do_update(
                index_elements=["player_id", "season_id", "team_id", "game_type_id"],
                set_={
                    k: v
                    for k, v in mapped.items()
                    if k not in ("player_id", "season_id", "team_id", "game_type_id", "id")
                    and hasattr(model, k)
                },
            )
        )
        await session.execute(stmt)
        upserted += 1

    logger.debug(
        "upserted goalie stats",
        report=report_type,
        season=season_id,
        game_type=game_type_id,
        count=upserted,
    )
    return upserted


async def upsert_team_stats(
    session: AsyncSession,
    report_type: str,
    season_id: int,
    game_type_id: int,
    records: list[dict[str, Any]],
) -> int:
    """Upsert a batch of team stats records for a given report type."""
    model = _TEAM_REPORT_MODEL_MAP.get(report_type.lower())
    if model is None:
        logger.warning("unknown team report type", report_type=report_type)
        return 0

    upserted = 0
    for record in records:
        mapped = _map_api_record(record, season_id, game_type_id, "team_id")
        stmt = (
            pg_insert(model)
            .values(**{k: v for k, v in mapped.items() if hasattr(model, k)})
            .on_conflict_do_update(
                index_elements=["team_id", "season_id", "game_type_id"],
                set_={
                    k: v
                    for k, v in mapped.items()
                    if k not in ("team_id", "season_id", "game_type_id", "id")
                    and hasattr(model, k)
                },
            )
        )
        await session.execute(stmt)
        upserted += 1

    logger.debug(
        "upserted team stats",
        report=report_type,
        season=season_id,
        game_type=game_type_id,
        count=upserted,
    )
    return upserted

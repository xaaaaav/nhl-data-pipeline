import asyncio
from datetime import date, timedelta
from typing import Any

import structlog

from src.api.client import NHLApiClient
from src.api.handlers import reference, schedule, standings, rosters, players, games
from src.api.handlers.stats import skaters as skater_handlers
from src.api.handlers.stats import goalies as goalie_handlers
from src.api.handlers.stats import teams as team_handlers
from src.config import settings
from src.database import get_session_factory
from src.services import (
    season_service,
    team_service,
    player_service,
    roster_service,
    schedule_service,
    game_service,
    standings_service,
    stats_service,
    draft_service,
)

logger = structlog.get_logger(__name__)

_GAME_TYPES = (2, 3)  # regular season, playoffs


class NHLCrawler:
    def __init__(
        self,
        season_id: int | None = None,
        step: str | None = None,
        requests_per_second: float | None = None,
    ) -> None:
        self._season_id = season_id
        self._step = step
        self._rps = requests_per_second or settings.requests_per_second
        self._session_factory = get_session_factory()

    async def run(self) -> None:
        """Run the full crawl pipeline in dependency order."""
        async with NHLApiClient(self._rps) as client:
            step = self._step

            if step is None or step == "seasons":
                await self._crawl_seasons(client)
            if step is None or step == "franchises":
                await self._crawl_franchises(client)
            if step is None or step == "rosters":
                await self._crawl_rosters(client)
            if step is None or step == "schedule":
                await self._crawl_schedule(client)
            if step is None or step == "games":
                await self._crawl_games(client)
            if step is None or step == "standings":
                await self._crawl_standings(client)
            if step is None or step == "skater_stats":
                await self._crawl_skater_stats(client)
            if step is None or step == "goalie_stats":
                await self._crawl_goalie_stats(client)
            if step is None or step == "team_stats":
                await self._crawl_team_stats(client)
            if step is None or step == "draft":
                await self._crawl_draft(client)

        logger.info("crawl complete")

    async def _get_season_ids(self) -> list[int]:
        async with self._session_factory() as session:
            if self._season_id is not None:
                return [self._season_id]
            return await season_service.get_all_season_ids(session)

    async def _crawl_seasons(self, client: NHLApiClient) -> None:
        logger.info("crawling seasons")
        raw_seasons = await reference.fetch_seasons(client)
        async with self._session_factory() as session:
            for raw in raw_seasons:
                await season_service.upsert_season(session, raw)
            await session.commit()
        logger.info("seasons done", count=len(raw_seasons))

    async def _crawl_franchises(self, client: NHLApiClient) -> None:
        logger.info("crawling franchises")
        raw_franchises = await reference.fetch_franchises(client)
        async with self._session_factory() as session:
            for raw in raw_franchises:
                await team_service.upsert_franchise(session, raw)
            await session.commit()
        logger.info("franchises done", count=len(raw_franchises))

    async def _crawl_rosters(self, client: NHLApiClient) -> None:
        """Crawl rosters for all teams across all seasons."""
        logger.info("crawling rosters")
        season_ids = await self._get_season_ids()

        raw_franchises = await reference.fetch_franchises(client)
        team_abbrevs: list[str] = [f.get("teamAbbrev", "") for f in raw_franchises if f.get("teamAbbrev")]

        for season_id in season_ids:
            for abbrev in team_abbrevs:
                try:
                    roster_data = await rosters.fetch_roster(client, abbrev, season_id)
                    team_id_raw: int | None = None
                    for group in ("forwards", "defensemen", "goalies"):
                        for p in roster_data.get(group, []):
                            pid = p.get("playerId")
                            if pid:
                                async with self._session_factory() as session:
                                    await player_service.upsert_player(session, p)
                                    await session.commit()
                    if team_id_raw is None:
                        continue
                    async with self._session_factory() as session:
                        await roster_service.upsert_roster(
                            session, team_id_raw, season_id, roster_data
                        )
                        await session.commit()
                except Exception as exc:
                    logger.warning(
                        "roster fetch failed",
                        team=abbrev,
                        season=season_id,
                        error=str(exc),
                    )

    async def _crawl_schedule(self, client: NHLApiClient) -> None:
        """Crawl schedule for all known season IDs."""
        logger.info("crawling schedule")
        season_ids = await self._get_season_ids()

        async with self._session_factory() as session:
            # Use club schedule for all active teams
            raw_franchises = await reference.fetch_franchises(client)
            for franchise in raw_franchises:
                abbrev = franchise.get("teamAbbrev", "")
                if not abbrev:
                    continue
                try:
                    sched = await schedule.fetch_club_season_schedule(client, abbrev)
                    await schedule_service.process_schedule_response(session, sched)
                except Exception as exc:
                    logger.warning("schedule fetch failed", team=abbrev, error=str(exc))
            await session.commit()
        logger.info("schedule done")

    async def _crawl_games(self, client: NHLApiClient) -> None:
        """Crawl boxscore + play-by-play for games needing fetch."""
        logger.info("crawling games")
        async with self._session_factory() as session:
            game_ids = await game_service.get_game_ids_needing_fetch(session)

        logger.info("games to fetch", count=len(game_ids))
        for game_id in game_ids:
            try:
                boxscore_data = await games.fetch_boxscore(client, game_id)
                pbp_data = await games.fetch_play_by_play(client, game_id)
                async with self._session_factory() as session:
                    await game_service.upsert_game(session, boxscore_data)
                    await game_service.upsert_boxscore(session, game_id, boxscore_data)
                    events: list[dict[str, Any]] = pbp_data.get("plays", [])
                    if events:
                        await game_service.upsert_play_by_play(session, game_id, events)
                    await session.commit()
            except Exception as exc:
                logger.warning("game fetch failed", game_id=game_id, error=str(exc))

        logger.info("games done")

    async def _crawl_standings(self, client: NHLApiClient) -> None:
        """Crawl current standings for each date in the regular season."""
        logger.info("crawling standings")
        today = str(date.today())
        try:
            standing_data = await standings.fetch_standings(client, today)
            async with self._session_factory() as session:
                for entry in standing_data.get("standings", []):
                    team_id: int = entry.get("teamId", 0)
                    if team_id:
                        await standings_service.upsert_standing(
                            session, entry, today, team_id
                        )
                await session.commit()
        except Exception as exc:
            logger.warning("standings fetch failed", date=today, error=str(exc))
        logger.info("standings done")

    async def _crawl_skater_stats(self, client: NHLApiClient) -> None:
        """Crawl all skater stat report types for all seasons."""
        logger.info("crawling skater stats")
        season_ids = await self._get_season_ids()

        for season_id in season_ids:
            for game_type_id in _GAME_TYPES:
                for report_type in skater_handlers.SKATER_REPORT_TYPES:
                    try:
                        records = await skater_handlers.fetch_all_skater_stats(
                            client, report_type, season_id, game_type_id
                        )
                        async with self._session_factory() as session:
                            await stats_service.upsert_skater_stats(
                                session, report_type, season_id, game_type_id, records
                            )
                            await session.commit()
                    except Exception as exc:
                        logger.warning(
                            "skater stats fetch failed",
                            report=report_type,
                            season=season_id,
                            error=str(exc),
                        )
        logger.info("skater stats done")

    async def _crawl_goalie_stats(self, client: NHLApiClient) -> None:
        """Crawl all goalie stat report types for all seasons."""
        logger.info("crawling goalie stats")
        season_ids = await self._get_season_ids()

        for season_id in season_ids:
            for game_type_id in _GAME_TYPES:
                for report_type in goalie_handlers.GOALIE_REPORT_TYPES:
                    try:
                        records = await goalie_handlers.fetch_all_goalie_stats(
                            client, report_type, season_id, game_type_id
                        )
                        async with self._session_factory() as session:
                            await stats_service.upsert_goalie_stats(
                                session, report_type, season_id, game_type_id, records
                            )
                            await session.commit()
                    except Exception as exc:
                        logger.warning(
                            "goalie stats fetch failed",
                            report=report_type,
                            season=season_id,
                            error=str(exc),
                        )
        logger.info("goalie stats done")

    async def _crawl_team_stats(self, client: NHLApiClient) -> None:
        """Crawl all team stat report types for all seasons."""
        logger.info("crawling team stats")
        season_ids = await self._get_season_ids()

        for season_id in season_ids:
            for game_type_id in _GAME_TYPES:
                for report_type in team_handlers.TEAM_REPORT_TYPES:
                    try:
                        records = await team_handlers.fetch_all_team_stats(
                            client, report_type, season_id, game_type_id
                        )
                        async with self._session_factory() as session:
                            await stats_service.upsert_team_stats(
                                session, report_type, season_id, game_type_id, records
                            )
                            await session.commit()
                    except Exception as exc:
                        logger.warning(
                            "team stats fetch failed",
                            report=report_type,
                            season=season_id,
                            error=str(exc),
                        )
        logger.info("team stats done")

    async def _crawl_draft(self, client: NHLApiClient) -> None:
        """Crawl draft picks for all known seasons."""
        logger.info("crawling draft")
        season_ids = await self._get_season_ids()
        draft_years = sorted({int(str(s)[:4]) for s in season_ids})

        for draft_year in draft_years:
            try:
                picks = await reference.fetch_draft(client, draft_year)
                async with self._session_factory() as session:
                    await draft_service.upsert_draft(session, picks)
                    await session.commit()
            except Exception as exc:
                logger.warning(
                    "draft fetch failed", year=draft_year, error=str(exc)
                )
        logger.info("draft done")

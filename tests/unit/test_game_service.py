"""Tests for game_service — upsert logic and routing to PBP detail tables."""
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from src.services.game_service import (
    get_game_ids_needing_fetch,
    upsert_boxscore,
    upsert_play_by_play,
)


class TestUpsertBoxscore:
    @pytest.mark.asyncio
    async def test_extracts_home_away_stats(self) -> None:
        raw = {
            "homeTeam": {
                "id": 10,
                "sog": 32,
                "hits": 22,
                "blockedShots": 12,
                "powerPlayGoals": 2,
                "powerPlayConversions": 5,
                "faceoffWinningPctg": 52.3,
                "giveaways": 8,
                "takeaways": 10,
                "pim": 6,
            },
            "awayTeam": {
                "id": 20,
                "sog": 28,
                "hits": 18,
                "blockedShots": 9,
                "powerPlayGoals": 1,
                "powerPlayConversions": 3,
                "faceoffWinningPctg": 47.7,
                "giveaways": 5,
                "takeaways": 7,
                "pim": 4,
            },
        }

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = MagicMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        captured_values: dict = {}

        with patch("src.services.game_service.pg_insert") as mock_insert:
            mock_stmt = MagicMock()
            mock_stmt.on_conflict_do_update.return_value = mock_stmt
            mock_stmt.returning.return_value = mock_stmt

            def capture_values(**kwargs):  # type: ignore[no-untyped-def]
                captured_values.update(kwargs)
                return mock_stmt

            mock_stmt.values = MagicMock(side_effect=capture_values)
            mock_insert.return_value = mock_stmt

            await upsert_boxscore(mock_session, game_id=12345, data=raw)

        assert captured_values["home_shots"] == 32
        assert captured_values["away_shots"] == 28
        assert captured_values["home_faceoff_pct"] == 52.3
        assert captured_values["raw"] == raw


class TestGetGameIdsNeedingFetch:
    @pytest.mark.asyncio
    async def test_returns_non_final_game_ids(self) -> None:
        mock_session = AsyncMock()

        # First execute: not-final game IDs
        not_final_result = MagicMock()
        not_final_result.scalars.return_value.all.return_value = [111, 222]

        # Second execute: final game IDs
        final_result = MagicMock()
        final_result.scalars.return_value.all.return_value = [333, 444]

        # Third execute: existing boxscore IDs
        boxscore_result = MagicMock()
        boxscore_result.scalars.return_value.all.return_value = [333]

        mock_session.execute = AsyncMock(
            side_effect=[not_final_result, final_result, boxscore_result]
        )

        result = await get_game_ids_needing_fetch(mock_session)

        # 111, 222 (not final) + 444 (final but no boxscore)
        assert set(result) == {111, 222, 444}

    @pytest.mark.asyncio
    async def test_excludes_final_games_with_boxscore(self) -> None:
        mock_session = AsyncMock()

        not_final_result = MagicMock()
        not_final_result.scalars.return_value.all.return_value = []

        final_result = MagicMock()
        final_result.scalars.return_value.all.return_value = [100, 200]

        boxscore_result = MagicMock()
        boxscore_result.scalars.return_value.all.return_value = [100, 200]

        mock_session.execute = AsyncMock(
            side_effect=[not_final_result, final_result, boxscore_result]
        )

        result = await get_game_ids_needing_fetch(mock_session)

        assert result == []


class TestUpsertPlayByPlay:
    @pytest.mark.asyncio
    async def test_routes_goal_to_pbp_goals(self) -> None:
        events = [
            {
                "eventId": 1,
                "typeDescKey": "goal",
                "periodDescriptor": {"number": 1, "periodType": "REG"},
                "timeInPeriod": "05:00",
                "timeRemaining": "15:00",
                "details": {
                    "scoringPlayerId": 100,
                    "assist1PlayerId": 200,
                    "shotType": "wrist",
                    "strength": "ev",
                },
            }
        ]

        mock_session = AsyncMock()
        event_result = MagicMock()
        event_result.scalar_one.return_value = 42
        detail_result = MagicMock()
        mock_session.execute = AsyncMock(side_effect=[event_result, detail_result])

        with patch("src.services.game_service.pg_insert") as mock_insert:
            mock_stmt = MagicMock()
            mock_stmt.on_conflict_do_update.return_value = mock_stmt
            mock_stmt.on_conflict_do_nothing.return_value = mock_stmt
            mock_stmt.returning.return_value = mock_stmt
            mock_stmt.values.return_value = mock_stmt
            mock_insert.return_value = mock_stmt

            await upsert_play_by_play(mock_session, game_id=999, events=events)

        # pg_insert should have been called for the base event and for PbpGoal
        from src.models.play_by_play import PbpGoal, PlayByPlayEvent

        calls = [c[0][0] for c in mock_insert.call_args_list]
        assert PlayByPlayEvent in calls
        assert PbpGoal in calls

    @pytest.mark.asyncio
    async def test_routes_hit_to_pbp_hits(self) -> None:
        events = [
            {
                "eventId": 2,
                "typeDescKey": "hit",
                "periodDescriptor": {"number": 2, "periodType": "REG"},
                "timeInPeriod": "10:00",
                "timeRemaining": "10:00",
                "details": {"hittingPlayerId": 50, "hitteePlayerId": 60},
            }
        ]

        mock_session = AsyncMock()
        event_result = MagicMock()
        event_result.scalar_one.return_value = 10
        detail_result = MagicMock()
        mock_session.execute = AsyncMock(side_effect=[event_result, detail_result])

        with patch("src.services.game_service.pg_insert") as mock_insert:
            mock_stmt = MagicMock()
            mock_stmt.on_conflict_do_update.return_value = mock_stmt
            mock_stmt.on_conflict_do_nothing.return_value = mock_stmt
            mock_stmt.returning.return_value = mock_stmt
            mock_stmt.values.return_value = mock_stmt
            mock_insert.return_value = mock_stmt

            await upsert_play_by_play(mock_session, game_id=999, events=events)

        from src.models.play_by_play import PbpHit

        calls = [c[0][0] for c in mock_insert.call_args_list]
        assert PbpHit in calls

    @pytest.mark.asyncio
    async def test_unknown_event_type_only_inserts_base(self) -> None:
        """Events with unrecognised type only insert the base event row."""
        events = [
            {
                "eventId": 99,
                "typeDescKey": "unknown-event",
                "periodDescriptor": {"number": 1, "periodType": "REG"},
                "timeInPeriod": "00:00",
                "timeRemaining": "20:00",
                "details": {},
            }
        ]

        mock_session = AsyncMock()
        event_result = MagicMock()
        event_result.scalar_one.return_value = 1
        mock_session.execute = AsyncMock(return_value=event_result)

        with patch("src.services.game_service.pg_insert") as mock_insert:
            mock_stmt = MagicMock()
            mock_stmt.on_conflict_do_update.return_value = mock_stmt
            mock_stmt.on_conflict_do_nothing.return_value = mock_stmt
            mock_stmt.returning.return_value = mock_stmt
            mock_stmt.values.return_value = mock_stmt
            mock_insert.return_value = mock_stmt

            await upsert_play_by_play(mock_session, game_id=999, events=events)

        from src.models.play_by_play import PlayByPlayEvent

        calls = [c[0][0] for c in mock_insert.call_args_list]
        assert calls == [PlayByPlayEvent]

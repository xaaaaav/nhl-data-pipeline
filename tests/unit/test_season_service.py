"""Tests for season_service upsert logic."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.season_service import _format_season_id, upsert_season, get_all_season_ids


class TestFormatSeasonId:
    def test_formats_correctly(self) -> None:
        assert _format_season_id(20232024) == "2023-24"

    def test_formats_early_season(self) -> None:
        assert _format_season_id(19171918) == "1917-18"

    def test_formats_2000s(self) -> None:
        assert _format_season_id(20002001) == "2000-01"


class TestUpsertSeason:
    @pytest.mark.asyncio
    async def test_parses_and_calls_insert(self) -> None:
        raw = {
            "id": 20232024,
            "regularSeasonStartDate": "2023-10-10",
            "regularSeasonEndDate": "2024-04-18",
            "playoffEndDate": "2024-06-24",
        }

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_season = MagicMock()
        mock_result.scalar_one.return_value = mock_season
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch("src.services.season_service.pg_insert") as mock_insert:
            mock_stmt = MagicMock()
            mock_stmt.on_conflict_do_update.return_value = mock_stmt
            mock_stmt.returning.return_value = mock_stmt
            mock_insert.return_value = mock_stmt
            mock_stmt.values.return_value = mock_stmt

            result = await upsert_season(mock_session, raw)

        mock_session.execute.assert_called_once()
        assert result == mock_season

    @pytest.mark.asyncio
    async def test_handles_missing_playoff_end(self) -> None:
        raw = {
            "id": 20042005,
            "regularSeasonStartDate": "2004-10-01",
            "regularSeasonEndDate": "2005-04-30",
            # No playoffEndDate — lockout season
        }

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = MagicMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch("src.services.season_service.pg_insert") as mock_insert:
            mock_stmt = MagicMock()
            mock_stmt.on_conflict_do_update.return_value = mock_stmt
            mock_stmt.returning.return_value = mock_stmt
            mock_stmt.values.return_value = mock_stmt
            mock_insert.return_value = mock_stmt

            # Should not raise even without playoffEndDate
            await upsert_season(mock_session, raw)

        mock_session.execute.assert_called_once()


class TestGetAllSeasonIds:
    @pytest.mark.asyncio
    async def test_returns_sorted_ids(self) -> None:
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [20212022, 20222023, 20232024]
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await get_all_season_ids(mock_session)

        assert result == [20212022, 20222023, 20232024]

    @pytest.mark.asyncio
    async def test_returns_empty_when_no_seasons(self) -> None:
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await get_all_season_ids(mock_session)

        assert result == []

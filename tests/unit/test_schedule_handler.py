"""Tests for schedule API handler."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.handlers.schedule import (
    fetch_club_season_schedule,
    fetch_schedule_by_date,
)


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.get = AsyncMock()
    return client


class TestFetchScheduleByDate:
    @pytest.mark.asyncio
    async def test_returns_raw_response(self, mock_client: MagicMock) -> None:
        expected = {
            "gameWeek": [
                {
                    "date": "2024-01-01",
                    "games": [
                        {"id": 2023020100, "homeTeam": {"id": 10}, "awayTeam": {"id": 20}},
                    ],
                }
            ]
        }
        mock_client.get.return_value = expected

        result = await fetch_schedule_by_date(mock_client, "2024-01-01")

        assert result == expected

    @pytest.mark.asyncio
    async def test_constructs_correct_path(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {}

        await fetch_schedule_by_date(mock_client, "2024-03-15")

        call_args = mock_client.get.call_args
        assert "/schedule/2024-03-15" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_handles_empty_schedule(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"gameWeek": []}

        result = await fetch_schedule_by_date(mock_client, "2024-07-01")

        assert result.get("gameWeek") == []


class TestFetchClubSeasonSchedule:
    @pytest.mark.asyncio
    async def test_returns_schedule_for_team(self, mock_client: MagicMock) -> None:
        expected = {"games": [{"id": 1}]}
        mock_client.get.return_value = expected

        result = await fetch_club_season_schedule(mock_client, "TOR")

        assert result == expected

    @pytest.mark.asyncio
    async def test_includes_team_abbrev_in_path(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {}

        await fetch_club_season_schedule(mock_client, "MTL")

        call_args = mock_client.get.call_args
        assert "MTL" in call_args[0][1]

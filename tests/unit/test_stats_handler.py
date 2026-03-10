"""Tests for stats handler pagination logic."""
from unittest.mock import AsyncMock, MagicMock, call

import pytest

from src.api.handlers.stats.skaters import (
    SKATER_REPORT_TYPES,
    fetch_all_skater_stats,
    fetch_skater_stats,
)


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.get = AsyncMock()
    return client


class TestFetchSkaterStats:
    @pytest.mark.asyncio
    async def test_passes_cayenne_exp(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"data": [], "total": 0}

        await fetch_skater_stats(mock_client, "summary", season_id=20232024, game_type_id=2)

        call_kwargs = mock_client.get.call_args[1]
        params = call_kwargs.get("params", {})
        assert "seasonId=20232024" in params["cayenneExp"]
        assert "gameTypeId=2" in params["cayenneExp"]

    @pytest.mark.asyncio
    async def test_default_pagination_params(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"data": [], "total": 0}

        await fetch_skater_stats(mock_client, "summary", 20232024, 2)

        call_kwargs = mock_client.get.call_args[1]
        params = call_kwargs["params"]
        assert params["start"] == 0
        assert params["limit"] == 100

    @pytest.mark.asyncio
    async def test_custom_pagination(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"data": [], "total": 0}

        await fetch_skater_stats(mock_client, "summary", 20232024, 2, start=100, limit=50)

        call_kwargs = mock_client.get.call_args[1]
        params = call_kwargs["params"]
        assert params["start"] == 100
        assert params["limit"] == 50

    @pytest.mark.asyncio
    async def test_builds_correct_path(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"data": [], "total": 0}

        await fetch_skater_stats(mock_client, "powerplay", 20232024, 2)

        call_args = mock_client.get.call_args
        assert "/skater/powerplay" in call_args[0][1]


class TestFetchAllSkaterStats:
    @pytest.mark.asyncio
    async def test_single_page(self, mock_client: MagicMock) -> None:
        records = [{"playerId": i} for i in range(5)]
        mock_client.get.return_value = {"data": records, "total": 5}

        result = await fetch_all_skater_stats(mock_client, "summary", 20232024, 2)

        assert len(result) == 5
        mock_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_multi_page_pagination(self, mock_client: MagicMock) -> None:
        """Should make multiple calls when total > page_size."""
        page1 = [{"playerId": i} for i in range(3)]
        page2 = [{"playerId": i + 3} for i in range(2)]

        call_responses = [
            {"data": page1, "total": 5},
            {"data": page2, "total": 5},
        ]
        mock_client.get.side_effect = call_responses

        result = await fetch_all_skater_stats(
            mock_client, "summary", 20232024, 2, page_size=3
        )

        assert len(result) == 5
        assert mock_client.get.call_count == 2

    @pytest.mark.asyncio
    async def test_stops_when_data_empty(self, mock_client: MagicMock) -> None:
        """Should stop paginating when data list is empty."""
        mock_client.get.side_effect = [
            {"data": [], "total": 100},  # Unexpectedly empty on first page
        ]

        result = await fetch_all_skater_stats(mock_client, "summary", 20232024, 2)

        assert result == []
        assert mock_client.get.call_count == 1

    @pytest.mark.asyncio
    async def test_second_page_offset(self, mock_client: MagicMock) -> None:
        """Verify that the second page request uses the correct start offset."""
        page1 = [{"playerId": i} for i in range(100)]
        page2 = [{"playerId": i + 100} for i in range(10)]

        mock_client.get.side_effect = [
            {"data": page1, "total": 110},
            {"data": page2, "total": 110},
        ]

        await fetch_all_skater_stats(mock_client, "summary", 20232024, 2, page_size=100)

        second_call = mock_client.get.call_args_list[1]
        params = second_call[1]["params"]
        assert params["start"] == 100


class TestSkaterReportTypes:
    def test_all_expected_report_types_present(self) -> None:
        expected = {
            "summary", "bios", "faceoffpercentages", "faceoffwins",
            "goalsForAgainst", "penalties", "penaltykill", "penaltyShots",
            "powerplay", "puckPossessions", "realtime", "shootout",
            "shottype", "timeonice", "pointspergame",
        }
        assert set(SKATER_REPORT_TYPES) == expected

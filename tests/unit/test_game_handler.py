"""Tests for game API handlers."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.handlers.games import fetch_boxscore, fetch_play_by_play


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.get = AsyncMock()
    return client


SAMPLE_BOXSCORE = {
    "id": 2023020100,
    "season": 20232024,
    "gameType": 2,
    "gameDate": "2024-01-01",
    "gameState": "FINAL",
    "homeTeam": {"id": 10, "score": 3, "sog": 30, "hits": 20},
    "awayTeam": {"id": 20, "score": 1, "sog": 25, "hits": 18},
}

SAMPLE_PBP = {
    "id": 2023020100,
    "plays": [
        {
            "eventId": 1,
            "typeDescKey": "faceoff",
            "periodDescriptor": {"number": 1, "periodType": "REG"},
            "timeInPeriod": "00:00",
            "timeRemaining": "20:00",
            "details": {"winningPlayerId": 1234, "losingPlayerId": 5678},
        },
        {
            "eventId": 2,
            "typeDescKey": "goal",
            "periodDescriptor": {"number": 1, "periodType": "REG"},
            "timeInPeriod": "05:32",
            "timeRemaining": "14:28",
            "details": {
                "scoringPlayerId": 111,
                "assist1PlayerId": 222,
                "shotType": "wrist",
                "strength": "ev",
            },
        },
    ],
}


class TestFetchBoxscore:
    @pytest.mark.asyncio
    async def test_returns_boxscore_data(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = SAMPLE_BOXSCORE

        result = await fetch_boxscore(mock_client, game_id=2023020100)

        assert result["id"] == 2023020100
        assert result["homeTeam"]["score"] == 3

    @pytest.mark.asyncio
    async def test_calls_correct_endpoint(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {}

        await fetch_boxscore(mock_client, game_id=2023020100)

        call_args = mock_client.get.call_args
        assert "2023020100" in call_args[0][1]
        assert "boxscore" in call_args[0][1]


class TestFetchPlayByPlay:
    @pytest.mark.asyncio
    async def test_returns_plays_list(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = SAMPLE_PBP

        result = await fetch_play_by_play(mock_client, game_id=2023020100)

        assert "plays" in result
        assert len(result["plays"]) == 2

    @pytest.mark.asyncio
    async def test_calls_correct_endpoint(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"plays": []}

        await fetch_play_by_play(mock_client, game_id=2023020100)

        call_args = mock_client.get.call_args
        assert "2023020100" in call_args[0][1]
        assert "play-by-play" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_handles_no_plays(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {}

        result = await fetch_play_by_play(mock_client, game_id=9999999)

        assert result == {}

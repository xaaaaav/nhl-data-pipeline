"""Tests for reference API handlers."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.handlers.reference import (
    fetch_countries,
    fetch_draft,
    fetch_franchises,
    fetch_seasons,
)


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.get = AsyncMock()
    return client


class TestFetchSeasons:
    @pytest.mark.asyncio
    async def test_returns_data_list(self, mock_client: MagicMock) -> None:
        seasons_data = [
            {"id": 20222023, "regularSeasonStartDate": "2022-10-07"},
            {"id": 20232024, "regularSeasonStartDate": "2023-10-10"},
        ]
        mock_client.get.return_value = {"data": seasons_data}

        result = await fetch_seasons(mock_client)

        assert result == seasons_data
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_calls_correct_endpoint(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"data": []}

        await fetch_seasons(mock_client)

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert "/season" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_returns_empty_list_when_no_data(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {}

        result = await fetch_seasons(mock_client)

        assert result == []


class TestFetchFranchises:
    @pytest.mark.asyncio
    async def test_returns_franchise_list(self, mock_client: MagicMock) -> None:
        franchise_data = [
            {"franchiseId": 1, "fullName": "Montreal Canadiens", "teamName": "Canadiens"},
            {"franchiseId": 2, "fullName": "Ottawa Senators (original)", "teamName": "Senators"},
        ]
        mock_client.get.return_value = {"data": franchise_data}

        result = await fetch_franchises(mock_client)

        assert len(result) == 2
        assert result[0]["franchiseId"] == 1

    @pytest.mark.asyncio
    async def test_calls_franchise_endpoint(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"data": []}

        await fetch_franchises(mock_client)

        call_args = mock_client.get.call_args
        assert "/franchise" in call_args[0][1]


class TestFetchCountries:
    @pytest.mark.asyncio
    async def test_returns_countries(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"data": [{"id": "CAN"}, {"id": "USA"}]}

        result = await fetch_countries(mock_client)

        assert len(result) == 2
        assert result[0]["id"] == "CAN"


class TestFetchDraft:
    @pytest.mark.asyncio
    async def test_flattens_rounds_to_picks(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {
            "rounds": [
                {
                    "roundNumber": 1,
                    "picks": [
                        {"pickInRound": 1, "overallPick": 1, "playerId": 100},
                        {"pickInRound": 2, "overallPick": 2, "playerId": 101},
                    ],
                },
                {
                    "roundNumber": 2,
                    "picks": [
                        {"pickInRound": 1, "overallPick": 33, "playerId": 200},
                    ],
                },
            ]
        }

        result = await fetch_draft(mock_client, draft_year=2023)

        assert len(result) == 3
        # Each pick should have draftYear injected
        for pick in result:
            assert pick["draftYear"] == 2023

    @pytest.mark.asyncio
    async def test_returns_empty_when_no_rounds(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {}

        result = await fetch_draft(mock_client, draft_year=2023)

        assert result == []

    @pytest.mark.asyncio
    async def test_calls_correct_url(self, mock_client: MagicMock) -> None:
        mock_client.get.return_value = {"rounds": []}

        await fetch_draft(mock_client, draft_year=2022)

        call_args = mock_client.get.call_args
        assert "2022" in call_args[0][1]

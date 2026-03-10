from typing import Any

import structlog

from src.api.client import NHLApiClient

logger = structlog.get_logger(__name__)


async def fetch_seasons(client: NHLApiClient) -> list[dict[str, Any]]:
    """Fetch all NHL seasons from the stats API."""
    data = await client.get(NHLApiClient.STATS_BASE, "/season")
    seasons: list[dict[str, Any]] = data.get("data", [])
    logger.info("fetched seasons", count=len(seasons))
    return seasons


async def fetch_franchises(client: NHLApiClient) -> list[dict[str, Any]]:
    """Fetch all NHL franchises."""
    data = await client.get(NHLApiClient.STATS_BASE, "/franchise")
    franchises: list[dict[str, Any]] = data.get("data", [])
    logger.info("fetched franchises", count=len(franchises))
    return franchises


async def fetch_countries(client: NHLApiClient) -> list[dict[str, Any]]:
    """Fetch all countries from the NHL reference data."""
    data = await client.get(NHLApiClient.STATS_BASE, "/country")
    countries: list[dict[str, Any]] = data.get("data", [])
    logger.info("fetched countries", count=len(countries))
    return countries


async def fetch_config(client: NHLApiClient) -> dict[str, Any]:
    """Fetch NHL API configuration / meta."""
    data = await client.get(NHLApiClient.WEB_BASE, "/config")
    return data


async def fetch_draft(client: NHLApiClient, draft_year: int) -> list[dict[str, Any]]:
    """Fetch draft picks for a given year."""
    data = await client.get(NHLApiClient.WEB_BASE, f"/draft/{draft_year}")
    rounds: list[dict[str, Any]] = data.get("rounds", [])
    picks: list[dict[str, Any]] = []
    for round_data in rounds:
        for pick in round_data.get("picks", []):
            pick["draftYear"] = draft_year
            picks.append(pick)
    logger.info("fetched draft picks", year=draft_year, count=len(picks))
    return picks

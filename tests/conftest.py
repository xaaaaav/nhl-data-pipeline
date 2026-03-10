"""Shared pytest fixtures."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.client import NHLApiClient


@pytest.fixture
def mock_client() -> MagicMock:
    """Return a MagicMock that mimics NHLApiClient with an async get()."""
    client = MagicMock(spec=NHLApiClient)
    client.get = AsyncMock()
    return client


@pytest.fixture
def mock_session() -> AsyncMock:
    """Return an AsyncMock that mimics an AsyncSession."""
    session = AsyncMock()
    # execute returns an AsyncMock whose scalar_one / scalars are also mock-able
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session

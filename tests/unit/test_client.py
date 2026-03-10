"""Tests for NHLApiClient rate limiting, retry, and success paths."""
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.api.client import NHLApiClient, _TokenBucket


class TestTokenBucket:
    @pytest.mark.asyncio
    async def test_first_acquire_no_wait(self) -> None:
        bucket = _TokenBucket(rate=10.0)
        # First acquire should not sleep
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            await bucket.acquire()
        mock_sleep.assert_not_called()

    @pytest.mark.asyncio
    async def test_rapid_acquires_causes_sleep(self) -> None:
        bucket = _TokenBucket(rate=1.0)
        slept: list[float] = []

        async def fake_sleep(t: float) -> None:
            slept.append(t)

        with patch("asyncio.sleep", side_effect=fake_sleep):
            await bucket.acquire()  # consumes the initial token
            await bucket.acquire()  # should need to wait

        assert len(slept) >= 1
        assert slept[0] > 0


class TestNHLApiClientSuccess:
    @pytest.mark.asyncio
    async def test_get_returns_json(self) -> None:
        expected = {"data": [{"id": 1}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            async with NHLApiClient(requests_per_second=100.0) as client:
                result = await client.get(NHLApiClient.STATS_BASE, "/season")

        assert result == expected

    @pytest.mark.asyncio
    async def test_get_builds_correct_url(self) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            async with NHLApiClient(requests_per_second=100.0) as client:
                await client.get(NHLApiClient.WEB_BASE, "/schedule/2024-01-01")

        called_url = mock_get.call_args[0][0]
        assert called_url == "https://api-web.nhle.com/v1/schedule/2024-01-01"

    @pytest.mark.asyncio
    async def test_get_passes_params(self) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        params = {"cayenneExp": "seasonId=20232024"}
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            async with NHLApiClient(requests_per_second=100.0) as client:
                await client.get(NHLApiClient.STATS_BASE, "/skater/summary", params=params)

        called_kwargs = mock_get.call_args[1]
        assert called_kwargs.get("params") == params


class TestNHLApiClientRetry:
    @pytest.mark.asyncio
    async def test_retries_on_429(self) -> None:
        """Client should retry on 429 and eventually succeed."""
        success_response = MagicMock()
        success_response.json.return_value = {"ok": True}
        success_response.status_code = 200
        success_response.raise_for_status = MagicMock()

        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 429
        rate_limit_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "rate limited",
            request=MagicMock(),
            response=rate_limit_response,
        )

        call_count = 0

        async def side_effect(*args, **kwargs):  # type: ignore[no-untyped-def]
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                return rate_limit_response
            return success_response

        with patch("httpx.AsyncClient.get", side_effect=side_effect):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                async with NHLApiClient(requests_per_second=100.0) as client:
                    result = await client.get(NHLApiClient.WEB_BASE, "/test")

        assert result == {"ok": True}
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_retries_on_500(self) -> None:
        """Client should retry on 500 errors."""
        success_response = MagicMock()
        success_response.json.return_value = {"ok": True}
        success_response.status_code = 200
        success_response.raise_for_status = MagicMock()

        server_error_response = MagicMock()
        server_error_response.status_code = 500
        server_error_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "server error",
            request=MagicMock(),
            response=server_error_response,
        )

        call_count = 0

        async def side_effect(*args, **kwargs):  # type: ignore[no-untyped-def]
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                return server_error_response
            return success_response

        with patch("httpx.AsyncClient.get", side_effect=side_effect):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                async with NHLApiClient(requests_per_second=100.0) as client:
                    result = await client.get(NHLApiClient.WEB_BASE, "/test")

        assert result == {"ok": True}
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_raises_after_max_retries(self) -> None:
        """Client should raise after exhausting retries."""
        error_response = MagicMock()
        error_response.status_code = 500
        error_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "server error",
            request=MagicMock(),
            response=error_response,
        )

        async def always_fail(*args, **kwargs):  # type: ignore[no-untyped-def]
            return error_response

        with patch("httpx.AsyncClient.get", side_effect=always_fail):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                with pytest.raises(httpx.HTTPStatusError):
                    async with NHLApiClient(requests_per_second=100.0) as client:
                        await client.get(NHLApiClient.WEB_BASE, "/test")

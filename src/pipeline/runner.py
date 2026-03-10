import asyncio
import logging

import click
import structlog

from src.config import settings
from src.database import get_session_factory
from src.models import Base
from src.services import season_service


def _configure_logging(log_level: str) -> None:
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
    )


@click.group()
def cli() -> None:
    """NHL Data Pipeline CLI."""
    _configure_logging(settings.log_level)


@cli.command()
@click.option(
    "--season",
    "season_id",
    type=int,
    default=None,
    help="Season ID (e.g. 20232024). Omit to crawl all seasons.",
)
@click.option(
    "--step",
    "step",
    type=click.Choice(
        [
            "seasons",
            "franchises",
            "rosters",
            "schedule",
            "games",
            "standings",
            "skater_stats",
            "goalie_stats",
            "team_stats",
            "draft",
        ]
    ),
    default=None,
    help="Run only a specific pipeline step.",
)
@click.option(
    "--rps",
    "requests_per_second",
    type=float,
    default=None,
    help="Override requests-per-second rate limit.",
)
def run(
    season_id: int | None,
    step: str | None,
    requests_per_second: float | None,
) -> None:
    """Run the NHL data pipeline."""
    from src.pipeline.crawler import NHLCrawler

    crawler = NHLCrawler(
        season_id=season_id,
        step=step,
        requests_per_second=requests_per_second,
    )
    asyncio.run(crawler.run())


@cli.command()
def status() -> None:
    """Print pipeline status (season counts, game counts)."""

    async def _status() -> None:
        factory = get_session_factory()
        async with factory() as session:
            season_ids = await season_service.get_all_season_ids(session)
            click.echo(f"Seasons stored: {len(season_ids)}")
            if season_ids:
                click.echo(f"  Oldest: {season_ids[0]}")
                click.echo(f"  Newest: {season_ids[-1]}")

    asyncio.run(_status())


if __name__ == "__main__":
    cli()

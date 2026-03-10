from typing import Any

from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


async def upsert_record(
    session: AsyncSession,
    model: type[Base],
    data: dict[str, Any],
    conflict_columns: list[str],
) -> None:
    """Generic upsert helper using PostgreSQL INSERT ... ON CONFLICT DO UPDATE.

    Args:
        session: Active async SQLAlchemy session.
        model: SQLAlchemy model class.
        data: Dict of column values to insert/update.
        conflict_columns: Column names that form the conflict target.
    """
    mapper = inspect(model)
    valid_columns = {col.key for col in mapper.columns}
    filtered: dict[str, Any] = {k: v for k, v in data.items() if k in valid_columns}

    stmt = pg_insert(model).values(**filtered)
    update_dict = {k: stmt.excluded[k] for k in filtered if k not in conflict_columns}

    if update_dict:
        stmt = stmt.on_conflict_do_update(
            index_elements=conflict_columns,
            set_=update_dict,
        )
    else:
        stmt = stmt.on_conflict_do_nothing(index_elements=conflict_columns)

    await session.execute(stmt)

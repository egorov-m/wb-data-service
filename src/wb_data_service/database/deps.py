from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from wb_data_service.database.core import get_session, engine, Base


async def get_db():
    session: AsyncSession = get_session()
    async with session.begin() as transaction:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db)]


async def db_metadata_create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

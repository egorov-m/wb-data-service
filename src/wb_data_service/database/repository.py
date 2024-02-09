from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

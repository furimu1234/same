from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
import os, asyncio
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

load_dotenv()
DATABASE = os.getenv("DATABASE")

m = MetaData(schema="public")

engine = create_async_engine(DATABASE, echo=True)

Base = automap_base(bind=engine, metadata=m)

session: AsyncSession = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, autocommit=False
)

Session = async_scoped_session(session, asyncio.current_task)

__all__ = ["DB", "Base", "session", "engine"]

from contextlib import asynccontextmanager


@asynccontextmanager
async def session_scope():
    async with Session() as ses:
        yield ses
        try:
            await ses.commit()
        except:
            await ses.rollback()


class DB:
    async def execute(self, query):
        async with session_scope() as session:

            result = await session.execute(query)

            return result

    async def _fetch(self, query):
        try:
            return (
                (await self.execute(query)).scalar()
                if await self.execute(query)
                else None
            )

        except:
            raise

    async def _fetchs(self, query) -> list:
        try:
            return (
                (await self.execute(query)).scalars().all()
                if await self.execute(query)
                else None
            )
        except:
            raise

    async def _insert(self, table):
        async with session_scope() as session:
            session.add(table)

    async def _update(self, table):
        async with session_scope() as session:
            session.add(table)

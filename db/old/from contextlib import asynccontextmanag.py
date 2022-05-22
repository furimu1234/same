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

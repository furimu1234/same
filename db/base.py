from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os, asyncpg

load_dotenv()

DB_DSN = os.environ.get("DB")

__all__ = ("session_scope",)


@asynccontextmanager
async def session_scope():
    async with asyncpg.create_pool(
        DB_DSN, command_timeout=60, min_size=1, max_size=1
    ) as pool:
        async with pool.acquire() as con:
            connect: asyncpg.Connection = con
            yield connect

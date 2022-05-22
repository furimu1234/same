from . import models
from .base import session_scope


__all__ = ("Profile",)


class Profile:
    def __init__(self) -> None:
        self.table = "info.profile"

    async def fetch(self, guild_id: int):
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where server_id = $1", guild_id
            )

            if data:
                return models.info.Profile(**data)

    async def insert(self, guild_id):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (server_id) values ($1)", guild_id
            )

    async def update_boy_id(self, channel_id: int, guild_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set boy_id=$1 where serve_idr=$2",
                channel_id,
                guild_id,
            )

    async def update_girl_id(self, channel_id: int, guild_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set girl_id=$1 where serve_idr=$2",
                channel_id,
                guild_id,
            )

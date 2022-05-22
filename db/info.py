from . import models
from .base import session_scope


__all__ = ("Users", "Role")


class Users:
    def __init__(self) -> None:
        self.table = "info.users"

    async def fetch(self, user_id) -> models.info.Users:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where user_id = $1", user_id
            )

            if data:
                return models.info.Users(**data)

    async def insert(self, user_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (user_id) values ($1)", user_id
            )

    async def update_user_name(self, user_name: str, user_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set user_name=$1 where user_id=$2",
                user_name,
                user_id,
            )

    async def update_gender(self, gender: str, user_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set gender=$1 where user_id=$2",
                gender,
                user_id,
            )

    async def update_guild_id(self, guild_id: int, user_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set guild_id=$1 where user_id=$2",
                guild_id,
                user_id,
            )

    async def update_guild_name(self, guild_name: str, user_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set guild_name=$1 where user_id=$2",
                guild_name,
                user_id,
            )


class Role:
    def __init__(self) -> None:
        self.table = "info.role"

    async def fetch(self, server_id) -> models.info.Role:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where server = $1", server_id
            )

            if data:
                return models.info.Role(**data)

    async def insert(self, server_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (server) values ($1)", server_id
            )

    async def update_boy(self, role_id: int, server_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set boy=$1 where server=$2",
                role_id,
                server_id,
            )

    async def update_girl(self, role_id: int, server_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set girl=$1 where server=$2",
                role_id,
                server_id,
            )

    async def update_bot(self, role_id: int, server_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set bot = array_append(bot, $1) where server = $2",
                role_id,
                server_id,
            )

    async def update_admin(self, role_id: int, server_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set admin = array_append(admin, $1) where server = $2",
                role_id,
                server_id,
            )

    async def update_event(self, role_id: int, server_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set eventer = array_append(eventer, $1) where server = $2",
                role_id,
                server_id,
            )

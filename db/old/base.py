from sqlalchemy.future import select

from sqlalchemy import *
from sqlalchemy.orm import *

from .sql import DB
from . import models

__all__ = ("Users", "GuildUsers", "Profile")


class Users(DB):
    def __init__(self):
        super().__init__()
        self.table = models.Users

    async def fetch(self, user_id: int) -> models.Users:
        q = select(self.table).where(self.table.user_id == user_id)

        return await self._fetch(q)

    async def insert(self, user_id: int, user_name: str, gender: str, guild=None):
        table = self.table()
        table.user_id = user_id
        table.user_name = user_name
        table.gender = gender
        table.guild_id = guild.id
        table.guild_name = guild.name

        await self._insert(table)

    async def update_user_name(self, user_name: str, user_id: int):
        result = await self.fetch(user_id)

        result.user_name = user_name

        await self._update(result)


class GuildUsers(DB):
    def __init__(self):
        super().__init__()
        self.table = models.GuildUsers

    async def fetch(self, user_id: int) -> models.GuildUsers:
        q = select(self.table).where(self.table.id == user_id)

        return await self._fetch(q)

    async def insert(self, server_id: int, user_id: int, display_name: str):
        table = self.table()
        table.server_id = server_id
        table.user_id = user_id
        table.user_display = display_name

        await self._insert(table)

    async def update_user_display_(self, user_display: str, user_id: int):
        result = await self.fetch(user_id)

        result.user_display = user_display

        await self._update(result)


class Profile(DB):
    def __init__(self):
        super().__init__()
        self.table: models.Profile = models.Profile

    async def fetch(self, server_id: int) -> models.Profile:
        q = select(self.table).where(self.table.server_id == server_id)

        return await self._fetch(q)

    async def insert(self, server_id: int):
        table = self.table()
        table.server_id = server_id

        await self._insert(table)

    async def update_boy_id(self, boy_id: int, server_id: int):
        result = await self.fetch(server_id)

        result.boy_id = boy_id

        await self._update(result)

    async def update_girl_id(self, girl_id: int, server_id: int):
        result = await self.fetch(server_id)

        result.girl_id = girl_id

        await self._update(result)

from sqlalchemy.future import select

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm.attributes import flag_modified
from .sql import DB
from . import models

from datetime import datetime

__all__ = ("Tier", "Stats", "Role", "Log")


class Role(DB):
    def __init__(self):
        super().__init__()

        self.table = models.RoleModels

    async def fetch(self, server_id: int) -> models.RoleModels:
        q = select(self.table).where(self.table.server == server_id)

        result = await self._fetch(q)

        return result

    async def insert(self, server_id: int):
        table = self.table()
        table.server = server_id

        await self._insert(table)

    async def update_boy(self, role_id: int, server_id: int):
        result = await self.fetch(server_id)
        result.boy = role_id
        await self._update(result)

    async def update_girl(self, role_id: int, server_id: int):
        result = await self.fetch(server_id)
        result.girl = role_id
        await self._update(result)

    async def update_bot(self, role_id: int | list, server_id: int):
        result = await self.fetch(server_id)

        if result is None:
            result.bot = []

        if isinstance(role_id, int):
            if role_id not in result.bot:
                result.bot.append(role_id)
        else:
            for _role_id in role_id:
                if _role_id not in result.bot:
                    result.bot.append(_role_id)

        flag_modified(result, "bot")

        await self._update(result)

    async def update_admin(self, role_id: int | list, server_id: int):
        result = await self.fetch(server_id)

        if result is None:
            result.admin = []

        if isinstance(role_id, int):
            if role_id not in result.admin:
                result.admin.append(role_id)
        else:
            for _role_id in role_id:
                if _role_id not in result.admin:
                    result.admin.append(_role_id)

        flag_modified(result, "admin")

        await self._update(result)

    async def update_eventer(self, role_id: int | list, server_id: int):
        result = await self.fetch(server_id)

        if result is None:
            result.eventer = []

        if isinstance(role_id, int):
            if role_id not in result.eventer:
                result.eventer.append(role_id)
        else:
            for _role_id in role_id:
                if _role_id not in result.eventer:
                    result.eventer.append(_role_id)

        flag_modified(result, "eventer")

        await self._update(result)

    async def update_edited_at(self, edited_at: datetime, server_id: int):
        result = await self.fetch(server_id)
        result.edited_at = edited_at
        await self._update(result)


class Tier(DB):
    def __init__(self):
        super().__init__()

        self.table: models.TierModels = models.TierModels

    async def fetch_server(self, server_id):
        q = select(self.table).where(self.table.server == server_id)

        result = await self._fetch(q)
        return result

    async def fetch_member(self, member_id):
        q = select(self.table).where(self.table.member == member_id)

        result = await self._fetch(q)
        return result

    async def insert_server(self, server_id):
        table = self.table()
        table.server = server_id

        await self._insert(table)

    async def insert_member(self, member_id):
        table = self.table()
        table.member = member_id

        await self._insert(table)

    async def delete_server(self, server_id):
        q = select(self.table).where(self.table.server == server_id)

        result = await self._delete(q)
        return result

    async def delete_member(self, member_id):
        q = select(self.table).where(self.table.member == member_id)

        result = await self._delete(q)
        return result


class Stats(DB):
    def __init__(self):
        super().__init__()

        self.table: models.StatsModels = models.StatsModels

    async def fetch(self, channel_id) -> models.StatsModels:
        q = select(self.table).where(self.table.channel == channel_id)
        result: models.StatsModels = await self._fetch(q)
        return result

    async def insert(self, channel_id):
        table = self.table()
        table.channel = channel_id

        await self._insert(table)

    async def is_not_channel(self, channel_id):
        r = await self.fetch(channel_id)

        if r is None or r.channel is None:
            await self.insert_channel(channel_id)

            q = select(self.table).where(self.table.channel == channel_id)

            r = await self._fetch(q)

        return r

    async def update_name_edited_at(self, name_edited_at, channel_id):
        r = await self.is_not_channel(channel_id)

        r.name_edited_at = name_edited_at

        await self._update(r)

    async def update(self, channel_id, opt, name):
        await self.update_opt(opt, channel_id)
        await self.update_vcname(name, channel_id)

    async def delete(self, channel_id):
        q = select(self.table).where(self.table.channel == channel_id)

        await self._delete(q)


class Log(DB):
    def __init__(self) -> None:
        super().__init__()

        self.table: models.Log = models.Log

    async def fetch(self, server_id: int, _type: str) -> models.Log:
        q = (
            select(self.table)
            .where(self.table.server_id == server_id)
            .where(self.table.type == _type)
        )

        result = await self._fetch(q)

        return result

    async def insert(self, server_id: int, channel_id: int, _type: str):
        table = self.table()
        table.server_id = server_id
        table.channel = channel_id
        table.type = _type

        await self._insert(table)

    async def update_enable(self, enable: bool, server_id: int, _type: str):
        result = await self.fetch(server_id, _type)
        result.enable = enable
        await self._update(result)

    async def update_channel(self, channel_id: int, server_id: int, _type: str):
        result = await self.fetch(server_id, _type)
        result.channel_id = channel_id
        await self._update(result)


class Check_Bot(DB):
    def __init__(self):
        super().__init__()

        self.table: models.Check_Bot = models.Check_Bot

    async def fetch(self, server_id: int) -> models.Check_Bot:
        q = select(self.table).where(self.table.server_id == server_id)

        result = await self._fetch(q)
        return result

    async def insert(self, server_id: int):
        table = self.table()
        table.server_id = server_id

        await self._insert(table)

    async def update_ok(self, ok: str, server_id: int):
        result = await self.fetch(server_id)
        result.ok = ok
        await self._update(result)

    async def update_no(self, no: str, server_id: int):
        result = await self.fetch(server_id)
        result.no = no
        await self._update(result)

from ..sql import DB
from sqlalchemy import select, desc
from sqlalchemy.orm.attributes import flag_modified

from ..models import ext

__all__ = ("Audition",)


class Audition(DB):
    def __init__(self):
        super().__init__()

        self.table: ext.fool.Audition = ext.fool.Audition

    async def fetch_by_message(self, message_id: int) -> ext.fool.Audition:
        query = select([self.table]).where(self.table.message_id == message_id)
        return await self._fetch(query)

    async def fetch_by_user(self, user_id: int) -> ext.fool.Audition:
        query = select([self.table]).where(self.table.user_id == user_id)
        return await self._fetch(query)

    async def insert(self, user_id: int, message_id: int):
        table = self.table()
        table.user_id = user_id
        table.message_id = message_id
        await self._insert(table)

    async def add_common(self, push_member_id, message_id):
        result = await self.fetch_by_message(message_id)

        if push_member_id in result.pushed_member:
            return

        result.pushed_member.append(push_member_id)
        flag_modified(result, "pushed_member")

        result.common += 1
        flag_modified(result, "common")

        await self._update(result)

    async def add_scraps(self, push_member_id, message_id):
        result = await self.fetch_by_message(message_id)

        if push_member_id in result.pushed_member:
            return

        result.pushed_member.append(push_member_id)
        flag_modified(result, "pushed_member")

        result.scraps += 1
        flag_modified(result, "scraps")

        await self._update(result)

    async def add_dont_know(self, push_member_id, message_id):
        result = await self.fetch_by_message(message_id)

        if push_member_id in result.pushed_member:
            return

        result.pushed_member.append(push_member_id)
        flag_modified(result, "pushed_member")

        result.dont_know += 1
        flag_modified(result, "dont_know")

        await self._update(result)

    async def add_ng(self, push_member_id, message_id):
        result = await self.fetch_by_message(message_id)

        if push_member_id in result.pushed_member:
            return

        result.pushed_member.append(push_member_id)
        flag_modified(result, "pushed_member")

        result.ng.append(push_member_id)
        flag_modified(result, "ng")

        await self._update(result)

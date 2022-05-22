from sqlalchemy import select, desc
from sqlalchemy.orm.attributes import flag_modified


from .sql import DB
from .models import StatsModel


class Stats_Setting(DB):
    def __init__(self):
        super().__init__()

        self.table: StatsModel = StatsModel

    async def fetch_by_channel(self, channel_id: int) -> StatsModel:
        q = select(self.table).where(self.table.channel_id == channel_id)
        return await self._fetch(q)

    async def fetchs_by_counter_type(self, counte_type: int) -> list[StatsModel]:
        q = select(self.table).where(self.table.counter_type == counte_type)

        return await self._fetchs(q)

    async def insert(self, channel_id: int):
        table = self.table()
        table.channel_id = channel_id

        await self._insert(table)

    async def update_counter_type(self, counte_type: int, channel_id: int):
        result = await self.fetch_by_channel(channel_id)

        result.counter_type = counte_type

        await self._update(result)

    async def update_name(self, name: str, channel_id: int):
        result = await self.fetch_by_channel(channel_id)

        result.name = name

        await self._update(result)

    async def update_role(self, role: int, channel_id: int):
        result = await self.fetch_by_channel(channel_id)

        result.role = role

        await self._update(result)

    async def update_category(self, category: int, channel_id: int):
        result = await self.fetch_by_channel(channel_id)

        result.category = category

        await self._update(result)

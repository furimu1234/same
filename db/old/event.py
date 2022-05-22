from sqlalchemy import select, desc
from sqlalchemy.orm.attributes import flag_modified

from .sql import *
from .models import Event_Panel_Model, Event_Panel_Embed_Model, NCVL_Model

__all__ = (
    "Event_Panel",
    "Event_Panel_Embed",
    "NCVL",
)


class Event_Panel(DB):
    def __init__(self):
        super().__init__()

        self.table: Event_Panel_Model = Event_Panel_Model

    async def fetch_data_by_channel_id(self, channel_id: int) -> Event_Panel_Model:
        q = select(self.table).where(self.table.channel_id == channel_id)

        result = await self._fetch(q)

        return result

    async def fetch_data_by_trigger_id(self, trigger_id: int) -> Event_Panel_Model:
        q = select(self.table).where(self.table.trigger_id == trigger_id)

        result = await self._fetch(q)

        return result

    async def insert(self, trigger_id: int):
        table = self.table()
        table.trigger_id = trigger_id

        await self._insert(table)

    async def update_channel_id(self, channel_id: int, trigger_id: int):
        result = await self.fetch_data_by_trigger_id(trigger_id)
        result.channel_id = channel_id

        await self._update(result)

    async def update_trigger_type(self, trigger_type: int, trigger_id: int):
        result = await self.fetch_data_by_trigger_id(trigger_id)

        result.trigger_type = trigger_type

        await self._update(result)

    async def update_panel_type(self, panel_type: str, trigger_id: int):
        result = await self.fetch_data_by_trigger_id(trigger_id)

        result.panel_type = panel_type

        await self._update(result)


class Event_Panel_Embed(DB):
    def __init__(self):
        super().__init__()

        self.table: Event_Panel_Embed_Model = Event_Panel_Embed_Model

    async def fetch_data_by_channel_id(
        self, channel_id: int
    ) -> Event_Panel_Embed_Model:
        q = select(self.table).where(self.table.channel_id == channel_id)

        result = await self._fetch(q)

        return result

    async def insert(self, channel_id: int):
        table = self.table()

        table.channel_id = channel_id

        await self._insert(table)

    async def update_content(self, content: str, channel_id: int):
        result = await self.fetch_data_by_channel_id(channel_id)

        result.content = content

        await self._update(result)

    async def update_title(self, title: str, channel_id: int):
        result = await self.fetch_data_by_channel_id(channel_id)

        result.title = title

        await self._update(result)

    async def update_description(self, description: str, channel_id: int):

        result = await self.fetch_data_by_channel_id(channel_id)

        result.description = description

        await self._update(result)

    async def update_color(self, color: int, channel_id: int):
        result = await self.fetch_data_by_channel_id(channel_id)

        result.color = color

        await self._update(result)

    async def update_name(self, name: str, channel_id: int):
        result = await self.fetch_data_by_channel_id(channel_id)

        result.name = name

        await self._update(result)

    async def update_icon_display(self, icon_display: bool, channel_id: int):
        result = await self.fetch_data_by_channel_id(channel_id)

        result.icon_display = icon_display

        await self._update(result)


class NCVL(DB):
    def __init__(self):
        super().__init__()

        self.table: NCVL_Model = NCVL_Model

    async def fetch_data_by_guild_id(self, guild_id: int) -> NCVL_Model:
        q = select(self.table).where(self.table.server_id == guild_id)

        result = await self._fetch(q)

        return result

    async def insert(self, guild_id: int):
        table = self.table()

        table.guild_id = guild_id

        await self._insert(table)

    async def add_channel(self, channel_id: int | list[int], guild_id: int):
        result = await self.fetch_data_by_guild_id(guild_id)

        if isinstance(channel_id, int):
            if channel_id not in result.channels:
                result.channels.append(channel_id)
        else:
            for _channel_id in channel_id:
                if _channel_id not in result.channels:
                    result.channels.append(_channel_id)

        flag_modified(result, "channels")

        await self._update(result)

    async def remove_channel(self, channel_id: int, guild_id: int):
        result = await self.fetch_data_by_guild_id(guild_id)

        result.channels.remove(channel_id)

        flag_modified(result, "channels")

        await self._update(result)

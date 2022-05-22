from .base import BaseSheet
from enums import NCVL as NCVL_Range

from ..event import Event_Panel, Event_Panel_Embed, NCVL

__all__ = (
    "Sheet_Event",
    "Sheet_NCVL",
)


class Sheet_Event(BaseSheet):
    def __init__(self):
        super().__init__()
        self.alphabets = [
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]

        self.event_panel = Event_Panel()
        self.event_embed = Event_Panel_Embed()

    async def fetch_all_data(self, guild_id: int) -> None:

        """
        coroutine
        """

        if not (bookinfo := await self.getbook(str(guild_id))):
            return None

        for alphabet in self.alphabets:

            payload = {
                "type": "get",
                "bookid": bookinfo["id"],
                "filename": str(guild_id),
                "sheetname": "イベントパネル",
                "range": f"{alphabet}2:{alphabet}",
            }

            data = await self.request(payload)

            try:
                channel_id = int(data[3])
                trigger_id = int(data[2])
            except:
                break

            if not await self.event_panel.fetch_data_by_trigger_id(trigger_id):
                await self.event_panel.insert(trigger_id)

            await self.event_panel.update_channel_id(channel_id, trigger_id)
            await self.event_panel.update_panel_type(data[1], trigger_id)
            await self.event_panel.update_trigger_type(int(data[0]), trigger_id)

            if not await self.event_embed.fetch_data_by_channel_id(channel_id):
                await self.event_embed.insert(channel_id)

            await self.event_embed.update_content(data[7], channel_id)

            if data[9] != "":
                await self.event_embed.update_title(data[9], channel_id)

            if data[10] != "":
                await self.event_embed.update_description(data[10], channel_id)

            if data[11] != "":
                await self.event_embed.update_color(
                    int(data[11][1:], base=16), channel_id
                )

            if data[13] != "":
                await self.event_embed.update_name(data[13], channel_id)

            if data[14] != "":
                await self.event_embed.update_icon_display(data[14] == "する", channel_id)


"""class Sheet_Vc_Role(BaseSheet):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        if not self.bot.spreadsheet.get("event"):
            self.bot.spreadsheet["event"] = {}

        if not self.bot.spreadsheet["event"].get("vc_role"):
            self.bot.spreadsheet["event"]["vc_role"] = {}

    async def get_vc_role_data(self, _channel_id: int, **kwargs):

        load_cache = kwargs.pop("load_cache", True)
        auto_cache = kwargs.pop("auto_cache", True)

        channel_id = str(_channel_id)

        channel = self.bot.get_channel(_channel_id)

        guild = channel.guild

        guild_id = str(guild.id)

        if load_cache:
            if cache := self.bot.spreadsheet["vc_role"].get(channel_id):
                return cache

        if not (bookinfo := await self.getbook(guild_id)):
            return None

        payload = {
            "type": "get",
            "bookid": bookinfo["id"],
            "filename": bookinfo["url"],
            "sheetname": "VC_ロール",
            "range": str(Vc_Role.TRIGGER_ID),
        }

        ids = await self.request(payload)

        for alphabet, trigger_id in zip(self.alphabets, ids):

            if trigger_id == "":
                continue

            if trigger_id == channel_id:
                break

        else:
            alphabet = "C"

        payload = {
            "type": "get",
            "bookid": bookinfo["id"],
            "filename": bookinfo["url"],
            "sheetname": "VCロール",
            "range": f"{alphabet}2:{alphabet}",
        }

        data = await self.request(payload)

        if auto_cache:
            self.cache(channel_id, "event", "vc_role", data)

        return data

    # TODO: VCロールの処理続きを書く
"""


class Sheet_NCVL(BaseSheet):
    def __init__(self):
        super().__init__()
        self.db_ncvl = NCVL()

    async def fetch_all_data(self, guild_id: int) -> None:

        if not (bookinfo := await self.getbook(str(guild_id))):
            return None

        payload = {
            "type": "get",
            "bookid": bookinfo["id"],
            "filename": str(guild_id),
            "sheetname": "椅子",
            "range": str(NCVL_Range.CHANNELS),
        }

        datas = await self.request(payload)

        if not await self.db_ncvl.fetch_data_by_guild_id(guild_id):
            await self.db_ncvl.insert(guild_id)

        for data in datas:
            if data == "":
                continue

            await self.db_ncvl.add_channel(int(data), guild_id)

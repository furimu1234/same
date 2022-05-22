from db.models import channel
from .base import BaseSheet
from typing import List

from enums import BackRange, BackRecruiti, QM

from .. import back

__all__ = ("GBack_Two", "GBack_Recruiti", "GQM")


class GBack_Two(BaseSheet):
    def __init__(self):
        super().__init__()
        self.back_panel = back.Base_Panel()
        self.open_panel = back.Open_Panel_Embed()
        self.label_panel = back.Label_Panel_Embed()

    async def fetch_all_data(self, guild_id: str) -> str:
        if not (bookinfo := await self.getbook(str(guild_id))):
            return "スプレッドシート未作成"

        datas = []

        for i in ["C", "D", "E", "F", "G"]:
            _range = f"{i}2:{i}61"
            payload = {
                "type": "get",
                "bookid": bookinfo["id"],
                "filename": guild_id,
                "sheetname": "裏2ショット",
                "range": _range,
            }
            data = await self.request(payload)

            try:
                channel_id = int(data[2])
                category_id = int(data[3])
                open_panel_id = int(data[0])
                label_panel_id = int(data[1])
                text_type = data[-1] if data[-1] != "" else "テキストチャンネル"

            except ValueError:
                break
            datas.append(channel_id)

            try:
                if not await self.back_panel.fetch_by_channel(channel_id):
                    await self.back_panel.insert(channel_id, guild_id)

                await self.back_panel.update_category_id(category_id, channel_id)
                await self.back_panel.update_open_panel(open_panel_id, channel_id)
                await self.back_panel.update_label_panel(label_panel_id, channel_id)
                await self.back_panel.update_text_type(text_type, channel_id)

                if not await self.open_panel.fetch_by_channel(channel_id):
                    await self.open_panel.insert(channel_id, guild_id)

                await self.open_panel.update_panel_id(open_panel_id, channel_id)
                await self.open_panel.update_title(data[9], channel_id)
                await self.open_panel.update_description(data[10], channel_id)
                await self.open_panel.update_color(
                    int(data[11][1:], base=16), channel_id
                )

                if not await self.label_panel.fetch_by_channel(channel_id):
                    await self.label_panel.insert(channel_id, guild_id)

                await self.label_panel.update_panel_id(label_panel_id, channel_id)
                await self.label_panel.update_field_one_key(data[41], channel_id)
                await self.label_panel.update_field_one_value(data[42], channel_id)
                await self.label_panel.update_field_two_key(data[44], channel_id)
                await self.label_panel.update_field_two_value(data[45], channel_id)
                await self.label_panel.update_field_three_key(data[47], channel_id)
                await self.label_panel.update_field_three_value(data[48], channel_id)
            except:
                import traceback

                traceback.print_exc()

        return "スプレッドシート保存完了"


class GBack_Recruiti(BaseSheet):
    def __init__(self):
        super().__init__()

        self.base_panel = back.Back_Recruiti_Base_Panel()
        self.desc = back.Back_Recruiti_Desc()
        self.panel = back.Back_Recruiti_Panel()
        self.panel_dm = back.Back_Recruiti_DM()

    async def fetch_back_recruiti_all_data_by_guild(
        self, guild_id: int
    ) -> List[List[str]]:
        """
        coroutine

        指定されたサーバーのパネルの設定情報・パネルのメッセージを取得する

        Parameters
        ----------
        guild_id : int
            取得するサーバー

        kwargs: dict
        load_cache: bool -> キャッシュを読み込むか
        auto_cache: bool -> キャッシュを作成するか

        Returns
        -------
        List[List[str]]
        """

        if not (bookinfo := await self.getbook(str(guild_id))):
            return None

        datas = []

        for i in ["C", "D", "E", "F", "G"]:
            _range = f"{i}2:{i}60"
            payload = {
                "type": "get",
                "bookid": bookinfo["id"],
                "filename": guild_id,
                "sheetname": "裏募集",
                "range": _range,
            }
            data = await self.request(payload)

            if data[0] == "":
                break

            datas.append(data)

            try:
                channel_id = int(data[0])
                boy_channel_id = int(data[1])
                girl_channel_id = int(data[2])

                boy_role_id = int(data[3])
                girl_role_id = int(data[4])

                night_boy_role_id = int(data[5])
                nigiht_girl_role = int(data[6])
            except ValueError:
                break

            if not await self.base_panel.fetch_by_channel(channel_id):
                await self.base_panel.insert(channel_id, guild_id)

            await self.base_panel.update_boy_channel(boy_channel_id, channel_id)
            await self.base_panel.update_girl_channel(girl_channel_id, channel_id)

            await self.base_panel.update_boy_role(boy_role_id, channel_id)
            await self.base_panel.update_girl_role(girl_role_id, channel_id)

            await self.base_panel.update_night_boy_role(night_boy_role_id, channel_id)
            await self.base_panel.update_nigiht_girl_role(nigiht_girl_role, channel_id)

            await self.base_panel.update_template(data[8], channel_id)

            if not await self.desc.fetch_by_channel(channel_id):
                await self.desc.insert(channel_id)

            await self.desc.update_title(data[14], channel_id)
            await self.desc.update_description(data[15], channel_id)

            try:
                color = int(data[16][1:], base=16)
                await self.desc.update_color(color, channel_id)
            except:
                pass

            if not await self.panel.fetch_by_channel(channel_id):
                await self.panel.insert(channel_id)

            await self.panel.update_content(data[30], channel_id)
            await self.panel.update_title(data[32], channel_id)
            await self.panel.update_description(data[33], channel_id)

            await self.panel.update_color(data[34], channel_id)

            await self.panel.update_name(data[37], channel_id)
            await self.panel.update_icon_display(data[38], channel_id)

            await self.panel.update_thumbnail_display(data[43], channel_id)

            if not await self.panel_dm.fetch_by_channel(channel_id):
                await self.panel_dm.insert(channel_id)

            await self.panel_dm.update_title(data[48], channel_id)
            await self.panel_dm.update_description(data[49], channel_id)

            try:
                color = int(data[50][1:], base=16)
                await self.panel_dm.update_color(color, channel_id)
            except:
                pass

            await self.panel_dm.update_field_one_key(data[52], channel_id)
            await self.panel_dm.update_field_one_value(data[53], channel_id)

            await self.panel_dm.update_field_two_key(data[55], channel_id)
            await self.panel_dm.update_field_two_value(data[56], channel_id)

        return "OK"

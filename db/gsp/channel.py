from .base import BaseSheet
from typing import List

from db import Stats_Setting


class Sheet_Stats(BaseSheet):
    def __init__(self):
        super().__init__()
        self.channel = Stats_Setting()

    async def fetch_all_datas(self, *, guild_id: int):
        """

        指定されたパネルの設定情報・パネルのメッセージを取得する

        Parameters
        ----------
        channelid : int
            パネルがあるチャンネルのID

        mesid : int
            パネルのメッセージのID

        Returns
        -------
        List[str]
        """

        if not (bookinfo := await self.getbook(str(guild_id))):
            return None

        for i in ["C", "D", "E", "F", "G"]:
            _range = f"{i}2:{i}6"
            payload = {
                "type": "get",
                "bookid": bookinfo["id"],
                "filename": str(guild_id),
                "sheetname": "カウンター",
                "range": _range,
            }
            data = await self.request(payload)

            try:
                channel_id = int(data[1])
            except:
                break

            counter_type = data[0]
            name = data[2]

            if counter_type == "メンバー数":
                counter_type = 1

            elif counter_type == "VC接続人数":
                counter_type = 2

            elif counter_type == "ロールが付いてる人数":
                counter_type = 3

            elif counter_type == "特定のカテゴリー内のVC接続人数":
                counter_type = 4

            elif counter_type == "チャンネル数":
                counter_type = 5

            elif counter_type == "ロール数":
                counter_type = 6

            if not await self.channel.fetch_by_channel(channel_id):
                await self.channel.insert(channel_id)

            await self.channel.update_counter_type(counter_type, channel_id)

            await self.channel.update_name(name, channel_id)

            if counter_type == 3:
                try:
                    role_id = int(data[3])

                    await self.channel.update_role(role_id, channel_id)

                except:
                    continue

            elif counter_type == 4:
                try:
                    category_id = int(data[4])
                    await self.channel.update_category(category_id, channel_id)
                except:
                    continue

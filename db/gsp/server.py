from __future__ import annotations

from .base import BaseSheet

from typing import List, Dict, TypedDict

from enums import BaseRange

from dc import gsp

import db

__all__ = ("Sheet_Profile", "Sheet_Role", "Log", "Check_Bot")


class Sheet_Profile(BaseSheet):
    def __init__(self):
        super().__init__()

        self.profile = db.server.Profile()

    async def fetch_prof_channels(self, guild_id: int) -> None:
        """
        coroutine

        男性プロフィール・女性プロフィールチャンネルを取得する

        Parameters
        ----------
        guild_id : int
            サーバーID (ブックの名前)

        kwargs: dict
            load_cache: bool キャッシュされたのを読み込むか
            auto_cache: bool キャッシュを自動的に作成するか

        Returns
        -------
        Dict[str, TextChannel]

        """

        if not (bookinfo := await self.getbook(str(guild_id))):
            return

        payload = {
            "type": "get",
            "bookid": bookinfo["id"],
            "filename": bookinfo["url"],
            "sheetname": "基本設定",
            "range": str(BaseRange.PROFILE_CHANNELS),
        }

        ids = await self.request(payload)

        if not ids:
            return

        if len(ids) != 2:
            return None

        try:
            boy_id = int(ids[0])
            girl_id = int(ids[1])
        except:
            return

        if not await self.profile.fetch(guild_id):
            await self.profile.insert(guild_id)

        await self.profile.update_boy_id(boy_id, guild_id)
        await self.profile.update_girl_id(girl_id, guild_id)


"""class Sheet_Role(BaseSheet):
    def __init__(self):
        super().__init__()
        self.role = Role()

    async def fetch_roles(self, guild_id: int = None) -> gsp.Role:

        if not (bookinfo := await self.getbook(str(guild_id))):
            return None

        if not await self.role.fetch(guild_id):
            await self.role.insert(guild_id)

        for alphabet in self.alphabets:
            payload = {
                "type": "get",
                "bookid": bookinfo["id"],
                "filename": guild_id,
                "sheetname": "基本設定",
                "range": f"{alphabet}4:{alphabet}8",
            }

            ids = await self.request(payload)

            if ids[0] != "":
                try:
                    role_id = int(ids[0])
                except:
                    continue

                await self.role.update_boy(role_id, guild_id)

            if ids[1] != "":

                try:
                    role_id = int(ids[1])
                except:
                    continue
                await self.role.update_girl(role_id, guild_id)

            if ids[2] != "":
                try:
                    role_id = int(ids[2])
                except:
                    continue
                await self.role.update_bot(role_id, guild_id)

            if ids[3] != "":
                try:
                    role_id = int(ids[3])
                except:
                    continue
                await self.role.update_admin(role_id, guild_id)

            if ids[4] != "":
                try:
                    role_id = int(ids[4])
                except:
                    continue
                await self.role.update_admin(role_id, guild_id)

        return await self.role.fetch(server_id=guild_id)


class Log(BaseSheet):
    def __init__(self):
        super().__init__()

        self.log = db.Log()

    async def fetch_all_data(self, guild_id: int):
        if not (bookinfo := await self.getbook(str(guild_id))):
            return None

        for alphabet in self.alphabets + [
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
        ]:
            payload = {
                "type": "get",
                "bookid": bookinfo["id"],
                "filename": guild_id,
                "sheetname": "ログ",
                "range": f"{alphabet}2:{alphabet}4",
            }

            ids = await self.request(payload)

            print(ids)
            if ids[1] is None or ids[1] == "":
                continue

            if not (await self.log.fetch(guild_id, ids[0])):
                await self.log.insert(guild_id, int(ids[1]), ids[0])

            await self.log.update_channel(int(ids[1]), guild_id, ids[0])

            await self.log.update_enable(
                True if ids[2] == "有効" else False, guild_id, ids[0]
            )


class Check_Bot(BaseSheet):
    def __init__(self):
        super().__init__()

        self.check = db.Check_Bot()

    async def fetch_all_data(self, guild_id: int):
        if not (bookinfo := await self.getbook(str(guild_id))):
            return None

        payload = {
            "type": "get",
            "bookid": bookinfo["id"],
            "filename": guild_id,
            "sheetname": "VCCheck",
            "range": f"C2:C3",
        }

        symbols = await self.request(payload)

        if symbols[0] == "":
            return

        if not await self.check.fetch(guild_id):
            await self.check.insert(guild_id)

        await self.check.update_no(symbols[0], guild_id)
        await self.check.update_ok(symbols[1], guild_id)
"""

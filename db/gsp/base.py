from datetime import timedelta
from aiohttp import ClientSession
from typing import Any, List, Optional, Dict
from colorama import Fore, Style, Back
import json, traceback, aiofiles

__all__ = "BaseSheet"


class BaseSheet:
    def __init__(self):
        self.alphabets = ["C", "D", "E", "F", "G"]

        # デプロイした時のURL
        script_id = (
            "AKfycbwI9e7swFGt4aDFrTNBZvJ6IurRbr5jBQNQ55A8q_9R1coWSg-PjRLQYXmfGy1AzNtj"
        )

        self.headers = {
            "Content-Type": "application/json",
        }

        self.url = f"https://script.google.com/macros/s/{script_id}/exec"

    async def request(self, payload: dict[Any]) -> Optional[List[str]]:
        """
        coroutine

        Parameters
        ----------
        payload: dict[Any]
            payload for google sheet

        Returns
        -------
        Optional[List[str]]
        """
        async with ClientSession() as session:
            async with session.post(
                self.url, data=json.dumps(payload), headers=self.headers
            ) as resp:

                if resp.status == 200:
                    return (await resp.text("utf-8")).split(",")

                else:
                    traceback.print_exc()
                    return None

    async def create(self, guildid: int, email: str) -> str:
        """
        coroutine

        Parameters
        ----------
        guildid: int
            guild id

        email: str
            編集するユーザーのメールアドレス

        Returns
        -------
        str
        """
        guild_id: str = str(guildid)

        if data := await self.getbook(guild_id):
            return data["url"]

        payload = {"type": "create", "gmail": email, "filename": guild_id}

        bookinfos = await self.request(payload)

        bookinfo = bookinfos[0]

        bookid = bookinfo.split(":")[0]
        bookurl = bookinfo.split(":")[1] + ":" + bookinfo.split(":")[2]

        async with aiofiles.open("config/book.json", "r", encoding="utf-8") as f:
            data: dict = json.loads(await f.read())

        data[guild_id] = {"id": bookid, "url": bookurl}

        async with aiofiles.open("config/book.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=4, ensure_ascii=False))

        return bookurl

    async def add_editer(self, _guild_id: int, email: str) -> str:
        """
        coroutine

        Parameters
        ----------
        _guild_id: int
            guild id

        email: str
            編集するユーザーのメールアドレス

        Returns
        -------
        str
        """

        guild_id: str = str(_guild_id)

        book = await self.getbook(guild_id)
        payload = {
            "type": "invite",
            "gmail": email,
            "filename": guild_id,
            "bookid": book["id"],
        }

        url = await self.request(payload)

        return url[0]

    async def getbook(self, guild_id: int) -> Dict:
        """
        coroutine

        Parameters
        ----------
        guild_id: int
            guild id

        Returns
        -------
        Dict
        """

        async with aiofiles.open("config/book.json", "r", encoding="utf-8") as f:
            data: dict = json.loads(await f.read())
        return data.get(str(guild_id))

    def cache(self, object_id: int, parent: str, key: str, value: Any) -> None:
        """
        coroutine

        Parameters
        ----------

        object_id: int
            object id

        parent: str
            parent key

        key: str
            key

        value: Any
            value

        Returns
        -------
        None
        """

        if self.bot:
            self.spreadsheet = self.bot.spreadsheet
        else:
            self.spreadsheet = {}

        if not self.spreadsheet.get(parent):
            self.spreadsheet[parent] = {}

        if not self.spreadsheet[parent].get(key):
            self.spreadsheet[parent][key] = {}

        self.spreadsheet[parent][key][object_id] = value


sheet = BaseSheet()


async def main():
    data = await sheet.create(754680802578792498, "enu7693@gmail.com")
    # data = await sheet.getbook(222222)

    """payload = {
        "type":"get",
        "bookid": data["id"],
        "sheetname": "基本設定",
        "row": 3,
        "col": 3
    }

    a = await sheet.request(payload)
     print(a)
    """


"""import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())"""

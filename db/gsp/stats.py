from .base import BaseSheet
from asyncio import TimeoutError

__all__ = "Sheet_Stats"


class Sheet_Stats(BaseSheet):
    def __init__(self, bot=None):
        super().__init__()

        self.locks = {}

        if not self.bot.spreadsheet.get("stat"):
            self.bot.spreadsheet["stat"] = {}

    def cache(self, key, value):
        self.bot.spreadsheet["stat"][key] = value

    def get_cache(self, **kwargs):

        stats_type = kwargs.pop("stats_type", None)

        if not stats_type: return
        if cache := self.bot.spreadsheet["stat"].get(str(stats_type)):       
            return cache


    async def get_stat_data(self, _guild_id: int, stats_type: str=None, **kwargs):
        """
        coroutine
        """

        load_cache = kwargs.pop("load_cache", True)
        auto_cache = kwargs.pop("auto_cache", True)

        guild_id = str(_guild_id)

        if stats_type:
            _type = str(stats_type)
        else:
            _type = None

        if load_cache:
            if cache := self.bot.spreadsheet["stat"].get(_type):
                #self.debug(f"{_type}: stats cache")
                return cache

        if not (bookinfo := await self.getbook(guild_id)):
            return

        if self.locks.get(_type):
            if self.locks[_type] == True:
                return []

        self.locks[_type] = True

        self.alphabets += [
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

        datas = []

        data_dict = {}

        for alphabet in self.alphabets:
            _range = f"{alphabet}2:{alphabet}"

            payload = {
                "type": "get",
                "bookid": bookinfo["id"],
                "filename": bookinfo["url"],
                "sheetname": "カウンター",
                "range": _range,
            }
            try:
                data = await self.request(payload)
            except TimeoutError:
                self.error(f"{_type}: stats request timeout")
                return

            #self.warning(f"{alphabet} {_type}: stats request")

            if data is None:
                #self.warning(f"{_type}: stats request data None")
                self.cache(_type, [])
                return []

            if data[1] == "":
                break

            if _type and (data[0] != _type):
                continue

            if not _type:
                if not data_dict.get(data[0]):
                    data_dict[data[0]] = []
                
                data_dict[data[0]].append(data)

                self.cache(data[0], data_dict[data[0]])

                #self.debug(f"{data[0]} {data[1]}")

            datas.append(data)

        if auto_cache and _type:
            self.cache(_type, datas)


        self.locks[_type] = False

        return datas

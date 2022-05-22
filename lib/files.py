import json, aiofiles
from numpy import unicode_


class Data:
    def __init__(self):
        self.temp_data = None

    async def temp_save(self, module: str, data: dict) -> None:
        async with aiofiles.open(f"temp/{module}.json", "w", encoding="utf-8") as f:
            await f.write(
                json.dumps(
                    data, indent=4, ensure_ascii=False, cls=SaveDatetimeJSONEncoder
                )
            )

    async def fore_save(self, module: str, data: dict) -> None:
        async with aiofiles.open(f"forever/{module}.json", "w", encoding="utf-8") as f:
            await f.write(
                json.dumps(
                    data, indent=4, ensure_ascii=False, cls=SaveDatetimeJSONEncoder
                )
            )

    async def fore_load(self, module: str, cast_dict: bool = True):
        try:
            async with aiofiles.open(f"forever/{module}.json", encoding="utf-8") as f:
                data = json.loads(await f.read())

            self.temp_data = data
        except OSError:
            await self.fore_save(module, {})
            await self.fore_load(module)

        if cast_dict:
            return self.temp_data

        return self

    async def temp_load(self, module: str, cast_dict: bool = True) -> dict:
        json_path = f"temp/{module}.json"
        try:
            async with aiofiles.open(json_path) as f:
                ff = await f.read()
            data = json.loads(ff)
            self.temp_data = data
        except OSError:
            await self.temp_save(module, {})
            await self.temp_load(module)

        if cast_dict:
            return self.temp_data

        return self

    def get(self, key: str):
        self.temp_data = self.temp_data.get(key)
        return self

    def to_dict(self):
        return self.temp_data

    def __repr__(self):
        return self.temp_data

    def __str__(self):
        return self.temp_data


from json import JSONEncoder


class SaveDatetimeJSONEncoder(JSONEncoder):  # JSONEncoderを継承させる
    def default(self, o):
        if type(o).__name__ == "datetime":  # 値がdatetime型だったら、
            return o.strftime("%Y%m%d-%H%M%S")  # 文字列に変換して返す
        else:
            return o

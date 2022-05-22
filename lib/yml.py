import aiofiles, yaml
from .attrdict import AttrDict

__all__ = ("mes_load",)


async def mes_load(file_name: str):
    async with aiofiles.open(f"mes/{file_name}.yaml", mode="r") as f:
        read = await f.read()
        data = yaml.safe_load(read)

        return AttrDict(data)

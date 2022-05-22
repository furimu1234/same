from discord.ext import commands as c
from discord import Member, Role, Role, Guild, Status, CustomActivity, Object

from dotenv import load_dotenv
import asyncio, os

from lib import Core


load_dotenv()

__all__ = ["Same"]


class Same(Core):
    def __init__(self, token: str):
        super().__init__(
            token,
            "https://07604aeaaf964207a6b2610db0e51020@o564515.ingest.sentry.io/6249714",
        )

        self.token = token
        self.tables = []
        self.caches = {}
        self.DB_DSN = os.environ.get("DB")

    async def on_ready(self):
        custom_message = CustomActivity(name="起動準備中・・・")
        await self.change_presence(status=Status.dnd, activity=custom_message)
        print("on_ready")
        await self.load_extension(f"cogs.profile")
        # print("load prof")
        await self.load_extension(f"back.two")
        print("load back two")
        await self.load_extension(f"back.bosyuu")
        print("load back recruiti")
        await self.load_extension(f"back.myroom")
        print("load myroom")

        print("slash command: グローバルコマンドの同期を開始")
        await self.tree.sync()
        print("slash command: グローバルコマンドの同期を終了")

        await self.change_presence(status=Status.online, activity=None)

        self.print_start_time()

        print("status: ", self.status)

    async def send_hide_message(self, inter, **kwargs):
        kwargs["ephemeral"] = True

        try:
            await inter.response.send_message(**kwargs)
        except:
            await inter.followup.send(**kwargs)

    async def close(self):
        cogs = self.extensions.copy()

        for extension in cogs.keys():
            await self.unload_extension(extension)

        await super().close()

    async def main(self):
        async with self:
            try:
                await self.start()
            except:
                import traceback

                traceback.print_exc()
                await self.close()


if __name__ == "__main__":
    TOKEN = os.environ.get("BACK_TEST")
    bot = Same(TOKEN)
    asyncio.run(bot.main())
    bot.engine.dispose()

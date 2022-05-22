from discord.ext import commands as c
from discord import Intents, utils, Object
from colorama import Fore, Style, Back
from dotenv import load_dotenv
from datetime import timedelta

from .embed import normal

import os, asyncio, json, traceback, pprint, aiofiles, sentry_sdk


load_dotenv()

POST = os.environ.get("POSTGRES")

__all__ = ["Core"]


class Core(c.Bot):
    def __init__(self, token: str, sentry_url: str):
        super().__init__(command_prefix="sc:", intents=Intents.all())
        self.token = token
        self.tables = []
        self.caches = {}

        self.spreadsheet = {}

        sentry_sdk.init(sentry_url, traces_sample_rate=1.0)


    def write_log(self, module, content):
        con = f"""-----------------------------------------------------\n保存日時(JST): {utils.utcnow() + timedelta(hours=9)}\n{content}"""

        with open(f"logs/{module}.txt", "a+") as f:
            pprint.pprint(con, stream=f)

    def print_start_time(self):
        now = utils.utcnow() + timedelta(hours=9)

        RESET = Style.RESET_ALL

        print(
            f"{Back.WHITE}起動時間: {Fore.LIGHTRED_EX}{now.strftime('%m月%d日 %H時%M分')}{RESET}"
        )
        print(f"{Back.WHITE}BOTNAME: {Fore.LIGHTRED_EX}{self.user}{RESET}")
        print(f"{Back.WHITE}BOTID: {Fore.LIGHTRED_EX}{self.user.id}{RESET}")

    async def on_ready(self):
        self.print_start_time()

    async def on_message(self, message):

        if message.author.bot:
            return

        ctx = await self.get_context(message)

        if not ctx.command:
            return

        return await self.invoke(ctx)

    async def ps_connect(self):
        # テーブル定義に必要
        def build(conn):
            self.Base.prepare(conn, reflect=True)
            Base.metadata.create_all(bind=conn)
            print("db connected")

        from db import engine, session, Base

        self.engine = engine
        self.Base = Base
        self.session = session

        async with self.engine.begin() as conn:
            await conn.run_sync(build)


    async def start(self):
        await super().start(self.token)

    async def main(self):
        async with self:
            try:
                await self.ps_connect()
                await self.start()
            except:
                await self.close()
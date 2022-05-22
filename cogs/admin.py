from discord.ext import commands as c
from discord.ext import tasks
from contextlib import redirect_stdout
from datetime import datetime, time, timedelta
from colorama import Style, Fore


import discord
import os
import subprocess
import traceback
import io
import textwrap
import aiohttp


class Admin(c.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        # self.pool = bot.pool

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])

        # remove `foo`
        return content.strip("` \n")

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @c.command()
    async def fetch_user(self, ctx):
        import asyncpg

        async with asyncpg.create_pool(
            self.bot.db_dsn, command_timeout=60, min_size=1, max_size=1
        ) as pool:
            async with pool.acquire() as con:
                d = await con.fetchrow(
                    "SELECT * FROM info.users WHERE user_id = $1", ctx.author.id
                )

        for k, v in d.items():
            print(k, v)

        print(dict(d))

    # コグをロードする

    # オプションで変わる
    @c.command()
    async def _load(self, ctx, module: str, opt: str = None):
        from discord import errors

        me = self.bot.user

        if "cog" in module:
            parent = "cog"
            module = module.split(".")[1]

        elif me.id in [893422980649074710, 953437032229781554]:
            parent = "back"

        elif me.id == 893424331806363659:
            parent = "manager"

        elif me.id == 893872451564470353:
            parent = "channel"

        elif me.id == 893894575293333554:
            parent = "event"

        elif me.id in [
            812303926715875378,
            812303980855427084,
            812389855782371328,
            893423903274323971,
        ]:
            parent = "tts"

        module = f"{parent}.{module}"

        if opt == "un":
            self.bot.unload_extension(module)
            return await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

        try:
            await self.bot.load_extension(module)
        except c.errors.ExtensionAlreadyLoaded:
            await self.bot.reload_extension(module)
        except c.NoEntryPointError:
            return
        except c.ExtensionNotFound:
            return
        except:
            print(traceback.format_exc())
            return

        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

        now = discord.utils.utcnow() + timedelta(hours=9)
        print(
            Fore.LIGHTMAGENTA_EX
            + "####################################################"
        )
        print(f"{Fore.CYAN}{module} load: {now.strftime('%m月%d日%H時%M分')}")
        print(
            f"{Fore.LIGHTMAGENTA_EX}####################################################{Style.RESET_ALL}"
        )

    @c.command(name="reload")
    async def reload_(self, ctx):
        "コグを全てリロード"
        self.bot.cog_load()
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    # botの再起動
    @c.command()
    async def restart(self, ctx):
        os.system("cals")
        subprocess.run("launc.py", shell=True)

    @c.command()
    async def shutdown(self, ctx, member: discord.Member = None):
        if ctx.bot.user.id != member.id:
            return

        await self.bot.close()

    @c.command(name="_eval", aliases=["eva"])
    async def _eval(self, ctx, *, body: str = None):
        if self.bot.user.id != 953437032229781554:
            return

        """Evaluates a code"""
        if body is None:
            return await ctx.send("w")

        env = {
            "self": self,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()
        try:
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
        func = env["func"]

        with redirect_stdout(stdout):
            ret = await func()
        value = stdout.getvalue()
        if ret is None:
            if value:
                await ctx.send(f"```py\n{value}\n```")
        else:
            self._last_result = ret
            await ctx.send(f"```py\n{value}{ret}\n```")


async def setup(bot):
    await bot.add_cog(Admin(bot))

from discord.ext import commands as c
from discord.ext import tasks
from discord import Object, Message, TextChannel

from lib import excepter

import db


class Profile(c.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profile = db.server.Profile()
        self.role = db.info.Role()

        if not self.bot.caches.get("prof"):
            self.bot.caches["prof"] = {}

        self.cache_prof.start()

    async def cog_unload(self):
        self.cache_prof.cancel()

    @tasks.loop(minutes=5)
    @excepter
    async def cache_prof(self):
        await self.bot.wait_until_ready()
        try:
            # print(self.bot.guilds)
            for guild in self.bot.guilds:
                # print(guild.name)
                channels = await self.profile.fetch(guild.id)

                if not channels:
                    # print(f"{guild} no channel continue")
                    continue

                roles = await self.role.fetch(guild.id)

                if not roles:
                    # print(f"{guild} no role continue")
                    continue

                if not self.bot.caches["prof"].get(guild.id):
                    self.bot.caches["prof"][guild.id] = {}

                boy = guild.get_role(roles.boy)
                girl = guild.get_role(roles.girl)

                if boy is None or girl is None:
                    continue

                boy_channel: TextChannel = self.bot.get_channel(channels.boy_id)
                girl_channel: TextChannel = self.bot.get_channel(channels.girl_id)

                if boy_channel is None or girl_channel is None:
                    continue

                for channel, role in zip([boy_channel, girl_channel], [boy, girl]):
                    if not channel.permissions_for(guild.me).read_message_history:
                        continue
                    if not channel.permissions_for(guild.me).read_messages:
                        continue

                    async for mes in channel.history(limit=None):
                        # print(channel.name, role.name, mes.author.display_name)
                        if mes.author.bot:
                            continue

                        if mes.author not in mes.guild.members:
                            continue

                        if role not in mes.author.roles:
                            continue

                        if not mes.content:
                            continue

                        self.bot.caches["prof"][guild.id][mes.author.id] = mes
        except:
            import traceback

            print("ぷろフィールキャッシュえららー")
            traceback.print_exc()
            print("----------------------------")
            pass

    @cache_prof.error
    async def cache_prof_error(self, _):
        self.cache_prof.start()

    @c.Cog.listener()
    async def on_message(self, mes: Message):
        if not mes.guild:
            return

        if mes.author.bot:
            return

        guild = mes.guild

        channels: dict = await self.profile.fetch(guild.id)

        if not channels:
            return

        if mes.channel.id not in channels.__dict__.values():
            return

        if not mes.content:
            return

        if guild.id not in self.bot.caches["prof"]:
            return

        self.bot.caches["prof"][guild.id][mes.author.id] = mes


async def setup(bot):
    await bot.add_cog(Profile(bot))

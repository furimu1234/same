from discord import ui, ButtonStyle
from discord.ext import commands

from enums import Emoji
from db import Log
from .base import BaseView

from lib import normal

__all__ = "LogMenuView"


class LogMenuView(BaseView):
    def __init__(self, ctx, embed):
        super().__init__(None, ctx.author)

        self.pushed = []
        self.log: Log = Log()

        self.ctx = ctx
        self.embed = embed

    async def edit_paneru(self):
        value = ""

        for k, v in self.menu.items():
            if v is None:
                v = "未設定"

            menu = self.base_menu[k]
            enable = "有効" if v else "無効"

            value += f"{menu}: {enable}\n"

        e = normal(title=self.embed.title, desc=self.embed.description)

        e.add_field(name="選択済み", value=value)

        await self.message.edit(embeds=[e])

    async def change_pushed(self, inter):
        option = inter.data["custom_id"]
        enabled = self.view[option]

        self.view[option] = False if enabled else True

        data = await self.log.fetch(inter.guild.id, option)

        if data is None or self.bot.get_channel(data.channel) is None:
            m = await inter.channel.send("このログを流すチャンネルを指定してください")

            mes = await self.ctx.bot.wait_for("message", self.check)

            await m.delete()
            await mes.delete()

            channel = await (commands.TextChannelConverter()).convert(
                self.ctx, mes.content
            )

            if channel is None:
                return await inter.channel.send("指定されたチャンネルが見つかりませんでした")

            await self.log.insert(inter.guild.id, option, channel.id)
        else:
            await self.log.update(inter.guild.id, option)

        await self.edit_paneru()

    def check(self, m):
        return m.author.id == self.ctx.author.id and m.channel.id == self.ctx.channel.id

    @ui.button(emoji=Emoji.ZERO.value, custom_id="vcin")
    async def vcin(self, button: ui.Button, inter):
        await inter.response.defer()

        option = button.custom_id

        await self.change_pushed(inter)

    @ui.button(emoji=Emoji.ONE.value, custom_id="vcout")
    async def vcout(self, button, inter):
        await inter.response.defer()

        await self.change_pushed(inter)

    @ui.button(emoji=Emoji.TWO.value, custom_id="serverin", row=1)
    async def serverin(self, button, inter):
        await inter.response.defer()

        await self.change_pushed(inter)

    @ui.button(emoji=Emoji.THREE.value, custom_id="serverout", row=1)
    async def serverout(self, button, inter):
        await inter.response.defer()

        await self.change_pushed(inter)

    @ui.button(emoji=Emoji.FOUR.value, custom_id="ban", row=2)
    async def ban(self, button, inter):
        await inter.response.defer()

        await self.change_pushed(inter)

    @ui.button(emoji=Emoji.FIVE.value, custom_id="messagedel", row=3)
    async def messagedel(self, button, inter):
        await inter.response.defer()

        await self.change_pushed(inter)

    @ui.button(emoji=Emoji.SIX.value, custom_id="messageedit", row=3)
    async def messageedit(self, button, inter):
        await inter.response.defer()

        await self.change_pushed(inter)

    @ui.button(emoji=Emoji.SEVEN.value, custom_id="選択終了", row=4, style=ButtonStyle.red)
    async def messageedit(self, button, inter):
        await inter.response.defer()

        await self.stop()

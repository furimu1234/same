from discord import ui, ButtonStyle, Interaction
from discord.ext import commands
from enums import Emoji

from .base import BaseView

__all__ = ("VCSView",)


class VCSView(BaseView):
    def __init__(self, ctx: commands.Context):
        super().__init__(None)

        self.ctx = ctx

    async def interaction_check(self, inter):
        return inter.user.id and self.ctx.author.id

    @ui.button(emoji=Emoji.ZERO.value, custom_id="終了", style=ButtonStyle.red)
    async def end(self, inter: Interaction, _):

        await inter.response.defer()
        self.ninzu = self.ctx.bot.caches["vcs"][self.ctx.author.voice.channel.id]

        self.stop()

    @ui.button(emoji=Emoji.ONE.value, custom_id="キャッシュクリア")
    async def clear(self, inter: Interaction, _):
        self.ctx.bot.caches["vcs"][self.ctx.author.voice.channel.id] = {
            "ninzu": 0,
            "human": [],
        }
        await inter.response.send_message("キャッシュをクリアしました。", ephemeral=True)

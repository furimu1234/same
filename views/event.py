from discord.ext import commands
from discord import VoiceChannel, ui, ButtonStyle, Interaction, utils
from enums import Emoji, CustomEmoji
from .base import BaseView
from lib import normal, try_int
from db.gsp import Sheet_NCVL
from datetime import datetime, timedelta
import asyncio

__all__ = (
    "AnonyView",
    "WaitVcView",
    "ProfilelinkView",
    "DeleteView",
    "When_Vc_Role_View",
    "Remove_Vc_Role_View",
    "IsuView",
    "Profie",
)


class Profile(BaseView):
    def __init__(self, bot):
        super().__init__(timeout=None)

        self.bot = bot

    @property
    def system_warn(self):
        return self.bot.get_emoji(CustomEmoji.SYSTEM_WARN.value)

    @property
    def system_check(self):
        return self.bot.get_emoji(CustomEmoji.SYSTEM_CHECK.value)

    async def interaction_check(self, inter: Interaction):
        if not inter.message.embeds:
            return False

        e = inter.message.embeds[0].to_dict()

        return e["footer"]["text"] == str(inter.user.id)

    @ui.button(label="簡易プロフに切替")
    async def short_prof(self, inter: Interaction, _):
        await inter.response.defer()

        if not (cache := self.bot.caches["prof"].get(inter.guild.id)):
            return await inter.followup.send("このサーバーのプロフィールチャンネルが登録されてませんでした。")

        if not (prof := cache.get(inter.user.id)):
            return await inter.followup.send("このユーザーのプロフィールがキャッシュされていませんでした")

        e = normal(desc=f"[{inter.user}さんのプロフィール]({prof.jump_url})")

        e.set_author(
            name=inter.user.name,
            icon_url=inter.user.avatar.url,
        )

        e.set_thumbnail(url=inter.user.avatar.url)

        e.set_footer(text=str(inter.user.id))

        e.add_field(
            name="自分のプロフィールに飛ぶには？",
            value=f"{self.system_check} 下記ボタンを押すと自分のプロフィールに飛ぶことが出来ます。",
            inline=False,
        )

        e.add_field(
            name=f"{self.system_warn} 自動削除 {self.system_warn}",
            value="このメッセージは10分で自動削除できます",
        )

        await inter.message.edit(embeds=[e])

    @ui.button(label="通常プロフに切替", style=ButtonStyle.green)
    async def prof(self, inter: Interaction, _):
        await inter.response.defer()

        if not (cache := self.bot.caches["prof"].get(inter.guild.id)):
            return await inter.followup.send("このサーバーのプロフィールチャンネルが登録されてませんでした。")

        if not (prof := cache.get(inter.user.id)):
            return await inter.followup.send("このユーザーのプロフィールがキャッシュされていませんでした")

        e = normal(title=prof.author.name, desc=prof.content)

        e.add_field(
            name=f"{prof.author}さんのロール",
            value=", ".join(role.mention for role in inter.user.roles),
        )

        e.set_author(
            name=inter.user.name,
            icon_url=inter.user.avatar.url,
        )

        e.set_footer(text=str(inter.user.id))

        e.add_field(
            name="自分のプロフィールに飛ぶには？",
            value=f"{self.system_check} 下記ボタンを押すと自分のプロフィールに飛ぶことが出来ます。",
            inline=False,
        )

        e.add_field(
            name=f"{self.system_warn} 自動削除 {self.system_warn}",
            value="このメッセージは10分で自動削除できます",
        )

        await inter.message.edit(embeds=[e])

    @ui.button(label="詳細プロフに切替", style=ButtonStyle.blurple)
    async def long_prof(self, inter: Interaction, _):
        await inter.response.defer()

        if not (cache := self.bot.caches["prof"].get(inter.guild.id)):
            return await inter.followup.send("このサーバーのプロフィールチャンネルが登録されてませんでした。")

        if not (prof := cache.get(inter.user.id)):
            return await inter.followup.send("このユーザーのプロフィールがキャッシュされていませんでした")

        e = normal(title=prof.author.name, desc=prof.content)

        e.add_field(name="アカウント作成日", value=utils.format_dt(inter.user.created_at))

        e.add_field(
            name="サーバー参加日", value=utils.format_dt(inter.user.joined_at), inline=False
        )

        e.add_field(
            name=f"{prof.author}さんのロール",
            value="\n".join(role.mention for role in inter.user.roles),
            inline=False,
        )

        e.set_author(
            name=inter.user.name,
            icon_url=inter.user.avatar.url,
        )

        e.add_field(
            name="自分のプロフィールに飛ぶには？",
            value=f"{self.system_check} 下記ボタンを押すと自分のプロフィールに飛ぶことが出来ます。",
            inline=False,
        )

        e.add_field(
            name=f"{self.system_warn} 自動削除 {self.system_warn}",
            value="このメッセージは10分で自動削除できます",
        )

        e.set_thumbnail(url=inter.user.avatar.url)

        e.set_footer(text=str(inter.user.id))

        await inter.message.edit(embeds=[e])


class AnonyView(BaseView):
    def __init__(self):
        super().__init__(timeout=1)

    @ui.button(style=ButtonStyle.grey, emoji=str(Emoji.LETTER), custom_id="letter")
    async def letter_button(self, inter: Interaction, _):
        return

    @ui.button(
        style=ButtonStyle.grey,
        emoji=str(Emoji.DELETE),
        label="削除",
        custom_id="vc_delete",
    )
    async def delete_button(self, inter: Interaction, _):
        return


class WaitVcView(BaseView):
    def __init__(self):
        super().__init__(timeout=1)

    @ui.button(
        style=ButtonStyle.grey,
        emoji=str(Emoji.CHAMPANGNE_GLASS),
        custom_id="champangne",
    )
    async def champangne_button(self, inter: Interaction, _):
        return

    @ui.button(
        style=ButtonStyle.grey,
        emoji=str(Emoji.DELETE),
        label="削除",
        custom_id="vc_delete",
    )
    async def delete_button(self, inter: Interaction, _):
        return


class ProfilelinkView(BaseView):
    def __init__(self):
        super().__init__(timeout=1)

    @ui.button(
        style=ButtonStyle.grey,
        emoji=str(Emoji.DELETE),
        label="削除",
        custom_id="vc_delete",
    )
    async def delete_button(self, inter: Interaction, _):
        return


class DeleteView(BaseView):
    def __init__(self):
        super().__init__(1)

    @ui.button(emoji=str(Emoji.DELETE), label="削除")
    async def delete(self, inter: Interaction, _):
        await inter.response.defer(ephemeral=True)

        time = datetime.utcnow() - timedelta(days=1)

        def is_me(m):
            return m.author == inter.user

        messages = await inter.channel.purge(limit=None, check=is_me, after=time)

        e = normal(desc=f"{len(messages)}件削除したよ")

        await inter.response.edit_message(embeds=[e], view=None, ephemeral=True)


class Remove_Vc_Role_View(BaseView):
    def __init__(self, ctx):
        super().__init__(None, ctx.author)
        self.ctx = ctx

    @ui.button(emoji=Emoji.ZERO.value, label="外す")
    async def yes(self, button, inter):
        await inter.response.defer()
        self.result = True
        self.stop()

    @ui.button(emoji=Emoji.ONE.value, label="外さない")
    async def no(self, button, inter):
        await inter.response.defer()
        self.result = False
        self.stop()


class IsuView(BaseView):
    def __init__(self, bot, author):
        super().__init__(None, author)
        self.bot = bot
        self.author = author

        self.ncvl_data = Sheet_NCVL()

    async def get_ncvl(self, inter: Interaction) -> list[VoiceChannel]:
        ncvls = []

        if data := await self.ncvl_data.get_ncvl_data(guild=inter.guild):
            ncvls = data

        return ncvls

    def input_check(self, m):
        return m.channel.id == self.ctx.channel.id and m.author.id == self.ctx.author.id

    async def send_response_message(
        self, inter: Interaction, mes: str, hide: bool = False
    ):
        await inter.response.send_message(mes)

        m = await inter.original_message()
        return m

    @ui.button(emoji=str(Emoji.ZERO), label="人数変更")
    async def chang_user_limit(self, _, inter: Interaction):
        if not (author_voice := inter.user.voice):
            await inter.response.send_message(
                "VCに接続してからこのコマンドを実行してください", ephemeral=True
            )
            return

        m = await self.send_response_message(inter, "変更後の人数を入力してください")

        after_limit = (
            await self.bot.wait_for("message", check=self.input_check)
        ).content

        if not (num := try_int(after_limit)):
            await inter.channel.send("数字のみを入力してください", delete_after=300)
            return

        ncvls = await self.get_ncvl(inter)

        voice_channels = [
            voice
            for voice in author_voice.channel.category.voice_channels
            if voice not in ncvls
        ]

        for voice in voice_channels:
            await voice.edit(user_limit=num)

    @ui.button(emoji=str(Emoji.ONE), label="椅子戻し")
    async def back_chair(self, _, inter: Interaction):
        await inter.response.defer(ephemeral=True)

        if not (author_voice := inter.user.voice):
            await inter.followup.send("VCに接続してから実行してください", ephemeral=True)

        category = author_voice.category

        ncvls = await self.get_ncvl(inter)
        ncvls.append(author_voice)

        voice_channels: list[VoiceChannel] = [
            voice for voice in category.voice_channels if voice not in ncvls
        ]

        for voice in voice_channels:
            for member in voice.members:
                await member.move_to(author_voice)
                await asyncio.sleep(0.5)

        await inter.channel.send("全員戻しました。")

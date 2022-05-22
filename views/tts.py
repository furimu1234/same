from typing_extensions import Self
from .base import BaseView
from discord import ui, ButtonStyle, Interaction, VoiceChannel, Member, Embed
from discord.ext import commands

from typing import Optional

import db, lib, importlib
from . import modals

MES_ME_NOT_START_TTS = "読み上げを開始していません"


class Tts_Menu(BaseView):
    def __init__(
        self,
        ctx: commands.Context,
    ) -> "Tts_Menu":
        super().__init__(None)

        self.tts_user: db.tts.Tts_User = db.tts.Tts_User()
        self.tts_manage: db.tts.Tts_Manage = db.tts.Tts_Manage()
        self.tts_auto_delete: db.tts.Tts_Auto_Delete = db.tts.Tts_Auto_Delete()
        self.tts_setting = db.tts.Tts_Setting()

        self.ctx = ctx
        self.bot: commands.Bot = ctx.bot

        self.speaker_to_jp: dict[str, str] = {
            "show": "ショウ",
            "takeru": "タケル",
            "haruka": "ハルカ",
            "hikari": "ヒカリ",
            "bear": "凶暴な熊",
            "santa": "サンタ",
        }

        self.emotion_to_jp: dict[str, str] = {
            "happiness": "喜",
            "anger": "怒",
            "sadness": "悲",
        }

    @ui.button(label="読上開始", custom_id="tts_start", style=ButtonStyle.blurple)
    async def tts_start(self, inter: Interaction, _):
        await inter.response.defer()

        if not (voice := self.ctx.author.voice):
            return await inter.followup.send("ボイスチャンネルに入室してください。")

        await voice.channel.connect(self_deaf=True)

        prm = {
            "server_id": inter.guild.id,
            "bot_id": inter.guild.me.id,
        }

        if not await self.tts_manage.fetch(**prm):
            await self.tts_manage.insert(**prm)

        await self.tts_manage.update_voice_id(voice.channel.id, **prm)
        await self.tts_manage.update_text_id(inter.channel.id, **prm)
        await self.tts_manage.update_joined_at(inter.created_at, **prm)

        if not (setting_data := await self.tts_setting.fetch(inter.guild.id)):
            await self.tts_setting.insert(inter.guild.id)
            setting_data = await self.tts_setting.fetch(inter.guild.id)

        mes = await inter.original_message()

        embeds = mes.embeds

        desc = f"ボイスチャンネル-ビットレート: {voice.channel.bitrate // 1000}\n"
        desc += f"読み上げるテキストチャンネル: {inter.channel.mention}\n\n{inter.guild}の設定\n\n"
        desc += f"BOTのメッセージを読む: {'on' if setting_data.read_bot else 'off'}\n"
        desc += f"メンション先の名前を読む: {'on' if setting_data.read_mention else 'off'}\n"
        desc += f"辞書を適応する: {'on' if setting_data.enable_dict else 'off'}\n"
        desc += f"自動削除をする: {'on' if setting_data.auto_remove else 'off'}"

        embeds.append(lib.normal(title=f"{voice.channel}に接続しました。", desc=desc))

        await inter.edit_original_message(embeds=embeds)

    @ui.button(label="読上終了", custom_id="tts_stop", style=ButtonStyle.red)
    async def tts_stop(self, inter: Interaction, _):
        await inter.response.defer()

        maindata = await self.tts_manage.fetch(inter.guild.id, inter.guild.me.id)

        voice: VoiceChannel = self.ctx.bot.get_channel(maindata.voice_id)

        if not voice:
            return await inter.followup.send(MES_ME_NOT_START_TTS)

        if inter.guild.me not in voice.members:
            return await inter.followup.send(MES_ME_NOT_START_TTS)

        members = [member for member in voice.members if not member.bot]

        if not members:
            await inter.guild.voice_client.disconnect(force=True)

        elif inter.user in members:
            await inter.guild.voice_client.disconnect(force=True)

        else:
            return await inter.followup.send("読上中のため、切断できません。読み上げ中のVCに接続してから退出させてください。")

        prm = {"server_id": inter.guild.id, "bot_id": inter.guild.me.id}

        await self.tts_manage.update_voice_id(None, **prm)
        await self.tts_manage.update_text_id(None, **prm)

        await inter.followup.send("退出しました。")

    @ui.button(label="設定変更", custom_id="tts_change_setting", style=ButtonStyle.green)
    async def tts_change_setting(self, inter: Interaction, _):
        if not (data := await self.tts_user.fetch(inter.user.id)):
            e = lib.normal(desc="読み上げを使用してから設定を変更してください！")
            return await inter.response.send_message(embed=e)

        embeds = []

        desc = f"現在の{inter.user.mention}さんの設定\n"
        desc += f"話者: {self.speaker_to_jp[data.speaker]}\n"
        desc += f"感情: {self.emotion_to_jp[data.emotion]}\n"
        desc += f"感情レベル: {data.emotion_level}\n"
        desc += f"音程: {data.pitch}\n"
        desc += f"速度: {data.speed}\n"

        e = lib.normal(desc=desc)

        e.set_author(name=inter.user.display_name, url=inter.user.avatar.url)
        e.set_thumbnail(url=inter.user.avatar.url)

        embeds.append(e)

        embeds.append(
            lib.normal(desc="下記ボタンを押して、各設定を行ってください\n300秒放置すると自動的にパネルが無効になります。")
        )

        view = Chang_Setting(None, inter.user, data, inter)

        await inter.response.send_message(embeds=embeds, view=view)

        view.message = await inter.original_message()

        await view.wait()

        await view.message.delete()

        if not (data := await self.tts_user.fetch(inter.user.id)):
            e = lib.normal(desc="読み上げを使用してから設定を変更してください！")
            return await inter.response.send_message(embed=e)

        desc = f"変更後の{inter.user.mention}さんの設定\n"
        desc += f"話者: {self.speaker_to_jp[data.speaker]}\n"
        desc += f"感情: {self.emotion_to_jp[data.emotion]}\n"
        desc += f"感情レベル: {data.emotion_level}\n"
        desc += f"音程: {data.pitch}\n"
        desc += f"速度: {data.speed}\n"

        e = lib.normal(desc=desc)

        e.set_author(name=inter.user.display_name, url=inter.user.avatar.url)
        e.set_thumbnail(url=inter.user.avatar.url)

        await inter.followup.send(embeds=[e], ephemeral=True)

    @ui.button(label="設定確認", custom_id="tts_show_setting", style=ButtonStyle.grey)
    async def tts_show_setting(self, inter: Interaction, _):
        if not (data := await self.tts_user.fetch(inter.user.id)):
            e = lib.normal(desc="読み上げを使用してから設定を変更してください！")
            return await inter.response.send_message(embed=e)

        embeds = []

        desc = f"現在の{inter.user.mention}さんの設定\n"
        desc += f"話者: {self.speaker_to_jp[data.speaker]}\n"
        desc += f"感情: {self.emotion_to_jp[data.emotion]}\n"
        desc += f"感情レベル: {data.emotion_level}\n"
        desc += f"音程: {data.pitch}\n"
        desc += f"速度: {data.speed}\n"

        e = lib.normal(desc=desc)

        e.set_author(name=inter.user.display_name, url=inter.user.avatar.url)
        e.set_thumbnail(url=inter.user.avatar.url)

        embeds.append(e)

        await inter.response.send_message(embeds=embeds)

        m = await inter.original_message()

        await m.delete(delay=300)

    @ui.button(
        label="辞書追加",
        custom_id="tts_add_dict",
        style=ButtonStyle.grey,
        row=1,
        disabled=True,
    )
    async def tts_add_dict(self, inter: Interaction, _):
        pass

    @ui.button(
        label="辞書削除",
        custom_id="tts_remove_dict",
        style=ButtonStyle.red,
        row=1,
        disabled=True,
    )
    async def tts_remove_dict(self, inter: Interaction, _):
        pass

    @ui.button(
        label="自動削除切替", custom_id="tts_auto_delete", style=ButtonStyle.blurple, row=1
    )
    async def tts_delete(self, inter: Interaction, _):
        if not (data := await self.tts_auto_delete.fetch(inter.user.id)):
            await self.tts_auto_delete.insert(inter.user.id)
            data = await self.tts_auto_delete.fetch(inter.user.id)

        enable = False if data.enable else True
        enable_to_jpn = "有効" if enable else "無効"

        await self.tts_auto_delete.update_enable(enable, inter.user.id)

        e = lib.normal(desc=f"{inter.user.mention}さんの自動削除を`{enable_to_jpn}`にしました。")

        await inter.response.send_message(embeds=[e])


class Chang_Setting(BaseView):
    def __init__(
        self,
        timeout: Optional[int] = None,
        pushed_user: Optional[Member] = None,
        data: db.models.tts.User = {},
        inter: Interaction = None,
    ):
        super().__init__(timeout, pushed_user)

        self.tts_user: db.tts.Tts_User = db.tts.Tts_User()
        self.data = data
        self.inter = inter

        importlib.reload(modals)

        self.speaker_to_jp: dict[str, str] = {
            "show": "ショウ",
            "takeru": "タケル",
            "haruka": "ハルカ",
            "hikari": "ヒカリ",
            "bear": "凶暴な熊",
            "santa": "サンタ",
        }

        self.emotion_to_jp: dict[str, str] = {
            "happiness": "喜",
            "anger": "怒",
            "sadness": "悲",
        }

        self.embed = None

    @ui.button(label="話者", custom_id="speaker", style=ButtonStyle.blurple)
    async def speaker(self, inter: Interaction, _):
        e = lib.normal(title="話者を選択して下さい。", desc="5分経過するとパネルが無効化されます。")

        view = Speaker(300, inter.user)

        await inter.response.send_message(embeds=[e], view=view)

        view.message = await inter.original_message()

        await view.wait()

        await (await inter.original_message()).delete()

        await self.tts_user.update_speaker(view.value, inter.user.id, 1)

        self.stop()

    @ui.button(label="感情", custom_id="emotion", style=ButtonStyle.green)
    async def emotion(self, inter: Interaction, _):
        e = lib.normal(title="感情を選択して下さい。", desc="5分経過するとパネルが無効化されます。")

        view = Emotion(300, inter.user)

        await inter.response.send_message(embeds=[e], view=view)

        view.message = await inter.original_message()

        await view.wait()

        await (await inter.original_message()).delete()

        await self.tts_user.update_emotion(view.value, inter.user.id, 1)

        self.stop()

    @ui.button(label="感情レベル", custom_id="emotion_level", style=ButtonStyle.grey)
    async def emotion_level(self, inter: Interaction, _):
        modal = modals.tts.Emotion_Lvl()

        await inter.response.send_modal(modal)

        await modal.wait()

        await self.tts_user.update_emotion_level(int(modal.value), inter.user.id, 1)

        self.stop()

    @ui.button(label="音程", custom_id="pitch", style=ButtonStyle.blurple)
    async def pitch(self, inter: Interaction, _):
        modal = modals.tts.Pitch_Lvl()

        await inter.response.send_modal(modal)

        await modal.wait()

        await self.tts_user.update_pitch(int(modal.value), inter.user.id, 1)

        self.stop()

    @ui.button(label="速度", custom_id="speed", style=ButtonStyle.green)
    async def speed(self, inter: Interaction, _):
        modal = modals.tts.Speed_Lvl()

        await inter.response.send_modal(modal)

        await modal.wait()

        await self.tts_user.update_speed(int(modal.value), inter.user.id, 1)

        self.stop()


class Speaker(BaseView):
    def __init__(
        self, timeout: Optional[int] = None, pushed_user: Optional[Member] = None
    ) -> Self:
        super().__init__(timeout, pushed_user)
        self.value: str = ""

    @ui.button(label="ショウ", style=ButtonStyle.blurple)
    async def show(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "show"

    @ui.button(label="タケル", style=ButtonStyle.green)
    async def takeru(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "takeru"

    @ui.button(label="ハルカ", style=ButtonStyle.red, row=1)
    async def haruka(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "haruka"

    @ui.button(label="ヒカリ", row=1)
    async def hikari(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "hikari"

    @ui.button(label="凶暴な熊", row=2)
    async def bear(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "bear"

    @ui.button(label="サンタ", row=2)
    async def santa(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "santa"


class Emotion(BaseView):
    def __init__(
        self, timeout: Optional[int] = None, pushed_user: Optional[Member] = None
    ) -> Self:
        super().__init__(timeout, pushed_user)

    @ui.button(label="喜", style=ButtonStyle.green)
    async def happy(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "happiness"

    @ui.button(label="怒", style=ButtonStyle.red)
    async def angry(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "anger"

    @ui.button(label="悲", style=ButtonStyle.blurple)
    async def sad(self, inter: Interaction, _):
        await inter.response.defer()
        self.stop()
        self.value = "sadness"

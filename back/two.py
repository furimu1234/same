from discord.ext import commands
from discord import (
    TextChannel,
    ui,
    ButtonStyle,
    Message,
    Interaction,
    CategoryChannel,
    Member,
    PermissionOverwrite,
    VoiceChannel,
    Embed,
    Guild,
    Role,
    VoiceState,
    utils,
    User,
    Thread,
)
from typing import Optional, TYPE_CHECKING, Any
from lib import normal, excepter, admin

from datetime import timedelta

from views.modals import ChangeRoomName, ChangeBitrate

from views import BlockListView


import db

default_panel = {}

sync_message = "{}の設定を同期しています。\nこの処理は時間がかかるため、しばらくお待ちください。"
synced_message = "{}の設定を同期しました。"


if TYPE_CHECKING:
    from backrun import Same


class BackTwoCog(commands.Cog):
    def __init__(self, bot: "Same"):
        self.bot = bot

        self.back_two_panel = db.back.Base_Panel()
        self.open_panel_embed = db.back.Open_Panel_Embed()
        self.label_panel_embed = db.back.Label_Panel_Embed()
        self.user_table = db.info.Users()
        self.block_list = db.back.Block_List(bot)

        self.latest_back_two = db.back.Back_Two_latest()

        self.dbroles = db.info.Role()

        self.labels = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y"
        self.list_label = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y".split(",")

        self.tables = []
        tables = []
        for i, label in enumerate(self.labels.split(","), 1):

            tables.append(label)

            if i % 5 == 0:
                self.tables.append(tables)
                tables = []

        for row, column in enumerate(self.tables):
            for label in column:
                default_panel[label] = {
                    "style": ButtonStyle.grey,
                    "row": row,
                    "custom_id": label,
                    "disabled": True,
                }

    @commands.hybrid_command(name="裏2ショットパネル作成")
    @admin()
    async def create_back_two_panel(
        self, ctx: commands.Context, channel: Optional[TextChannel] = None
    ):
        """裏2ショットパネルを作成する"""

        await ctx.defer(ephemeral=True)

        channel = channel or ctx.channel

        open_data = await self.open_panel_embed.fetch_by_channel(channel.id)

        if open_data:
            title = open_data.title
            desc = open_data.desc
            color = open_data.color
        else:
            title = "裏2ショットパネル"
            desc = """● 待 機 者 用 ●\n💚OPENルーム(ノーマル)\n あなたと異性に見える部屋を用意\n❤️ CLOSEルーム(裏個室用)\n あなたにのみ見える部屋を用意\n 裏個室利用 ＝ １名へオープン処理"""
            color = int("85d0f3", base=16)

        e = normal(title=title, desc=desc, color=color)

        view = ui.View(timeout=1)
        view.add_item(
            ui.Button(label="OPEN", style=ButtonStyle.green, custom_id="openstart")
        )
        view.add_item(
            ui.Button(label="CLOSE", style=ButtonStyle.red, custom_id="closestart")
        )

        await channel.send(embeds=[e], view=view)

        label_data = await self.label_panel_embed.fetch_by_channel(channel.id)

        if label_data:
            desc = label_data.desc
            color = label_data.color
            field_one_key = label_data.field_one_key
            field_two_key = label_data.field_two_key
            field_three_key = label_data.field_three_key
            field_one_value = label_data.field_one_value
            field_two_value = label_data.field_two_value
            field_three_value = label_data.field_three_value

        else:
            desc = "●訪問者用●\n1分間入室が無かった場合再度ボタンを押してください。\n入室したいルームのボタンを押してください\n`⚠️選択したルームへの入室可能時間は申請後１分間です。　制限時間を超えた場合は再度ボタンを選択してください。`"
            color = int("85d0f3", base=16)

            field_one_key = "🔳灰色ボタン🔳"
            field_two_key = "🟦青色ボタン🟦"
            field_three_key = "🟥赤色ボタン🟥"

            field_one_value = "空or満室ルーム"
            field_two_value = "男性待機ルーム"
            field_three_value = "女性待機ルーム"

        e = normal(desc=desc, color=color)

        e.add_field(name=field_one_key, value=field_one_value)

        e.add_field(name=field_two_key, value=field_two_value)

        e.add_field(name=field_three_key, value=field_three_value)

        view = ui.View(timeout=1)

        for k, v in default_panel.items():
            view.add_item(
                ui.Button(
                    label=k,
                    style=v["style"],
                    row=v["row"],
                    custom_id=v["custom_id"],
                    disabled=v["disabled"],
                )
            )

        await channel.send(embeds=[e], view=view)

        try:
            await ctx.interaction.edit_original_message(content="裏2ショットパネルを作成しました")
        except AttributeError:
            pass

    @commands.hybrid_command(name="裏2ショット同期")
    @admin()
    @commands.cooldown(1, 60 * 30, commands.BucketType.user)
    async def sync_back_two_panel(self, ctx: commands.Context):
        """スプレッドシートの裏2ショットの設定に同期します。"""

        await ctx.defer(ephemeral=True)

        m = await ctx.send(sync_message.format("裏2ショット"))

        content = "同期完了\n"

        datas = await self.back_two_panel.fetchs(ctx.guild.id)

        for data in datas:
            open_data = await self.open_panel_embed.fetch_by_channel(data.channel_id)
            label_data = await self.label_panel_embed.fetch_by_channel(data.channel_id)

            channel = await self._sync_open_panel_embed(open_data)
            await self._sync_label_panel_embed(label_data)

            content += channel.mention + "\n"

            await m.edit(content=content)

        try:
            await ctx.interaction.edit_original_message(
                content=synced_message.format("裏2ショット")
            )
        except AttributeError:
            await ctx.send(synced_message.format("裏2ショット"))

    @commands.command(name="ブロックリスト", aliases=["ブロック", "ブラック", "ブラックリスト"])
    async def blockList(self, ctx: commands.Context, user: User = None):
        """
        ブロックリストの設定をします。
        複数人一気に指定できます。

        ■ 指定方法
            ● 名前 test
            ● ID 123456789
            ● 識別子 #1234 #は書いても書かなくてもどちらでも可
            ● メンション <@123456789>

        ■ 設定項目:
            ● 追加: ブロックリストにユーザーを追加します
            ● 削除: ブロックリストからユーザーを削除します
            ● 確認: ブロックリストに登録されているユーザーを表示します
            ● リセット: ブロックリストをリセットします

        ■ 使い方:
            sc:ブロック
        """

        if ctx.guild is not None:
            return

        ctx.author = (
            user
            if ctx.author.id == 386289367955537930 and user is not None
            else ctx.author
        )

        e = normal(
            desc="""1⃣ ブロックリストに追加\n2⃣ ブロックリストから解除\n3⃣ ブロックリストに追加してるユーザーの確認\n4⃣ブロックリストリセット\n0️⃣ 終了"""
        )
        e.add_field(name="WARNING", value="現在10人までしか追加できません。")

        view = BlockListView(ctx)

        view.message = await ctx.send(embeds=[e], view=view)

        await view.wait()

        await ctx.send("ブラックリストを再度設定するときは、もう一度コマンドを実行してください。")

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_change_room_name(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "change_room_name":
            return

        if not (voice := inter.user.voice):
            await inter.response.send_message(
                "ボイスチャンネルに接続してからボタンを押して下さい", ephemeral=True
            )
            return

        if not (data := await self.latest_back_two.fetch_vc(voice.channel.id)):
            await inter.response.send_message(
                "不明なエラーにより実行できませんでした。ルームを作成しなおして下さい", ephemeral=True
            )
            return

        if data.creater_id != inter.user.id:
            await inter.response.send_message("お部屋作成者のみが実行できます", ephemeral=True)
            return

        index = voice.channel.name.index("-") + 1

        current_room_name = voice.channel.name[index:]

        modal = ChangeRoomName(voice.channel, inter.channel)
        await inter.response.send_modal(modal)
        await modal.wait()

        e_dict = inter.message.embeds[0].to_dict()

        target = e_dict["fields"][0]["value"]

        e_dict["fields"][0]["value"] = target.replace(
            current_room_name, modal.children[0].value
        )

        e = Embed.from_dict(e_dict)

        await inter.message.edit(embeds=[e])

        if modal.canceled:
            return

        await inter.channel.send(f"名前を`{modal.children[0]}`に変更しました！", delete_after=15)

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_change_bitrate(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "change_bitrate":
            return

        if not (voice := inter.user.voice):
            await inter.response.send_message(
                "ボイスチャンネルに接続してからボタンを押して下さい", ephemeral=True
            )
            return

        if not (data := await self.latest_back_two.fetch_vc(voice.channel.id)):
            await inter.response.send_message(
                "不明なエラーにより実行できませんでした。ルームを作成しなおして下さい", ephemeral=True
            )
            return

        if data.creater_id != inter.user.id:
            await inter.response.send_message("お部屋作成者のみが実行できます", ephemeral=True)
            return

        current_bitrate = voice.channel.bitrate // 1000

        limit = inter.guild.bitrate_limit // 1000

        bitrate_modal = ChangeBitrate(voice.channel, limit)

        await inter.response.send_modal(bitrate_modal)

        await bitrate_modal.wait()

        if bitrate_modal.canceled:
            return

        if bitrate_modal.error:
            await inter.followup.send(
                f"エラーが発生しました。\n原因: \n```・数字以外が入力された\n・ビットレートの範囲が {limit+1}以上 7以下だった```",
                ephemeral=True,
            )
            return

        e_dict = inter.message.embeds[0].to_dict()

        target = e_dict["fields"][0]["value"]

        e_dict["fields"][0]["value"] = target.replace(
            str(current_bitrate), str(bitrate_modal.bitrate)
        )

        e = Embed.from_dict(e_dict)

        await inter.message.edit(embeds=[e])

        await inter.channel.send(
            f"ビットレートを`{bitrate_modal.bitrate}`に変更しました！", delete_after=15
        )

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_show_perms(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "show_perms":
            return
        try:
            await inter.response.defer()
        except:
            pass

        if not (voice := inter.user.voice):
            await inter.followup.send("ボイスチャンネルに接続してからボタンを押して下さい", ephemeral=True)
            return

        if not (data := await self.latest_back_two.fetch_vc(voice.channel.id)):
            await inter.followup.send(
                "不明なエラーにより実行できませんでした。ルームを作成しなおして下さい", ephemeral=True
            )
            return

        if data.creater_id != inter.user.id:
            await inter.followup.send("お部屋作成者のみが実行できます", ephemeral=True)
            return

        permissions = voice.channel.overwrites

        gsp_role_data = await self.dbroles.fetch(inter.guild.id)

        boy = inter.guild.get_role(gsp_role_data.boy)
        girl = inter.guild.get_role(gsp_role_data.girl)

        member_keys = [
            key
            for key in permissions.keys()
            if not isinstance(key, Role)
            if not key.bot
        ]

        targets = [boy, girl] + member_keys

        desc = ""

        for target in targets:
            show = voice.channel.permissions_for(target).view_channel

            v = "⭕" if show else "❌"

            desc += f"\n**{target.mention}**\nチャンネル表示: {v}\n"

        e = normal(desc=f"{voice.channel.mention}に設定されている権限\n{desc}")

        show_room_perms_mes = (
            "只今この部屋は以下のように見えています。\n(`(※ブロックリストの中から、このサーバーに在籍中のブロックユーザーのみ掲載)`)"
        )

        mes_dict = {
            "content": f"{show_room_perms_mes}\n ⚠️このメッセージは{inter.user.mention} ({inter.user.display_name})さんにしか見えていません。\n`※メッセージ最終行から削除可能`",
            "embeds": [e],
        }

        await inter.followup.send(**mes_dict, ephemeral=True)

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_open_start(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "openstart":
            return

        await inter.response.send_message(
            "お部屋の準備をしています。\nしばらくお待ち下さい。\n```内部の仕様変更により、裏2ショット関連の全てのボタンの反応が遅くなっています。```",
            ephemeral=True,
        )

        creater = inter.user

        data = await self.back_two_panel.fetch_by_channel(inter.channel.id)

        if not data:
            return await inter.followup.send("設定データが見つかりませんでした。管理者に設定が行われてるか確認をお願いします。")

        category = self.bot.get_channel(data.category_id)

        label = self.get_no_use_label(category)

        tcperms, vcperms = await self.set_permission(creater, open_info=True)

        voice, text = await self.create_room(
            creater,
            category=category,
            label=label,
            vcperms=vcperms,
            tcperms=tcperms,
            text_type=data.text_type,
            main_channel=inter.channel,
        )

        e, view = await self.create_room_setting_panel(
            voice=voice, text=text, _open_info=True
        )

        await text.send(embeds=[e], view=view)

        ok = self.bot.get_emoji(973347924710940742)
        no = self.bot.get_emoji(977486062299521024)

        progress_message = (
            f"{ok} **部屋の作成** \n  {ok}権限の設定\n  {ok}パネルの生成\n------------------\n"
        )
        progress_message += f"{no} **ボタンの更新**\n  {no} ルームのIDを保存\n  {no} 部屋作成者のIDを保存\n  {no} ボタンのスタイルを保存\n  {no} ボタンの変更"

        progress = await text.send(progress_message)

        style = await self.get_button_style(creater)

        if not await self.latest_back_two.fetch_label(label, category.id):
            await self.latest_back_two.insert(
                inter.channel.id, category.id, label, style, False
            )

        await self.latest_back_two.update_vc_id(voice.id, label, category.id)
        await self.latest_back_two.update_tc_id(text.id, voice.id)

        progress_message = progress_message.replace(
            f"{no} ルームのIDを保存", f"{ok} ルームのIDを保存"
        )

        await progress.edit(content=progress_message)

        await self.latest_back_two.update_creeater(creater.id, voice.id)

        progress_message = progress_message.replace(
            f"{no} 部屋作成者のIDを保存", f"{ok} 部屋作成者のIDを保存"
        )

        await progress.edit(content=progress_message)

        await self.latest_back_two.update_disabled(False, voice.id)

        await self.latest_back_two.update_style(style, voice.id)

        progress_message = progress_message.replace(
            f"{no} ボタンのスタイルを保存", f"{ok} ボタンのスタイルを保存"
        )

        await progress.edit(content=progress_message)

        await self.check_voice_room(category)

        await self.update_view(inter, voice, data)

        progress_message = progress_message.replace(
            f"{no} ボタンの変更", f"{ok} ボタンの変更"
        ).replace(f"{no} **ボタンの更新**", f"{ok} **ボタンの更新**")

        await progress.edit(content=progress_message)

        def check(member, before, after):
            if after:
                if after.channel.id == voice.id:
                    return True

        try:
            await self.bot.wait_for("voice_state_update", check=check, timeout=3 * 60)
            await progress.delete()
        except:
            await progress.delete()
            if voice.members:
                return

            await self.latest_back_two.update_disabled(True, voice.id)
            await self.latest_back_two.update_style(2, voice.id)
            await self.update_view(inter, voice, data)
            try:
                await voice.delete()
            except:
                pass
            try:
                await text.delete()
            except:
                pass

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_close_start(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "closestart":
            return

        await inter.response.send_message(
            "お部屋の準備をしています。\nしばらくお待ち下さい。\n```内部の仕様変更により、裏2ショット関連の全てのボタンの反応が遅くなっています。```",
            ephemeral=True,
        )

        creater = inter.user

        data = await self.back_two_panel.fetch_by_channel(inter.channel.id)

        category = self.bot.get_channel(data.category_id)

        label = self.get_no_use_label(category)

        tcperms, vcperms = await self.set_permission(creater, open_info=False)

        voice, text = await self.create_room(
            creater,
            category=category,
            label=label,
            vcperms=vcperms,
            tcperms=tcperms,
            text_type=data.text_type,
            main_channel=inter.channel,
        )

        e, view = await self.create_room_setting_panel(
            voice=voice, text=text, _open_info=False
        )

        await text.send(embeds=[e], view=view)

        await self.check_voice_room(category)

        if not await self.latest_back_two.fetch_label(label, category.id):
            await self.latest_back_two.insert(
                inter.channel.id, category.id, label, 2, True
            )

        await self.latest_back_two.update_vc_id(voice.id, label, category.id)
        await self.latest_back_two.update_tc_id(text.id, voice.id)
        await self.latest_back_two.update_creeater(creater.id, voice.id)

        await self.latest_back_two.update_disabled(True, voice.id)
        await self.latest_back_two.update_style(2, voice.id)

        await self.update_view(inter, voice, data)

        def check(member, before, after):
            if after:
                if after.channel.id == voice.id:
                    return True

        try:
            await self.bot.wait_for("voice_state_update", check=check, timeout=3 * 60)
        except:
            if voice.members:
                return

            await self.update_view(inter, voice, data)

            try:
                await voice.delete()
            except:
                pass
            try:
                await text.delete()
            except:
                pass

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_label_open(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id not in self.list_label:
            return

        await inter.response.send_message(
            "お部屋の準備をしています。\nしばらくお待ち下さい。\n```内部の仕様変更により、裏2ショット関連の全てのボタンの反応が遅くなっています。```",
            ephemeral=True,
        )

        maindata = await self.latest_back_two.fetch_label(
            custom_id, inter.channel.category.id
        )

        creater = inter.guild.get_member(maindata.creater_id)

        if not (createrdata := await self.user_table.fetch(creater.id)):
            createrdata = await self.set_member_gender(creater)
            pass

        if not (pusherdata := await self.user_table.fetch(inter.user.id)):
            pusherdata = await self.set_member_gender(inter.user)
            pass

        if createrdata.gender == pusherdata.gender:
            return

        if not (voice := self.bot.get_channel(maindata.vc)):
            return

        if not (text := inter.guild.get_channel_or_thread(maindata.tc)):
            return

        await self.latest_back_two.update_disabled(True, voice.id)
        await self.latest_back_two.update_style(2, voice.id)
        await self.update_view(inter, voice, maindata)

        perms = {
            inter.guild.default_role: PermissionOverwrite(view_channel=False),
            creater: PermissionOverwrite(view_channel=True, connect=True),
            inter.user: PermissionOverwrite(view_channel=True, connect=True),
        }

        async for role in self.get_bot_roles(inter.guild):

            perms[role] = PermissionOverwrite(view_channel=True)

        await voice.edit(overwrites=perms)

        if isinstance(text, TextChannel):
            await text.edit(overwrites=perms)

        else:
            async for role in self.get_bot_roles(inter.guild):
                await text.send(role.mention)

        async for message in text.history(limit=None):
            if message.author.id != self.bot.user.id:
                continue

            if not message.embeds:
                continue

            e_dict = message.embeds[0].to_dict()

            target = e_dict["fields"][0]["value"]

            e_dict["fields"][0]["value"] = target.replace(": オープン", ": クローズ")

            e = Embed.from_dict(e_dict)
            await message.edit(embeds=[e])

        await text.send(f"{inter.user.mention}がこの部屋のボタンを押したので {voice.mention}をクローズしました")

        def check(member, before, after):
            if after:
                if after.channel.id == voice.id:
                    return True

        try:
            _, _, after = await self.bot.wait_for(
                "voice_state_update", check=check, timeout=1 * 60
            )
        except:
            members = [member for member in voice.members if not member.bot]

            if len(members) >= 2:
                return

            style = int(await self.get_button_style(creater))

            await self.latest_back_two.update_disabled(False, voice.id)
            await self.latest_back_two.update_style(style, voice.id)

            await self.update_view(inter, voice, maindata)

            async for message in text.history(limit=None):
                if message.author.id != self.bot.user.id:
                    continue

                if not message.embeds:
                    continue

                e_dict = message.embeds[0].to_dict()

                target = e_dict["fields"][0]["value"]

                e_dict["fields"][0]["value"] = target.replace(": クローズ", ": オープン")

                e = Embed.from_dict(e_dict)
                await message.edit(embeds=[e])

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_invite_user(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "invite_user":
            return

        await inter.response.defer()

        if not (voice := inter.user.voice):
            await inter.followup.send("ボイスチャンネルに接続してからボタンを押して下さい", ephemeral=True)
            return

        roomdata = await self.latest_back_two.fetch_vc(voice.channel.id)

        if roomdata.creater_id != inter.user.id:
            await inter.channel.send("このボタンは作成者のみ使用できます", delete_after=15)
            return

        if not (voice := self.bot.get_channel(roomdata.vc)):
            return

        if not (text := self.bot.get_channel(roomdata.tc)):
            return

        isomerism = await self.get_isomerism_role(inter.user)
        over = voice.overwrites

        if not roomdata.disabled:
            await self.latest_back_two.update_disabled(True, voice.id)
            await self.latest_back_two.update_style(2, voice.id)

            over[isomerism] = PermissionOverwrite(view_channel=False, connect=False)

            members = [
                member for member in inter.user.voice.channel.members if not member.bot
            ]

            if len(members) >= 2:
                name = f"{voice.name[0]}複数-{voice.name[1:]}"

            else:
                name = f"{voice.name[0]}-{voice.name[1:]}"

            await voice.edit(name=name, overwrites=over)

            e = normal(
                title="強制クローズしました",
                desc="```diff\n-個人に招待する処理のボタンがおされたため、強制的にクローズしました\n```",
            )

            e.add_field(name="WARNING", value="```\n再度オープンする時は、クローズ切り替えボタンを押して下さい\n```")

            await inter.channel.send(embeds=[e])

            e_dict = inter.message.embeds[0].to_dict()

            target = e_dict["fields"][0]["value"]

            e_dict["fields"][0]["value"] = target.replace(": オープン", ": クローズ")

            e = Embed.from_dict(e_dict)

            await inter.message.edit(embeds=[e])

        bot_message = await inter.channel.send(
            "3分以内に招待するユーザーの下4桁を入力してください。\n**#を含めても大丈夫です。**\n複数入力するときは必ず**半角**空白を開けて下さい\n入力例: #1234 5678 #9012"
        )

        def check(m):
            return m.author.id == inter.user.id and m.channel.id == inter.channel.id

        try:
            m = await self.bot.wait_for("message", check=check, timeout=3 * 60)
        except:
            return await inter.channel.send("入力されなかったため、キャンセルされました", delete_after=15)

        replace_m = m.content.replace("#", "")

        discriminators = replace_m.split(" ")

        current_discriminator = discriminators[0]
        current_number = 1

        results = {}

        for i, discriminator in enumerate(discriminators, 1):
            result = self.search_member_by_discriminator(inter.guild, discriminator)
            if not result:
                continue

            results[i] = {discriminator: result}

        if not results:
            return await inter.channel.send("指定された下4桁のユーザーが見つかりませんでした", delete_after=15)

        selected_members = []

        def make_embed(min_size, max_size):
            embed = normal(
                title="招待するユーザーを選択してください (20人ずつ表示)\n選択を終了するときは、全選択終了のボタンを押して下さい",
                description="\n".join(
                    f"{i}: {member.mention}"
                    for i, member in enumerate(selected_members, 1)
                ),
            )

            members = results[current_number][current_discriminator]

            embed.add_field(
                name=current_discriminator + " のユーザー一覧",
                value="\n".join(
                    f"{i}: {member.mention} ({member})"
                    for i, member in enumerate(members[min_size - 1 : max_size + 1], 1)
                ),
            )
            return embed

        e = make_embed(1, 21)

        def make_view(min_size, max_size):

            view = ui.View()
            try:
                next_discriminator = discriminators[current_number + 1]
            except:
                next_discriminator = None

            if next_discriminator is not None:

                view.add_item(
                    ui.Button(
                        label=f"次の #{next_discriminator}に移動",
                        custom_id="next_discriminator",
                        style=ButtonStyle.blurple,
                    )
                )

            view.add_item(
                ui.Button(
                    label=f"次の20人を表示",
                    custom_id="next_members",
                    style=ButtonStyle.green,
                )
            )

            view.add_item(ui.Button(label=f"前の20人を表示", custom_id="back_members"))

            view.add_item(
                ui.Button(label=f"全選択終了", custom_id="exit", style=ButtonStyle.red)
            )

            members = results[current_number][current_discriminator]

            row = 1
            for i in range(min_size, max_size):
                if i > len(members):
                    break

                view.add_item(ui.Button(label=f"{i}", row=row, custom_id=str(i)))

                if i % 5 == 0:
                    row += 1

            return view

        view = make_view(1, 21)

        m = await inter.channel.send(embeds=[e], view=view)

        def check(_inter):
            return _inter.message.id == m.id

        while True:
            _inter = await self.bot.wait_for("interaction", check=check)

            try:
                await _inter.response.defer()
            except:
                pass

            if current_number >= len(discriminator):
                break

            current_min = 1
            current_max = 21

            custom_id = _inter.data["custom_id"]

            if custom_id == "next_discriminator":
                current_discriminator += 1
                current_number += 1
                e = make_embed()
                view = make_view(1, 21)
                await m.edit(embeds=[e], view=view)

                continue

            if custom_id == "next_members":
                current_min += 20
                current_max += 20
                e = make_embed(current_min, current_max)
                view = make_view(current_min, current_max)

                await m.edit(embeds=[e], view=view)
                continue

            if custom_id == "back_members":
                current_min -= 20
                current_max -= 20
                e = make_embed(current_min, current_max)
                view = make_view(current_min, current_max)

                await m.edit(embeds=[e], view=view)
                continue

            if custom_id == "exit":
                try:
                    await bot_message.delete()
                    await m.delete()
                except:
                    pass
                break

            invite_user = results[current_number][current_discriminator][
                int(custom_id) - 1
            ]

            vcperms = voice.overwrites
            tcperms = text.overwrites

            vcperms[invite_user] = PermissionOverwrite(view_channel=True, connect=True)
            tcperms[invite_user] = PermissionOverwrite(view_channel=True, connect=True)

            await voice.edit(overwrites=vcperms)
            await text.edit(overwrites=tcperms)

            await text.send(
                f"{invite_user.mention}\nを{voice.mention}に招待しました！", delete_after=15
            )

        try:
            await bot_message.delete()
            await m.delete()
        except:
            pass

    def search_member_by_discriminator(self, guild: Guild, discriminator: str):
        results = []

        for member in guild.members:
            if member.bot:
                continue
            if member.discriminator == discriminator:
                results.append(member)

        return results

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_change_close(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "change_close_info":
            return

        await inter.response.defer()

        if not (voice := inter.user.voice):
            await inter.followup.send("ボイスチャンネルに接続してからボタンを押して下さい", ephemeral=True)
            return

        if not (data := await self.latest_back_two.fetch_vc(voice.channel.id)):
            await inter.followup.send(
                "不明なエラーにより実行できませんでした。ルームを作成しなおして下さい", ephemeral=True
            )
            return

        if data.creater_id != inter.user.id:
            await inter.followup.send("お部屋作成者のみが実行できます", ephemeral=True)
            return

        isomerism = await self.get_isomerism_role(inter.user)
        over = voice.channel.overwrites

        if data.disabled:
            await self.latest_back_two.update_disabled(False, voice.channel.id)
            style = await self.get_button_style(inter.user)
            await self.latest_back_two.update_style(int(style), voice.channel.id)
            before_info = ": クローズ"
            info = ": オープン"

            over[isomerism] = PermissionOverwrite(view_channel=True, connect=False)
            await voice.channel.edit(overwrites=over)

        else:
            await self.latest_back_two.update_disabled(True, voice.channel.id)
            await self.latest_back_two.update_style(2, voice.channel.id)
            before_info = ": オープン"
            info = ": クローズ"

            over[isomerism] = PermissionOverwrite(view_channel=False, connect=False)
            await voice.channel.edit(overwrites=over)

        e_dict = inter.message.embeds[0].to_dict()

        target = e_dict["fields"][0]["value"]

        e_dict["fields"][0]["value"] = target.replace(before_info, info)

        e = Embed.from_dict(e_dict)

        await inter.message.edit(embeds=[e])

        await self.update_view(inter, voice.channel, data)

        await inter.channel.send(f"お部屋を{info[2:]}しました！", delete_after=15)

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_reset_perms(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "reset_perms":
            return

        await inter.response.defer()

        if not (voice := inter.user.voice):
            await inter.followup.send("ボイスチャンネルに接続してからボタンを押して下さい", ephemeral=True)
            return

        if not (data := await self.latest_back_two.fetch_vc(voice.channel.id)):
            await inter.followup.send(
                "不明なエラーにより実行できませんでした。ルームを作成しなおして下さい", ephemeral=True
            )
            return

        if data.creater_id != inter.user.id:
            await inter.followup.send("お部屋作成者のみが実行できます", ephemeral=True)
            return

        tcperms, vcperms = await self.set_permission(inter.user, open_info=False)

        await self.latest_back_two.update_disabled(True, voice.channel.id)
        await self.latest_back_two.update_style(2, voice.channel.id)

        await voice.channel.edit(overwrites=vcperms)
        await inter.channel.edit(overwrites=tcperms)

        e_dict = inter.message.embeds[0].to_dict()

        target = e_dict["fields"][0]["value"]

        e_dict["fields"][0]["value"] = target.replace(": オープン", ": クローズ")

        e = Embed.from_dict(e_dict)

        await inter.message.edit(embeds=[e])

        await inter.channel.send(
            f"{inter.user.mention}\n権限をリセットし、クローズルームにしました。\nオープンルームにするときは、クローズ状況切り替えボタンを押して下さい。",
            delete_after=15,
        )

    @commands.Cog.listener("on_interaction")
    @excepter
    async def on_delete_message_log(self, inter: Interaction):
        if (custom_id := inter.data.get("custom_id")) is None:
            return

        if custom_id != "delete_message_log":
            return

        await inter.response.defer()

        if not (voice := inter.user.voice):
            await inter.followup.send("ボイスチャンネルに接続してからボタンを押して下さい", ephemeral=True)
            return

        if not (maindata := await self.latest_back_two.fetch_vc(voice.channel.id)):
            await inter.followup.send("不明なエラーが発生しました。お部屋を作成しなおしてください", ephemeral=True)
            return

        try:
            messages = [message async for message in inter.channel.history(limit=None)][
                :-1
            ]
        except:
            return await inter.followup.send("削除するメッセージが見つかりませんでした。", ephemeral=True)

        def check(m):
            return m in messages

        await inter.channel.purge(
            check=check, limit=None, reason="裏2ショット-全メッセージ削除ボタンが押されたため"
        )

    @commands.Cog.listener("on_voice_state_update")
    @excepter
    async def on_user_remove(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if (before.channel and after.channel) and (
            before.channel.id == after.channel.id
        ):
            return

        if not before.channel:
            return

        if not (data := await self.latest_back_two.fetch_vc(before.channel.id)):
            return

        members = [member for member in before.channel.members if not member.bot]

        if members:
            return

        text = member.guild.get_channel_or_thread(data.tc)

        if text:
            await text.delete()

        await before.channel.delete()

        await self.latest_back_two.update_style(2, before.channel.id)
        await self.latest_back_two.update_disabled(True, before.channel.id)

        await self.update_view(None, before.channel, data)

    async def update_view(self, inter: Interaction, voice: VoiceChannel, back_two_data):

        try:
            channel = self.bot.get_channel(back_two_data.panel_channel_id)
        except:
            channel = self.bot.get_channel(back_two_data.channel_id)

        label_panel = await channel.fetch_message(back_two_data.label_panel_id)

        panel_view = default_panel.copy()

        for category_data in await self.latest_back_two.fetchs_category(
            voice.category.id
        ):
            voice = self.bot.get_channel(category_data.vc)

            if not voice:
                category_data.disabled = True
                category_data.style = 2

            if voice:
                members = [member for member in voice.members if not member.bot]

                if (
                    not members
                    and (voice.created_at + timedelta(minutes=3)) < utils.utcnow()
                ):
                    panel_view[category_data.label]["disabled"] = True
                    panel_view[category_data.label]["style"] = 2
                    continue

            panel_view[category_data.label]["disabled"] = category_data.disabled
            panel_view[category_data.label]["style"] = category_data.style

        view = ui.View(timeout=1)

        for k, v in panel_view.items():

            view.add_item(
                ui.Button(
                    label=k,
                    style=v["style"],
                    row=v["row"],
                    custom_id=v["custom_id"],
                    disabled=v["disabled"],
                )
            )

        await label_panel.edit(view=view)

    async def check_voice_room(self, category: CategoryChannel):
        datas = await self.latest_back_two.fetchs_category(category.id)

        for data in datas:
            vc = self.bot.get_channel(data.vc)

            if vc is None:
                await self.latest_back_two.update_disabled(True, data.vc)
                await self.latest_back_two.update_style(2, data.vc)

    async def _sync_open_panel_embed(
        self, data: db.models.back.Open_Panel_Embed
    ) -> TextChannel:

        e = normal(
            title=data.title,
            desc=data.description,
            color=data.color,
        )

        channel: TextChannel = self.bot.get_channel(data.channel_id)
        message: Message = await channel.fetch_message(data.panel_id)

        await message.edit(embeds=[e])

        return channel

    async def _sync_label_panel_embed(
        self, data: db.models.back.Label_Panel_Embed
    ) -> TextChannel:

        e = normal(
            desc=data.description,
            color=data.color,
        )

        e.add_field(name=data.field_one_key, value=data.field_one_value)

        e.add_field(name=data.field_two_key, value=data.field_two_value)

        e.add_field(name=data.field_three_key, value=data.field_three_value)

        channel: TextChannel = self.bot.get_channel(data.channel_id)
        message: Message = await channel.fetch_message(data.panel_id)

        await message.edit(embeds=[e])

        return channel

    def get_no_use_label(self, category: CategoryChannel):
        used_name = [channel.name[0] for channel in category.voice_channels]

        # 使われてないラベルを取得
        no_used_name = [abc for abc in self.list_label if abc not in used_name][0]

        return no_used_name

    async def set_member_gender(self, member: Member):
        guild = member.guild
        data = await self.dbroles.fetch(guild.id)
        boy = guild.get_role(data.boy)

        if boy in member.roles:
            gender = "boy"
            await self.user_table.insert(member.id)

        else:
            gender = "girl"
            await self.user_table.insert(member.id, member.name, "girl", guild)

        await self.user_table.update_user_name(member.name, member.id)
        await self.user_table.update_gender(gender, member.id)
        await self.user_table.update_guild_id(guild.id, member.id)
        await self.user_table.update_guild_name(guild.name, member.id)

        return await self.user_table.fetch(member.id)

    async def get_button_style(self, member: Member):
        data = await self.user_table.fetch(member.id)

        if data.gender == "boy":
            return ButtonStyle.blurple
        else:
            return ButtonStyle.red

    async def get_block_list(self, member: Member):
        if not (data := await self.block_list.fetch(member.id)):
            return

        for user_id in data.users:
            user = member.guild.get_member(user_id)

            if not user:
                continue

            yield user

    async def get_isomerism_role(self, member: Member):
        guild = member.guild

        if not (data := await self.user_table.fetch(member.id)):
            data = await self.set_member_gender(member)

        gsp_role_data = await self.dbroles.fetch(guild.id)

        if data.gender == "boy":
            isomerism = guild.get_role(gsp_role_data.girl)
        else:
            isomerism = guild.get_role(gsp_role_data.boy)

        return isomerism

    async def get_bot_roles(self, guild: Guild):
        gsp_role_data = await self.dbroles.fetch(guild.id)

        bot_roles = [
            guild.get_role(role_id)
            for role_id in gsp_role_data.bot
            if guild.get_role(role_id)
        ]

        for bot_role in bot_roles:
            yield bot_role

    async def set_permission(self, creater: Member, *, open_info):
        guild = creater.guild
        tcperms = {
            guild.default_role: PermissionOverwrite(view_channel=False, connect=False),
            creater: PermissionOverwrite(view_channel=True, connect=True),
        }

        if not (data := await self.user_table.fetch(creater.id)):
            data = await self.set_member_gender(creater)

        gsp_role_data = await self.dbroles.fetch(guild.id)

        async for block_list_user in self.get_block_list(creater):
            tcperms[block_list_user] = PermissionOverwrite(view_channel=False)

        async for bot_role in self.get_bot_roles(guild):
            tcperms[bot_role] = PermissionOverwrite(view_channel=True, connect=True)

        vcperms = tcperms.copy()

        if open_info:
            if data.gender == "boy":
                isomerism = guild.get_role(gsp_role_data.girl)
            else:
                isomerism = guild.get_role(gsp_role_data.boy)

            vcperms[isomerism] = PermissionOverwrite(view_channel=True)

        return tcperms, vcperms

    async def create_room(
        self,
        creater: Member,
        *,
        category: CategoryChannel,
        label: str,
        vcperms: dict[Any, PermissionOverwrite],
        tcperms: dict[Any, PermissionOverwrite],
        text_type: int,
        main_channel: TextChannel = None,
    ):

        name = f"{label}-{creater.name}"

        voice = await category.create_voice_channel(name=name, overwrites=vcperms)

        if (
            creater.guild.premium_subscription_count >= 7
            and text_type == 0
            and main_channel
        ):
            text: Thread = await main_channel.create_thread(name=name)
            await text.add_user(creater)

            async for role in self.get_bot_roles(creater.guild):
                await text.send(role.mention)

        else:

            text = await category.create_text_channel(
                name=name, overwrites=tcperms, topic=str(voice.id)
            )

        return voice, text

    async def create_room_setting_panel(
        self, *, voice: VoiceChannel, text: TextChannel, _open_info: bool
    ):
        open_info = "オープン" if _open_info else "クローズ"

        guild = voice.guild
        view = ui.View(timeout=1)

        view.add_item(
            ui.Button(
                label="ルーム名変更", style=ButtonStyle.green, custom_id="change_room_name"
            )
        )
        view.add_item(
            ui.Button(
                label="ビットレート変更", style=ButtonStyle.blurple, custom_id="change_bitrate"
            )
        )
        view.add_item(
            ui.Button(label="簡易閲覧権限確認", style=ButtonStyle.red, custom_id="show_perms")
        )

        view.add_item(ui.Button(label="クローズ状況切替", custom_id="change_close_info", row=1))

        view.add_item(ui.Button(label="招待ユーザー指定", custom_id="invite_user", row=1))
        view.add_item(
            ui.Button(
                label="権限リセット", custom_id="reset_perms", style=ButtonStyle.red, row=2
            )
        )

        view.add_item(
            ui.Button(
                label="メッセージ全削除",
                custom_id="delete_message_log",
                style=ButtonStyle.red,
                row=2,
            )
        )

        e = normal(
            desc=f"```diff\n- VCに接続せずに押しても反応しません\n```",
        )

        e.add_field(
            name="●ルームinfo●",
            value=f"```\nルーム名: {voice.name}\nビットレート: {voice.bitrate // 1000}\nクローズ状況: {open_info}\n```",
            inline=False,
        )

        e.add_field(
            name="⛔永久ブロック設定⛔",
            value=f"`{guild.me.name}Botが入っている全サーバー共通の裏２shot用ブロック機能`\n"
            f"《追加/解除/確認》\n{guild.me.mention}のDMでコマンド実行\n"
            "　　　　　　sc:ブロック",
        )

        return e, view


async def setup(bot):
    await bot.add_cog(BackTwoCog(bot))

    await bot.tree.sync()

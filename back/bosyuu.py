from discord.ext import commands

from datetime import timedelta
from typing import TYPE_CHECKING
from lib import normal, admin

from views import modals

import db

from discord import (
    ui,
    ButtonStyle,
    utils,
    Colour,
    Interaction,
    TextChannel,
    Member,
    Embed,
    Message,
    Role,
)

if TYPE_CHECKING:
    from backrun import Same


class BosyuuView(ui.View):
    @ui.button(label="立候補", custom_id="rikkouho", style=ButtonStyle.green)
    async def rikkouho(self, button, inter):
        pass

    @ui.button(label="取消", custom_id="torikesi", style=ButtonStyle.red)
    async def torikesi(self, button, inter):
        pass


class CheckView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="削除", custom_id="check_delete", style=ButtonStyle.red)
    async def delete(self, inter, _):
        await self.message.delete()

        await inter.response.send_message(
            f"{self.message.channel}の募集文を削除しました！", ephemeral=True
        )

        self.stop()


class Back_Recruiti:
    def __init__(self, bot: "Same"):
        self.bot = bot

        self.base_panel = db.back.Back_Recruiti_Base_Panel()
        self.panel_desc = db.back.Back_Recruiti_Desc()
        self.panel = db.back.Back_Recruiti_Panel()
        self.panel_dm = db.back.Back_Recruiti_DM()
        self.user_panel = db.back.Back_Recruiti_User_Panel()

        self.users = db.info.Users()
        self.dbroles = db.info.Role()

    async def get_user_recruiti_data(self, base_channel: TextChannel, member: Member):
        return await self.user_panel.fetch_by_user(member.id, base_channel.id)

    async def get_modal_default_content(self, inter: Interaction) -> str:
        if data := await self.get_user_recruiti_data(inter.channel, inter.user):
            content = data.content
        else:
            data = await self.base_panel.fetch_by_channel(inter.channel.id)
            content = data.template

        return content

    async def input_recruiti(self, inter: Interaction) -> str:
        default_content = await self.get_modal_default_content(inter)

        modal = modals.Recruiti(default_content)

        await modal.wait()

        return modal.children[0].value

    def replace_message(self, content: str, member: Member) -> str:
        prof = self.get_profile(member)

        return (
            content.replace("{nickname}", member.display_name)
            .replace("{mention}", member.mention)
            .replace("{user}", str(member))
            .replace("{url}", prof.jump_url)
        )

    async def get_genders(self, member: Member) -> tuple[Role, Role]:
        guild = member.guild
        role_data = await self.dbroles.fetch(guild.id)

        boy = guild.get_role(role_data.boy)
        girl = guild.get_role(role_data.girl)

        user_info = await self.users.fetch(member.id)

        if user_info.gender == "boy":
            isomerism = girl
            gender = boy
        else:
            isomerism = boy
            gender = girl

        return isomerism, gender

    async def replace_mention(self, content: str, member: Member) -> str:
        genders = await self.get_genders(member.guild)
        return content.replace("{異性メンション}", genders[0].mention).replace(
            "{同性メンション}", genders[1].mention
        )

    async def replace_color(self, content: str, member: Member) -> str:
        genders = await self.get_genders(member.guild)

        return content.replace("{異性カラー}", genders[0].color).replace(
            "{同性カラー}", genders[1].color
        )

    def _replace_recruiti(self, content: str, recruiti_channel: TextChannel) -> str:

        now = utils.utcnow()

        fmt_now = utils.format_dt(now)

        content = content.replace("{channel}", recruiti_channel.mention)
        content = content.replace("{category}", recruiti_channel.category.name)
        content = content.replace("{now}", fmt_now)

        return content

    async def replace(
        self, content: str, inter: Interaction, recruiti_channel: TextChannel
    ):
        content = self.replace_message(content, inter.user)
        content = await self.replace_mention(content, inter.user)
        content = await self.replace_color(content, inter.user)
        content = self._replace_recruiti(content, recruiti_channel)

        return content

    async def set_recruiti_panel(self, inter: Interaction) -> Embed:
        maindata = await self.panel.fetch_data_by_channel(inter.channel.id)

        prm = {}

        if maindata.title:
            prm["title"] = self.replae(maindata.title)

        if maindata.description:
            prm["description"] = maindata.description

        if maindata.color:
            prm["color"] = Colour(maindata.color)

        e = normal(**prm)

        author_prm = {}

        if maindata.name:
            author_prm["name"] = maindata.name

        if maindata.icon_display == "する":
            author_prm["icon_url"] = inter.user.avatar.url

        e.set_author(**author_prm)

        thumbnail_prm = {}

        if maindata.icon_display == "する":
            thumbnail_prm["url"] = inter.user.avatar.url

        e.set_thumbnail(**thumbnail_prm)
        return e


# COG
class BackBosyuu(commands.Cog, name="裏募集"):
    def __init__(self, bot: "Same"):
        self.bot = bot
        self.base_panel = db.back.Back_Recruiti_Base_Panel()
        self.panel_desc = db.back.Back_Recruiti_Desc()
        self.panel = db.back.Back_Recruiti_Panel()
        self.panel_dm = db.back.Back_Recruiti_DM()
        self.user_panel = db.back.Back_Recruiti_User_Panel()

        self.ext_back_recruiti = Back_Recruiti(bot)

        self.users = db.info.Users()
        self.dbroles = db.info.Role()

        self.night_time: list[int] = [0, 1, 2, 3, 4, 5, 6, 7]

    @commands.hybrid_command(name="裏募集作成", description="裏募集を作成する")
    @admin()
    async def create_recruiti(self, ctx: commands.Context, tc: TextChannel = None):
        await ctx.defer(ephemeral=True)

        tc = tc or ctx.channel

        e = normal(
            title="裏募集パネル",
            desc="下記のボタンを押すと、あなた専用の代理投稿用チャンネルが作成されます。`(投稿後自動削除 or 5分で自動消滅)`",
        )

        view = ui.View(timeout=1)
        view.add_item(
            ui.Button(label="新規/編集", style=ButtonStyle.green, custom_id="create")
        )
        view.add_item(ui.Button(label="削除", style=ButtonStyle.red, custom_id="delete"))
        view.add_item(
            ui.Button(label="確認", style=ButtonStyle.primary, custom_id="check")
        )

        await tc.send(embeds=[e], view=view)

    @commands.hybrid_command(
        name="裏募集同期",
    )
    @admin()
    @commands.cooldown(1, 60 * 30, commands.BucketType.user)
    async def sync_recruiti(self, ctx: commands.Context, tc: TextChannel = None):
        """
        裏募集の設定を同期する

        """

        await ctx.send("裏募集を同期しています。\nこの処理はかなり時間がかかるため、完了するまで暫くお待ちください")
        print("スプシ同期中")
        await self.gback_recruiti.fetch_back_recruiti_all_data_by_guild(ctx.guild.id)

        datas = await self.base_panel.fetchs(ctx.guild.id)
        if not datas:
            return await ctx.send("データが見つかりませんでした。")

        for data in datas:
            channel: TextChannel = self.bot.get_channel(data.base_channel_id)

            if not channel:
                continue

            desc_data = await self.panel_desc.fetch_data_by_channel(channel.id)
            prm = {}

            if desc_data.title:
                prm["title"] = desc_data.title

            if desc_data.description:
                prm["description"] = desc_data.description

            if desc_data.color:
                prm["color"] = desc_data.color

            try:
                message: Message = await channel.fetch_message(desc_data.panel_id)
            except:
                continue

            e = normal(**prm)

            await message.edit(embeds=[e])

        await ctx.send("裏募集の同期が完了しました。")

    @sync_recruiti.error
    async def sync_recruiti_error(self, ctx: commands.Context, error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                f"このコマンドは30分に一回しか実行できません。`約{int(error.retry_after) // 60}秒後`に再実行してください。"
            )

    async def is_run(self, inter, custom_id: int) -> bool:
        """
        実行していいか確認する

        Parameters
        ----------
        inter : Interaction
            discord.Interaction
        custom_id : int
            押されたボタンのcustom_id


        Returns
        -------
        bool 実行していいならBack_Paneru それ以外はFalse


        """

        if inter.data.get("custom_id") is None:
            return False

        if inter.data["custom_id"] != custom_id:
            return False

        return True

    @commands.Cog.listener("on_interaction")
    async def on_new_back(self, inter: Interaction):

        if (data := await self.is_run(inter, "create")) == False:
            return

        user_recruiti_message_id = None

        # モーダルウィンドウのデフォルト文章を作成
        # 募集文が作成されてなければ、テンプレートを使う

        # 募集済みかどうか判定する
        if user_data := await self.user_panel.fetch_by_user(
            inter.user.id, inter.channel.id
        ):

            default_content = ""

            # 募集文を1行ずつパース
            for content in user_data.content.splitlines():

                # contentに <@!{user_id}>が含まれてたらデフォルト文章に含めない
                if str(inter.user.id) in content:
                    continue

                # contentに https://discord.com/guild_id が含まれてたらデフォルト文章に含めない
                if str(inter.guild.id) in content:
                    continue

                # contentが空だったらデフォルト文章に含めない
                if content == "":
                    continue

                default_content += content + "\n"

            user_recruiti_message_id = user_data.recruiti_panel_id
        else:
            data = await self.base_panel.fetch_by_channel(inter.channel.id)

            if not data:
                return await inter.response.send_message(
                    "データが見つかりませんでした。管理者にスプレッドシートを確認するように報告してください"
                )
            default_content = data.template

        modal = modals.Recruiti(default_content)

        try:
            await inter.response.send_modal(modal)
        except:
            return await inter.user.send("投稿フォームの作成に失敗しました。もう一度ボタンを押して下さい")

        await modal.wait()

        recruiti_content = modal.children[0].value

        maindata = await self.base_panel.fetch_by_channel(inter.channel.id)

        role_data = await self.dbroles.fetch(inter.guild.id)

        base_boy = inter.guild.get_role(role_data.boy)
        base_girl = inter.guild.get_role(role_data.girl)

        if base_boy in inter.user.roles:
            gender_name = "boy"
            recruiti_channel_id = maindata.boy_channel_id
        else:
            gender_name = "girl"
            recruiti_channel_id = maindata.girl_channel_id

        if not await self.users.fetch(inter.user.id):
            await self.users.insert(inter.user.id)

            await self.users.update_user_name(inter.user.name, inter.user.id)
            await self.users.update_gender(gender_name, inter.user.id)
            await self.users.update_guild_id(inter.guild.id, inter.user.id)
            await self.users.update_guild_name(inter.guild.name, inter.user.id)

        recruiti_channel = self.bot.get_channel(recruiti_channel_id)

        prof = self.get_profile(inter.user)

        fmt_now = utils.format_dt(inter.created_at)

        def replace(content):
            now = utils.utcnow() + timedelta(hours=9)

            if now.hour not in self.night_time:
                boy = inter.guild.get_role(maindata.boy_role_id)
                girl = inter.guild.get_role(maindata.girl_role_id)

            else:
                boy = inter.guild.get_role(maindata.night_boy_role_id)
                girl = inter.guild.get_role(maindata.night_girl_role_id)

            if base_boy in inter.user.roles:
                isomerism = girl
                gender = base_boy
            else:
                isomerism = boy
                gender = base_girl

            result = (
                str(content)
                .replace("{nickname}", inter.user.display_name)
                .replace("{mention}", inter.user.mention)
                .replace("{user}", str(inter.user))
                .replace("{url}", prof.jump_url)
                .replace("{異性メンション}", isomerism.mention)
                .replace("{同性メンション}", gender.mention)
                .replace("{異性カラー}", str(int(isomerism.color)))
                .replace("{同性カラー}", str(int(gender.color)))
                .replace("{channel}", recruiti_channel.name)
                .replace("{category}", recruiti_channel.category.name)
                .replace("{now}", fmt_now)
                .replace("{募集文}", recruiti_content)
            )

            return result

        prm = {}

        recruiti_data = await self.panel.fetch_by_channel(inter.channel.id)

        if recruiti_data.title:
            prm["title"] = replace(recruiti_data.title)

        if recruiti_data.description:
            prm["description"] = replace(recruiti_data.description)

        if recruiti_data.color:
            prm["color"] = int(replace(recruiti_data.color))

        e = normal(**prm)

        author_prm = {}

        if recruiti_data.name:
            author_prm["name"] = replace(recruiti_data.name)

        if recruiti_data.icon_display == "する":
            author_prm["icon_url"] = inter.user.avatar.url

        e.set_author(**author_prm)

        thumbnail_prm = {}

        if recruiti_data.icon_display == "する":
            thumbnail_prm["url"] = inter.user.avatar.url

        e.set_thumbnail(**thumbnail_prm)

        message_prm = {"content": replace(recruiti_data.content), "embeds": [e]}

        if "匿名ボタン" in prm["description"]:
            message_prm["view"] = BosyuuView()
        else:
            message_prm["view"] = None

        if not user_recruiti_message_id:
            recrutied = await recruiti_channel.send(**message_prm)

            await self.user_panel.insert(recrutied.id)
            await self.user_panel.update_user_id(inter.user.id, recrutied.id)
            await self.user_panel.update_base_channel_id(inter.channel.id, recrutied.id)
            await self.user_panel.update_recruiti_channel_id(
                recruiti_channel_id, recrutied.id
            )

        else:
            try:
                recrutied = await recruiti_channel.fetch_message(
                    user_recruiti_message_id
                )
            except:
                recrutied = await recruiti_channel.send(**message_prm)

                await self.user_panel.update_panel(
                    recrutied.id, inter.user.id, inter.channel.id
                )
            else:
                await recrutied.edit(**message_prm)

        await self.user_panel.update_content(prm["description"], recrutied.id)

        dm_data = await self.panel_dm.fetch_by_channel(inter.channel.id)

        if dm_data.title:
            prm["title"] = replace(dm_data.title)

        if prm.get("description"):
            del prm["description"]

        if dm_data.color:
            prm["color"] = int(replace(dm_data.color))

        e = normal(**prm)

        if dm_data.field_one_key:
            e.add_field(
                name=dm_data.field_one_key,
                value=replace(dm_data.field_one_value),
            )

        if dm_data.field_two_key:
            e.add_field(
                name=dm_data.field_two_key,
                value=replace(dm_data.field_two_value),
            )

        await inter.user.send(embeds=[e])

    def get_profile(self, member: Member) -> Message:
        if cache := self.bot.caches["prof"].get(member.guild.id):
            return cache.get(member.id)

    @commands.Cog.listener("on_interaction")
    async def on_delete_back(self, inter: Interaction):
        if (data := await self.is_run(inter, "delete")) == False:
            return

        def check(m):
            return m.author.id == self.bot.user.id

        await inter.response.defer(ephemeral=True)

        if not (
            user_data := await self.user_panel.fetch_by_user(
                inter.user.id, inter.channel.id
            )
        ):
            return await inter.followup.send(
                "まだ募集を出していません！\n**募集更新**ボタンを押して募集を出してください！", ephemeral=True
            )

        channel: TextChannel = self.bot.get_channel(user_data.recruiti_channel_id)
        message = await channel.fetch_message(user_data.recruiti_panel_id)

        await self.user_panel.delete(inter.channel.id, inter.user.id)

        await message.delete()

        e = normal(desc=f"{channel}の{inter.user}の募集を削除したよ!")
        await inter.followup.send(
            f"**このメッセージは{inter.user}のみに見えているよ。**", embeds=[e], ephemeral=True
        )

    @commands.Cog.listener("on_interaction")
    async def on_check_back(self, inter: Interaction):
        if (data := await self.is_run(inter, "check")) == False:
            return

        await inter.response.defer()

        if not (
            user_data := await self.user_panel.fetch_by_user(
                inter.user.id, inter.channel.id
            )
        ):
            return await inter.followup.send(
                "まだ募集を出していません！\n**募集更新**ボタンを押して募集を出してください！", ephemeral=True
            )

        channel: TextChannel = self.bot.get_channel(user_data.recruiti_channel_id)
        message = await channel.fetch_message(user_data.recruiti_panel_id)

        content = user_data.content

        view = CheckView()
        view.message = message

        e = normal(desc=f"{channel}の投稿内容を削除する時は**削除**ボタンを押してください")
        e.add_field(name="投稿内容", value=content)
        await inter.user.send(embeds=[e], view=view)

        await view.wait()

        await self.user_panel.delete(inter.channel.id, inter.user.id)

    @commands.Cog.listener("on_interaction")
    async def on_standby_cancel(self, inter: Interaction):
        if inter.data.get("custom_id") is None:
            return False

        custom_id = inter.data["custom_id"]

        if custom_id not in ["rikkouho", "torikesi"]:
            return

        try:
            await inter.response.defer()
        except:
            pass

        user_data = await self.user_panel.fetch_by_panel_id(inter.message.id)

        if not user_data:
            await inter.followup.send(
                "申し訳ございません。こちらの募集文は不具合により立候補受付無効となっています。", ephemeral=True
            )
            try:
                await inter.guild.owner.send(
                    f"{inter.message.jump_url}\nこちらの募集文のデータが破損しました。\n募集を削除したうえで、募集投稿主に削除した旨を連絡してください。"
                )
            except:
                pass

            dev = self.bot.get_user(386289367955537930)
            await dev.send(
                f"募集の立候補に失敗\nサーバー: {inter.guild}\nチャンネル: {inter.channel}",
                embeds=inter.message.embeds,
            )
            return

        channel = inter.channel
        create_time = inter.message.created_at

        user_id = user_data.user_id
        fmt_create_time = utils.format_dt(create_time)

        if inter.message.embeds == []:
            return

        target = inter.guild.get_member(user_id)
        member = inter.user
        if custom_id == "rikkouho":
            await target.send(
                f"🙋 {member.display_name} から 立候補\n【ｱｶｳﾝﾄ名】{member.mention} ({member})\n【投稿日時】{fmt_create_time}\n({inter.guild.name} / #{channel})\n------------------------------------------"
            )
            await member.send(
                f"✋ {target.display_name} へ 立候補完了\n【ｱｶｳﾝﾄ名】{target.mention} ({target})\n【投稿日時】{fmt_create_time}\n({inter.guild.name} / {channel.mention})\n`取り消しをする場合は、募集文の`取消`を押してください`\n------------------------------------------"
            )
        elif custom_id == "torikesi":
            await target.send(
                f"🙏 {member.display_name} から 取消\n【ｱｶｳﾝﾄ名】{member.mention} ({member})\n【投稿日時】{fmt_create_time}\n({inter.guild.name} / #{channel})\n------------------------------------------"
            )

            await member.send(
                f"❎ {target.display_name} へ 取消完了\n【ｱｶｳﾝﾄ名】{target.mention} ({target})\n【投稿日時】{fmt_create_time}\n({inter.guild.name} / {channel.mention})\n------------------------------------------"
            )


async def setup(bot):
    await bot.add_cog(BackBosyuu(bot))

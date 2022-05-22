from discord.ext import commands as c
from discord import ui
from typing import List, Optional, Tuple
from lib import normal, error

import db

import re

from discord import (
    ui,
    ButtonStyle,
    utils,
    PermissionOverwrite,
    Colour,
    Interaction,
    User,
    Message,
)


emojis = {
    0: "0️⃣",
    1: "1⃣",
    2: "2⃣",
    3: "3⃣",
    4: "4⃣",
}


__all__ = ("BlockListView",)


class BlockListView(ui.View):
    def __init__(self, ctx: c.Context, author: Optional[User] = None):
        self.ctx: c.Context = ctx
        self.author: User = author or ctx.author
        super().__init__(timeout=None)
        self.min_size: int = 0
        self.max_size: int = 20
        self.block_list_name: str = "block_list"
        self.block_list = db.back.Block_List(bot=ctx.bot)

        self.bot: c.Bot = ctx.bot
        self.creater_id: int = self.author.id

        self.stop_flag: bool = False

    @ui.button(label="1⃣ 追加", custom_id=f"back_1")
    async def add_black_list(self, inter, _):
        self.stop()

        if not (user_data := await self.block_list.get_block_list(self.creater_id)):
            await self.block_list.insert(self.creater_id)
            user_data = await self.block_list.get_block_list(self.creater_id)

        if await self.add_check(user_data.users) == False:
            return

        e = normal(
            desc="追加するユーザーを指定してください。\n〖指定方法〗#以降の4桁、名前#0000、IDいずれか\n`例：@裏サメの場合　⇒　5204、#5204、裏サメ#5204、893422980649074710`"
        )
        await inter.response.send_message("⚠️ 複数人同時に並べて指定できます", embeds=[e])
        try:
            input_user: Message = await self.bot.wait_for(
                "message",
                check=lambda m: m.author.id == self.creater_id,
                timeout=60 * 60 * 2,
            )
        except:
            return await self.message.edit(
                content=f"30分以内に指定されなかったため、終了しました。\n再度設定する場合はもう一度`sa:{self.ctx.command}`と入力してください"
            )

        add_block_users, no_found_users = await self.search_user(input_user)

        if len(add_block_users) > 10:
            e = error("現在10人までしか追加できません")
            return await inter.channel.send(embeds=[e])

        await self.db_add_block_users(add_block_users)

        await self.send_alert_embed()

        if len(no_found_users) > 0 and len(add_block_users) == 0:
            return

        await self.send_found_user(add_block_users)

        if len(no_found_users) == 0:
            return

        await self.send_no_found_user(no_found_users)

    @ui.button(label="2⃣ 削除", custom_id=f"back_2", style=ButtonStyle.primary)
    async def rm_black_list(self, inter: Interaction, _):
        self.stop()

        if not (user_data := await self.block_list.get_block_list(self.creater_id)):
            await self.block_list.insert(self.creater_id)
            user_data = await self.block_list.get_block_list(self.creater_id)

        if await self.remove_check(user_data.users) == False:
            return

        e = normal(
            desc="削除するユーザーを指定してください。\n〖指定方法〗#以降の4桁、名前#0000、IDいずれか\n`例：@裏サメの場合　⇒　5204、#5204、裏サメ#5204、893422980649074710`"
        )
        await inter.response.send_message("⚠️ 複数人同時に並べて指定できます", embeds=[e])
        try:
            input_user = await self.bot.wait_for(
                "message",
                check=lambda m: m.author.id == self.creater_id,
                timeout=60 * 60 * 2,
            )
        except:
            return await self.message.edit(
                content=f"時間内に指定されなかったため、終了しました。\n再度設定する場合はもう一度`sa:{self.ctx.command}`と入力してください"
            )

        rm_block_users, no_found_users = await self.search_user(input_user)

        await self.db_rm_block_users(rm_block_users)

        if len(no_found_users) > 0 and len(rm_block_users) == 0:
            return

        await self.send_found_user(rm_block_users, False)

        if len(no_found_users) == 0:
            return

        await self.send_no_found_user(no_found_users)

    @ui.button(label="3⃣ 確認", style=ButtonStyle.green, custom_id=f"back_3")
    async def check_black_list(self, inter: Interaction, _):
        self.stop()

        if not (user_data := await self.block_list.get_block_list(self.creater_id)):
            e = error("ブロックリストに誰も追加していません！")
            return await self.ctx.send(embeds=[e])

        desc = ""

        for i, user_id in enumerate(user_data.users, 1):
            desc += f"{i}: {self.bot.get_user(int(user_id)) or user_id}\n"

        e = normal(title="キャッシュに存在しないユーザーはID表示になります。", desc=desc)
        await inter.response.send_message(
            f"{self.ctx.author.mention}さんが登録しているブロックリストです。", embeds=[e]
        )

    @ui.button(label="0️⃣ 終了", style=ButtonStyle.red, custom_id=f"back_0", row=1)
    async def end_back(self, _, __):
        self.stop()
        try:
            await self.message.delete()
        except:
            pass

    @ui.button(label="4⃣ リセット", style=ButtonStyle.red, custom_id="back_4", row=1)
    async def rs_back(self, inter: Interaction, _):
        await inter.response.defer()
        if not await self.block_list.get_block_list(self.creater_id):
            e = error("ブロックリストに誰も追加していません！")
            return await self.ctx.send(embeds=[e])

        def check(res):
            return res.message.id == m.id and res.user.id == self.creater_id

        view = ui.View()
        view.add_item(ui.Button(label="YES", style=ButtonStyle.green, custom_id="yes"))
        view.add_item(ui.Button(label="NO", style=ButtonStyle.red, custom_id="no"))

        m = await self.ctx.send("本当にブラックリストをリセットしますか？", view=view)

        try:
            res = await self.bot.wait_for("interaction", check=check, timeout=180)
        except:
            await self.ctx.send("処理を中断しました。", delete_after=300)

        if res.data["custom_id"] == "no":
            await m.delete()
            return

        await self.block_list.delete(self.creater_id)

        e = normal(desc=f"{self.ctx.author}のブラックリストを正常にリセットしました。")

        await inter.followup.send(embeds=[e])

        self.stop()

    async def add_check(self, block_list: List[int], max_size: int = 10) -> bool:
        """
        coroutine

        ブラックリストに追加できるか確認する

        Parameters
        ----------
        block_list : List[int]
            ブラックリストのデータ

        max_size : int
            ブラックリストの最大サイズ

        Returns
        -------
        bool
        """

        if len(block_list) > max_size:
            mes = "ブロックリストに追加できませんでした。\n"
            mes += f"ブロックリストに追加できるユーザーは{max_size}人までです。"

            e = error(mes)
            await self.ctx.send(embeds=[e])
            return False

        return True

    async def remove_check(self, data):
        """
        coroutine

        ブラックリストから削除できるか確認する

        Parameters
        ----------
        block_list : List[int]
            ブラックリストのデータ

        Returns
        -------
        bool
        """

        if len(data) == 0:
            mes = "ブロックリストから削除できませんでした。\n"
            mes += f"ブロックリストにユーザーを追加してください。"

            e = error(mes)
            await self.ctx.send(embeds=[e])
            return False

        return True

    def search_discriminator(self, discriminator: str) -> List[int]:
        """
        指定された識別番号と一致するユーザーを検索する

        Parameters
        ----------
        discriminator : str
            識別番号

        Returns
        -------
        List[int]

        """
        target = []
        for user in self.bot.users:
            if user.discriminator == discriminator:
                if user.id not in target:
                    target.append(user.id)

        return target

    async def wait_interaction(self, mes: Message) -> Optional[Message]:
        """
        coroutine

        ユーザーからのボタン操作を待つ

        Parameters
        ----------
        mes : discord.Message
            メッセージ

        Return
        --------
        Optional[Message]
        """
        try:
            return await self.bot.wait_for(
                "interaction",
                check=lambda res: res.message.id == mes.id,
                timeout=60 * 30,
            )
        except:
            await mes.delete()
            await self.message.edit(
                content="30分以内に押されなかったため、終了しました。\n再度設定する場合はもう一度`b_b`と入力してください"
            )
            return None

    def check_id(self, res: Interaction, max_size: int) -> str:
        """
        custom_idを確認する

        次の20人を見るか、前の20人を見るか、止めるか

        Parameters
        ----------
        res : Interaction
            インタラクション

        max_size : int
            表示する人数最大サイズ

        Returns
        -------
        str
        """

        if res.data["custom_id"] == f"back_users_end":
            return "break"

        elif res.data["custom_id"] == f"back_users_next":
            max_size += 20
            return "continue"
        elif res.data["custom_id"] == f"back_users_back":
            max_size -= 20
            return "continue"

    async def append_user(
        self, res: Interaction, add_block_users: List[int], mes: Message
    ) -> None:
        """
        coroutine

        指定したユーザーをブラックリストに追加する

        Parameters
        ----------
        res : Interaction
            インタラクション

        add_block_users : List[int]
            ブラックリストのデータ

        mes : discord.Message
            メッセージ

        Returns
        -------
        None
        """

        custom_id_split = res.data["custom_id"].split(f"back_users_")
        add_block_users.append(int(custom_id_split[1]))
        await mes.delete()

    async def search_user(self, input_user: Message) -> Tuple[List[int], List[int]]:
        """
        coroutine
        ユーザーを検索する

        Parameters
        ----------
        input_user : discord.Message
            メッセージ

        Returns
        -------
        Tuple[List[int], List[int]]
        """

        pat = r"(?P<user>(\w+)#([0-9]{4}))|(?P<userid>[0-9]{17,19})|(?P<user_dis>(#)?([0-9]{4}))"
        add_block_users = []
        no_found_user = []

        results = re.finditer(pat, input_user.content)
        for result in results:
            for v in result.groupdict():
                if v is None:
                    continue
                group = result.group(v)
                if group is None:
                    continue
                r = str(group)

                if v == "user":
                    user_split = r.split("#")
                    user = utils.get(
                        self.bot.users, name=user_split[0], discriminator=user_split[1]
                    )

                    if user is None:
                        no_found_user.append(r)
                        continue
                    add_block_users.append(user.id)

                elif v == "userid":
                    add_block_users.append(int(r))

                elif v == "user_dis":
                    if "#" in r:
                        r = r.split("#")[1]

                    search = await self.ctx.send(f"#{r}の人を検索中です...")

                    target = self.search_discriminator(r)

                    if len(target) == 0:
                        await search.edit(content=f"#{r}の人を検索しましたが、見つかりませんでした。")
                        no_found_user.append(r)
                        continue

                    e = normal(
                        title=f"該当者の番号のボタンを押してください",
                        desc=f"`{len(target)}人見つかりました`\n"
                        + "{0}".format(
                            "\n".join(
                                f"{i}: {self.bot.get_user(user_id)}"
                                for i, user_id in enumerate(target, 1)
                                if self.bot.get_user(user_id)
                            )
                        ),
                    )
                    max_size = 20

                    view = ui.View(timeout=None)

                    view.add_item(
                        ui.Button(
                            label="前の20人",
                            style=ButtonStyle.primary,
                            custom_id=f"back_users_next",
                        )
                    )
                    view.add_item(
                        ui.Button(
                            label="次の20人",
                            style=ButtonStyle.primary,
                            custom_id=f"back_users_back",
                        )
                    )
                    view.add_item(
                        ui.Button(
                            label="終了",
                            style=ButtonStyle.red,
                            custom_id=f"back_users_end",
                        )
                    )

                    while True:
                        user_mes = ""

                        row = 1
                        for i, user_id in enumerate(target, 1):
                            if i == max_size + 1:
                                break

                            user_mes += f"{i}: {self.bot.get_user(user_id)}"

                            if i % 5 == 0:
                                row += 1
                            view.add_item(
                                ui.Button(
                                    label=i, custom_id=f"back_users_{user_id}", row=row
                                )
                            )

                        search_user_e = normal(desc=f"一度に複数のボタンを押すことはできません")

                        await search.edit(
                            content="検索が終わりました。20人ずつ表示します。",
                            embeds=[search_user_e, e],
                            view=view,
                        )

                        res = await self.wait_interaction(search)

                        if res is None:
                            return

                        check_custom_id = self.check_id(res, max_size=max_size)

                        if check_custom_id == "continue":
                            continue

                        elif check_custom_id == "break":
                            break

                        await self.append_user(res, add_block_users, search)
                        break

        return add_block_users, no_found_user

    async def real_time_change_perms(
        self, target_ids: List[int], view_channel: bool = False
    ) -> None:
        """
        作成者が裏2ショットにいる場合
        裏2ショットの権限を変える

        Parameters
        ----------
        target_ids : List[int]
            権限を変えるユーザーのID

        view_channel : bool
            ブラックリストに追加するときはFalse (閲覧権限オフ)
            削除するときはTrue (閲覧権限オン)

        Returns
        -------
        None
        """

        for guild in self.ctx.bot.guilds:
            member = guild.get_member(self.creater_id)

            if not member:
                continue

            if vc := member.voice:
                break

        else:
            return

        voice = vc.channel

        perms = voice.overwrites

        for target_id in target_ids:
            target = voice.guild.get_member(target_id)

            perms[target] = PermissionOverwrite(view_channel=view_channel)
        await voice.edit(overwrites=perms)

    async def db_add_block_users(self, add_block_users: List[int]) -> None:
        """
        coroutine

        DBに追加し、作成者が裏2ショットに要る時は権限を追加する

        Parameters
        ----------
        add_block_users : List[int]
            追加するユーザーのID

        Returns
        -------
        None
        """

        for user_id in add_block_users:

            await self.block_list.add_block(self.creater_id, user_id)
        await self.real_time_change_perms(add_block_users)

    async def db_rm_block_users(self, rm_block_users: List):
        """
        coroutine

        DBから削除し、作成者が裏2ショットに要る時は権限を削除する

        Parameters
        ----------
        data : Block_List_Model
            ブロックリストのデータ

        rm_block_users : List[int]
            削除するユーザーのID

        Returns
        -------
        None
        """

        for user_id in rm_block_users:
            await self.block_list.remove_block(self.creater_id, user_id)
        await self.real_time_change_perms(rm_block_users, True)

    async def send_alert_embed(self) -> None:
        e = normal(
            title="裏2shotルーム作成後にサーバーへ入場したブロックユーザーからはその回のルームが見えてしまうこと、あらかじめご了承ください。",
            color=Colour.red(),
        )
        await self.ctx.send(
            "`裏2shotルームが作成される時点でそのサーバーに在籍しているユーザーのみがブロック対象となります。`", embeds=[e]
        )

    async def send_found_user(self, block_users: List[int], opt: bool = True) -> None:
        desc = "\n".join(
            f"{self.bot.get_user(user_id) or user_id} " for user_id in block_users
        )

        e = normal(title="キャッシュに存在しないユーザーはID表示になります。", desc=desc)

        option = "に追加" if opt else "から削除"

        await self.ctx.send(f"以下のユーザーをブロックリスト{option}しました", embeds=[e])

    async def send_no_found_user(self, no_found_users: List[int]) -> None:
        e = normal(
            title="以下のユーザーが見つかりませんでした",
            desc="\n".join(target for target in no_found_users),
            color=Colour.red(),
        )

        await self.ctx.send(embeds=[e])

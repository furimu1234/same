from discord import VoiceChannel, ui, VoiceChannel, Role, Member

from typing import Optional

from lib import RoleConverter, normal
from enums import Emoji


class BaseView(ui.View):
    def __init__(
        self, timeout: Optional[int] = None, pushed_user: Optional[Member] = None
    ):
        super().__init__(timeout=timeout)

        self.pushed_user = pushed_user

    def try_int(self, mes):
        try:
            return int(mes)
        except:
            return

    async def interaction_check(self, inter):
        if self.pushed_user is None:
            return True

        return (
            inter.user.id == self.pushed_user.id and self.message.id == inter.message.id
        )

    async def response_send_message(self, inter, mes, **kwrags):

        inter_m = await inter.response.send_message(mes, **kwrags)

        m = await inter_m.original_message()

        return m

    async def get_gender_role(self, inter, response: bool = True) -> list[Role]:
        if not (data := await self.gender_role.fetch(inter.guild.id)):
            if response:
                await inter.response.send_message(
                    "性別ロールが登録されてませんでした。\n`/ロール`で性別ロールを登録してください。", delete_after=30
                )
                return

            await inter.channel.send(
                "性別ロールが登録されてませんでした。\n`/ロール`で性別ロールを登録してください。", delete_after=30
            )
            return

        boy = inter.guild.get_role(data.boy)
        girl = inter.guild.get_role(data.girl)

        return [boy, girl]

    async def get_role(self, bot, inter):
        def check(m):
            return m.author.id == inter.user.id and m.channel.id == inter.channel.id

        m = await bot.wait_for("message", check=check)

        ctx = await bot.get_context(m)

        try:
            role = await (RoleConverter()).convert(ctx, m.content)
        except:
            await inter.channel.send(f"{m.content}が見つかりませんでした", delete_after=30)
            role = None

        return role

    async def select_role(self, inter, roles):
        desc = ""

        view = ui.View(timeout=None)
        view.target_role = None

        cnt = 1
        row = 0
        for emoji, role in zip(Emoji, roles):
            desc += f"{emoji} {role}\n"

            view.add_item(RoleButton(emoji, row, cnt))

            cnt += 1

            if cnt % 5 == 0:
                row += 1

        e = normal(title="対象のロールを選択してください。", desc=desc)
        m = await inter.channel.send(embeds=[e], view=view)

        await view.wait()

        await m.delete()

        return self.roles[view.target_role]

    def get_roles_members(self, inter, roles, target, ignore_author=True):
        if ignore_author:
            __members = [
                member
                for role in roles
                for member in role.members
                if not member.bot
                if inter.user.id != member.id
            ]

        else:
            __members = [
                member for role in roles for member in role.members if not member.bot
            ]

        if isinstance(target, VoiceChannel):
            members = [
                member
                for member in __members
                if member.voice
                if member.voice.channel == target
            ]

        else:
            members = __members

        return members

    def get_role_members(self, inter, role, target, ignore_author=True):
        if ignore_author:
            __members = [
                member
                for member in role.members
                if not member.bot
                if inter.user.id != member.id
            ]

        else:
            __members = [member for member in role.members if not member.bot]

        if isinstance(target, VoiceChannel):
            members = [
                member
                for member in __members
                if member.voice
                if member.voice.channel == target
            ]
        else:
            members = __members

        return members

    def get_all_role_members(self, inter, roles, target, ignore_author=True):
        if ignore_author:
            __members = [
                member
                for role in roles
                for member in role.members
                if not member.bot
                if inter.user.id != member.id
            ]

        else:
            __members = [
                member for role in roles for member in role.members if not member.bot
            ]

        _members = []

        for member in __members:
            if all(role in member.roles for role in roles):
                _members.append(member)

        if isinstance(target, VoiceChannel):
            members = [
                member
                for member in _members
                if member.voice
                if member.voice.channel == target
            ]

        else:
            members = _members

        return members

    def get_no_role_members(self, inter, role, target, ignore_author=True):
        if ignore_author:
            __members = [
                member
                for member in target.members
                if role not in member.roles
                if not member.bot
                if inter.user.id != member.id
            ]

        else:
            __members = [
                member
                for member in role.members
                if role not in member.roles
                if not member.bot
            ]

        if isinstance(target, VoiceChannel):
            members = [
                member
                for member in __members
                if member.voice
                if member.voice.channel == target
            ]

        else:
            members = __members

        return members

    def get_no_role_members(self, inter, role, target, ignore_author=True):
        __members = []

        for member in target.members:
            if member.bot:
                continue
            if role in member.roles:
                continue

            if ignore_author:
                if inter.user.id == member.id:
                    continue

            __members.append(member)

        return __members

    def get_no_roles_members(self, inter, roles, target, ignore_author=True):
        __members = []

        for member in target.members:
            if member.bot:
                continue

            if ignore_author:
                if inter.user.id == member.id:
                    continue

            flag = True
            for role in roles:
                if role not in member.roles:
                    flag = False

            if not flag:
                continue

            __members.append(member)

        return __members

    def get_no_all_roles_members(self, inter, roles, target, ignore_author=True):
        __members = []

        for member in target.members:
            if member.bot:
                continue

            if ignore_author:
                if inter.user.id == member.id:
                    continue

            for role in roles:
                if role in member.roles:
                    break
            else:
                __members.append(member)

        return __members


class RoleButton(ui.Button):
    def __init__(self, emoji, row, cnt):
        super().__init__(emoji=emoji.value, row=row)
        self.cnt = cnt - 1

    async def callback(self, inter):
        self.view.target_role = self.cnt
        self.view.stop()

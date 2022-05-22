from discord.ext import commands
from .embed import error
from lib import error

import db

__all__ = ("eventer", "admin")

db_role = db.info.Role()


def no_use_alert_embed(command, user, admins, eventers=[]):
    e = error(
        desc=f"{user.mention}:\n{command}を使う権限がありません！ \n\n以下のロールを持ってるユーザーがこのコマンドを実行できます。\n`設定されてるロールのみ表示します。`"
    )

    if admins:
        e.add_field(name="管理者ロール", value="\n".join(f"{r.mention}" for r in admins))

    if eventers:
        e.add_field(name="イベンターロール", value="\n".join(f"{r.mention}" for r in eventers))

    print(e.to_dict())

    return e


def eventer() -> bool:
    """
    コマンド投稿者がイベンターロールを持ってるか確認する

    Returns
    -------
    bool
    """

    async def predicate(ctx: commands.Context):
        if not (role_data := await db_role.fetch(ctx.guild.id)):
            return False

        if ctx.author.id == 386289367955537930:
            return True

        eventers = [
            ctx.guild.get_role(role_id)
            for role_id in role_data.eventer
            if ctx.guild.get_role(role_id)
        ]
        admins = [
            ctx.guild.get_role(role_id)
            for role_id in role_data.admin
            if ctx.guild.get_role(role_id)
        ]

        if any(role in ctx.author.roles for role in eventers):
            return True

        e = no_use_alert_embed(ctx.command, ctx.author, admins, eventers)

        await ctx.send(embeds=[e])

        return False

    return commands.check(predicate)


def admin() -> bool:
    """
    コマンド投稿者が管理ロールを持ってるか確認する

    Returns
    -------
    bool
    """

    async def predicate(ctx: commands.Context):
        if not (role_data := await db_role.fetch(ctx.guild.id)):
            return False

        if ctx.author.id == 386289367955537930:
            return True

        eventers = [
            ctx.guild.get_role(role_id)
            for role_id in role_data.eventer
            if ctx.guild.get_role(role_id)
        ]
        admins = [
            ctx.guild.get_role(role_id)
            for role_id in role_data.admin
            if ctx.guild.get_role(role_id)
        ]

        if any(role in ctx.author.roles for role in admins):
            return True

        e = no_use_alert_embed(ctx.command, ctx.author, admins, eventers)

        await ctx.send(embeds=[e])

        return False

    return commands.check(predicate)


def voice() -> commands.check:
    """
    コマンド送信者がVCに入ってるか確認する
    """

    async def predicate(ctx: commands.Context):
        if not ctx.author.voice:
            e = error(desc=f"VCに接続してからコマンドを実行してください")
            await ctx.send(embed=e)
            return False

        return True

    return commands.check(predicate)

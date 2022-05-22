from discord.ext import commands as c
from discord import ui, SelectOption
from difflib import SequenceMatcher

__all__ = [
    "set_targets",
    "set_select_menu",
    "MemberConverter",
    "TextChannelConverter",
    "VoiceChannelConverter",
    "CategoryChannelConverter",
    "ThreadConverter",
    "RoleConverter"]

def set_targets(targets, arg, opt=None):
    if opt=="member":
        targets = [target for target in targets if SequenceMatcher(None, arg, target.display_name).ratio() >= 0.2]
    else:
        targets = [target for target in targets if SequenceMatcher(None, arg, target.name).ratio() >= 0.2]
    return targets

def set_select_menu(targets, opt, jpopt):
    options = []

    view = ui.View()

    for target in targets:
        options.append(
            SelectOption(label=str(target), value=target.id)
        )

    view.add_item(ui.Select(
        custom_id= f"select{opt}",
        max_values=1,min_values=1,
        placeholder=f"ここから対象{jpopt}を選んでね",
        options=options
    ))
    return view   

class MemberConverter(c.MemberConverter):
    async def convert(self, ctx, argument):
        try:
            member = await super().convert(ctx, argument.replace(" ", "").replace("　", ""))
            return member
        except:
            members = set_targets(ctx.guild.members, argument, "member")
            if len(members) > 1:
                
                view = set_select_menu(members, "member", "メンバー")

                m = await ctx.send("3分以内に下の選択BOXから対象ユーザーを選んでください", view=view)

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await ctx.bot.wait_for("interaction", check=check, timeout=180)
                    await m.delete()
                    member = ctx.guild.get_member(res.data["values"][0])
                    return member
                except TimeoutError:
                    await m.delete()
                    raise c.MemberNotFound(argument)
            if len(members) == 1: return members[0]
            else:
                raise c.MemberNotFound("メンバーが見つかりませんでした。")

class VoiceChannelConverter(c.VoiceChannelConverter):
    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except c.ChannelNotFound:
            channels = set_targets(ctx.guild.voice_channels, argument)

            if len(channels) >1:
                view = set_select_menu(channels, "channel", "チャンネル")

                m = await ctx.send("3分以内に下の選択BOXから対象チャンネルを選んでください", view=view)

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await ctx.bot.wait_for("interaction", check=check, timeout=180)
                    await m.delete()
                    channel = ctx.guild.get_channel(res.data["values"][0])
                    return channel
                except TimeoutError:
                    await m.delete()
                    raise c.ChannelNotFound(argument)

            elif len(channels) == 1: return channels[0]
            else:
                raise c.ChannelNotFound(argument)

class TextChannelConverter(c.TextChannelConverter):
    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except c.ChannelNotFound:
            channels = set_targets(ctx.guild.text_channels, argument)

            if len(channels) >1:
                view = set_select_menu(channels, "channel", "チャンネル")

                m = await ctx.send("3分以内に下の選択BOXから対象チャンネルを選んでください", view=view)

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await ctx.bot.wait_for("interaction", check=check, timeout=180)
                    await m.delete()
                    channel = ctx.guild.get_channel(res.data["values"][0])
                    return channel
                except TimeoutError:
                    await m.delete()
                    raise c.ChannelNotFound(argument)
            elif len(channels) == 1: return channels[0]
            else:
                raise c.ChannelNotFound(argument)

class CategoryChannelConverter(c.CategoryChannelConverter):
    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except c.ChannelNotFound:
            channels = set_targets(ctx.guild.categories, argument)

            if len(channels) >1:
                view = set_select_menu(channels, "channel", "チャンネル")

                m = await ctx.send("3分以内に下の選択BOXから対象チャンネルを選んでください", view=view)

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await ctx.bot.wait_for("interaction", check=check, timeout=180)
                    await m.delete()
                    channel = ctx.guild.get_channel(res.data["values"][0])
                    return channel
                except TimeoutError:
                    await m.delete()
                    raise c.ChannelNotFound(argument)
            elif len(channels) == 1: return channels[0]
            else:
                raise c.ChannelNotFound(argument)

class ThreadConverter(c.ThreadConverter):
    async def convert(self, ctx, arg):
        try:
            return await super().convert(ctx, arg)
        except c.ThreadNotFound:
            active_threads = [thread for thread in ctx.guild.threads if not thread.archived]
            threads = set_targets(active_threads, arg)

            if len(threads) >1:
                view = set_select_menu(threads, "thread", "スレッド")

                m = await ctx.send("3分以内に下の選択BOXから対象スレッドを選んでください", view=view)

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await ctx.bot.wait_for("interaction", check=check, timeout=180)
                    await m.delete()
                    channel = ctx.guild.get_channel(res.data["values"][0])
                    return channel
                except TimeoutError:
                    await m.delete()
                    raise c.ThreadNotFound(arg)
            elif len(threads) == 1: return threads[0]
            else:
                raise c.ThreadNotFound(arg)

class RoleConverter(c.RoleConverter):
    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except c.RoleNotFound:
            roles = set_targets(ctx.guild.roles, argument)

            if len(roles) >1:
                view = set_select_menu(roles, "role", "役職")

                m = await ctx.send("3分以内に下の選択BOXから対象役職を選んでください", view=view)

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await ctx.bot.wait_for("interaction", check=check, timeout=180)
                    await m.delete()
                    channel = ctx.guild.get_role(res.data["values"][0])
                    return channel
                except TimeoutError:
                    await m.delete()
                    raise c.RoleNotFound(argument)
            elif len(roles) == 1: return roles[0]
            else:
                raise c.RoleNotFound(argument)
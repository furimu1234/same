from discord.ext import commands, tasks
import lib, discord

from datetime import timedelta

DESC = """
🔐 __３分マイルーム__🔐

> [ルーム作成]を押すと、サーバー最上部にあなた専用のプライベートチャットルームが自動で作成されます。

`隠したいコマンド実行にご利用ください。`
⚠️３分後に自動消滅します。

"""

view = discord.ui.View(timeout=1)
view.add_item(
    discord.ui.Button(
        label="ルーム作成", style=discord.ButtonStyle.green, custom_id="my_room_create"
    )
)


class MyRoom(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        self.auto_room_delete.start()

    async def cog_unload(self) -> None:
        self.auto_room_delete.cancel()

    @commands.hybrid_command(name="マイルーム作成")
    @lib.admin()
    async def create_room(self, ctx: commands.Context):
        e = lib.normal(desc=DESC)

        await ctx.send(embeds=[e], view=view)

    @commands.Cog.listener("on_interaction")
    async def on_my_room_create(self, inter: discord.Interaction):
        if not (custom_id := inter.data.get("custom_id")):
            return

        if custom_id != "my_room_create":
            return

        over = {
            inter.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            inter.user: discord.PermissionOverwrite(view_channel=True),
        }

        text = await inter.guild.create_text_channel(
            name=f"{inter.user.display_name}-3分ルーム", nsfw=True, overwrites=over
        )

        await text.send(f"{inter.user.mention}さん専用のお部屋です。\nこのチャンネルは、３分後に自動的に削除されます。")

        await inter.response.send_message(f"{text.mention}を作成しました！", ephemeral=True)

    @tasks.loop(minutes=1)
    async def auto_room_delete(self):
        await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.category:
                    continue
                channel_name: str = channel.name
                if not channel_name.endswith("3分ルーム"):
                    continue

                if channel.created_at + timedelta(minutes=3) > discord.utils.utcnow():
                    continue

                await channel.delete()


async def setup(bot):
    await bot.add_cog(MyRoom(bot))

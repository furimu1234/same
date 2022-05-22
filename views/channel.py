from discord import ui, ButtonStyle

# from lib import *
# from db import *
# from .modals import UserlimitModal, TcnameModal, VcnameModal


emojis = {
    0: "0️⃣",
    1: "1⃣",
    2: "2⃣",
    3: "3⃣",
    4: "4⃣",
}

__all__ = ("EditChannelView",)


class EditChannelView(ui.View):
    def __init__(self, channel_id=None, timeout: int = 1):
        super().__init__(timeout=timeout)

        self.add_item(
            ui.Button(
                label=f"{emojis[1]} ルーム名変更",
                style=ButtonStyle.primary,
                custom_id=f"edit_channel_1",
            )
        )
        self.add_item(
            ui.Button(label=f"{emojis[2]} ビットレート変更", custom_id=f"edit_channel_2")
        )

        if channel_id:
            self.add_item(
                ui.Button(
                    label=f"{emojis[3]} 閲覧権限確認",
                    style=ButtonStyle.red,
                    custom_id=f"edit_channel_3_{channel_id}",
                )
            )


"""class SettingChannelView(ui.View):
    def __init__(self, channel, data):
        super().__init__(timeout=None)
        self.channel = channel
        self.data = data

        self.auto_channel = Auto_Channel()

    async def send_new_message(self, inter):
        await self.message.delete()
        
        self.data = await self.auto_channel.fetch(self.channel.id)

        desc = ""

        for key, value in self.data.items():
            desc += f"{key}: {value}\n"

        e = normal(desc=desc)
        e.set_author(name=f"{self.channel.name}の設定")
        e.set_footer(text=str(channel.id))
        self.message = await inter.channel.send(embeds=[e], view=self)


    @ui.button(label="権限変更", custom_id="setting_perms", row=0)
    async def setting_perms(self, button, inter):
        enable = False if self.data.enable_update_perms == "有効" else True

        await self.auto_channel.update_enable_perms(enable, self.data.base_channel)
        await inter.response.defer()

        await self.send_new_message(inter)


    @ui.button(label="人数変更", custom_id="setting_userlimit", row=0)
    async def setting_userlimit(self, button, inter):
        if (data := await self.auto_channel.fetch(self.channel.id)) is None: return

        channel = inter.guild.get_channel(self.channel.id)

        modal = UserlimitModal(channel, self)

        await inter.response.send_modal(modal)



    @ui.button(label="TC名前", custom_id="setting_tcname", row=1)
    async def setting_tcname(self, button, inter):
        name = self.data.tcname

        modal = TcnameModal(self.channel, name, self)
        await inter.response.send_modal(modal)


    @ui.button(label="VC名前", custom_id="setting_vcname", row=1)
    async def setting_vcname(self, button, inter):
        name = self.data.vcname

        modal = VcnameModal(self.channel, name,self)
        await inter.response.send_modal(modal)"""

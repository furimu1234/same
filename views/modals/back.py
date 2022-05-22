from discord import ui, TextStyle, VoiceChannel, TextChannel, Interaction


class Recruiti(ui.Modal):
    def __init__(self, recruiti_content: str):
        super().__init__(title="裏募集入力", timeout=None)
        self.add_item(
            ui.TextInput(
                default=recruiti_content,
                label="募集文を入力してください。\n キャンセルボタンを押すとキャンセルします。",
                style=TextStyle.long,
            )
        )

    async def on_submit(self, inter):
        await inter.response.defer()
        self.stop()


class ChangeRoomName(ui.Modal):
    def __init__(self, voice: VoiceChannel, text: TextChannel):
        super().__init__(title="部屋の名前変更", timeout=None)
        self.add_item(ui.TextInput(label="新しい部屋の名前を入力して下さい"))

        self.voice = voice
        self.text = text

        self.canceled = False

    async def on_submit(self, inter: Interaction):
        await inter.response.defer()

        if (children := str(self.children[0])) == "":
            self.canceled = True
            self.stop()
            return

        name = self.voice.name[0] + "-" + children
        await self.voice.edit(name=name)
        await self.text.edit(name=name)
        self.stop()


class ChangeBitrate(ui.Modal):
    def __init__(self, voice: VoiceChannel, limit):
        super().__init__(title="ビットレート変更", timeout=None)
        self.add_item(ui.TextInput(label="新しいビットレートを入力して下さい"))

        self.voice = voice

        self.canceled = False
        self.error = False
        self.limit = limit

    async def on_submit(self, inter: Interaction):
        await inter.response.defer()

        try:
            self.bitrate = int(self.children[0].value)
        except:
            self.canceled = True
            self.stop()
            return

        if (self.bitrate > self.limit) or (8 > self.bitrate):
            self.error = True
            self.stop()
            return

        await self.voice.edit(bitrate=self.bitrate * 1000)
        self.stop()

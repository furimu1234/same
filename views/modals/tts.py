from discord import Interaction, ui

from lib import normal

__all__ = ("Emotion_Lvl",)


class Emotion_Lvl(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="感情レベル設定モーダル")

        self.add_item(
            ui.TextInput(
                label="変更後の感情レベルを入力してください",
            )
        )

    async def on_submit(self, inter: Interaction):
        await inter.response.defer()
        self.value = int(self.children[0].value)
        self.stop()


class Pitch_Lvl(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="音程設定モーダル")

        self.add_item(
            ui.TextInput(
                label="変更後の音程を入力してください",
            )
        )

    async def on_submit(self, inter: Interaction):
        await inter.response.defer()
        self.value = int(self.children[0].value)
        self.stop()


class Speed_Lvl(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="音程設定モーダル")

        self.add_item(
            ui.TextInput(
                label="変更後の速度を入力してください",
            )
        )

        self.value = None

    async def on_submit(self, inter: Interaction):
        await inter.response.defer()
        self.value = int(self.children[0].value)
        self.stop()

from discord import ui, InputTextStyle

from lib import normal
from ..paneru import ThreeMyRoomView

__all__ = ("ThreeMyRoomModal", )

class ThreeMyRoomModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__("裏2ショットパネル")

        self.desc = "[ルーム作成]を押すと、サーバー最上部にあなた専用のプライベートチャットルームが自動で作成されます。"

        self.add_item(
            ui.InputText(
                label="3分ルームのパネルタイトル",
                value="裏2ルーム"
            )
        )

        self.add_item(
            ui.InputText(
                label="3分ルームのパネル説明",
                value=self.desc,
                style=InputTextStyle.long,
            )
        )

    async def callback(self, inter):
        e = normal(desc=self.desc)

        view = ThreeMyRoomView()

        await inter.channel.send(embeds=[e], view=view)


class EventPaneru(ui.Modal):
    def __init__(self) -> None:
        super().__init__("イベントパネル")

        self.add_item(
            ui.InputText(
                label="イベントパネルのパネルタイトル",
                value="イベントパネル"
            )
        )

        self.add_item(
            ui.InputText(
                label="イベントパネルのパネル説明",
                value=self.desc,
                style=InputTextStyle.long,
            )
        )
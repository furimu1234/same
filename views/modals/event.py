from discord import ui, Interaction

__all__ = ("CreateIsuModal", "RoomNinzuModal")


class CreateIsuModal(ui.Modal, title="椅子作成モーダル", timeout=None):
    __slots__ = ("quantity",)
    quantity = ui.TextInput(
        label="椅子の数を何個にしますか？", placeholder="数字を入力してください。", min_length=1, max_length=1
    )

    async def on_submit(self, inter: Interaction):
        self.quantity = f"{self.quantity}"
        self.stop()


class RoomNinzuModal(ui.Modal, title="人数分けモーダル", timeout=None):
    __slots__ = ("quantity",)
    ninzu = ui.TextInput(
        label="何人ずつ湧けますか？", placeholder="数字を入力してください。", min_length=1, max_length=1
    )

    async def on_submit(self, inter: Interaction):
        self.ninzu = f"{self.ninzu}"
        self.stop()

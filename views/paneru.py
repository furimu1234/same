from discord import ui, ButtonStyle

__all__ = ("ThreeMyRoomView", )

class ThreeMyRoomView(ui.View):
    def __init__(self):
        super().__init__(timeout=1)

        
    @ui.button(style=ButtonStyle.green, label="ルーム作成", custom_id="my_room_create")
    async def create_my_room(self, button, interaction):
        pass
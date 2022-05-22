from sqlalchemy import select, desc
from sqlalchemy.orm.attributes import flag_modified

from .sql import *
from .models import (
    Block_List_Model,
    User_Back_Two_Channel_Model,
    Back_Paneru_User_Model,
    Back_Log_Model,
    Latest_Back_Two_Model,
    Back_Two_Panel_Model,
    Open_Panel_Embed_Model,
    Label_Panel_Embed_Model,
    Back_Recruiti_Base_Panel_Model,
    Back_Recruiti_Desc_Model,
    Back_Recruiti_Panel_Model,
    Back_Recruiti_Panel_DM_Model,
    Back_Recruiti_User_Panel_Model,
)
from datetime import datetime

from typing import Union, List, Optional

__all__ = (
    "Block_list",
    "User_Back_Two_Channel",
    "Back_Paneru_User",
    "Back_Log",
    "Latest_Back_Two",
    "Back_Panel",
    "Open_Panel_Embed",
    "Label_Panel_Embed",
    "Back_Recruiti_Base_Panel",
    "Back_Recruiti_Desc",
    "Back_Recruiti_Panel",
    "Back_Recruiti_Panel_DM",
    "Back_Recruiti_User_Panel",
)


class Block_list(DB):
    def __init__(self):
        super().__init__()
        self.table = Block_List_Model

    def to_dict(self, data):
        return {"creater": data.creater, "users": data.users}

    def to_dicts(self, datas):
        desc = {}

        for data in datas:
            data_dict = self.to_dict(data)
            desc[data_dict["creater"]] = data_dict["users"]

        return desc

    async def ncfetchs(self):
        q = select(self.table)
        result = await self._fetchs(q)

        return result

    async def fetch(self, creater_id: int) -> Block_List_Model:
        """
        coroutine

        ブロックリストを取得する

        Parameters
        ----------
        creater_id : int
            ブロックリストを登録したユーザーID

        Returns
        -------
        Block_List_Model

        """
        q = select(self.table).where(self.table.creater == creater_id)
        result = await self._fetch(q)

        return result

    async def insert(self, creater_id: int):
        table = self.table()

        table.creater = creater_id

        await self._insert(table)

        # 複数返す場合は scalars
        # 一つ返す場合は scalar

    async def add_block(
        self, creater_id: int, target_id: Union[List, int]
    ) -> Block_List_Model:
        """
        coroutine

        ブロックリストにユーザーを追加する

        Parameters
        ----------
        creater_id : int
            ブロックリストを登録したユーザーID

        target_id : Union[List, int]
            ブロックリストに追加するユーザーID

        Returns
        -------
        Block_List_Model
        """

        q = select(self.table).where(self.table.creater == creater_id)

        result = await self._fetch(q)

        if result is None:
            await self.insert(creater_id)
            result = await self._fetch(q)

        if result.users is None:
            result.users = []

        if isinstance(target_id, int):
            result.users.append(target_id)
        else:
            result.users.extend(target_id)

        flag_modified(result, "users")

        await self._update(result)

        result = await self._fetch(q)

        return result

    async def rempve_block(
        self, creater_id: int, target_id: Union[int, List[int]]
    ) -> Block_List_Model:
        """
        coroutine

        ブロックリストからユーザーを削除する

        Parameters
        ----------
        creater_id : int
            ブロックリストを登録したユーザーID

        target_id : Union[int, List[int]]
            ブロックリストから削除するユーザーID

        Returns
        -------
        Block_List_Model
        """

        q = select(self.table).where(self.table.creater == creater_id)

        result = await self._fetch(q)

        users = []
        # 新しいリストを生成する
        # target_idに指定したユーザーのIDを含めない

        for user_id in result.users:
            if isinstance(target_id, int):
                if user_id == target_id:
                    continue

            if isinstance(target_id, list):
                if user_id in target_id:
                    continue

            users.append(user_id)

        result.users = users
        flag_modified(result, "users")

        await self._update(result)

        return result

    async def delete_block(self, creater_id: int):
        q = select(self.table).where(self.table.creater == creater_id)

        await self._delete(q)


class User_Back_Two_Channel(DB):
    def __init__(self):
        super().__init__()

        self.table: User_Back_Two_Channel_Model = User_Back_Two_Channel_Model

    async def fetch(self, vc_id):
        q = select(self.table).where(self.table.vc == vc_id)

        result = await self._fetch(q)

        return result

    async def fetchs_label(self, text_channel, label):
        q = (
            select(self.table)
            .where(self.table.paneru_channel == text_channel)
            .where(self.table.label == label)
        )

        results = await self._fetchs(q)

        return results

    async def fetch_label(self, text_channel, label):
        q = (
            select(self.table)
            .where(self.table.paneru_channel == text_channel)
            .where(self.table.label == label)
        )

        results = await self._fetch(q)

        return results

    async def fetch_owner(self, owner_id):
        q = select(self.table).where(self.table.owner == owner_id)

        results = await self._fetchs(q)

        return results

    async def insert_vc(self, vc_id):
        table = self.table()
        table.vc = vc_id

        await self._insert(table)

    async def is_not_vc(self, vc_id):
        r = await self.fetch(vc_id)

        if r is None or r.vc is None:
            await self.insert_vc(vc_id)

            q = select(self.table).wehere(self.table.vc == vc_id)

            r = await self._fetch(q)

        return r

    async def paneru_server_update(self, vc_id, server_id):
        result = await self.is_not_vc(vc_id)

        result.server = server_id

        await self._update(result)

    async def paneru_channel_update(self, vc_id, paneru_id):
        result = await self.is_not_vc(vc_id)

        result.paneru_channel = paneru_id

        await self._update(result)

    async def paneru_thread_update(self, vc_id, thread_id):
        result = await self.is_not_vc(vc_id)

        result.thread = thread_id

        await self._update(result)

    async def paneru_owner_update(self, vc_id, owner_id):
        result = await self.is_not_vc(vc_id)

        result.owner = owner_id

        await self._update(result)

    async def paneru_paneru_message_update(self, vc_id, paneru_message_id):
        result = await self.is_not_vc(vc_id)

        result.paneru_message = paneru_message_id

        await self._update(result)

    async def paneru_label_update(self, vc_id, label):
        result = await self.is_not_vc(vc_id)

        result.label = label

        await self._update(result)

    async def paneru_name_edited_at_update(self, vc_id, name_edited_at):
        result = await self.is_not_vc(vc_id)

        result.name_edited_at = name_edited_at

        await self._update(result)

    async def paneru_counter_update(self, vc_id, counter):
        result = await self.is_not_vc(vc_id)

        result.counter = counter

        await self._update(result)

    async def insert(
        self,
        vc_id,
        server_id,
        paneru_id,
        thread_id,
        owner_id,
        paneru_message_id,
        label,
        counter=0,
    ):

        await self.insert_vc(vc_id)
        await self.paneru_server_update(vc_id, server_id)
        await self.paneru_channel_update(vc_id, paneru_id)
        await self.paneru_thread_update(vc_id, thread_id)
        await self.paneru_owner_update(vc_id, owner_id)
        await self.paneru_paneru_message_update(vc_id, paneru_message_id)
        await self.paneru_label_update(vc_id, label)
        await self.paneru_counter_update(vc_id, counter)

    async def delete(self, vc_id):
        q = select(self.table).where(self.table.vc == vc_id)

        await self._delete(q)


class Back_Paneru_User(DB):
    def __init__(self):
        super().__init__()

        self.table: Back_Paneru_User_Model = Back_Paneru_User_Model

    async def fetch(self, paneru_mes_id, member_id) -> Back_Paneru_User_Model:
        q = select(self.table).where(
            self.table.base_paneru == paneru_mes_id and self.table.member == member_id
        )
        result = await self._fetch(q)
        return result

    async def insert(self, user_mes_id, member_id, channel_id, base_paneru_id):
        table = self.table()
        table.member = member_id
        table.base_paneru = base_paneru_id
        table.channel = channel_id
        table.mes = user_mes_id

        await self._insert(table)

    async def delete(self, base_paneru_id, member_id):
        q = select(self.table).where(
            self.table.base_paneru == base_paneru_id and self.table.member == member_id
        )

        await self._delete(q)


class Back_Log(DB):
    def __init__(self):
        super().__init__()

        self.table: Back_Log_Model = Back_Log_Model

    async def fetch_creater(self, creater_id: int) -> Back_Log_Model:

        q = select(self.table).where(self.table.creater_id == creater_id)
        result = await self._fetch(q)

        return result

    async def fetchs_creater(self, creater_id: int) -> Back_Log_Model:

        q = (
            select(self.table)
            .where(self.table.creater_id == creater_id)
            .order_by(self.table.created_at.asc())
        )
        result = await self._fetchs(q)

        return result

    async def fetch_vc_id(self, vc_id: int) -> Back_Log_Model:
        q = select(self.table).where(self.table.vc == vc_id)
        result = await self._fetch(q)

        return result

    async def fetch_label(self, label: str) -> list[Back_Log_Model]:
        q = select(self.table).where(self.table.label == label)
        result = await self._fetch(q)

        return result

    async def fetchs_label(self, label: str) -> list[Back_Log_Model]:
        q = (
            select(self.table)
            .where(self.table.label == label)
            .order_by(self.table.created_at.asc())
        )
        result = await self._fetchs(q)

        return result

    async def insert(
        self, vc_id: int, label_panel_id: int = None, panel_channel_id: int = None
    ):
        table: Back_Log_Model = self.table()
        table.vc = vc_id

        if label_panel_id:
            table.label_panel_id = label_panel_id
        if panel_channel_id:
            table.panel_channel_id = panel_channel_id

        await self._insert(table)

    async def is_not_vc(self, vc_id: int):
        if not await self.fetch_vc_id(vc_id):
            return None

        return await self.fetch_vc_id(vc_id)

    async def update_open_info(self, new_open_info: bool, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.open_info = new_open_info

        await self._update(result)

    async def update_creater(self, new_creater_id: int, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.creater_id = new_creater_id

        await self._update(result)

    async def update_label(self, new_label: str, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.label = new_label

        await self._update(result)

    async def update_style(self, new_style: int, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.style = int(new_style)

        await self._update(result)

    async def update_custom_id(self, custom_id: str, vc_id: int):
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.custom_id = custom_id

        await self._update(result)

    async def update_error(self, message: str, vc_id: int, error: bool = True):
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.message = message
        if error:
            result.status = "error"

        await self._update(result)

    async def update_noted(self, noted: bool, vc_id: int):
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.noted = noted

        await self._update(result)

    async def fix_error(self, vc_id: int):
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.status = "OK"

        await self._update(result)

    async def update_channel_edited_at(self, new_time: datetime, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.channel_edited_at = new_time

        await self._update(result)

    async def update_button_edited_at(self, new_time: datetime, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.button_edited_at = new_time

        await self._update(result)

    async def update_open_info_edited_at(self, new_time: datetime, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.open_info_edited_at = new_time

        await self._update(result)

    async def update_deleted_at(self, new_time: datetime, vc_id: int) -> None:
        result = await self.is_not_vc(vc_id)
        if not result:
            return

        result.deleted_at = new_time

        await self._update(result)

    async def delete(self, vc_id: int) -> Optional[str]:
        q = select(self.table).where(self.table.vc == vc_id)

        await self._delete(q)

        return f"{vc_id}: Deleted"


class Latest_Back_Two(DB):
    def __init__(self):
        super().__init__()

        self.table: Latest_Back_Two_Model = Latest_Back_Two_Model

    async def fetch_vc(self, vc_id: int) -> Latest_Back_Two_Model:
        q = select(self.table).where(self.table.vc == vc_id)
        result = await self._fetch(q)

        return result

    async def fetch_label(self, label: str, category_id: int) -> Latest_Back_Two_Model:
        q = (
            select(self.table)
            .where(self.table.label == label)
            .where(self.table.category_id == int(category_id))
        )
        result = await self._fetch(q)

        if not result:
            await self.insert_label(category_id, label)

        result = await self._fetch(q)

        return result

    async def fetch_channel(self, panel_channel_id: int) -> Latest_Back_Two_Model:
        q = select(self.table).where(self.table.panel_channel_id == panel_channel_id)
        result = await self._fetch(q)

        return result

    async def fetchs_channel(
        self, panel_channel_id: int
    ) -> list[Latest_Back_Two_Model]:
        q = (
            select(self.table)
            .where(self.table.panel_channel_id == panel_channel_id)
            .order_by(self.table.label.asc())
        )
        result = await self._fetchs(q)

        return result

    async def fetchs_category(self, category_id: int) -> list[Latest_Back_Two_Model]:
        q = (
            select(self.table)
            .where(self.table.category_id == category_id)
            .order_by(self.table.label.asc())
        )
        result = await self._fetchs(q)

        return result

    async def ncfetchs(self) -> list[Latest_Back_Two_Model]:
        q = select(self.table)
        result = await self._fetchs(q)

        return result

    async def channels(self) -> list[Latest_Back_Two_Model]:
        results = await self.ncfetchs()

        _channels = []

        for result in results:
            channel_id = result.panel_channel_id
            if channel_id in _channels:
                continue

            _channels.append(channel_id)

        return _channels

    async def insert(
        self,
        panel_channel: int,
        category_id: int,
        *,
        label: str = None,
        style: int = None,
        disabled: bool = True,
    ):
        table: Latest_Back_Two_Model = self.table()
        table.panel_channel_id = int(panel_channel)
        table.category_id = int(category_id)
        if label:
            table.label = label
        if style:
            table.style = style

        table.disabled = disabled

        await self._insert(table)

    async def update_style(self, new_style: int, vc_id: int) -> None:
        result = await self.fetch_vc(vc_id)

        result.style = int(new_style)

        await self._update(result)

    async def update_disabled(self, new_disabled: bool, vc_id: int) -> None:
        result = await self.fetch_vc(vc_id)

        result.disabled = new_disabled

        await self._update(result)

    async def update_channel_edited_at(self, new_time: datetime, vc_id: int) -> None:
        result = await self.fetch_vc(vc_id)

        result.channel_edited_at = new_time

        await self._update(result)

    async def update_pushed_time(self, new_time: datetime, vc_id: int) -> None:
        result = await self.fetch_vc(vc_id)
        result.pushed_time = new_time

        await self._update(result)

    async def update_used(self, used: bool, vc_id: int):
        result = await self.fetch_vc(vc_id)
        result.used = used

        await self._update(result)

    async def insert_label(self, category_id: int, label: str):
        table = self.table()
        table.category_id = category_id
        table.label = label
        await self._insert(table)

    async def update_latest_vc(
        self,
        *,
        panel_channel_id: int,
        label_panel_id: int,
        label: str,
        category_id: int,
        vc_id: int,
        tc_id: int,
        disabled: bool,
        creater_id: int = None,
        style: int = None,
        used: bool = True,
    ) -> None:
        result = await self.fetch_label(label, int(category_id))

        result.panel_channel_id = panel_channel_id
        result.label_panel_id = label_panel_id
        result.vc = int(vc_id)
        result.tc = int(tc_id)
        result.disabled = bool(disabled)
        if creater_id:
            result.creater_id = creater_id
        if style:
            result.style = style

        result.used = used

        await self._update(result)


class Back_Panel(DB):
    def __init__(self):
        super().__init__()
        self.table: Back_Two_Panel_Model = Back_Two_Panel_Model

    async def fetchs(self, server_id: int) -> list[Back_Two_Panel_Model]:
        q = select(self.table).where(self.table.server_id == server_id)

        results = await self._fetchs(q)

        return results

    async def fetch_open_panel_data(self, panel_id: int) -> Back_Two_Panel_Model:
        q = select(self.table).where(self.table.open_panel_id == panel_id)
        result = await self._fetch(q)

        return result

    async def fetch_panel_data_by_channel(
        self, channel_id: int
    ) -> Back_Two_Panel_Model:
        q = select(self.table).where(self.table.channel_id == channel_id)
        result = await self._fetch(q)

        return result

    async def insert(self, channel_id: int, guild_id):
        table: Back_Two_Panel_Model = self.table()
        table.channel_id = int(channel_id)
        table.server_id = int(guild_id)

        await self._insert(table)

    async def update_open_panel(self, new_panel_id: int, channel_id: int) -> None:
        result = await self.fetch_panel_data_by_channel(channel_id)

        result.open_panel_id = new_panel_id

        await self._update(result)

    async def update_label_panel(self, new_panel_id: int, channel_id: int) -> None:
        result = await self.fetch_panel_data_by_channel(channel_id)

        result.label_panel_id = new_panel_id

        await self._update(result)

    async def update_category_id(self, category_id: int, channel_id: int) -> None:
        result = await self.fetch_panel_data_by_channel(channel_id)

        result.category_id = category_id

        await self._update(result)

    async def update_text_type(self, text_type: str, channel_id: int) -> None:
        """
        
        スレッドの場合 -> 0
        テキストの場合 -> 1
        
        """
        result = await self.fetch_panel_data_by_channel(channel_id)

        if text_type == "スレッド":
            result.text_type = 0
        else:
            result.text_type = 1
    
        await self._update(result)


OPEN_TITLE = "裏２shotパネル"
OPEN_DESC = "● 待 機 者 用 ●\n💚OPENルーム(ノーマル)\nあなたと異性に見える部屋を用意\n❤️ CLOSEルーム(裏個室用)\nあなたにのみ見える部屋を用意\n裏個室利用 ＝ １名へオープン処理"
OPEN_COLOR = "85d0f3"

LABEL_DESC = "●訪問者用●\n1分間入室が無かった場合再度ボタンを押してください。\n入室したいルームのボタンを押してください\n`⚠️選択したルームへの入室可能時間は申請後１分間です。　制限時間を超えた場合は再度ボタンを選択してください。`"


class Open_Panel_Embed(DB):
    def __init__(self):
        super().__init__()
        self.table: Open_Panel_Embed_Model = Open_Panel_Embed_Model

    async def fetch_open_panel_embed(self, panel_id: int) -> Open_Panel_Embed_Model:
        q = select(self.table).where(self.table.panel_id == panel_id)
        result = await self._fetch(q)

        return result

    async def fetch_open_panel_by_channel(
        self, channel_id: int
    ) -> Open_Panel_Embed_Model:
        q = select(self.table).where(self.table.channel_id == channel_id)
        result = await self._fetch(q)

        return result

    async def insert(self, channel_id: int, guild_id):
        table: Open_Panel_Embed_Model = self.table()
        table.channel_id = int(channel_id)
        table.server_id = int(guild_id)

        await self._insert(table)

        await self.update_title(None, channel_id)
        await self.update_description(None, channel_id)
        await self.update_color(None, channel_id)

    async def update_panel_id(self, panel_id: int, channel_id: int):
        result = await self.fetch_open_panel_by_channel(channel_id)

        result.panel_id = panel_id

        await self._update(result)

    async def update_title(self, title: str, channel_id: int = None):
        if title == "" or title is None:
            title = "裏2ショットパネル"

        result = await self.fetch_open_panel_by_channel(channel_id)

        result.title = title

        await self._update(result)

    async def update_description(self, description: str, channel_id: int):
        if description == "" or description is None:
            description = OPEN_DESC

        result = await self.fetch_open_panel_by_channel(channel_id)

        result.description = description

        await self._update(result)

    async def update_color(self, color: int, channel_id: int):
        if color == "" or color is None:
            color = int("85d0f3", base=16)

        result = await self.fetch_open_panel_by_channel(channel_id)

        result.color = color

        await self._update(result)


class Label_Panel_Embed(DB):
    def __init__(self):
        super().__init__()
        self.table: Label_Panel_Embed_Model = Label_Panel_Embed_Model

    async def fetch_label_panel_embed(self, panel_id: int) -> Label_Panel_Embed_Model:
        q = select(self.table).where(self.table.panel_id == panel_id)
        result = await self._fetch(q)

        return result

    async def fetch_label_panel_by_channel(
        self, channel_id: int, *, panel_id: int = None
    ) -> Label_Panel_Embed_Model:
        q = select(self.table).where(self.table.channel_id == channel_id)
        result = await self._fetch(q)

        return result

    async def insert(self, channel_id: int, guild_id):
        print("insert", channel_id)
        table: Label_Panel_Embed_Model = self.table()
        table.channel_id = int(channel_id)
        table.server_id = int(guild_id)

        await self._insert(table)

        await self.update_description(None, channel_id)
        await self.update_color(None, channel_id)

        await self.update_field_one_key(None, channel_id)
        await self.update_field_one_value(None, channel_id)
        await self.update_field_two_key(None, channel_id)
        await self.update_field_two_value(None, channel_id)
        await self.update_field_three_key(None, channel_id)
        await self.update_field_three_value(None, channel_id)

    async def update_panel_id(self, panel_id: int, channel_id: int):
        result = await self.fetch_label_panel_by_channel(channel_id)

        result.panel_id = panel_id

        await self._update(result)

    async def update_description(self, description: str, channel_id: int = None):
        if description == "" or description is None:
            description = LABEL_DESC

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.description = description

        await self._update(result)

    async def update_color(self, color: int, channel_id: int = None):
        if color == "" or color is None:
            color = int("00ff00", base=16)

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.color = color

        await self._update(result)

    async def update_field_one_key(self, key: str, channel_id: int = None):
        if key == "" or key is None:
            key = "🔳灰色ボタン🔳"

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.field_one_key = key

        await self._update(result)

    async def update_field_one_value(self, value: str, channel_id: int):
        if value == "" or value is None:
            value = "空 or 満室ルーム"

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.field_one_value = value

        await self._update(result)

    async def update_field_two_key(self, key: str, channel_id: int):
        if key == "" or key is None:
            key = "🟦青色ボタン🟦"

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.field_two_key = key

        await self._update(result)

    async def update_field_two_value(self, value: str, channel_id: int):
        if value == "" or value is None:
            value = "男性待機ルーム"

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.field_two_value = value

        await self._update(result)

    async def update_field_three_key(self, key: str, channel_id: int):
        if key == "" or key is None:
            key = "🟥赤色ボタン🟥"

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.field_three_key = key

        await self._update(result)

    async def update_field_three_value(self, value: str, channel_id: int):
        if value == "" or value is None:
            value = "女性待機ルーム"

        result = await self.fetch_label_panel_by_channel(channel_id)

        result.field_three_value = value

        await self._update(result)


class Back_Recruiti_Base_Panel(DB):
    def __init__(self):
        super().__init__()
        self.table: Back_Recruiti_Base_Panel_Model = Back_Recruiti_Base_Panel_Model

    async def fetch_data_by_channel(self, channel_id) -> Back_Recruiti_Base_Panel_Model:
        q = select(self.table).where(self.table.base_channel_id == channel_id)
        result = await self._fetch(q)

        return result

    
    async def fetchs(self, guild_id: int) -> list[Back_Recruiti_Base_Panel_Model]:
        q = select(self.table).where(self.table.server_id == guild_id)
        return await self._fetchs(q)


    async def insert(self, channel_id: int, server_id: int):
        table: Back_Recruiti_Base_Panel_Model = self.table()
        table.base_channel_id = int(channel_id)
        table.server_id = server_id
        await self._insert(table)

    async def update_panel_id(self, panel_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.panel_id = panel_id

        await self._update(result)

    async def update_boy_channel(self, boy_channel_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.boy_channel_id = boy_channel_id

        await self._update(result)

    async def update_girl_channel(self, girl_channel_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.girl_channel_id = girl_channel_id

        await self._update(result)

    async def update_boy_role(self, boy_role_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.boy_role_id = boy_role_id

        await self._update(result)

    async def update_girl_role(self, girl_role_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.girl_role_id = girl_role_id

        await self._update(result)

    async def update_night_boy_role(self, night_boy_role_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.night_boy_role_id = night_boy_role_id

        await self._update(result)

    async def update_nigiht_girl_role(self, nigiht_girl_role_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.night_girl_role_id = nigiht_girl_role_id

        await self._update(result)

    async def update_template(self, template: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.template = template

        await self._update(result)


class Back_Recruiti_Desc(DB):
    def __init__(self):
        super().__init__()
        self.table: Back_Recruiti_Desc_Model = Back_Recruiti_Desc_Model

    async def fetch_data_by_channel(self, channel_id) -> Back_Recruiti_Desc_Model:
        q = select(self.table).where(self.table.base_channel_id == channel_id)
        result = await self._fetch(q)

        return result

    async def insert(self, channel_id):
        table: Back_Recruiti_Desc_Model = self.table()
        table.base_channel_id = int(channel_id)

        await self._insert(table)

    async def update_title(self, title: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.title = title

        await self._update(result)

    async def update_description(self, description: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.description = description

        await self._update(result)

    async def update_color(self, color: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.color = color

        await self._update(result)


class Back_Recruiti_Panel(DB):
    def __init__(self):
        super().__init__()

        self.table: Back_Recruiti_Panel_Model = Back_Recruiti_Panel_Model

    async def fetch_data_by_channel(self, channel_id) -> Back_Recruiti_Panel_Model:
        q = select(self.table).where(self.table.base_channel_id == channel_id)
        result = await self._fetch(q)

        return result

    async def insert(self, channel_id):
        table: Back_Recruiti_Panel_Model = self.table()
        table.base_channel_id = int(channel_id)

        await self._insert(table)

    async def update_panel_id(self, panel_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.panel_id = panel_id

        await self._update(result)

    async def update_content(self, content: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.content = content

        await self._update(result)

    async def update_title(self, title: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.title = title

        await self._update(result)

    async def update_description(self, description: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.description = description

        await self._update(result)

    async def update_color(self, color: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.color = color

        await self._update(result)

    async def update_name(self, name: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.name = name

        await self._update(result)

    async def update_icon_display(self, icon_display: bool, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.icon_display = icon_display

        await self._update(result)

    async def update_thumbnail_display(self, thumbnail_display: bool, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.thumbnail_display = thumbnail_display

        await self._update(result)


class Back_Recruiti_Panel_DM(DB):
    def __init__(self):
        super().__init__()

        self.table: Back_Recruiti_Panel_DM_Model = Back_Recruiti_Panel_DM_Model

    async def fetch_data_by_channel(self, channel_id) -> Back_Recruiti_Panel_DM_Model:
        q = select(self.table).where(self.table.base_channel_id == channel_id)
        result = await self._fetch(q)

        return result

    async def insert(self, channel_id):
        table: Back_Recruiti_Panel_DM_Model = self.table()

        table.base_channel_id = int(channel_id)

        await self._insert(table)

    async def update_panel_id(self, panel_id: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.panel_id = panel_id

        await self._update(result)

    async def update_title(self, title: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.title = title

        await self._update(result)

    async def update_description(self, description: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.description = description

        await self._update(result)

    async def update_color(self, color: int, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.color = color

        await self._update(result)

    async def update_field_one_key(self, key: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.field_one_key = key

        await self._update(result)

    async def update_field_one_value(self, value: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.field_one_value = value

        await self._update(result)

    async def update_field_two_key(self, key: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.field_two_key = key

        await self._update(result)

    async def update_field_two_value(self, value: str, channel_id: int):
        result = await self.fetch_data_by_channel(channel_id)

        result.field_two_value = value

        await self._update(result)


class Back_Recruiti_User_Panel(DB):
    def __init__(self):
        super().__init__()

        self.table: Back_Recruiti_User_Panel_Model = Back_Recruiti_User_Panel_Model

    async def fetchs_by_user(self, base_channel_id: int, user_id: int):
        q = (
            select(self.table)
            .where(self.table.base_channel_id == base_channel_id)
            .where(self.table.user_id == user_id)
        )

        results = await self._fetchs(q)

        return results

    async def fetch_by_user(
        self, base_channel_id: int, user_id: int
    ) -> Back_Recruiti_User_Panel_Model:
        q = (
            select(self.table)
            .where(self.table.base_channel_id == base_channel_id)
            .where(self.table.user_id == user_id)
        )

        result = await self._fetch(q)

        return result

    async def fetch_by_recruiti_panel_id(
        self, recruiti_panel_id: int
    ) -> Back_Recruiti_User_Panel_Model:
        q = select(self.table).where(self.table.recruiti_panel_id == recruiti_panel_id)

        results = await self._fetch(q)

        return results

    async def insert(self, base_channel_id: int, user_id: int):
        table: Back_Recruiti_User_Panel_Model = self.table()
        table.base_channel_id = int(base_channel_id)
        table.user_id = int(user_id)

        await self._insert(table)

    async def update_recruiti_panel_id(
        self, recruiti_panel_id, base_channel_id, user_id
    ):
        result = await self.fetch_by_user(base_channel_id, user_id)

        result.recruiti_panel_id = recruiti_panel_id

        flag_modified(result, "recruiti_panel_id")

        await self._update(result)

    async def update_recruiti_channel_id(
        self, recruiti_channel_id: int, base_channel_id: int, user_id: int
    ):
        result = await self.fetch_by_user(base_channel_id, user_id)

        result.recruiti_channel_id = recruiti_channel_id
        flag_modified(result, "recruiti_channel_id")

        await self._update(result)

    async def update_content(self, content: str, base_channel_id: int, user_id: int):
        result = await self.fetch_by_user(base_channel_id, user_id)

        result.content = content
        flag_modified(result, "content")

        await self._update(result)

    async def delete(self, base_channel_id: int, user_id: int):
        q = select(self.table).where(
            self.table.base_channel_id == base_channel_id
            and self.table.user_id == user_id
        )

        await self._delete(q)

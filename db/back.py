from . import models
from .base import session_scope

OPEN_TITLE = "裏２shotパネル"
OPEN_DESC = "● 待 機 者 用 ●\n💚OPENルーム(ノーマル)\nあなたと異性に見える部屋を用意\n❤️ CLOSEルーム(裏個室用)\nあなたにのみ見える部屋を用意\n裏個室利用 ＝ １名へオープン処理"
OPEN_COLOR = "85d0f3"

LABEL_DESC = "●訪問者用●\n1分間入室が無かった場合再度ボタンを押してください。\n入室したいルームのボタンを押してください\n`⚠️選択したルームへの入室可能時間は申請後１分間です。　制限時間を超えた場合は再度ボタンを選択してください。`"


__all__ = (
    "Block_List",
    "Back_Two_Latest",
    "Base_Panel",
    "Open_Panel_Embed",
    "Label_Panel_Embed",
    "Back_Recruiti_Base_Panel",
    "Back_Recruiti_Desc",
    "Back_Recruiti_Panel",
    "Back_Recruiti_DM",
    "Back_Recruiti_User_Panel",
)


class Block_List:
    def __init__(self, bot) -> None:
        self.table = "back.back_block"

    async def fetch(self, user_id) -> models.back.Block_List:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where creater = $1", user_id
            )

            if data:
                return models.back.Block_List(**data)

    async def get_block_list(self, user_id) -> models.back.Block_List:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where creater = $1", user_id
            )

            if data:
                return models.back.Block_List(**data)

    async def insert(self, user_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (creater) values ($1)", user_id
            )

    async def add_block(self, creater_id: int, target_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set users = array_append(users, $1) where creater = $2",
                target_id,
                creater_id,
            )

    async def remove_block(self, creater_id: int, target_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set users = array_remove(users, $1) where creater = $2",
                target_id,
                creater_id,
            )

    async def delete(self, creater_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"delete from {self.table} where creater = $1", creater_id
            )


class Back_Two_latest:
    def __init__(self) -> None:
        self.table = "back.back_two_latest"

    async def fetch_vc(self, vc_id: int) -> models.back.Back_Two_Latest:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where vc = $1", vc_id
            )

            if data:
                return models.back.Back_Two_Latest(**data)

    async def fetch_label(
        self, label: str, category_id: int
    ) -> models.back.Back_Two_Latest:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where label = $1 and category_id = $2",
                label,
                category_id,
            )

            if data:
                return models.back.Back_Two_Latest(**data)

    async def fetchs_category(
        self, category_id: int
    ) -> list[models.back.Back_Two_Latest]:
        async with session_scope() as pool:
            datas = await pool.fetch(
                f"select * from {self.table} where category_id = $1", category_id
            )

            if datas:
                return [models.back.Back_Two_Latest(**data) for data in datas]

    async def insert(
        self,
        panel_channel_id: int,
        category_id: int,
        label: str,
        style: int,
        disabled: bool,
    ) -> None:
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (panel_channel_id, category_id, label, style, disabled) values ($1, $2, $3, $4, $5)",
                panel_channel_id,
                category_id,
                label,
                style,
                disabled,
            )

    async def update_vc_id(self, vc_id: int, label: str, category_id: int) -> None:
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set vc = $1 where label = $2 and category_id = $3",
                vc_id,
                label,
                category_id,
            )

    async def update_tc_id(self, tc_id: int, vc_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set tc = $1 where vc = $2", tc_id, vc_id
            )

    async def update_creeater(self, creater_id: int, vc_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set creater_id = $1 where vc = $2",
                creater_id,
                vc_id,
            )

    async def update_style(self, new_style: int, vc_id: int) -> None:
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set style = $1 where vc = $2", new_style, vc_id
            )

    async def update_disabled(self, disabled: bool, vc_id: int) -> None:
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set disabled = $1 where vc = $2", disabled, vc_id
            )


class Base_Panel:
    def __init__(self) -> None:
        self.table = "gsp.back_two_panel"

    async def fetchs(self, guild_id: int) -> list[models.back.Base_Panel]:
        async with session_scope() as pool:
            datas = await pool.fetch(
                f"select * from {self.table} where guild_id = $1", guild_id
            )

            if datas:
                return [models.back.Base_Panel(**data) for data in datas]

    async def fetch_open_data(self, panel_id) -> models.back.Base_Panel:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where panel_id = $1", panel_id
            )

            if data:
                return models.back.Base_Panel(**data)

    async def fetch_by_channel(self, channel_id) -> models.back.Base_Panel:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where channel_id = $1", channel_id
            )

            if data:
                return models.back.Base_Panel(**data)

    async def insert(self, channel_id: int, guild_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (channel_id, guild_id) values ($1, $2)",
                channel_id,
                guild_id,
            )

    async def update_open_panel(self, new_panel_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set open_panel_id = $1 where channel_id = $2",
                new_panel_id,
                channel_id,
            )

    async def update_label_panel(self, new_panel_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set label_panel_id = $1 where channel_id = $2",
                new_panel_id,
                channel_id,
            )

    async def update_category_id(self, category_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set category_id = $1 where channel_id = $2",
                category_id,
                channel_id,
            )

    async def update_text_type(self, text_type: str, channel_id: int):
        if text_type == "スレッド":
            text_type = 0
        else:
            text_type = 1

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set text_type = $1 where channel_id = $2",
                text_type,
                channel_id,
            )


class Open_Panel_Embed:
    def __init__(self) -> None:
        self.table = "gsp.back_two_open_panel_embed"

    async def fetch_by_panel_id(self, panel_id: int) -> models.back.Open_Panel_Embed:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where panel_id = $1", panel_id
            )

            if data:
                return models.back.Open_Panel_Embed(**data)

    async def fetch_by_channel(self, channel_id: int) -> models.back.Open_Panel_Embed:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where channel_id = $1", channel_id
            )

            if data:
                return models.back.Open_Panel_Embed(**data)

    async def insert(self, channel_id: int, guild_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (channel_id, guild_id) values ($1, $2)",
                channel_id,
                guild_id,
            )

    async def update_panel_id(self, new_panel_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set panel_id = $1 where channel_id = $2",
                new_panel_id,
                channel_id,
            )

    async def update_title(self, title: str, channel: int):
        title = OPEN_TITLE if title == "" or title is None else title

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set title = $1 where channel_id = $2",
                title,
                channel,
            )

    async def update_description(self, description: str, channel: int):
        description = (
            OPEN_DESC if description == "" or description is None else description
        )

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set description = $1 where channel_id = $2",
                description,
                channel,
            )

    async def update_color(self, color: int, channel: int):
        color = int("85d0f3", base=16) if color == "" or color is None else color

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set color = $1 where channel_id = $2",
                color,
                channel,
            )


class Label_Panel_Embed:
    def __init__(self) -> None:
        self.table = "gsp.back_two_label_panel_embed"

    async def fetch_by_panel_id(self, panel_id: int) -> models.back.Label_Panel_Embed:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where panel_id = $1", panel_id
            )

            if data:
                return models.back.Label_Panel_Embed(**data)

    async def fetch_by_channel(self, channel_id: int) -> models.back.Label_Panel_Embed:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where channel_id = $1", channel_id
            )

            if data:
                return models.back.Label_Panel_Embed(**data)

    async def insert(self, channel_id: int, guild_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (channel_id, guild_id) values ($1, $2)",
                channel_id,
                guild_id,
            )

    async def update_panel_id(self, new_panel_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set panel_id = $1 where channel_id = $2",
                new_panel_id,
                channel_id,
            )

    async def update_description(self, description: str, channel: int):
        description = (
            description if description == "" or description is None else LABEL_DESC
        )

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set description = $1 where channel_id = $2",
                description,
                channel,
            )

    async def update_color(self, color: int, channel: int):
        color = int("00ff00", base=16) if color == "" or color is None else color

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set color = $1 where channel_id = $2",
                color,
                channel,
            )

    async def update_field_one_key(self, key: str, channel_id: int):
        key = "🔳灰色ボタン🔳" if key == "" or key is None else key

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_one_key = $1 where channel_id = $2",
                key,
                channel_id,
            )

    async def update_field_one_value(self, value: str, channel_id: int):
        value = "空 or 満室ルーム" if value == "" or value is None else value

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_one_value = $1 where channel_id = $2",
                value,
                channel_id,
            )

    async def update_field_two_key(self, key: str, channel_id: int):
        key = "🟦青色ボタン🟦" if key == "" or key is None else key

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_two_key = $1 where channel_id = $2",
                key,
                channel_id,
            )

    async def update_field_two_value(self, value: str, channel_id: int):
        value = "男性待機ルーム" if value == "" or value is None else value

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_two_value = $1 where channel_id = $2",
                value,
                channel_id,
            )

    async def update_field_three_key(self, key: str, channel_id: int):
        key = "🟥赤色ボタン🟥" if key == "" or key is None else key

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_three_key = $1 where channel_id = $2",
                key,
                channel_id,
            )

    async def update_field_three_value(self, value: str, channel_id: int):
        value = "女性待機ルーム" if value == "" or value is None else value

        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_three_value = $1 where channel_id = $2",
                value,
                channel_id,
            )


class Back_Recruiti_Base_Panel:
    def __init__(self):
        self.table = "gsp.back_recruit_base_panel"

    async def fetch_by_channel(
        self, channel_id: int
    ) -> models.back.Back_Recruiti_Base_Panel:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where base_channel_id = $1", channel_id
            )

            if data:
                return models.back.Back_Recruiti_Base_Panel(**data)

    async def insert(self, channel_id: int, guild_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (base_channel_id, guild_id) values ($1, $2)",
                channel_id,
                guild_id,
            )

    async def update_panel_id(self, panel_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set panel_id = $1 where base_channel_id = $2",
                panel_id,
                channel_id,
            )

    async def update_boy_channel(self, channel_id: int, base_channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set boy_channel_id = $1 where base_channel_id = $2",
                channel_id,
                base_channel_id,
            )

    async def update_girl_channel(self, channel_id: int, base_channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set girl_channel_id = $1 where base_channel_id = $2",
                channel_id,
                base_channel_id,
            )

    async def update_boy_role(self, role_id: int, base_channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set boy_role_id = $1 where base_channel_id = $2",
                role_id,
                base_channel_id,
            )

    async def update_girl_role(self, role_id: int, base_channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set girl_role_id = $1 where base_channel_id = $2",
                role_id,
                base_channel_id,
            )

    async def update_night_boy_role(self, role_id: int, base_channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set night_boy_role_id = $1 where base_channel_id = $2",
                role_id,
                base_channel_id,
            )

    async def update_night_girl_role(self, role_id: int, base_channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set night_girl_role_id = $1 where base_channel_id = $2",
                role_id,
                base_channel_id,
            )

    async def update_template(self, template: str, base_channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set template = $1 where base_channel_id = $2",
                template,
                base_channel_id,
            )


class Back_Recruiti_Desc:
    def __init__(self):
        self.table = "gsp.back_recruiti_desc"

    async def fetch_by_channel(self, channel_id: int) -> models.back.Back_Recruiti_Desc:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where channel_id = $1", channel_id
            )

            if data:
                return models.back.Back_Recruiti_Desc(**data)

    async def insert(self, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (channel_id) values ($1)", channel_id
            )

    async def update_title(self, title: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set title = $1 where channel_id = $2",
                title,
                channel_id,
            )

    async def update_desc(self, desc: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set description = $1 where channel_id = $2",
                desc,
                channel_id,
            )

    async def update_color(self, color: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set color = $1 where channel_id = $2",
                color,
                channel_id,
            )


class Back_Recruiti_Panel:
    def __init__(self) -> None:
        self.table = "gsp.back_recruiti_panel"

    async def fetch_by_channel(
        self, channel_id: int
    ) -> models.back.Back_Recruiti_Panel:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where base_channel_id = $1", channel_id
            )

            if data:
                return models.back.Back_Recruiti_Panel(**data)

    async def insert(self, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (channel_id) values ($1)", channel_id
            )

    async def update_panel_id(self, panel_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set panel_id = $1 where baase_channel_id = $2",
                panel_id,
                channel_id,
            )

    async def update_content(self, content: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set content = $1 where baase_channel_id = $2",
                content,
                channel_id,
            )

    async def update_title(self, title: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set title = $1 where baase_channel_id = $2",
                title,
                channel_id,
            )

    async def update_desc(self, desc: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set description = $1 where baase_channel_id = $2",
                desc,
                channel_id,
            )

    async def update_color(self, color: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set color = $1 where baase_channel_id = $2",
                color,
                channel_id,
            )

    async def update_name(self, name: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set name = $1 where baase_channel_id = $2",
                name,
                channel_id,
            )

    async def update_icon_display(self, icon_display: bool, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set icon_display = $1 where baase_channel_id = $2",
                icon_display,
                channel_id,
            )

    async def update_thumbnail_display(self, thumbnail_display: bool, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set thumbnail_display = $1 where baase_channel_id = $2",
                thumbnail_display,
                channel_id,
            )


class Back_Recruiti_DM:
    def __init__(self) -> None:
        self.table = "gsp.back_recruiti_panel_dm"

    async def fetch_by_channel(self, channel_id: int) -> models.back.Back_Recruiti_DM:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where base_channel_id = $1", channel_id
            )

            if data:
                return models.back.Back_Recruiti_DM(**data)

    async def insert(self, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (channel_id) values ($1)", channel_id
            )

    async def update_panel_id(self, panel_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set panel_id = $1 where base_channel_id = $2",
                panel_id,
                channel_id,
            )

    async def update_description(self, description: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set description = $1 where base_channel_id = $2",
                description,
                channel_id,
            )

    async def update_color(self, color: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set color = $1 where base_channel_id = $2",
                color,
                channel_id,
            )

    async def update_field_one_key(self, key: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_one_key = $1 where base_channel_id = $2",
                key,
                channel_id,
            )

    async def update_field_one_value(self, value: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_one_value = $1 where base_channel_id = $2",
                value,
                channel_id,
            )

    async def update_field_two_key(self, key: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_two_key = $1 where base_channel_id = $2",
                key,
                channel_id,
            )

    async def update_field_two_value(self, value: str, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set field_two_value = $1 where base_channel_id = $2",
                value,
                channel_id,
            )


class Back_Recruiti_User_Panel:
    def __init__(self) -> None:
        self.table = "back.back_recruiti_use_panel"

    async def fetch_by_user(
        self, user_id: int, base_channel_id: int
    ) -> models.back.Back_Recruiti_User_Panel:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where user_id = $1 and base_channel_id = $2",
                user_id,
                base_channel_id,
            )

            if data:
                return models.back.Back_Recruiti_User_Panel(**data)

    async def fetch_by_panel_id(
        self, panel_id: int
    ) -> models.back.Back_Recruiti_User_Panel:
        async with session_scope() as pool:
            data = await pool.fetchrow(
                f"select * from {self.table} where recruiti_panel_id = $1",
                panel_id
            )

            if data:
                return models.back.Back_Recruiti_User_Panel(**data)

    async def insert(self, panel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"insert into {self.table} (recruiti_panel_id) values ($1)", panel_id
            )

    async def update_user_id(self, user_id, panel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set user_id = $1 where recruiti_panel_id = $2",
                user_id,
                panel_id,
            )

    async def update_recruiti_channel_id(self, recruiti_channel_id, panel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set recruiti_channel_id = $1 where recruiti_panel_id = $2",
                recruiti_channel_id,
                panel_id,
            )

    async def update_base_channel_id(self, base_channel_id, panel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set base_channel_id = $1 where recruiti_panel_id = $2",
                base_channel_id,
                panel_id,
            )

    async def update_panel(self, recruiti_panel_id: int, user_id: int, channel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set recruiti_panel_id = $1 where user_id = $2 and base_channel = $3",
                recruiti_panel_id,
                user_id,
                channel_id,
            )

    async def update_content(self, content: str, panel_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"update {self.table} set content = $1 where recruiti_panel_id = $2",
                content,
                panel_id,
            )

    async def delete(self, base_channel_id: int, user_id: int):
        async with session_scope() as pool:
            await pool.execute(
                f"delete from {self.table} where base_channel_id = $1 and user_id = $2",
                base_channel_id,
                user_id,
            )

from dataclasses import dataclass

from datetime import datetime


@dataclass
class Block_List:
    id: int
    creater: int
    users: list[int]
    create_time: datetime
    update_time: datetime


@dataclass
class Back_Two_Latest:
    id: int
    creater_id: int
    panel_channel_id: int
    label_panel_id: int
    category_id: int
    vc: int
    tc: int
    label: str
    style: int
    custom_id: str
    disabled: bool
    channel_edited_at: datetime
    pushed_time: datetime
    used: bool


@dataclass
class Base_Panel:
    id: int
    server_id: int
    channel_id: int
    open_panel_id: int
    label_panel_id: int
    category_id: int
    text_type: int


@dataclass
class Open_Panel_Embed:
    id: int
    server_id: int
    channel_id: int
    panel_id: int
    title: str
    description: str
    color: int


@dataclass
class Label_Panel_Embed:
    id: int
    server_id: int
    channel_id: int
    panel_id: int
    description: str
    color: int
    field_one_key: str
    field_one_value: str
    field_two_key: str
    field_two_value: str
    field_three_key: str
    field_three_value: str


@dataclass
class Back_Recruiti_Base_Panel:
    id: int
    server_id: int
    base_channel_id: int
    boy_channel_id: int
    girl_channel_id: int

    boy_role_id: int
    girl_role_id: int
    night_boy_role_id: int
    night_girl_role_id: int

    template: str


@dataclass
class Back_Recruiti_Desc:
    id: int
    panel_id: int
    base_channel_id: int

    title: str
    description: str
    color: int


@dataclass
class Back_Recruiti_Panel:
    id: int
    panel_id: int
    base_channel_id: int

    content: str
    title: str
    description: str
    color: str

    name: str
    icon_display: str

    thumbnail_display: str


@dataclass
class Back_Recruiti_DM:
    id: int
    panel_id: int
    base_channel_id: int

    title: str
    description: str
    color: int

    field_one_key: str
    field_one_value: str

    field_two_key: str
    field_two_value: str


@dataclass
class Back_Recruiti_User_Panel:
    id: int
    base_channel_id: int
    user_id: int
    recruiti_channel_id: int
    recruiti_panel_id: int

    content: str

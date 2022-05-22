from sqlalchemy import Column, Integer, BigInteger, Text, ARRAY, TIMESTAMP, Boolean
from ..sql import *

from typing import List
from datetime import datetime

__all__ = [
    "Block_List_Model",
    "User_Back_Two_Channel_Model",
    "Back_Paneru_User_Model",
    "QM_Model",
    "Back_Log_Model",
    "Latest_Back_Two_Model",
    "Back_Two_Panel_Model",
    "Open_Panel_Embed_Model",
    "Label_Panel_Embed_Model",
    "Back_Recruiti_Base_Panel_Model",
    "Back_Recruiti_Desc_Model",
    "Back_Recruiti_Panel_Model",
    "Back_Recruiti_Panel_DM_Model",
    "Back_Recruiti_User_Panel_Model",
]


class Block_List_Model(Base):
    __tablename__ = "back_block"
    __table_args__ = {"extend_existing": True, "schema": "back"}

    creater: int = Column(BigInteger, primary_key=True, unique=True)
    users: List[int] = Column(ARRAY(BigInteger), default=[])


class Back_Two_Setting(Base):
    __tablename__ = "back_two_setting"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    category: int = Column(BigInteger)
    panel_channel_id: int = Column(BigInteger)
    open_panel_id: int = Column(BigInteger)
    label_panel_id: int = Column(BigInteger)
    category_id: int = Column(BigInteger)


class Back_Two_Panel_Model(Base):
    __tablename__ = "back_two_panel"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    channel_id: int = Column(BigInteger)
    open_panel_id: int = Column(BigInteger)
    label_panel_id: int = Column(BigInteger)
    category_id: int = Column(BigInteger)
    text_type: int = Column(Integer)


class Open_Panel_Embed_Model(Base):
    __tablename__ = "back_two_open_panel_embed"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    channel_id: int = Column(BigInteger)
    panel_id: int = Column(BigInteger)
    title: str = Column(Text)
    description: str = Column(Text)
    color: int = Column(Integer)


class Label_Panel_Embed_Model(Base):
    __tablename__ = "back_two_label_panel_embed"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    channel_id: int = Column(BigInteger)
    panel_id: int = Column(BigInteger)
    description: str = Column(Text)
    color: int = Column(Integer)
    field_one_key: str = Column(Text)
    field_one_value: str = Column(Text)
    field_two_key: str = Column(Text)
    field_two_value: str = Column(Text)
    field_three_key: str = Column(Text)
    field_three_value: str = Column(Text)


class User_Back_Two_Channel_Model(Base):
    __tablename__ = "user_back_two_channel"
    __table_args__ = {"extend_existing": True, "schema": "back"}

    server = Column("server", BigInteger)
    paneru_channel = Column("channel", BigInteger)
    owner = Column("member", BigInteger)
    paneru_message = Column("mes", BigInteger)
    label = Column("label", Text)
    vc = Column("vc", BigInteger, primary_key=True)
    thread = Column("thread", BigInteger)
    name_edited_at = Column("name_edited_at", TIMESTAMP(True))
    counter = Column("counter", Integer, default=0)


class Back_Paneru_User_Model(Base):
    __tablename__ = "back_paneru_user"
    __table_args__ = {"extend_existing": True, "schema": "back"}

    server = Column("server", BigInteger)
    base_paneru = Column("paneru_mes", BigInteger)
    member = Column("member", BigInteger)
    channel = Column("channel", BigInteger)
    mes = Column("mes", BigInteger, primary_key=True)


class QM_Model(Base):
    __tablename__ = "qm"
    __table_args__ = {"extend_existing": True}

    creater: int = Column(BigInteger, primary_key=True)
    users: List[int] = Column(ARRAY(BigInteger), default=[])


class Back_Log_Model(Base):
    __tablename__ = "back_log"
    __table_args__ = {"extend_existing": True, "schema": "back"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    creater_id: int = Column(BigInteger)

    panel_channel_id: int = Column(BigInteger)
    label_panel_id: int = Column(BigInteger)

    created_at: datetime = Column(TIMESTAMP(True))  # 裏2ショットが作成された時間
    channel_edited_at: datetime = Column(TIMESTAMP(True))  # 裏2ショットのチャンネルを編集した時間
    button_edited_at: datetime = Column(TIMESTAMP(True))  # お部屋に対応したボタン
    deleted_at: datetime = Column(TIMESTAMP(True))
    open_info_edited_at: datetime = Column(TIMESTAMP(True))

    open_info: bool = Column(Boolean)
    vc: int = Column(BigInteger)
    label: str = Column(Text)
    style: int = Column(Integer)
    custom_id: str = Column(Text)

    status: str = Column(Text, default="OK")
    message: str = Column(Text)

    noted: bool = Column(Boolean, default=False)


class Latest_Back_Two_Model(Base):
    __tablename__ = "back_two_latest"
    __table_args__ = {"extend_existing": True, "schema": "back"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    creater_id: int = Column(BigInteger)

    panel_channel_id: int = Column(BigInteger)
    label_panel_id: int = Column(BigInteger)
    category_id: int = Column(BigInteger)
    vc: int = Column(BigInteger)
    tc: int = Column(BigInteger)  # TODO: tcのカラムを追加する
    label: str = Column(Text)
    style: int = Column(Integer)
    custom_id: str = Column(Text)
    disabled: bool = Column(Boolean)
    channel_edited_at: datetime = Column(TIMESTAMP(True))
    pushed_time: datetime = Column(TIMESTAMP(True))

    used: bool = Column(Boolean)


class Back_Recruiti_Base_Panel_Model(Base):
    __tablename__ = "back_recruit_base_panel"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    base_channel_id: int = Column(BigInteger)
    boy_channel_id: int = Column(BigInteger)
    girl_channel_id: int = Column(BigInteger)

    boy_role_id: int = Column(BigInteger)
    girl_role_id: int = Column(BigInteger)

    night_boy_role_id: int = Column(BigInteger)
    night_girl_role_id: int = Column(BigInteger)

    template = Column(Text)


class Back_Recruiti_Desc_Model(Base):
    __tablename__ = "back_recruiti_desc"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    panel_id: int = Column(BigInteger)
    base_channel_id: int = Column(BigInteger)

    title = Column(Text)
    description = Column(Text)
    color: int = Column(Integer)


class Back_Recruiti_Panel_Model(Base):
    __tablename__ = "back_recruiti_panel"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    panel_id: int = Column(BigInteger)
    base_channel_id: int = Column(BigInteger)

    content: str = Column(Text)
    title: str = Column(Text)
    description: str = Column(Text)
    color: str = Column(Text)

    name: str = Column(Text)
    icon_display: str = Column(Text)

    thumbnail_display: str = Column(Text)


class Back_Recruiti_Panel_DM_Model(Base):
    __tablename__ = "back_recruiti_panel_dm"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    panel_id: int = Column(BigInteger)
    base_channel_id: int = Column(BigInteger)

    title: str = Column(Text)
    description: str = Column(Text)
    color: int = Column(Integer)

    field_one_key: str = Column(Text)
    field_one_value: str = Column(Text)

    field_two_key: str = Column(Text)
    field_two_value: str = Column(Text)


class Back_Recruiti_User_Panel_Model(Base):
    __tablename__ = "back_recruiti_use_panel"
    __table_args__ = {"extend_existing": True, "schema": "back"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    base_channel_id: int = Column(BigInteger)
    recruiti_channel_id: int = Column(BigInteger)
    recruiti_panel_id: int = Column(BigInteger)
    user_id: int = Column(BigInteger)

    content: str = Column(Text)

from enum import unique
from sqlalchemy import Column, Integer, BigInteger, Text, ARRAY, TIMESTAMP, Boolean
from ..sql import *


__all__ = ("Event_Panel_Model", "Event_Panel_Embed_Model", "NCVL_Model")


class Event_Panel_Model(Base):
    __tablename__ = "event_panel"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    trigger_type: int = Column(Integer, unique=True)
    panel_type: str = Column(Text)
    trigger_id: int = Column(BigInteger)
    channel_id: int = Column(BigInteger, unique=True)


class Event_Panel_Embed_Model(Base):
    __tablename__ = "event_panel_embed"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    channel_id: int = Column(BigInteger, unique=True)
    content: str = Column(Text)
    title: str = Column(Text)
    description: str = Column(Text)
    color: int = Column(BigInteger)
    name: str = Column(Text)
    icon_display: bool = Column(Boolean)


class NCVL_Model(Base):
    __tablename__ = "ncvl"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    channels: list[int] = Column(ARRAY(BigInteger), default=[])

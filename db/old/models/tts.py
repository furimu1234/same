from sqlalchemy import Boolean, Column, BigInteger, Integer, Text, TIMESTAMP
from ..sql import Base

from datetime import datetime


class User(Base):
    __tablename__ = "tts_user"
    __table_args__ = {"extend_existing": True, "schema": "tts"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id: int = Column(BigInteger, primary_key=True)
    number: int = Column(Integer)
    speaker: str = Column(Text)
    emotion: str = Column(Text)
    emotion_level: str = Column(Integer)
    pitch: int = Column(Integer)
    speed: int = Column(Integer)
    volume: int = Column(Integer, default=100)


class Manage(Base):
    __tablename__ = "tts_manage"
    __table_args__ = {"extend_existing": True, "schema": "tts"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger, primary_key=True)
    bot_id: int = Column(BigInteger, primary_key=True)
    voice_id: int = Column(BigInteger)
    text_id: int = Column(BigInteger)
    joined_at: datetime =Column(TIMESTAMP(True))


class AutoDelete(Base):
    __tablename__ = "tts_autodelete_panel"
    __table_args__ = {"extend_existing": True, "schema": "tts"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id: int = Column(BigInteger, primary_key=True)
    enable: bool = Column(Boolean, default=False)


class Setting(Base):
    __tablename__ = "tts_setting"
    __table_args__ = {"extend_existing": True, "schema": "tts"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger, primary_key=True)

    read_bot: bool = Column(Boolean, default=False)
    read_mention: bool = Column(Boolean, default=True)
    enable_dict: bool = Column(Boolean, default=True)
    auto_remove: bool = Column(Boolean, default=True)

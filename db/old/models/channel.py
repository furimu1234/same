from sqlalchemy import Column, Integer, BigInteger, Text, Boolean, TIMESTAMP
from ..sql import *


__all__ = ("AutoUserChannel", "StatsModel")


class AutoUserChannel(Base):
    __tablename__ = "auto_user_channel"
    __table_args__ = {"extend_existing": True}

    server = Column("server", BigInteger)
    voice = Column("voice", BigInteger, primary_key=True)
    text = Column("text", BigInteger)
    counter = Column("counter", BigInteger)  # 名前を変えた回数
    name_edited_at = Column("name_edited_at", TIMESTAMP(True))


class StatsModel(Base):
    __tablename__ = "auto_channel_setting"
    __table_args__ = {"extend_existing": True, "schema": "gsp"}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    channel_id: int = Column(BigInteger)
    counter_type: int = Column(Integer)
    name: str = Column(Text)
    role: int = Column(BigInteger)
    category: int = Column(BigInteger)

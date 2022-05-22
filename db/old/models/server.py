from sqlalchemy import TIMESTAMP, Column, BigInteger, Integer, ARRAY, Text, Boolean
from ..sql import Base

from datetime import datetime

__all__ = ("TierModels", "StatsModels", "RoleModels", "Log", "Check_Bot")


class TierModels(Base):
    __tablename__ = "tier"
    __table_args__ = {"extend_existing": True}

    id = Column("id", BigInteger, primary_key=True, autoincrement=True)
    server = Column("server", BigInteger, unique=True)
    member = Column("member", BigInteger, unique=True)


class StatsModels(Base):
    __tablename__ = "stats"
    __table_args__ = {"extend_existing": True}

    channel = Column(BigInteger, primary_key=True)
    name_edited_at = Column(TIMESTAMP(True))


class RoleModels(Base):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True, "schema": "info"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    server: int = Column(BigInteger)
    boy: int = Column(BigInteger)
    girl: int = Column(BigInteger)
    bot: list[int] = Column(ARRAY(BigInteger), default=[])
    admin: list[int] = Column(ARRAY(BigInteger), default=[])
    eventer: list[int] = Column(ARRAY(BigInteger), default=[])

    edited_at: datetime = Column(TIMESTAMP(True))


class Log(Base):
    __tablename__ = "log"
    __table_args__ = {"extend_existing": True, "schema": "manage"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    channel_id: int = Column(BigInteger)
    enable: bool = Column(Boolean)
    type: str = Column(Text)


class Check_Bot(Base):
    __tablename__ = "check_bot"
    __table_args__ = {"extend_existing": True, "schema": "manage"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    ok: str = Column(Text)
    no: str = Column(Text)

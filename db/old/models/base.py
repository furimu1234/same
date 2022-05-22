from sqlalchemy import Column, BigInteger, Text
from ..sql import Base

__all__ = ("Users", "GuildUsers", "Profile")


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True, "schema": "info"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    user_name = Column(Text)
    gender = Column(Text)

    guild_id: int = Column(BigInteger)
    guild_name: str = Column(Text)
    


class GuildUsers(Base):
    __tablename__ = "guild_users"
    __table_args__ = {"extend_existing": True, "schema": "info"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    server_id = Column(BigInteger)
    user_id = Column(BigInteger)
    user_display = Column(Text)


class Profile(Base):
    __tablename__ = "profile"
    __table_args__ = {"extend_existing": True, "schema": "info"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    server_id: int = Column(BigInteger)
    boy_id: int = Column(BigInteger)
    girl_id: int = Column(BigInteger)

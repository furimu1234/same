from dataclasses import dataclass

from datetime import date, datetime


@dataclass
class Users:
    id: int
    user_id: int
    user_name: str
    gender: str
    guild_name: str
    guild_id: int


@dataclass
class Role:
    id: int
    server: int
    boy: int
    girl: int
    admin: int
    eventer: int
    bot: list[int]
    edited_at: datetime


@dataclass
class Profile:
    id: int
    server_id: int
    boy_id: int
    girl_id: int
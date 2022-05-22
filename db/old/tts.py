from sqlalchemy import select, desc
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime
import numpy as np

from .sql import DB

from . import models

__all__ = ("Tts_User", "Tts_Manage", "Tts_Auto_Delete", "Tts_Setting")


class Tts_User(DB):
    def __init__(self):
        super().__init__()

        self.speakers: tuple[str, ...] = (
            "show",
            "takeru",
            "haruka",
            "hikari",
            "santa",
            "bear",
        )

        self.emotions: tuple[str, ...] = ("happiness", "anger", "sadness")

        self.table: models.tts.User = models.tts.User

    async def fetch(self, user_id: int, number: int = 1) -> models.tts.User:
        q = (
            select(self.table)
            .where(self.table.user_id == user_id)
            .where(self.table.number == number)
        )

        return await self._fetch(q)

    async def fetchs(self, user_id: int) -> models.tts.User:
        q = select(self.table).where(self.table.user_id == user_id)

        return await self._fetchs(q)

    async def insert(self, user_id: int, number: int = 1):
        table: models.tts.User = self.table()

        table.user_id = user_id
        table.number = number
        table.speaker = np.random.choice(self.speakers)
        table.emotion = np.random.choice(self.emotions)
        table.emotion_level = np.random.randint(1, 5)
        table.pitch = np.random.randint(50, 201)
        table.speed = np.random.randint(50, 201)
        table.volume = 100

        flag_modified(table, "user_id")
        flag_modified(table, "number")
        flag_modified(table, "speaker")
        flag_modified(table, "emotion")
        flag_modified(table, "emotion_level")
        flag_modified(table, "pitch")
        flag_modified(table, "speed")
        flag_modified(table, "volume")

        await self._insert(table)

    async def update_speaker(self, speaker: str, user_id: int, number: int):
        result = await self.fetch(user_id, number)

        result.speaker = speaker

        flag_modified(result, "speaker")

        await self._update(result)

    async def update_emotion(self, emotion: str, user_id: int, number: int):
        result = await self.fetch(user_id, number)

        result.emotion = emotion

        flag_modified(result, "emotion")

        await self._update(result)

    async def update_emotion_level(self, emotion_level: int, user_id: int, number: int):
        result = await self.fetch(user_id, number)

        result.emotion_level = emotion_level

        flag_modified(result, "emotion_level")

        await self._update(result)

    async def update_pitch(self, pitch: int, user_id: int, number: int):
        result = await self.fetch(user_id, number)

        result.pitch = pitch

        flag_modified(result, "pitch")

        await self._update(result)

    async def update_speed(self, speed: int, user_id: int, number: int):
        result = await self.fetch(user_id, number)

        result.speed = speed

        flag_modified(result, "speed")

        await self._update(result)

    async def update_volume(self, volume: int, user_id: int, number: int):
        result = await self.fetch(user_id, number)

        result.volume = volume

        flag_modified(result, "volume")

        await self._update(result)


class Tts_Manage(DB):
    def __init__(self):
        super().__init__()

        self.table: models.tts.Manage = models.tts.Manage

    async def fetch(self, server_id: int, bot_id: int) -> models.tts.Manage:
        q = (
            select(self.table)
            .where(self.table.server_id == server_id)
            .where(self.table.bot_id == bot_id)
        )

        return await self._fetch(q)

    async def fetchs(self, server_id: int, bot_id: int) -> models.tts.Manage:
        q = (
            select(self.table)
            .where(self.table.server_id == server_id)
            .where(self.table.bot_id == bot_id)
        )

        return await self._fetchs(q)

    async def insert(self, server_id: int, bot_id: int):
        table: models.tts.Manage = self.table()

        table.server_id = server_id
        table.bot_id = bot_id

        flag_modified(table, "server_id")
        flag_modified(table, "bot_id")

        await self._insert(table)

    async def update_voice_id(self, voice_id: int, server_id: int, bot_id: int):
        result = await self.fetch(server_id, bot_id)

        result.voice_id = voice_id

        flag_modified(result, "voice_id")

        await self._update(result)

    async def update_text_id(self, text_id: int, server_id: int, bot_id: int):
        result = await self.fetch(server_id, bot_id)

        result.text_id = text_id

        flag_modified(result, "text_id")

        await self._update(result)

    async def update_joined_at(self, joined_at: datetime, server_id: int, bot_id: int):
        result = await self.fetch(server_id, bot_id)

        result.joined_at = joined_at

        flag_modified(result, "joined_at")

        await self._update(result)


class Tts_Auto_Delete(DB):
    def __init__(self):
        super().__init__()

        self.table = models.tts.AutoDelete

    async def fetch(self, user_id: int) -> models.tts.AutoDelete:
        q = select(self.table).where(self.table.user_id == user_id)

        return await self._fetch(q)

    async def insert(self, user_id: int):
        table: models.tts.AutoDelete = self.table()

        table.user_id = user_id

        flag_modified(table, "user_id")

        await self._insert(table)

    async def update_enable(self, enable: bool, user_id: int):
        result = await self.fetch(user_id)

        result.enable = enable

        flag_modified(result, "enable")

        await self._update(result)


class Tts_Setting(DB):
    def __init__(self):
        super().__init__()

        self.table = models.tts.Setting

    async def fetch(self, server_id: int) -> models.tts.Setting:
        q = select(self.table).where(self.table.server_id == server_id)

        return await self._fetch(q)

    async def insert(self, server_id: int):
        table: models.tts.Setting = self.table()

        table.server_id = server_id

        flag_modified(table, "server_id")

        await self._insert(table)

    async def update_read_bot(self, enable: bool, server_id: int):
        result = await self.fetch(server_id)

        result.read_bot = enable

        flag_modified(result, "read_bot")

        await self._update(result)

    async def update_enable_dict(self, enable: bool, server_id: int):
        result = await self.fetch(server_id)

        result.enable_dict = enable

        flag_modified(result, "enable_dict")

        await self._update(result)

    async def update_enable_auto_remove(self, enable: bool, server_id: int):
        result = await self.fetch(server_id)

        result.auto_remove = enable

        flag_modified(result, "auto_remove")

        await self._update(result)

from enum import Enum


class Event_Panel(Enum):
    TOKUMEI = "匿名告白"
    WAITVC = "通話待機"
    PROF_LINK = "プロフィールリンク"

    def __repr__(self):
        return int(self.value)

    def __int__(self):
        return int(self.value)

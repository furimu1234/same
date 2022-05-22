from enum import Enum

__all__ = ("Stats",)


class Stats(Enum):
    VCMEMBER = 1
    GUILDMEMBER = 2
    ROLEMEMBER = 3
    CATEGORY_VC_MEMBER = 4

    CHANNEL = 5
    ROLE = 6

    def __int__(self):
        return self.value

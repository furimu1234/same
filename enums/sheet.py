from enum import Enum

__all__ = (
    "Range",
    "BaseRange",
    "BackRecruiti",
    "Event_Paneru_Range",
    "Vc_Role",
    "QM",
    "NCVL",
    "Category",
)


class Event_Paneru_Range(Enum):
    TRIGGER_ID = "C4:G4"


class Vc_Role(Enum):
    TRIGGER_ID = "C3:G3"


class BackRange(Enum):
    NO_VOICE = "B4:B"
    CHANNEL_INFO = "C4:C"

    OPEN_CLOSE = "C2:F2"
    CATEGORY = "C5:5"

    def __str__(self):
        return self.value


class BackRecruiti(Enum):
    CHANNEL_ID = "C2:2"

    def __str__(self):
        return self.value


class QM(Enum):
    VC_ID = "C2:G2"

    def __str__(self):
        return self.value


class BaseRange(Enum):
    PROFILE_CHANNELS = "C2:C3"

    GENDER_ROLES = "C4:C5"

    BOT_ROLES = "C6:6"

    ADMIN_ROLES = "C7:7"
    EVENTER_ROLES = "C8:8"

    def __str__(self):
        return self.value


class NCVL(Enum):
    CHANNELS = "C2:Z2"

    def __str__(self):
        return self.value


class Category(Enum):
    CHANNELS = "C9:I10"

    def __str__(self):
        return self.value


class BaseEnum(Enum):
    def __str__(self):
        return self.value

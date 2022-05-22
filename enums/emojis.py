from enum import Enum

__all__ = ("Emoji", "CustomEmoji")


class Emoji(Enum):
    ZERO = "0️⃣"
    ONE = "1⃣"
    TWO = "2⃣"
    THREE = "3⃣"
    FOUR = "4⃣"
    FIVE = "5️⃣"
    SIX = "6️⃣"
    SEVEN = "7️⃣"
    EIGHT = "8️⃣"
    NINE = "9️⃣"
    TEN = "🔟"

    LETTER = "💌"
    CHAMPANGNE_GLASS = "🥂"

    MAILBOXWITHMAIL = "📬"
    CHAMPAGNE = "🍾"

    DELETE = "🗑️"

    BACK_FORWARD = "◀️"
    FORWARD = "▶️"

    def __str__(self) -> str:
        return self.value


class CustomEmoji(Enum):
    SYSTEM_WARN: int = 973346775257710604
    SYSTEM_CHECK: int = 973347924710940742

    def __str__(self) -> str:
        return self.value

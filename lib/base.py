from typing import Optional

def try_int(mes: str) -> Optional[int]:
    try:
        return int(mes)
    except:
        return
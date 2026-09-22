from enum import StrEnum


class MetaCache(StrEnum):
    BYPASS = "bypass"
    HIT = "hit"
    MISS = "miss"

    def __str__(self) -> str:
        return str(self.value)

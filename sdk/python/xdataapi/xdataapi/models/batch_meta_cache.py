from enum import StrEnum


class BatchMetaCache(StrEnum):
    BYPASS = "bypass"
    HIT = "hit"
    MISS = "miss"
    MIXED = "mixed"

    def __str__(self) -> str:
        return str(self.value)

from enum import StrEnum


class CreateCheckoutBodyPack(StrEnum):
    BUILDER = "builder"
    GROWTH = "growth"
    SCALE = "scale"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)

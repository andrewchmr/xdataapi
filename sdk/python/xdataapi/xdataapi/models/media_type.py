from enum import StrEnum


class MediaType(StrEnum):
    ANIMATED_GIF = "animated_gif"
    PHOTO = "photo"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)

from enum import StrEnum


class SearchTweetsProduct(StrEnum):
    LATEST = "Latest"
    PEOPLE = "People"
    PHOTOS = "Photos"
    TOP = "Top"
    VIDEOS = "Videos"

    def __str__(self) -> str:
        return str(self.value)

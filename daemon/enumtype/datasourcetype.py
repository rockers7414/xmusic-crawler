from enum import Enum, unique


@unique
class DataSourceType(Enum):
    Spotify = "SPOTIFY"
    DataBase = "DB"

    def describe(self):
        return self.name, self.value

from enum import Enum, unique


@unique
class DataSourceType(Enum):
    Spotify = "spotify"
    DataBase = "db"

    def describe(self):
        return self.name, self.value

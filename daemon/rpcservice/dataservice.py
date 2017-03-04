from enumtype.datasourcetype import DataSourceType
from decorator.serialize import serializeController

from enumtype.serializetype import SerializeType
from enumtype.datasourcetype import DataSourceType


class DataService:

    def __init__(self, source_type):
        self.source_type = source_type

    def source_adapter(self, from_db, from_spotify):
        if (self.source_type.upper() == DataSourceType.DataBase.value):
            return from_db()
        elif (self.source_type.upper() == DataSourceType.Spotify.value):
            return from_spotify()

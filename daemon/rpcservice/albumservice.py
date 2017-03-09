
from .dataservice import DataService
from enumtype.serializetype import SerializeType
from enumtype.datasourcetype import DataSourceType
from decorator.serialize import serializeController
from database.albumrepo import AlbumRepo


class AlbumService(DataService):

    def __init__(self, source_type=DataSourceType.DataBase.value, data_type=SerializeType.JSON.value):
        super(AlbumService, self).__init__(source_type.upper())
        self.data_type = data_type.upper()

    def get_album(self, album_name):

        @serializeController(self.data_type)
        def fromDB():
            return AlbumRepo().get_album(album_name)

        @serializeController(self.data_type)
        def fromSpotify():
            pass

        return self.source_adapter(fromDB, fromSpotify)

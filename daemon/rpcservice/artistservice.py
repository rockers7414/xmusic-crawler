from .dataservice import DataService
from enumtype.serializetype import SerializeType
from enumtype.datasourcetype import DataSourceType
from decorator.serialize import serializeController
from database.artistrepo import ArtistRepo


class ArtistService(DataService):

    def __init__(self, source_type=DataSourceType.DataBase.value, data_type=SerializeType.JSON.value):
        super(ArtistService, self).__init__(source_type.upper())
        self.data_type = data_type.upper()

    def get_artist(self, artist_name):

        @serializeController(self.data_type)
        def fromDB():
            return ArtistRepo().get_artist(artist_name)

        @serializeController(self.data_type)
        def fromSpotify():
            pass

        return self.source_adapter(fromDB, fromSpotify)

    def get_artists_list(self, index=None, offset=None, data_type=SerializeType.JSON):

        @serializeController(self.data_type)
        def fromDB():
            if index is None or offset is None:
                return ArtistRepo().get_artists_list()
            else:
                return ArtistRepo().get_artists_by_page(index, offset)

        @serializeController(self.data_type)
        def fromSpotify():
            pass

        return self.source_adapter(fromDB, fromSpotify)

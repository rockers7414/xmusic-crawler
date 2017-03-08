from .dataservice import DataService
from enumtype.serializetype import SerializeType
from enumtype.datasourcetype import DataSourceType
from decorator.serialize import serializeController
from database.trackrepo import TrackRepo


class TrackService(DataService):

    def __init__(self, source_type=DataSourceType.DataBase.value, data_type=SerializeType.JSON.value):
        super(TrackService, self).__init__(source_type.upper())
        self.data_type = data_type.upper()

    def get_track_by_name(self, track_name):

        @serializeController(self.data_type)
        def fromDB():
            return TrackRepo().get_track_by_name(track_name)

        @serializeController(self.data_type)
        def fromSpotify():
            pass

        return self.source_adapter(fromDB, fromSpotify)

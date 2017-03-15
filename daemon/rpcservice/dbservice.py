from rpcservice.rpcservice import RPCService
from database.artistrepo import ArtistRepo
from database.albumrepo import AlbumRepo
from database.trackrepo import TrackRepo
from database import Session

from decorator.serialize import serialize
from decorator.singleton import singleton


@singleton()
@serialize()
class DBService(RPCService):

    def get_artists(self, index=None, offset=None):
        if index is None or offset is None:
            return ArtistRepo().get_artists_list()
        else:
            return ArtistRepo().get_artists_by_page(index, offset)

    def get_artist(self, artist_name):
        return ArtistRepo().get_artist(artist_name)

    def get_album(self, album_name):
        return AlbumRepo().get_album(album_name)

    def get_track(self, track_name):
        return TrackRepo().get_track_by_name(track_name)

    def raw_sql(self, sql):
        session = Session()
        result = session.execute(sql)
        return result

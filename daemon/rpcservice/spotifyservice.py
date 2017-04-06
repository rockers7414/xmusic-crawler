from .rpcservice import RPCService

from decorator.singleton import singleton
from decorator.serialize import serialize


@singleton()
@serialize()
class SpotifyService(RPCService):

    def get_artists(self, index, offset):
        if index is None or offset is None:
            pass
        else:
            pass

    def get_artists_by_name(self, artist_name):
        pass

    def get_albums_by_name(self, album_name):
        pass

    def get_tracks(self, track_name):
        pass

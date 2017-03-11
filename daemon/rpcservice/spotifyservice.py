from rpcservice import RPCService

from decorator.singleton import singleton
from decorator.serialize import json_decorate


@singleton
@json_decorate
class SpotifyService(RPCService):

    def get_artists(self, index, offset):
        if index is None or offset is None:
            pass
        else:
            pass

    def get_artist(self, artist_name):
        pass

    def get_album(self, album_name):
        pass

    def get_track(self, track_name):
        pass

from .metroprovider import MetroProvider
from .geniusprovider import GeniusProvider


class LyricProvider:

    def get_lyric(self, artist_name, track_name):
        raise NotImplementedError("get_lyric is not implemented")

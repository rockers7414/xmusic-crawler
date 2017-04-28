from .lyricparser import LyricParser
from decorator.singleton import singleton

@singleton()
class MetroProvider(LyricParser):

     # metro result url
    __metro_lyrics_url = "http://www.metrolyrics.com/{track_name}-lyrics-{artist_name}.html"
    # metro search api
    __metro_lyrics_search_url = "http://www.metrolyrics.com/search.html?search={keyword}"

    def __init__(self):
        LyricParser.__init__(self, self.__metro_lyrics_url,
                             self.__metro_lyrics_search_url)

    def gen_search_url(self, artist_name, track_name):
        raise NotImplementedError("gen_search_url is not implemented")

    def search_url_parse(self):
        raise NotImplementedError("search_url_parse is not implemented")

    def gen_result_url(self, artist_name, track_name):
        artist_name = artist_name.strip().replace(" ", "-")
        track_name = track_name.strip().replace(" ", "-")
        return self.__metro_lyrics_url.format(track_name=track_name, artist_name=artist_name)

    def result_url_parse(self):
        raise NotImplementedError("result_url_parse is not implemented")

    def etl_result(self):
        raise NotImplementedError("etl is not implemented")

    def get_lyric(self):
        raise NotImplementedError("get_lyric is not implemented")



import json
from .lyricparser import LyricParser
from decorator.singleton import singleton
from html.parser import HTMLParser


@singleton()
class MetroProvider(LyricParser):

     # metro result url
    __metro_lyrics_url = "http://www.metrolyrics.com/{track_name}-lyrics-{artist_name}.html"
    # metro search api
    # __metro_lyrics_search_url = "http://www.metrolyrics.com/search.html?search={track_name} {artist_name}"
    __metro_lyrics_search_url = "http://api.metrolyrics.com/v1/multisearch/all/X-API-KEY/196f657a46afb63ce3fd2015b9ed781280337ea7/format/json?find={track_name} {artist_name}"

    def __init__(self):
        LyricParser.__init__(self, self.__metro_lyrics_url,
                             self.__metro_lyrics_search_url)

    def gen_search_url(self, artist_name, track_name):
        artist_name = artist_name.strip().replace(" ", "-")
        track_name = track_name.strip().replace(" ", "-")
        return self.__metro_lyrics_search_url.format(track_name=track_name, artist_name=artist_name)

    def search_url_parse(self, page_data):
        # parser = MetroSearchHTMLParser()
        # parser.feed(page_data)
        # return parser.get_result()
        print("==================")
        jsonObj = json.loads(page_data)
        # print(jsonObj["results"]["songs"])
        extract_data = jsonObj["results"]["songs"]["d"]
        # for index in range(0..len(extract_data)):
            # print(extract_data[index]["u"])


        print(str(extract_data))
        return page_data

    def gen_result_url(self, artist_name, track_name):
        artist_name = artist_name.strip().replace(" ", "-")
        track_name = track_name.strip().replace(" ", "-")
        return self.__metro_lyrics_url.format(track_name=track_name, artist_name=artist_name)

    def result_url_parse(self, page_data):
        parser = MetroResultHTMLParser()
        parser.feed(page_data)
        return parser.get_result()
        # raise NotImplementedError("result_url_parse is not implemented")

    def etl_result(self, result):
        return result

    def get_lyric(self):
        raise NotImplementedError("get_lyric is not implemented")


class MetroResultHTMLParser(HTMLParser):

    """
        For parse result page.
    """

    # container
    __target_container = "div"

    # container identity
    __target_attr = "id"
    __target_attr_value = "lyrics-body-text"

    # flag for is target
    __is_target = False

    # result
    __result = ""

    def handle_starttag(self, tag, attrs):
        if tag == self.__target_container:
            for key, value in attrs:
                if key == self.__target_attr and value == self.__target_attr_value:
                    self.__is_target = True

    def handle_data(self, data):
        if self.__is_target:
            self.__result += "{0}".format(data)

    def handle_endtag(self, tag):
        if tag == self.__target_container:
            self.__is_target = False

    def get_result(self):
        if self.__result != "":
            return self.__result
        else:
            return None

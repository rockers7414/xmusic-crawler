
import pycurl

from io import BytesIO


class LyricParser():

    # http status code
    HTTP_OK = 200

    # result url
    result_lyric_url = None
    # search url
    search_lyric_url = None

    # result
    result = None

    def __init__(self, lyric_url, lyric_search_url):
        self.lyric_url = lyric_url
        self.lyric_search_url = lyric_search_url

    def request(self, url):
        buf = BytesIO()
        client = pycurl.Curl()
        client.setopt(client.URL, url)
        client.setopt(client.WRITEFUNCTION, buf.write)
        client.setopt(client.VERBOSE, True)
        # client.setopt(pycurl.CONNECTTIMEOUT, 30)
        client.perform()

        data = None
        if client.getinfo(pycurl.HTTP_CODE) == self.HTTP_OK:
            data = buf.getvalue().decode()

        client.close()
        buf.close()
        return data

    def gen_search_url(self, artist_name, track_name):
        raise NotImplementedError("gen_search_url is not implemented")

    def search_url_parse(self, page_data):
        raise NotImplementedError("search_url_parse is not implemented")

    def gen_result_url(self, artist_name, track_name):
        raise NotImplementedError("gen_result_url is not implemented")

    def result_url_parse(self, page_data):
        raise NotImplementedError("result_url_parse is not implemented")

    def etl_result(self, result):
        raise NotImplementedError("etl is not implemented")

    def get_lyric(self):
        raise NotImplementedError("get_lyric is not implemented")

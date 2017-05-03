from .lyricprovider import LyricProvider
from decorator.lyricsource import LyricSource
from .metroprovider import MetroProvider
from .geniusprovider import GeniusProvider


class CompositeLyricProvider(LyricProvider):

    def __init__(self):
        pass

    @LyricSource([GeniusProvider(), MetroProvider()])
    def get_lyric(self, artist_name, track_name, **kwargs):

        for key, source in kwargs.items():
            # gen result url
            result_url = source.gen_result_url(artist_name, track_name)
            # request result url
            page_data = source.request(result_url)
            if page_data is not None:
                # parse html and etl data
                result = source.result_url_parse(page_data)
                # etl
                etl_data = source.etl_result(result)
                return etl_data
            elif page_data is None:
                # gen search url
                search_url = source.gen_search_url(artist_name, track_name)
                # request search result
                search_page_data = source.request(search_url)
                # parse search data and get url list
                result_url_list = source.search_url_parse(search_page_data)
                if result_url_list is not None:
                    for url in result_url_list:
                        _page_data = source.request(url)
                        result = source.result_url_parse(_page_data)
                        etl_data = source.etl_result(result)
                        if etl_data is not None:
                            return etl_data
        return None

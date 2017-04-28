from .metroprovider import MetroProvider


class LyricProvider:

    def get_lyric(self, artist_name, track_name):

        providers = self.__get_providers()
        for provider in providers:

            # gen result url
            result_url = provider.gen_result_url(artist_name, track_name)

            # request result url
            page_data = provider.request(result_url)

            if page_data is not None:
                # parse html and etl data
                result = provider.result_url_parse(page_data)
                # etl
                etl_data = provider.etl_result(result)
                return etl_data
            elif page_data is None:
                # gen search url
                # search_url = provider.gen_search_url(artist_name, track_name)
                # request search result
                # result_url_list = provider.request(search_url)
                pass

        return None

    def __get_providers(self):
        return {MetroProvider()}

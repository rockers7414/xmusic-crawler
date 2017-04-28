from provider.lyric.lyricprovider import LyricProvider

import pycurl

from io import BytesIO


if __name__ == '__main__':
    # result_url = MetroProvider().gen_result_url("maroon 5", "sugar")
    # print(result_url)
    tmp = LyricProvider().get_lyric("maroon 5", "sugar")
    print("done.")


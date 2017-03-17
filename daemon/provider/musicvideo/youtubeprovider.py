import json
import logging
from urllib.parse import urlencode

import isodate
import pycurl
from database.entity import Repository
from provider.musicvideo.musicvideoprovider import MusicVideoProvider

from config import Config


try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class YoutubeProvider(MusicVideoProvider):
    logger = logging.getLogger(__name__)

    SERVICE_HOST = "https://www.googleapis.com"
    VIDEO_LINK_FORMAT = "https://www.youtube.com/watch?v={0}"

    def __init__(self):
        super().__init__()
        self.key = Config.youtube_api_key

    def get_music_video(self, artist_name, album_name, track_name):
        video_id = self.__search_video_id(("{0} {1}")
                                          .format(artist_name, track_name))

        link = self.VIDEO_LINK_FORMAT.format(video_id)
        duration_seconds = self.__get_video_duration(video_id)

        return Repository(link, duration_seconds)

    def __search_video_id(self, query):
        params = {
            "key": self.key,
            "part": "id,snippet",
            "order": "relevance",
            "type": "video",
            "videoSyndicated": "true",
            "maxResults": 3,
            "q": query
        }

        buf = BytesIO()

        client = pycurl.Curl()
        client.setopt(pycurl.URL, self.SERVICE_HOST + "/youtube/v3/search?" +
                      urlencode(params))
        client.setopt(pycurl.WRITEFUNCTION, buf.write)
        client.perform()
        client.close()

        body = json.loads(buf.getvalue().decode("utf-8"))
        buf.close()

        if "error" in body:
            raise Exception("query error: {0}".format(body))

        if len(body["items"]) == 0:
            raise Exception("result not found")

        video_id = body["items"][0]["id"]["videoId"]

        return video_id

    def __get_video_duration(self, video_id):
        params = {
            "key": self.key,
            "part": "contentDetails",
            "id": video_id
        }

        buf = BytesIO()

        client = pycurl.Curl()
        client.setopt(pycurl.URL, self.SERVICE_HOST + "/youtube/v3/videos?" +
                      urlencode(params))
        client.setopt(pycurl.WRITEFUNCTION, buf.write)
        client.perform()
        client.close()

        body = json.loads(buf.getvalue().decode("utf-8"))
        buf.close()

        if "error" in body:
            raise Exception("query error: {0}".format(body))

        if len(body["items"]) == 0:
            raise Exception("result not found")

        duration = body["items"][0]["contentDetails"]["duration"]
        duration_seconds = isodate.parse_duration(duration).seconds

        return duration_seconds

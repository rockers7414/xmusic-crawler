import configparser
import json
import logging
import os
from urllib.parse import urlencode

import isodate
import pycurl
from database.entity import Repository
from provider.musicvideo.musicvideoprovider import MusicVideoProvider

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class YoutubeProvider(MusicVideoProvider):
    logger = logging.getLogger(__name__)
    SERVICE_HOST = 'https://www.googleapis.com'
    VIDEO_LINK_FORMAT = 'https://www.youtube.com/watch?v={}'

    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read("config.cfg")
        self.key = os.environ['YOUTUBE_API_KEY']

    def getMusicVideo(self, artist_name, album_name, track_name):
        videoId = self.__searchVideoId('{} {}'.format(artist_name, track_name))

        link = self.VIDEO_LINK_FORMAT.format(videoId)
        duration_seconds = self.__getVideoDuration(videoId)

        return Repository(link, duration_seconds)

    def __searchVideoId(self, query):
        params = {
            'key': self.key,
            'part': 'id,snippet',
            'order': 'relevance',
            'type': 'video',
            'videoSyndicated': 'true',
            'maxResults': 3,
            'q': query
        }

        buf = BytesIO()

        client = pycurl.Curl()
        client.setopt(pycurl.URL, self.SERVICE_HOST + '/youtube/v3/search?' +
                      urlencode(params))
        client.setopt(pycurl.WRITEFUNCTION, buf.write)
        client.perform()
        client.close()

        body = json.loads(buf.getvalue().decode("utf-8"))
        buf.close()

        if 'error' in body:
            raise Exception('query error: {}'.format(body))

        if len(body['items']) == 0:
            raise Exception('result not found')

        videoId = body['items'][0]['id']['videoId']

        return videoId

    def __getVideoDuration(self, videoId):
        params = {
            'key': self.key,
            'part': 'contentDetails',
            'id': videoId
        }

        buf = BytesIO()

        client = pycurl.Curl()
        client.setopt(pycurl.URL, self.SERVICE_HOST + '/youtube/v3/videos?' +
                      urlencode(params))
        client.setopt(pycurl.WRITEFUNCTION, buf.write)
        client.perform()
        client.close()

        body = json.loads(buf.getvalue().decode("utf-8"))
        buf.close()

        if 'error' in body:
            raise Exception('query error: {}'.format(body))

        if len(body['items']) == 0:
            raise Exception('result not found')

        duration = body['items'][0]['contentDetails']['duration']
        duration_seconds = isodate.parse_duration(duration).seconds

        return duration_seconds

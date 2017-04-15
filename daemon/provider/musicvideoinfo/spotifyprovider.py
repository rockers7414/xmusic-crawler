import logging
import pycurl
import json
import sys
sys.path.append('../../')
from config import Config
from authorization.spotify import Spotify

from urllib.parse import urlencode
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from database.entity import Artist, Album, Track, Image, Genre
from .musicvideoinfoprovider import MusicVideoInfoProvider


class SpotifyProvider(MusicVideoInfoProvider):
    logger = logging.getLogger(__name__)

    service_host = "https://api.spotify.com"

    #  FIXME: This property is the workaround, once the datasrouce decorator is
    #  refactored, this function should be replaced with decorator.
    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, value):
        self._provider = value

    def __search(self, keyword, search_type):
        offset = 0
        result_key = search_type + "s"
        result = []

        while True:
            self.logger.info("search " + keyword + ", offset = " + str(offset))
            params = {
                "q": keyword,
                "type": search_type,
                "offset": offset,
                "limit": 50
            }

            buf = BytesIO()

            client = pycurl.Curl()
            client.setopt(pycurl.URL, self.service_host +
                          "/v1/search" + "?" + urlencode(params))
            client.setopt(pycurl.WRITEFUNCTION, buf.write)
            client.perform()
            client.close()

            body = json.loads(buf.getvalue().decode("utf-8"))
            buf.close()

            if body[result_key]["total"] > 0:
                for data in body[result_key]["items"]:
                    result.append(data)

            if body[result_key]["total"] > \
                    body[result_key]["limit"] * (offset + 1):
                offset = offset + 1
            else:
                break

        self.logger.info("Done")
        return result

    def get_artists_by_name(self, artist_name):
        self.logger.info("Search the artist({0}) from Spotify."
                         .format(artist_name))

        result = self.__search(artist_name, "artist")
        artists = []
        for data in result:
            artist = Artist(data["name"], data["popularity"])

            images = []
            for image_data in data["images"]:
                images.append(Image(image_data["url"],
                                    image_data["width"],
                                    image_data["height"]))

            genres = []
            for genre in data["genres"]:
                genres.append(Genre(genre))

            artist.images = images
            artist.genres = genres

            artist.provider = self._provider
            artist.provider_res_id = data["id"]

            self.logger.info(artist)
            artists.append(artist)

        return artists

    def get_albums_by_name(self, album_name):
        self.logger.info("Search the album({0}) from Spotify."
                         .format(album_name))

        result = self.__search(album_name, "album")
        albums = []
        for data in result:
            album = Album(data["name"], None)

            images = []
            for image_data in data["images"]:
                images.append(Image(image_data["url"],
                                    image_data["width"],
                                    image_data["height"]))

            album.images = images

            album.provider = self._provider
            album.provider_res_id = data["id"]

            self.logger.info(album)
            albums.append(album)

        return albums

    def get_albums_by_artist_id(self, artist_id):
        self.logger.info("Get albums of the artist(" +
                         artist_id + ") from Spotify.")
        if not artist_id:
            return None

        offset = 0
        albums = []
        while True:
            params = {
                "album_type": "album",
                "offset": offset,
                "limit": 50
            }

            buf = BytesIO()

            client = pycurl.Curl()
            client.setopt(pycurl.URL, self.service_host + "/v1/artists/" +
                          artist_id + "/albums" + "?" + urlencode(params))
            client.setopt(pycurl.WRITEFUNCTION, buf.write)
            client.perform()
            client.close()

            body = json.loads(buf.getvalue().decode("utf-8"))
            buf.close()

            if body["total"] > 0:
                for data in body["items"]:
                    album = Album(data["name"], None)

                    images = []
                    for image_data in data["images"]:
                        images.append(Image(image_data["url"],
                                            image_data["width"],
                                            image_data["height"]))

                    album.images = images

                    album.provider = self._provider
                    album.provider_res_id = data["id"]

                    albums.append(album)

            if body["total"] > body["limit"] * (offset + 1):
                offset = offset + 1
            else:
                break

        return albums

    def get_tracks_by_name(self, track_name):
        self.logger.info("Search the track({0}) from Spotify."
                         .format(track_name))

        result = self.__search(track_name, "track")
        tracks = []

        for data in result:
            tracks.append(Track(data["name"], None, data["track_number"]))

        return tracks

    def get_tracks_by_album_id(self, album_id):
        self.logger.info("Get tracks of the album(" +
                         album_id + ") from Spotify.")
        if not album_id:
            return None

        offset = 0
        tracks = []
        while True:
            params = {
                "offset": offset,
                "limit": 50
            }

            buf = BytesIO()

            client = pycurl.Curl()
            client.setopt(pycurl.URL, self.service_host + "/v1/albums/" +
                          album_id + "/tracks" + "?" + urlencode(params))
            client.setopt(pycurl.WRITEFUNCTION, buf.write)
            client.perform()
            client.close()

            body = json.loads(buf.getvalue().decode("utf-8"))
            buf.close()

            if body["total"] > 0:
                for data in body["items"]:
                    tracks.append(
                        Track(data["name"], None, data["track_number"]))

            if body["total"] > body["limit"] * (offset + 1):
                offset = offset + 1
            else:
                break

        return tracks

    def get_new_release_by_album_id(self):
        self.logger.info("Get albums of the new release from Spotify.")
        service_host = "https://api.spotify.com"
        """
            Get client_id and client_secret value from local.
        """
        config = Config("../../xmusic.cfg")
        print("1")
        client_id = config.spotify_client_id
        client_secret = config.spotify_client_secret

        access_token = Spotify(client_id, client_secret).get_token()
        headers = ["Authorization: Bearer " + access_token]

        offset = 0
        limit = 20
        new_release = []
        while True:
            params = {"offset": offset*limit, "limit": limit}
            buf = BytesIO()
            client = pycurl.Curl()
            client.setopt(pycurl.HEADER, False)
            client.setopt(pycurl.HTTPHEADER, headers)
            client.setopt(pycurl.URL, service_host + "/v1/browse/new-releases" + "?" + urlencode(params))
            client.setopt(pycurl.WRITEFUNCTION, buf.write)
            client.perform()
            client.close()
            body = json.loads(buf.getvalue().decode("utf-8"))
            buf.close()

            for album_data in body["albums"]["items"]:
                image = []
                for image_data in album_data["images"]:
                    image.append((image_data["url"],
                                  image_data["width"],
                                  image_data["height"]))

                artists = album_data["artists"][0]
                artist_data = (artists["name"], artists["id"])
                new_release.append((album_data["id"],
                                    album_data["type"],
                                    artist_data,
                                    image))

            if body["albums"]["total"] > body["albums"]["offset"]:
                offset = offset + 1
            else:
                break

        return new_release

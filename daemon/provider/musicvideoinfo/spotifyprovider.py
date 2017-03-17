import logging
import pycurl
import json

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

    def get_artists_by_name(self, artist_name):
        self.logger.info("Search the artist({0}) from Spotify."
                         .format(artist_name))

        offset = 0
        artists = []

        while True:
            params = {
                "q": artist_name,
                "type": "artist",
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

            if body["artists"]["total"] > 0:
                for artist_data in body["artists"]["items"]:
                    artist = Artist(
                        artist_data["name"], artist_data["popularity"])

                    images = []
                    for image_data in artist_data["images"]:
                        images.append(Image(image_data["url"],
                                            image_data["width"],
                                            image_data["height"]))

                    genres = []
                    for genre in artist_data["genres"]:
                        genres.append(Genre(genre))

                    artist.images = images
                    artist.genres = genres

                    artist.provider = self._provider
                    artist.provider_res_id = artist_data["id"]

                    self.logger.info(artist)
                    artists.append(artist)

            if body["artists"]["total"] > body["artists"]["limit"]:
                offset = offset + 1
            else:
                break

        return artists

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

            if body["total"] > body["limit"]:
                offset = offset + 1
            else:
                break

        return albums

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

            if body["total"] > body["limit"]:
                offset = offset + 1
            else:
                break

        return tracks

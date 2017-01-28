import pycurl
import json
from crawler import Crawler
from objects.artist import Artist
from objects.album import Album
from objects.track import Track
from urllib.parse import urlencode
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

class SpotifyCrawler(Crawler):

    service_host = "https://api.spotify.com"

    def searchArtist(self, name):
        print("Searching " + name + "...")

        params = {
            "q": name,
            "type": "artist"
        }

        buf = BytesIO()

        client = pycurl.Curl()
        client.setopt(pycurl.URL, self.service_host + "/v1/search" + "?" + urlencode(params))
        client.setopt(pycurl.WRITEFUNCTION, buf.write)
        client.perform()
        client.close()

        body = json.loads(buf.getvalue().decode("utf-8"))
        buf.close()

        if body["artists"]["total"] > 0:
            data = max(body["artists"]["items"], key = lambda a: a["followers"]["total"])
            artist = Artist(data["id"], data["name"], data["popularity"], data["genres"], data["images"])
            return artist

        return None

    def getAlbumsByArtist(self, artistId):
        if not artistId:
            return None

        print("Get spotifiy albums by artist id = " + artistId)

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
            client.setopt(pycurl.URL, self.service_host + "/v1/artists/" + artistId + "/albums" + "?" + urlencode(params))
            client.setopt(pycurl.WRITEFUNCTION, buf.write)
            client.perform()
            client.close()

            body = json.loads(buf.getvalue().decode("utf-8"))
            buf.close()

            if body["total"] > 0:
                for data in body["items"]:
                    albums.append(Album(data["id"], data["name"], data["images"]))

            if body["total"] > body["limit"]:
                offset = offset + 1
            else:
                break

        return albums

    def getTracksByAlbum(self, albumId):
        if not albumId:
            return None

        print("Get spotifiy tracks by album id = " + albumId)

        offset = 0
        tracks = []
        while True:
            params = {
                "offset": offset,
                "limit": 50
            }
            
            buf = BytesIO()

            client = pycurl.Curl()
            client.setopt(pycurl.URL, self.service_host + "/v1/albums/" + albumId + "/tracks" + "?" + urlencode(params))
            client.setopt(pycurl.WRITEFUNCTION, buf.write)
            client.perform()
            client.close()

            body = json.loads(buf.getvalue().decode("utf-8"))
            buf.close()

            if body["total"] > 0:
                for data in body["items"]:
                    tracks.append(Track(data["id"], data["name"], data["track_number"]))

            if body["total"] > body["limit"]:
                offset = offset + 1
            else:
                break

        return tracks

import json
from objects.album import Album

class Artist:
    artistId = ""
    name = ""
    popularity = 0
    genres = []
    images = []

    albums = []

    def __init__(self, artistId, name, popularity, genres, images):
        self.artistId = artistId
        self.name = name
        self.popularity = popularity
        self.genres = genres
        self.images = images

    def getArtistId(self):
        return self.artistId

    def getName(self):
        return self.name

    def getPopularity(self):
        return self.popularity

    def getGenres(self):
        return self.genres

    def getImages(self):
        return self.images

    def setAlbums(self, albums):
        self.albums = albums

    def getAlbums(self):
        return self.albums

    def toJSON(self):
        return json.dumps(self, cls = Artist.ArtistEncoder)

    class ArtistEncoder(json.JSONEncoder):
        def default(self, obj):
            return obj.__dict__

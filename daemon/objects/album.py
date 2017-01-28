import json

class Album:
    albumId = ""
    name = ""
    popularity = 0
    genres = []
    images = []

    tracks = []

    def __init__(self, albumId, name, images, popularity = 0, genres = []):
        self.albumId = albumId
        self.name = name
        self.images = images
        self.popularity = popularity
        self.genres = genres

    def getAlbumId(self):
        return self.albumId

    def getName(self):
        return self.name

    def getImages(self):
        return self.images

    def getGenres(self):
        return self.genres

    def getPopularity(self):
        return self.popularity

    def setTracks(self, tracks):
        self.tracks = tracks

    def getTracks(self):
        return self.tracks

    def toJSON(self):
        return json.dumps(self, cls = Album.AlbumEncoder)

    class AlbumEncoder(json.JSONEncoder):
        def default(self, obj):
            return obj.__dict__

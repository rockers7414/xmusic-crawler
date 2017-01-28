import json

class Track:
    trackId = ""
    name = ""
    popularity = 0
    track_number = 0
    genres = []

    def __init__(self, trackId, name, track_number, popularity = 0, genres = []):
        self.trackId = trackId
        self.name = name
        self.track_number = track_number
        self.popularity = popularity
        self.genres = genres

    def getTrackId(self):
        return self.trackId

    def getName(self):
        return self.name

    def getTrackNumber(self):
        return self.track_number

    def getPopularity(self):
        return self.popularity

    def getGenres(self):
        return self.genres
    
    def toJSON(self):
        return json.dumps(self, cls = Track.TrackEncoder)

    class TrackEncoder(json.JSONEncoder):
        def default(self, obj):
            return obj.__dict__


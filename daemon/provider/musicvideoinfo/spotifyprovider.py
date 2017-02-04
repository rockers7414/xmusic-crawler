import logging
from .musicvideoinfoprovider import MusicVideoInfoProvider

class SpotifyProvider(MusicVideoInfoProvider):
    logger = logging.getLogger(__name__)

    def getArtistByName(self, artist_name):
        self.logger.info("Search the artist(" + artist_name + ") from Spotify.")

    def getAlbumsByArtist(self, artist_id):
        self.logger.info("Get albums of the artist(" + artist_id + ") from Spotify.")

    def getTracksByAlbum(self, album_id):
        self.logger.info("Get tracks of the album(" + album_id + ") from Spotify.")

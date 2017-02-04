import logging

from .artist import Artist
from .connection import Connection

class ArtistRepo:
    logger = logging.getLogger(__name__)

    def __init__(self, session):
        self._session = session

    def getArtistsByName(self, artist_name):
        query = self._session.query(Artist).filter(Artist.name == artist_name)
        return query.all()

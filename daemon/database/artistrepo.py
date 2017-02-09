import logging

from .entity import Artist

class ArtistRepo:
    logger = logging.getLogger(__name__)

    def __init__(self, Session):
        self._session = Session()

    def getArtistsByName(self, artist_name):
        query = self._session.query(Artist).filter(Artist.name == artist_name)
        return query.all()

    def save(self, artist):
        try:
            self._session.add(artist)
            self._session.flush()
            self._session.commit()
        except:
            self._session.rollback()
            raise

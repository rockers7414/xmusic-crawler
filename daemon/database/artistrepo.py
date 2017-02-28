import logging

from decorator.injectdbsession import inject_db_session

from .entity import Artist


@inject_db_session()
class ArtistRepo:
    logger = logging.getLogger(__name__)

    def getArtistsByName(self, artist_name):
        query = self._session.query(Artist).filter(Artist.name == artist_name)
        return query.all()

    def get_all_artists(self, index, offset):
        query = self._session.query(Artist).order_by(
            Artist.name).limit(offset).offset((index - 1) * offset)
        return query.all()

    def save(self, artist):
        try:
            self._session.add(artist)
            self._session.flush()
            self._session.commit()
        except:
            self._session.rollback()
            raise

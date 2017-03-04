import logging

from decorator.injectdbsession import inject_db_session
from .entity import Artist
# from sqlalchemy.orm import deferred
from sqlalchemy.orm import load_only, Load, lazyload


@inject_db_session()
class ArtistRepo:
    logger = logging.getLogger(__name__)

    def getArtistsByName(self, artist_name):
        query = self._session.query(Artist).filter(Artist.name == artist_name)
        return query.all()

    def get_artists_list(self, index=None, offset=None):
        if index is None or offset is None:
            query = self._session.query(Artist).options(
                lazyload("albums")).order_by(Artist.name)
        else:
            query = self._session.query(Artist).options(lazyload("albums")).order_by(
                Artist.name).limit(offset).offset((index - 1) * offset)

        return query.all()

    def get_artist(self, artist_name):
        query = self._session.query(Artist).filter(
            Artist.name == artist_name)
        return query.all()

    def save(self, artist):
        try:
            self._session.add(artist)
            self._session.flush()
            self._session.commit()
        except:
            self._session.rollback()
            raise

import logging

from decorator.injectdbsession import inject_db_session
from .entity import Artist
from sqlalchemy.orm import lazyload


@inject_db_session()
class ArtistRepo:
    logger = logging.getLogger(__name__)

    def get_artists_by_page(self, index, offset):
        query = self._session.query(Artist).options(lazyload("albums")).order_by(
            Artist.name).limit(offset).offset((index - 1) * offset)
        return query.all()

    def get_artists_list(self):
        query = self._session.query(Artist).options(
            lazyload("albums")).order_by(Artist.name)
        return query.all()

    def get_artist_by_name(self, artist_name):
        query = self._session.query(Artist).options(lazyload("albums")).filter(
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

import logging

from decorator.injectdbsession import inject_db_session
from .entity import Album
from sqlalchemy.orm import lazyload


@inject_db_session()
class AlbumRepo:
    logger = logging.getLogger(__name__)

    def get_albums_by_name(self, album_name):
        query = self._session.query(Album).options(
            lazyload("tracks.repositories")).filter(Album.name == album_name)
        return query.all()

    def save(self, album):
        try:
            self._session.add(album)
            self._session.flush()
            self._session.commit()
        except:
            self._session.rollback()
            raise

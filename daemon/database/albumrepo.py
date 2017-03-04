import logging

from decorator.injectdbsession import inject_db_session
from .entity import Album
from .entity import Artist


@inject_db_session()
class AlbumRepo:
    logger = logging.getLogger(__name__)

    def save(self, album):
        try:
            self._session.add(Album)
            self._session.flush()
            self._session.commit()
        except:
            self._session.rollback()
            raise

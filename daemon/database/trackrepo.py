import logging

from decorator.injectdbsession import inject_db_session
from .entity import Track


@inject_db_session()
class TrackRepo:
    logger = logging.getLogger(__name__)

    def get_tracks_by_name(self, track_name):
        query = self._session.query(Track).filter(Track.name == track_name)
        return query.all()

    def save(self, track):
        try:
            self._session.add(track)
            self._session.flush()
            self._session.commit()
            return track
        except:
            self._session.rollback()
            raise

    def delete(self, track):
        try:
            self._session.delete(track)
            self._session.commit()
        except:
            self._session.rollback()
            raise

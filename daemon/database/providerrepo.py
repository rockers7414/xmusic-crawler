import logging

from database.entity import Provider, Repository, Track
from decorator.injectdbsession import inject_db_session


@inject_db_session()
class ProviderRepo(object):
    logger = logging.getLogger(__name__)

    def get_provider(self, name):
        return Provider(name)

    def get_unfetched_tracks_by_provider(self, provider):
        query = self._session.query(Track).join(Track.album).filter(
            ~Track.track_id.in_(
                self._session.query(Repository.track_id).filter(
                    Repository.provider == provider
                )
            )
        )

        return query.all()

    def save(self, provider):
        try:
            self._session.add(provider)
            self._session.flush()
            self._session.commit()
        except:
            self._session.rollback()
            raise

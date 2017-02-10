import logging

from decorator.injectdbsession import inject_db_session

from .entity import Album, Datasource, Repository, Track


@inject_db_session
class DatasourceRepo(object):
    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    def getDatasource(self, name):
        return Datasource(name)

    def getUnparseTracksByDatasource(self, datasource):
        query = self._session.query(Track).join(Track.album).filter(
            ~Track.track_id.in_(
                self._session.query(Repository.track_id).filter(
                    Repository.datasource == datasource
                )
            )
        )

        return query.all()

    def save(self, datasource):
        try:
            self._session.add(datasource)
            self._session.flush()
            self._session.commit()
        except:
            self._session.rollback()
            raise

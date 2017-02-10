import logging

from database.datasourcerepo import DatasourceRepo


class datasource(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def _null_init(self, *args, **kwargs):
            pass

        def fetch(self):
            if '_process' not in dir(self):
                raise NotImplementedError(
                    'with datasource decorator, ' +
                    'method: _process(self, datasource, tracks) is required')

            datasource = self.datasource_repo.getDatasource(
                self._datasource_name)
            tracks = self.datasource_repo.getUnparseTracksByDatasource(
                datasource)

            self.logger.info('processing... datasource={}, tracks={}'.format(
                datasource, tracks))
            self._process(datasource, tracks)
            self.logger.info('done. datasource={}, tracks={}'.format(
                datasource, tracks))

            self.datasource_repo.save(datasource)

        def __new__(cls, bases, *args, **kwargs):
            obj = object.__new__(cls)
            obj.__datasource__ = True
            obj._datasource_name = self.name
            obj.datasource_repo = DatasourceRepo()
            obj.logger = logging.getLogger('{}.{}'.format(self.name, __name__))
            obj._init(*args, **kwargs)

            return obj

        cls._init = cls.__init__
        cls.__init__ = _null_init
        cls.__new__ = classmethod(__new__)
        cls.fetch = fetch

        return cls

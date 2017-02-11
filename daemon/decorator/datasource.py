from database.datasourcerepo import DatasourceRepo

dic_curr_datasources = {}

class datasource(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def _null_init(self, *args, **kwargs):
            pass

        def fetch(self):
            if '_process' not in dir(self):
                raise NotImplementedError(
                    'the datasource of "' + self._datasource_name + '" ' +
                    'method: _process(self, datasource, tracks) is required')

            datasource = self.datasource_repo.getDatasource(
                self._datasource_name)
            tracks = self.datasource_repo.getUnfetchedTracksByDatasource(
                datasource)

            # TODO: temporarily limit fetching times
            self._process(datasource, tracks[:10])

            self.datasource_repo.save(datasource)

        def __new__(cls, bases, *args, **kwargs):
            obj = object.__new__(cls)
            obj._datasource_name = self.name
            obj.datasource_repo = DatasourceRepo()
            obj._init(*args, **kwargs)

            return obj

        cls._init = cls.__init__
        cls.__init__ = _null_init
        cls.__new__ = classmethod(__new__)
        cls.fetch = fetch

        dic_curr_datasources[self.name] = cls

        return cls

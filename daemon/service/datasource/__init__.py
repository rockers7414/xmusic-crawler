from decorator.datasource import dic_curr_datasources
from utils import dynamic_load

dynamic_load(__file__, 'service.datasource')


class Datasource(object):

    @staticmethod
    def fetch():
        for name, datasource in dic_curr_datasources.items():
            datasource().fetch()

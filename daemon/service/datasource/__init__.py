import glob
from os.path import basename, dirname, isfile

from decorator.datasource import dic_curr_datasources


def dynamic_load():
    files = glob.glob(dirname(__file__)+"/*.py")

    for f in files:
        if isfile(f) and not f.endswith('__init__.py'):
            module = 'service.datasource.{}'.format(basename(f)[:-3])
            __import__(module, globals(), locals(), [], 0)

dynamic_load()

class Datasource(object):

    @staticmethod
    def fetch():
        for name, datasource in dic_curr_datasources.items():
            datasource().fetch()

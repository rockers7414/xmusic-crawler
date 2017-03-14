import glob
from os.path import basename, dirname, isfile

from decorator.provider import dic_curr_providers


def dynamic_load():
    files = glob.glob(dirname(__file__) + '/*.py')

    for f in files:
        if isfile(f) and not f.endswith('__init__.py'):
            module = 'service.provider.{}'.format(basename(f)[:-3])
            __import__(module, globals(), locals(), [], 0)

dynamic_load()


class ProviderService(object):

    @staticmethod
    def fetch():
        for name, provider in dic_curr_providers.items():
            provider().fetch()

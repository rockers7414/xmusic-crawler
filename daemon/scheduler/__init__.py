import glob
import threading
from os.path import dirname, join, basename, isfile

from decorator.schedule import scheduler


class Scheduler(threading.Thread):

    def __init__(self):
        super(Scheduler, self).__init__(name='Scheduler', daemon=True)
        self.load()

    def run(self):
        scheduler.run()

    def load(self):
        path = join(dirname(__file__), 'jobs/*')
        module_prefix = 'scheduler.jobs'
        files = glob.glob(dirname(path) + '/*.py')

        for f in files:
            if isfile(f) and not f.endswith('__init__.py'):
                module = '{}.{}'.format(module_prefix, basename(f)[:-3])
                __import__(module, globals(), locals(), [], 0)

    @staticmethod
    def is_scheduled(job):
        event = [q for q in scheduler.queue if q.kwargs['job'] is job]

        return len(event) > 0

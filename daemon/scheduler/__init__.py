import threading
from os.path import dirname, join

from decorator.schedule import scheduler
from utils import dynamic_load

dynamic_load(join(dirname(__file__), 'jobs/*'), 'scheduler.jobs')


class Scheduler(threading.Thread):

    def __init__(self):
        super(Scheduler, self).__init__(name='Scheduler', daemon=True)

    def run(self):
        scheduler.run()

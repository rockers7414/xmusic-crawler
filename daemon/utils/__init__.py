import glob
from os.path import basename, dirname, isfile

from decorator.schedule import scheduler


def dynamic_load(path_name, module_prefix):
    files = glob.glob(dirname(path_name) + '/*.py')

    for f in files:
        if isfile(f) and not f.endswith('__init__.py'):
            module = '{}.{}'.format(module_prefix, basename(f)[:-3])
            __import__(module, globals(), locals(), [], 0)


def is_job_sched(job_func):
    event = [q for q in scheduler.queue if q.kwargs['job_func'] is job_func]

    return len(event) > 0

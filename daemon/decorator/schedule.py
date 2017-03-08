import logging
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)


class add_job(object):

    def __init__(self, timedelta, repeat=False, args=(), kwargs={}):
        self.logger = logging.getLogger(__name__)
        self.__interval = timedelta.total_seconds()
        self.__repeat = repeat
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, job_func):
        def trigger_job(*args, **kwargs):
            try:
                self.logger.debug('executing trigger_job: {}({}, {})'.format(
                    job_func.__qualname__, self.__args, self.__kwargs))
                job_func(*self.__args, **self.__kwargs)
            except Exception as e:
                self.logger.error(e)
            finally:
                self.logger.debug('excuted done.')

                # set up repeat scheduling job if its need.
                if self.__repeat:
                    scheduler.enter(self.__interval, 1, trigger_job,
                                    (), {'job_func': job_func})

        # scheduling the current job with the specific interval, args, kwargs.
        scheduler.enter(self.__interval, 1, trigger_job,
                        (), {'job_func': job_func})

        return job_func

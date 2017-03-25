import logging
from datetime import timedelta

from decorator.schedule import schedule
from scheduler import Scheduler

logger = logging.getLogger(__name__)


# the usage for @schedule:
#  @schedule(timedelta(seconds=2),
#           repeat=False,
#           args=('test args',),
#           kwargs={'msg': 'hello wolrd'})
#  def test_job1(arg1, msg=''):
#      logger.info('this is test_job1, with arg1={}, msg={}'.format(arg1, msg))

@schedule(timedelta(days=1), repeat=True)
def fetch_new_release_job():
    logger.info('is job sched? {}'.format(Scheduler.is_scheduled(
        fetch_new_release_job)))
    logger.info('fetching new release...')


@schedule(timedelta(minutes=1), repeat=True)
def fetch_track_datasource():
    logger.info('fetching datasouce...')

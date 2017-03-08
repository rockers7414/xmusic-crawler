import logging
from datetime import timedelta

from decorator.schedule import add_job
from utils import is_job_sched

logger = logging.getLogger(__name__)


# the usage for @add_job:
#  @add_job(timedelta(seconds=2),
#           repeat=False,
#           args=('test args',),
#           kwargs={'msg': 'hello wolrd'})
#  def test_job1(arg1, msg=''):
#      logger.info('this is test_job1, with arg1={}, msg={}'.format(arg1, msg))

@add_job(timedelta(days=1), repeat=True)
def fetch_new_release_job():
    logger.info('is job sched? {}'.format(is_job_sched(fetch_new_release_job)))
    logger.info('fetching new release...')


@add_job(timedelta(minutes=1), repeat=True)
def fetch_track_datasource():
    logger.info('fetching datasouce...')

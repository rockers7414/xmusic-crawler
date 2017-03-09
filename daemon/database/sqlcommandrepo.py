import logging

from decorator.injectdbsession import inject_db_session


@inject_db_session()
class SqlCommandRepo:
    logger = logging.getLogger(__name__)

    def execute(self, sql_command):
        result = self._session.execute(sql_command)
        return result

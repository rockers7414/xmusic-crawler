import logging
import sqlalchemy.orm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Connection:
    logger = logging.getLogger(__name__)

    def __init__(self, username, password, host, port, database):
        self.logger.info("Initialize the database connection.")
        conn_string = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
                username, password, host, port, database)
        self.logger.debug(conn_string)
        self._engine = create_engine(conn_string)
        self.__Session = sessionmaker(bind = self._engine)
        self._session = self.__Session()

    def getSession(self):
       return self._session

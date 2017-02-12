from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker())


def db_init(username, password, host, port, database):
    conn_string = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        username, password, host, port, database)
    engine = create_engine(conn_string, echo=True)
    Session.configure(bind=engine)

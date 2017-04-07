from database import db_init
from config import Config
from rpcservice.dbservice import DBService

if __name__ == "__main__":
    config = Config("xmusic.cfg")
    db_init(config.db_username,
            config.db_password,
            "localhost",
            config.db_port,
            config.db_database)

    data = DBService().get_artists_by_name("obama")
    print(data)

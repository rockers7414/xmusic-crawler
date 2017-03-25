import configparser
import logging


class Config(object):

    def __init__(self, config_file):
        self.__config_file = config_file

        self.__config = configparser.ConfigParser()
        self.__config.read(config_file)

        self._reload()

    def _reload(self):
        logging.basicConfig(
            filename=self.logging_file,
            level=self.logging_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def save(self):
        with open(self.__config_file, "w") as f:
            self.__config.write(f)

    @property
    def spotify_client_id(self):
        return self.__config["SPOTIFY"]["client_id"]

    @property
    def spotify_client_secret(self):
        return self.__config["SPOTIFY"]["client_secret"]

    @property
    def youtube_api_key(self):
        return self.__config["YOUTUBE"]["apikey"]

    @property
    def rpcserver_host(self):
        return self.__config["RPCSERVICE"]["host"]

    @property
    def rpcserver_port(self):
        return self.__config["RPCSERVICE"]["port"]

    @property
    def logging_level(self):
        return self.__config["LOGGING"]["level"]

    @logging_level.setter
    def logging_level(self, value):
        if value.upper() not in ["CRITICAL", "ERROR", "WANRING", "INFO",
                                 "DEBUG", "NOTSET"]:
            return
        self.__config["LOGGING"]["level"] = value.upper()
        self._reload()

    @property
    def logging_file(self):
        return self.__config["LOGGING"]["file"]

    @property
    def db_username(self):
        return self.__config["DATABASE"]["username"]

    @property
    def db_password(self):
        return self.__config["DATABASE"]["password"]

    @property
    def db_host(self):
        return self.__config["DATABASE"]["host"]

    @property
    def db_port(self):
        return self.__config["DATABASE"]["port"]

    @property
    def db_database(self):
        return self.__config["DATABASE"]["database"]

    @property
    def mq_host(self):
        return self.__config["ACTIVEMQ"]["host"]

    @property
    def mq_port(self):
        return self.__config["ACTIVEMQ"]["port"]

    @property
    def mq_username(self):
        return self.__config["ACTIVEMQ"]["username"]

    @property
    def mq_password(self):
        return self.__config["ACTIVEMQ"]["password"]

    @property
    def mq_queue(self):
        return self.__config["ACTIVEMQ"]["queue"]

    @property
    def mq_num_of_workers(self):
        return int(self.__config["ACTIVEMQ"]["num_of_workers"])

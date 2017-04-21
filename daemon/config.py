from decorator.singleton import singleton

import configparser
import logging


@singleton()
class Config(object):

    def __init__(self, config_file="xmusic.cfg"):
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

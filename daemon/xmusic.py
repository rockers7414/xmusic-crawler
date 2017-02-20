#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging
import signal
import sys

from activemq.client import MQClient
from database import db_init
from rpcservice.rpcserver import RPCServer

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")

    logging.basicConfig(
        filename=config["LOGGING"]["file"],
        level=config["LOGGING"]["level"],
        format="%(asctime)s - [%(threadName)s]%(name)s - %(levelname)s - %(message)s")

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            config["DATABASE"]["host"],
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    mq = MQClient(config["ACTIVEMQ"]["host"],
                  config["ACTIVEMQ"]["port"],
                  config["ACTIVEMQ"]["username"],
                  config["ACTIVEMQ"]["password"])
    mq.start()

    def handle_signal(signal, frame):
        mq.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)

    server = RPCServer(config["RPCSERVICE"]["host"],
                       config["RPCSERVICE"]["port"])
    server.start()

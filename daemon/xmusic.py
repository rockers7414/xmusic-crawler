#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging

from activemq.worker import MQWorker
from database import db_init
from rpcservice.rpcserver import RPCServer
from scheduler import Scheduler

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")

    logging.basicConfig(
        filename=config["LOGGING"]["file"],
        level=config["LOGGING"]["level"],
        datefmt='%Y-%m-%d %H:%M:%S',
        format=("[%(asctime)s][%(levelname)s][%(threadName)s][%(name)s] - "
                "%(message)s")
    )

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            config["DATABASE"]["host"],
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    scheduler = Scheduler()
    scheduler.start()

    mq = MQWorker(config.get("ACTIVEMQ", "host"),
                  config.get("ACTIVEMQ", "port"),
                  config.get("ACTIVEMQ", "username"),
                  config.get("ACTIVEMQ", "password"),
                  config.get("ACTIVEMQ", "queue"),
                  config.getint("ACTIVEMQ", "numofworkers"))
    mq.start()

    server = RPCServer(config["RPCSERVICE"]["host"],
                       config["RPCSERVICE"]["port"])
    server.start()

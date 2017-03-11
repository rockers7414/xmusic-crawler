import configparser
import json
import types
import uuid
import psutil

from database import db_init
from database.artistrepo import ArtistRepo
from database.albumrepo import AlbumRepo
from database.trackrepo import TrackRepo

from database.entity import Artist

from rpcservice.rpcservice import RPCService
from rpcservice.dbservice import DBService
# from rpcservice.spotifyservice import SpotifyService
from rpcservice.systemservice import SystemService

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.cfg")

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            "localhost",
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    # result = ttt()
    # print("\n\n\n\n")1
    # print(result)

    # rpc = RPCService()
    # result = rpc.raw_sql("select * from artists")
    # print(result)

    # rpc = DBService()
    # result = rpc.get_artist("obama")
    # print(result)

    # print(RPCService().get_server_status())

    # print("\n\n\n")
    # artistrepo = ArtistRepo()
    # result = artistrepo.get_artist("obama")
    # print(result)

    # print("=======================")

    # aa = DBService().get_artist("obama")
    # print("\n\n\n")
    # print(aa)

    print(SystemService().get_server_status())


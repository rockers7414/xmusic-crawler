import configparser
import json
import types
import uuid
import psutil

from database import db_init
from database.artistrepo import ArtistRepo
from database.albumrepo import AlbumRepo
from database.sqlcommandrepo import SqlCommandRepo
from database.trackrepo import TrackRepo
from rpcservice.rpcserver import get_artists_list
from decorator.serialize import *
from database.entity import Artist

from rpcservice.artistservice import ArtistService
from rpcservice.albumservice import AlbumService


@serializeController("JSON")
def ttt():
    # artist = ArtistService()
    # result = artist.get_artists_list()
    # result = artist.get_artist("obama")

    # album = AlbumRepo()
    # result = album.get_album("obama_album")

    # track = TrackRepo()
    # result = track.get_track_by_name("obama song11")
    # sql = SqlCommandRepo()
    # result = sql.excute("SELECT * FROM tracks")

    return result

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.cfg")

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            "localhost",
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    # result = ttt()
    # print("\n\n\n\n")
    # print(result)
    # print(type(result))


    # must install psutil,  update dockerfile 
    for x in range(3):
        print(psutil.cpu_percent(interval = 1))

    print(psutil.virtual_memory().percent)

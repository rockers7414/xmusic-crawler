import configparser
import json
import types

from database import db_init
from database.artistrepo import ArtistRepo
from database.albumrepo import AlbumRepo
from rpcservice.rpcserver import get_artists_list
from decorator.serialize import *
from database.entity import Artist
from rpcservice.artistservice import ArtistService


def testController(type):
    def wrapped(function):
        def aa(aa):
            print(type)
            origin = function(aa)
            # print(SerializeType.JSON.value == type.upper())
            return "fdfs" + origin
        return aa
    return wrapped


@testController("JSON")
def tmp(aa):
    return "hello" + aa


@serializeController("JSON")
def ttt():
    # album = AlbumRepo()
    # result = album.get_albums_by_artist("obama")
    artist = ArtistRepo()
    result = artist.get_artist("obama")
    # result = artist.get_artists_list(1, 1)
    return result

if __name__ == '__main__':
    # print(tmp("AA"))
    # print("TEST")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            "localhost",
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    # album = AlbumRepo()
    # result = album.get_albums_by_artist("obama")

    # artist = ArtistRepo()
    # result = artist.get_artist("obama2")
    # result = artist.get_artists_list()

    # print("===================")
    # print(ttt())
    # print(result)

    # print([c.name for c in Artist.__table__.c])

    # for column in Artist.__table__.c:
    #     print(column.name)
    # data = DataService("a")
    data = ArtistService("db", "json")
    print(data.get_artist("obama"))
    # print(data.test())

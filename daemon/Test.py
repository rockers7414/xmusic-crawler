import configparser
import json
import types

from database import db_init
from database.artistrepo import ArtistRepo
from rpcservice.rpcserver import get_all_artists
from decorator.serialize import *


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
    result = ArtistRepo().get_all_artists(1, 1)
    return result

if __name__ == '__main__':
    # print(tmp("AA"))

    config = configparser.ConfigParser()
    config.read("config.cfg")

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            "localhost",
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    #TODO enum class (SerializeType) move to enumtype directory ? 


    # print(DataSourceType.DataBase.value)

    # get_all_artists(None)

    # print(ttt())

    # artists = ArtistRepo().get_all_artists(1, 1)
    # print(artists)

    # for artist in artists:
    #     for key, value in artist.__dict__.items():
    #         print(key, value)
    #         print(type(value))
    #         print(isinstance(value, list))
    #         if(isinstance(value, list)):
    #             for _column in value.__dict__.items():
    #                 print(_column, "fffffffffffffffff")

    #         print(artist.images)
    #         for image in artist.images:
    #             print(image.path)
    #     print()

import configparser
import json
import types

from database import db_init
from database.artistrepo import ArtistRepo
from database.albumrepo import AlbumRepo
from database.trackrepo import TrackRepo
from rpcservice.rpcserver import get_artists_list
from decorator.serialize import *
from database.entity import Artist

from rpcservice.artistservice import ArtistService
from rpcservice.albumservice import AlbumService


# @serializeController("JSON")
def ttt():
    # artist = ArtistRepo()
    # result = artist.get_artists_list()

    track = TrackRepo()
    result = track.get_track_by_name("obama song11")

    return result

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.cfg")

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            "localhost",
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    print(ttt())
    print("!")

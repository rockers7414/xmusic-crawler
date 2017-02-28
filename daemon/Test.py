import configparser

from database import db_init
from database.artistrepo import ArtistRepo

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read("config.cfg")

    db_init(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            config["DATABASE"]["host"],
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    artist = ArtistRepo()
    artists = artist.get_all_artists(1, 10)


    print(len(artists))

    for artist in artists:
        print(artist.name)
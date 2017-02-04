#!/usr/bin/env python

import os
import configparser
import logging

from database.connection import Connection
from database.artistrepo import ArtistRepo

from provider.musicvideoinfo.spotifyprovider import SpotifyProvider

if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    config.read("config.cfg")

    logging.basicConfig(
        filename = config["LOGGING"]["file"],
        level = config["LOGGING"]["level"],
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    db = Connection(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            config["DATABASE"]["host"],
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])

    artist_model = ArtistRepo(db.getSession())
    artists = artist_model.getArtistsByName("Ed Sheeran")
    logging.info(artists)

    # musicVideoInfoProvider = SpotifyProvider()
    # musicVideoInfoProvider.getArtistByName("Test")

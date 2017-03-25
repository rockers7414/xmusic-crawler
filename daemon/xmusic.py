#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database import db_init
from database.artistrepo import ArtistRepo
from database.providerrepo import ProviderRepo
from provider.musicvideoinfo.spotifyprovider import SpotifyProvider
from rpcservice.rpcserver import RPCServer
from config import Config
from activemq.worker import MQWorker
from scheduler import Scheduler

if __name__ == "__main__":

    config = Config("xmusic.cfg")
    db_init(config.db_username,
            config.db_password,
            config.db_host,
            config.db_port,
            config.db_database)

    """
    artist_repo = ArtistRepo()
    target = "Ed Sheeran"

    # Fetching the information of the artist name from data provider.
    musicVideoInfoProvider = SpotifyProvider()
    musicVideoInfoProvider.provider = ProviderRepo().get_provider("spotify")

    artists = musicVideoInfoProvider.get_artists_by_name(target)
    artist = artists[0]
    artist.albums = []

    albums = musicVideoInfoProvider \
        .get_albums_by_artist_id(artist.provider_res_id)
    for album in albums:
        tracks = musicVideoInfoProvider.get_tracks_by_album_id(
            album.provider_res_id)
        album.tracks = tracks
        artist.albums.append(album)

    logging.info("Fetching(" + target + ") done.")
    logging.debug(artist)

    # Insert the fetching result into xmusic-db.
    logging.info("Store the fetching result(" + target + ") into database.")
    artist_repo.save(artist)

    # Fetching the information of the artist name from xmusic-db.
    artists = artist_repo.get_artists_by_name(target)
    logging.info("Artist(" + target + ") information in the database.")
    logging.debug(artists)
    """

    scheduler = Scheduler()
    scheduler.start()

    mq = MQWorker(config.mq_host,
                  config.mq_port,
                  config.mq_username,
                  config.mq_password,
                  config.mq_queue,
                  config.mq_num_of_workers)
    mq.start()

    server = RPCServer(config.rpcserver_host, config.rpcserver_port)
    server.start()

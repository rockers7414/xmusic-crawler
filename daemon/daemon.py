#!/usr/bin/env python
import json
from objects.album import Album
from spotify_crawler import SpotifyCrawler

if __name__ == "__main__":
    crawler = SpotifyCrawler()
    
    artist_name = "Ed Sheeran"
    artist = crawler.searchArtist(artist_name)

    if artist:
        albums = crawler.getAlbumsByArtist(artist.getArtistId())

        for album in albums:
            tracks = crawler.getTracksByAlbum(album.getAlbumId())
            album.setTracks(tracks)

        artist.setAlbums(albums)
    
        print(artist.toJSON())
    else:
        print("Cannot find " + artist_name)

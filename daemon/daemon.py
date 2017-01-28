#!/usr/bin/env python
import json
from objects.album import Album
from spotify_crawler import SpotifyCrawler

if __name__ == "__main__":
    crawler = SpotifyCrawler()
    
    artist = crawler.searchArtist("Ed Sheeran")

    if artist:
        albums = crawler.getAlbumsByArtist(artist.getArtistId())

        for album in albums:
            tracks = crawler.getTracksByAlbum(album.getAlbumId())
            album.setTracks(tracks)

        artist.setAlbums(albums)
    
    print(artist.toJSON())

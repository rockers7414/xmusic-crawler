#!/usr/bin/env python
import json
import psycopg2
import traceback
from objects.album import Album
from spotify_crawler import SpotifyCrawler

if __name__ == "__main__":
    conn = psycopg2.connect(host = "xmusic-db", port = "5432", dbname = "xmusic", user = "admin", password="admin")
    cur = conn.cursor()

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
        
        try:
            # save artist
            cur.execute("INSERT INTO artists(name, popularity) VALUES(%s, %s) RETURNING artist_id", (artist.getName(), artist.getPopularity()))
            artistId = cur.fetchone()[0]

            # save images
            for image in artist.getImages():
                cur.execute("INSERT INTO images(width, height, path) VALUES(%s, %s, %s) RETURNING image_id", (image["width"], image["height"], image["url"]))
                imageId = cur.fetchone()[0]
                cur.execute("INSERT INTO artists_images(artist_id, image_id) VALUES(%s, %s)", (artistId, imageId))

            # save genres
            genreId = None
            for genre in artist.getGenres():
                cur.execute("SELECT * FROM genres WHERE name = %s", (genre,))
                if cur.rowcount > 0:
                    genreId = cur.fetchone()[0]
                else:
                    cur.execute("INSERT INTO genres(name) VALUES(%s) RETURNING genre_id", (genre,))
                    genreId = cur.fetchone()[0]
                cur.execute("INSERT INTO artists_genres(artist_id, genre_id) VALUES(%s, %s)", (artistId, genreId))

            # save albums of the artist
            for album in artist.getAlbums():
                cur.execute("INSERT INTO albums(artist_id, name, popularity) VALUES(%s, %s, %s) RETURNING album_id", (artistId, album.getName(), album.getPopularity()))
                albumId = cur.fetchone()[0]

                # save images of the album
                for image in album.getImages():
                    cur.execute("INSERT INTO images(width, height, path) VALUES(%s, %s, %s) RETURNING image_id", (image["width"], image["height"], image["url"]))
                    imageId = cur.fetchone()[0]
                    cur.execute("INSERT INTO albums_images(album_id, image_id) VALUES(%s, %s)", (albumId, imageId))

                # save genres of the album
                genreId = None
                for genre in album.getGenres():
                    cur.execute("SELECT * FROM genres WHERE name = %s", (genre,))
                    if cur.rowcount > 0:
                        genreId = cur.fetchone()[0]
                    else:
                        cur.execute("INSERT INTO genres(name) VALUES(%s) RETURNING genre_id")
                        genreId = cur.fetchone()[0]
                    cur.execute("INSERT INTO albums_genres(album_id, genre_id) VALUES(%s, %s)", (albumId, genreId))

                # save tracks of the album
                for track in album.getTracks():
                    cur.execute("INSERT INTO tracks(album_id, name, popularity, track_number) VALUES(%s, %s, %s, %s) RETURNING track_id", (albumId, track.getName(), track.getPopularity(), track.getTrackNumber()))
                    trackId = cur.fetchone()[0]

                    # save genres of the track
                    genreId = None
                    for genre in track.getGenres():
                        cur.execute("SELECT * FROM genres WHERE name = %s", (genre,))
                        if cur.rowcount > 0:
                            genreId = cur.fetchone()[0]
                        else:
                            cur.execute("INSERT INTO genres(name) VALUES(%s) RETURNING genre_id", (genre,))
                            genreId = cur.fetchone()[0]
                        cur.execute("INSERT INTO tracks_genres(track_id, genre_id) VALUES(%s, %s)", (trackId, genreId))

            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
    else:
        print("Cannot find " + artist_name)

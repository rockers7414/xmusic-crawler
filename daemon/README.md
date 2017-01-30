# Daemon

The purpose of daemon is used to query the artist, artist's album and the tracks of the album from the several data sources, such as [Spotify](https://www.spotify.com/). In addition, the daemon will also get the information of music video from the provider, such as [YouTube](http://www.youtube.com).

## Features

* Fetch the artist, artist's album and the tracks of the album from Spotify.

### TODO:

* Fetch the corresponding link of music video from YouTube.
* Store the data to the PostgreSQL.
* Prepare the unit test for the daemon's function.

## Prerequirements

* Python 3+
* [pycurl](http://pycurl.io/)
* [Psycopg](http://initd.org/psycopg/)

## Quick start

Note: Please make sure the docker container of `xmusic-db` is started. If the `xmusic-daemon` exist, you can execute below command directly.

```
$ docker start xmusic-daemon
```

Or you can change the path to `docker/`, then execute the below command.

```
$ docker-compose up -d xmusic-daemon
```

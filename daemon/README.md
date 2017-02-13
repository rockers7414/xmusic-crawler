# Daemon

The purpose of daemon is used to query the artist, artist's album and the tracks of the album from the several data sources, such as [Spotify](https://www.spotify.com/). In addition, the daemon will also get the information of music video from the provider, such as [YouTube](http://www.youtube.com).

## Features

* Fetch the artist, artist's album and the tracks of the album from Spotify.
* Store the above information to the database (PostgreSQL).

## Prerequirements

* Python 3+
* [pycurl](http://pycurl.io/)
* [Psycopg](http://initd.org/psycopg/)
* [PostgreSQL version 9.6.1](https://www.postgresql.org/download/)
* [isodate](https://pypi.python.org/pypi/isodate)
* [json-rpc](https://github.com/pavlov99/json-rpc)

## Quick start

Note: Please make sure the docker container of `xmusic-db` is started. If the `xmusic-daemon` exist, you can execute below command directly.

```
$ docker start xmusic-daemon
```

Or you can change the path to `docker/`, then execute the below command.

```
$ docker-compose up -d xmusic-daemon
```
Checking the detailed logs.

```
$ docker-compose logs xmusic-daemon
```

Or you can use `docker logs` simply.
Once you figure out the service cannot work normally, maybe you should re-build the docker image, cause we may updated the library or settings in the Dockerfile.

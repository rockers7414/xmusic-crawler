import datetime
import uuid

from decorator.unique import unique
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, UUID, VARCHAR, \
    TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()

artists_images = Table(
    "artists_images",
    Base.metadata,
    Column("artist_id", UUID, ForeignKey("artists.artist_id")),
    Column("image_id", UUID, ForeignKey("images.image_id"))
)

artists_genres = Table(
    "artists_genres",
    Base.metadata,
    Column("artist_id", UUID, ForeignKey("artists.artist_id")),
    Column("genre_id", UUID, ForeignKey("genres.genre_id"))
)

albums_images = Table(
    "albums_images",
    Base.metadata,
    Column("album_id", UUID, ForeignKey("albums.album_id")),
    Column("image_id", UUID, ForeignKey("images.image_id"))
)

albums_genres = Table(
    "albums_genres",
    Base.metadata,
    Column("album_id", UUID, ForeignKey("albums.album_id")),
    Column("genre_id", UUID, ForeignKey("genres.genre_id"))
)

tracks_genres = Table(
    "tracks_genres",
    Base.metadata,
    Column("track_id", UUID, ForeignKey("tracks.track_id")),
    Column("genre_id", UUID, ForeignKey("genres.genre_id"))
)


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    provider_id = Column(UUID, ForeignKey("providers.provider_id"))
    provider_res_id = Column(VARCHAR)

    provider = relationship(
        "Provider",
        backref=backref("artists", order_by=artist_id, lazy="joined")
    )
    images = relationship("Image", secondary=artists_images, lazy="joined")
    genres = relationship("Genre", secondary=artists_genres, lazy="joined")

    def __init__(self, name, popularity):
        self.artist_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity

    def __repr__(self):
        return ("Artist(name={0},popularity={1},genres={2},images={3},"
                "albums={4},provider={5},provider_res_id={6})").format(
                    self.name,
                    self.popularity,
                    self.genres,
                    self.images,
                    self.albums,
                    self.provider_id,
                    self.provider_res_id)


class Album(Base):
    __tablename__ = "albums"

    album_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    artist_id = Column(UUID, ForeignKey("artists.artist_id"))
    provider_id = Column(UUID, ForeignKey("providers.provider_id"))
    provider_res_id = Column(VARCHAR)

    artist = relationship(
        "Artist",
        backref=backref("albums", order_by=album_id, lazy="joined")
    )
    provider = relationship(
        "Provider",
        backref=backref("albums", order_by=album_id, lazy="joined")
    )
    images = relationship("Image", secondary=albums_images, lazy="joined")
    genres = relationship("Genre", secondary=albums_genres, lazy="joined")

    def __init__(self, name, popularity):
        self.album_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity

    def __repr__(self):
        return ("Album(name={0},populariy={1},genres={2},images={3},"
                "tracks={4},provider_id={5},provider_res_id={6})").format(
                    self.name,
                    self.popularity,
                    self.genres,
                    self.images,
                    self.tracks,
                    self.provider_id,
                    self.provider_res_id)


class Track(Base):
    __tablename__ = "tracks"

    track_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    track_number = Column(INTEGER)
    lyric = Column(TEXT)
    album_id = Column(UUID, ForeignKey("albums.album_id"))

    album = relationship(
        "Album",
        backref=backref("tracks", order_by=track_id, lazy="joined")
    )
    genres = relationship("Genre", secondary=tracks_genres, lazy="joined")

    def __init__(self, name, popularity, track_number):
        self.track_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity
        self.track_number = track_number

    def __repr__(self):
        return ("Track(name={0},popularity={1},track_number={2},genres={3},"
                "repositories={4})").format(
                    self.name,
                    self.popularity,
                    self.track_number,
                    self.genres,
                    self.repositories)


class Image(Base):
    __tablename__ = "images"

    image_id = Column(UUID, primary_key=True)
    width = Column(INTEGER)
    height = Column(INTEGER)
    path = Column(VARCHAR)

    def __init__(self, path, width, height):
        self.image_id = str(uuid.uuid4())
        self.width = width
        self.height = height
        self.path = path

    def __repr__(self):
        return "Image(path={0},width={1},height={1})".format(
            self.path, self.width, self.height)


@unique(
    lambda name: name,
    lambda query, name: query.filter(Genre.name == name)
)
class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR, unique=True)

    def __init__(self, name):
        self.genre_id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return "Genre(name={0})".format(self.name)


@unique(
    lambda name: name,
    lambda query, name: query.filter(Provider.name == name)
)
class Provider(Base):
    __tablename__ = "providers"

    provider_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR, unique=True)

    def __init__(self, name):
        self.provider_id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return "Provider(name={0})".format(self.name)


class Repository(Base):
    __tablename__ = "repository"

    track_id = Column(UUID, ForeignKey("tracks.track_id"), primary_key=True)
    provider_id = Column(
        UUID,
        ForeignKey("providers.provider_id"),
        primary_key=True
    )
    link = Column(VARCHAR)
    duration_second = Column(INTEGER)
    updated_time = Column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now)

    provider = relationship("Provider", backref=backref("repositories"))
    track = relationship(
        "Track",
        backref=backref("repositories", lazy="joined")
    )

    def __init__(self, link, duration_second):
        self.link = link
        self.duration_second = duration_second

    def __repr__(self):
        return ("Repository(link={0},duration_second={1},"
                "updated_time={2}").format(
                    self.link,
                    self.duration_second,
                    self.updated_time)

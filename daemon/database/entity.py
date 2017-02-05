import uuid
from .connection import *

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, INTEGER

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

class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(UUID, primary_key = True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    images = relationship("Image", secondary = artists_images)
    genres = relationship("Genre", secondary = artists_genres)

    def __init__(self, name, popularity):
        self.artist_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity

    def __repr__(self):
        return "Artist(name={0},popularity={1},genres={2},images={3},albums={4})".format(self.name, self.popularity, self.genres, self.images, self.albums)

class Album(Base):
    __tablename__ = "albums"

    album_id = Column(UUID, primary_key = True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    artist_id = Column(UUID, ForeignKey("artists.artist_id"))
    artist = relationship("Artist", backref = backref("albums", order_by = album_id))
    images = relationship("Image", secondary = albums_images)
    genres = relationship("Genre", secondary = albums_genres)

    def __init__(self, name, popularity):
        self.album_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity

    def __repr__(self):
        return "Album(name={0},populariy={1},genres={2},images={3},tracks={4})".format(self.name, self.popularity, self.genres, self.images, self.tracks)

class Track(Base):
    __tablename__ = "tracks"

    track_id = Column(UUID, primary_key = True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    track_number = Column(INTEGER)
    album_id = Column(UUID, ForeignKey("albums.album_id"))
    album = relationship("Album", backref = backref("tracks", order_by = track_id))

    def __init__(self, name, popularity, track_number):
        self.track_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity
        self.track_number = track_number

    def __repr__(self):
        return "Track(name={0},popularity={1},track_number={2})".format(self.name, self.popularity, self.track_number)

class Image(Base):
    __tablename__ = "images"

    image_id = Column(UUID, primary_key = True)
    width = Column(INTEGER)
    height = Column(INTEGER)
    path = Column(VARCHAR)

    def __init__(self, path, width, height):
        self.image_id = str(uuid.uuid4())
        self.width = width
        self.height = height
        self.path = path

    def __repr__(self):
        return "Image(path={0},width={1},height={1})".format(self.path, self.width, self.height)

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(UUID, primary_key = True)
    name = Column(VARCHAR)

    def __init__(self, name):
        self.genre_id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return "Genre(name={0})".format(self.name)

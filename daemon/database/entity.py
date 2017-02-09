import uuid

from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, UUID, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

from decorator import Unique

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

    images = relationship("Image", secondary=artists_images, lazy='joined')
    genres = relationship("Genre", secondary=artists_genres, lazy='joined')

    def __init__(self, name, popularity):
        self.artist_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity

    def __repr__(self):
        return "Artist(name={0},popularity={1},genres={2},images={3},albums={4})".format(
            self.name, self.popularity, self.genres, self.images, self.albums)


class Album(Base):
    __tablename__ = "albums"

    album_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    artist_id = Column(UUID, ForeignKey("artists.artist_id"))

    artist = relationship(
        "Artist",
        backref=backref("albums", order_by=album_id, lazy='joined')
    )
    images = relationship("Image", secondary=albums_images, lazy='joined')
    genres = relationship("Genre", secondary=albums_genres, lazy='joined')

    def __init__(self, name, popularity):
        self.album_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity

    def __repr__(self):
        return "Album(name={0},populariy={1},genres={2},images={3},tracks={4})".format(
            self.name, self.popularity, self.genres, self.images, self.tracks)


class Track(Base):
    __tablename__ = "tracks"

    track_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)
    track_number = Column(INTEGER)
    album_id = Column(UUID, ForeignKey("albums.album_id"))

    album = relationship(
        "Album",
        backref=backref("tracks", order_by=track_id, lazy='joined')
    )
    genres = relationship("Genre", secondary=tracks_genres, lazy='joined')

    def __init__(self, name, popularity, track_number):
        self.track_id = str(uuid.uuid4())
        self.name = name
        self.popularity = popularity
        self.track_number = track_number

    def __repr__(self):
        return "Track(name={0},popularity={1},track_number={2},genres={3})".format(
            self.name, self.popularity, self.track_number, self.genres)


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

@Unique(
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


class Datasource(Base):
    __tablename__ = 'datasource'

    source_id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)

    def __init__(self, name):
        self.source_id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return 'Datasource(name={})'.format(self.name)


class Repository(Base):
    __tablename__ = 'repository'
    __table_args__ = (
        PrimaryKeyConstraint('track_id', 'source_id'),
    )

    track_id = Column(UUID, ForeignKey('tracks.track_id'))
    source_id = Column(UUID, ForeignKey('datasource.source_id'))
    link = Column(VARCHAR)
    duration_second = Column(INTEGER)
    updated_time = Column(TIMESTAMP)

    def __init__(self, source_id, link, duration_second):
        self.source_id = source_id
        self.link = link
        self.duration_second = duration_second

    def __repr__(self):
        return 'Repository(link={}, duration_second={}, updated_time={}'.format(
            self.link, self.duration_second, self.updated_time)

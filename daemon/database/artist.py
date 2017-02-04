from .connection import *

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, INTEGER

class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(UUID, primary_key = True)
    name = Column(VARCHAR)
    popularity = Column(INTEGER)

    def __init__(self, name, popularity):
        self.name = name
        self.popularity = popularity

    def __repr__(self):
        return "Artist(name={0},popularity={1})".format(self.name, self.popularity)

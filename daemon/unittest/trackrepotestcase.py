import unittest
import sys
sys.path.append('../')

from database import db_init
from database.trackrepo import TrackRepo
from database.providerrepo import ProviderRepo
from database.albumrepo import AlbumRepo
from database.artistrepo import ArtistRepo
from database.entity import Track, Artist, Album
from config import Config


class TrackRepoTestCase(unittest.TestCase):

    def setUp(self):

        config = Config("../xmusic.cfg")
        db_init(config.db_username,
                config.db_password,
                "localhost",
                config.db_port,
                config.db_database)

        # repo
        self.repo = TrackRepo()
        self.provider_repo = ProviderRepo()
        self.album_repo = AlbumRepo()
        self.artist_repo = ArtistRepo()

        self.provider = ProviderRepo().get_provider("youtube")

        # test data
        self.artist = Artist("obama II", 123)
        self.artist.provider = self.provider
        self.artist.provider_res_id = "res_id"

        self.album = Album("Feel Good", 10000)
        self.album.provider = self.provider
        self.album.provider_res_id = "res_id"
        self.album.artist_id = self.artist.artist_id

        self.data_list = []
        track = Track("haha song", 100, 1)
        track.album_id = self.album.album_id
        self.data_list.append(track)

        track2 = Track("One more time", 11, 2)
        track2.album_id = self.album.album_id
        self.data_list.append(track2)

        try:
            self.artist = self.artist_repo.save(self.artist)
            self.album = self.album_repo.save(self.album)
            for data in self.data_list:
                data = self.repo.save(data)
        except:
            self.fail()

    def tearDown(self):
        try:
            for data in self.data_list:
                self.repo.delete(data)
            self.album_repo.delete(self.album)
            self.artist = self.artist_repo.delete(self.artist)
        except:
            self.fail()

    def test_get_track_by_name(self):
        for data in self.data_list:
            track_name = data.name
            result = self.repo.get_track_by_name(track_name)
            self.assertIn(data, result)

if __name__ == "__main__":
    unittest.main(verbosity=2)

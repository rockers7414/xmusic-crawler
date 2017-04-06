import unittest
import sys
sys.path.append('../')

from database import db_init
from database.artistrepo import ArtistRepo
from database.providerrepo import ProviderRepo
from database.entity import Artist
from config import Config


class AritstRepoTestCase(unittest.TestCase):

    def setUp(self):

        config = Config("../xmusic.cfg")
        db_init(config.db_username,
                config.db_password,
                "localhost",
                config.db_port,
                config.db_database)

        # repo
        self.repo = ArtistRepo()
        self.provider_repo = ProviderRepo()

        self.provider = ProviderRepo().get_provider("youtube")[0]

        # test data
        self.data_list = []
        artist = Artist("obama II", 123)
        artist.provider = self.provider
        artist.provider_res_id = "res_id"
        self.data_list.append(artist)

        artist2 = Artist("kid kim", -1)
        artist2.provider = self.provider
        artist2.provider_res_id = "res_id2"
        self.data_list.append(artist2)

        artist3 = Artist("english tsai", 1)
        artist3.provider = self.provider
        artist3.provider_res_id = "res_id3"
        self.data_list.append(artist3)

        try:
            for data in self.data_list:
                data = self.repo.save(data)
        except:
            self.fail()

    def tearDown(self):
        try:
            for data in self.data_list:
                self.repo.delete(data)
        except:
            self.fail()

    def test_get_artists_by_page(self):
        index = 1
        offset = 5
        result = self.repo.get_artists_by_page(index, offset)
        for row in result:
            with self.subTest(row=row):
                self.assertIn(row, self.data_list)

    def test_get_artists_list(self):
        result = self.repo.get_artists_list()

        for data in self.data_list:
            with self.subTest(data=data):
                self.assertIn(data, result)

    def test_get_artist_by_name(self):

        for data in self.data_list:
            artist_name = data.name
            with self.subTest(data=data):
                result = self.repo.get_artists_by_name(artist_name)
                self.assertIn(data, result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

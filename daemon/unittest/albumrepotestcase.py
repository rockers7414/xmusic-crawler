import unittest
import configparser

import sys
sys.path.append('../')
from database import db_init
from database.albumrepo import AlbumRepo
from database.providerrepo import ProviderRepo
from database.artistrepo import ArtistRepo
from database.entity import Album, Artist


class AlbumRepoTestCase(unittest.TestCase):

    def setUp(self):

        config = configparser.ConfigParser()
        config.read("../config.cfg")

        db_init(config["DATABASE"]["username"],
                config["DATABASE"]["password"],
                "localhost",
                config["DATABASE"]["port"],
                config["DATABASE"]["database"])

        # repo
        self.repo = AlbumRepo()
        self.provider_repo = ProviderRepo()
        self.artist_repo = ArtistRepo()

        self.provider = ProviderRepo().get_provider("youtube")

        # test data
        self.artist = Artist("obama II", 123)
        self.artist.provider = self.provider
        self.artist.provider_res_id = "res_id"

        self.data_list = []

        album = Album("Feel Good", 10000)
        album.provider = self.provider
        album.provider_res_id = "res_id"
        album.artist_id = self.artist.artist_id
        self.data_list.append(album)

        album2 = Album("中文測試", -1)
        album2.provider = self.provider
        album2.provider_res_id = "res_id2"
        album2.artist_id = self.artist.artist_id
        self.data_list.append(album2)

        album3 = Album("Rockabye", 223)
        album3.provider = self.provider
        album3.provider_res_id = "res_id3"
        album3.artist_id = self.artist.artist_id
        self.data_list.append(album3)

        try:
            self.artist = self.artist_repo.save(self.artist)
            for data in self.data_list:
                data = self.repo.save(data)
        except:
            self.fail()

    def tearDown(self):
        try:
            for data in self.data_list:
                self.repo.delete(data)
            self.artist_repo.delete(self.artist)
        except:
            self.fail()

    def test_get_album_by_name(self):
        for data in self.data_list:
            with self.subTest(data = data):
                album_name = data.name
                result = self.repo.get_album_by_name(album_name)
                self.assertIn(data, result)

if __name__ == "__main__":
    unittest.main(verbosity=2)

import unittest
import configparser

import sys
sys.path.append('../')
from database import db_init
from database.albumrepo import AlbumRepo
from database.entity import Album


class AlbumRepoTestCase(unittest.TestCase):

    def setUp(self):

        config = configparser.ConfigParser()
        config.read("../config.cfg")

        db_init(config["DATABASE"]["username"],
                config["DATABASE"]["password"],
                "localhost",
                config["DATABASE"]["port"],
                config["DATABASE"]["database"])

        # test data
        self.data_list = []
        self.data_list.append(Album("Feel Good", 10000))
        self.data_list.append(Album("Rockabye", -1))
        self.data_list.append(Album("Starboy", 234))
        self.data_list.append(Album("2K17", 11111))
        self.data_list.append(Album("DREAM", 99999))

        # repo
        self.repo = AlbumRepo()

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

    def test_get_album(self):
        for data in self.data_list:
            album_name = data.name
            result = self.repo.get_album(album_name)
            self.assertIn(data, result)

if __name__ == "__main__":
    unittest.main(verbosity=2)

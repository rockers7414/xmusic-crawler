import unittest
import configparser

import sys
sys.path.append('../')
from database import db_init
from database.artistrepo import ArtistRepo
from database.entity import Artist


class AritstRepoTestCase(unittest.TestCase):

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
        self.data_list.append(Artist("obama II", 123))
        self.data_list.append(Artist("kid kim", -1))
        self.data_list.append(Artist("english tsai", 1))
        self.data_list.append(Artist("horse nine", 223))
        self.data_list.append(Artist("big gg", 222))
        self.data_list.append(Artist("iiii", 0))

        # repo
        self.repo = ArtistRepo()

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
            self.assertIn(row, self.data_list)

    def test_get_artists_list(self):
        result = self.repo.get_artists_list()

        for data in self.data_list:
            self.assertIn(data, result)

    def test_get_artist_by_name(self):

        for data in self.data_list:
            artist_name = data.name
            result = self.repo.get_artist_by_name(artist_name)
            self.assertIn(data, result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

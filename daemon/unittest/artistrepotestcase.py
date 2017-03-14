import unittest
import configparser

import sys
sys.path.append('../')
from database import db_init
from database.artistrepo import ArtistRepo
from database.entity import Artist
from database import Session


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
        self.data_list.append(Artist("obama", 123))
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

    def test(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

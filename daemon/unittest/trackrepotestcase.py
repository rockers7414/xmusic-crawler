import unittest
import configparser

import sys
sys.path.append('../')
from database import db_init
from database.trackrepo import TrackRepo
from database.entity import Track


class TrackRepoTestCase(unittest.TestCase):

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
        self.data_list.append(Track("haha song", 100, 1))
        self.data_list.append(Track("One more time", 11, 2))
        self.data_list.append(Track("Heart of Courage", 111, 3))
        self.data_list.append(Track("All of my light", 22, 4))
        self.data_list.append(Track("Empire of Angels", 100, 5))

        # repo
        self.repo = TrackRepo()

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

    def test_get_track_by_name(self):
        for data in self.data_list:
            track_name = data.name
            result = self.repo.get_track_by_name(track_name)
            self.assertIn(data, result)

if __name__ == "__main__":
    unittest.main(verbosity=2)

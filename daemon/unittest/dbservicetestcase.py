import unittest
import configparser
import uuid
import sys
sys.path.append('../')
from database import db_init
from config import Config
from rpcservice.dbservice import DBService


class DBServiceTestCase(unittest.TestCase):

    def setUp(self):
        config = Config("../xmusic.cfg")
        db_init(config.db_username,
                config.db_password,
                "localhost",
                config.db_port,
                config.db_database)

        # raw_sql test case
        self.image_id = uuid.uuid4()
        self.image_width = 90
        self.image_height = 180
        self.image_path = "C:/xmusic/images"

    def test_raw_sql(self):
        insert_sql = "INSERT INTO images(image_id, width, height, path) VALUES('{0}', {1}, {2}, '{3}')".format(
            self.image_id, self.image_width, self.image_height, self.image_path)
        # insert
        DBService().raw_sql(insert_sql)

        # select
        select_sql = "SELECT * FROM images WHERE image_id = '{0}' AND width = {1} AND height = {2} AND path = '{3}'".format(
            self.image_id, self.image_width, self.image_height, self.image_path)
        select_data = DBService().raw_sql(select_sql)
        # test case 1
        self.assertEqual(len(select_data), 1)
        self.assertEqual(select_data[0].get("image_id"), str(self.image_id))
        self.assertEqual(int(select_data[0].get("width")), self.image_width)
        self.assertEqual(int(select_data[0].get("height")), self.image_height)
        self.assertEqual(select_data[0].get("path"), self.image_path)

        # update
        self.image_width = 10
        self.image_height = 20
        update_sql = "UPDATE images SET width = {0}, height = {1} WHERE image_id = '{2}'".format(
            self.image_width, self.image_height, self.image_id)
        DBService().raw_sql(update_sql)

        # select
        select_sql = "SELECT * FROM images WHERE image_id = '{0}' AND width = {1} AND height = {2} AND path = '{3}'".format(
            self.image_id, self.image_width, self.image_height, self.image_path)
        select_data = DBService().raw_sql(select_sql)

        # test case 2
        self.assertEqual(len(select_data), 1)
        self.assertEqual(select_data[0].get("image_id"), str(self.image_id))
        self.assertEqual(int(select_data[0].get("width")), self.image_width)
        self.assertEqual(int(select_data[0].get("height")), self.image_height)
        self.assertEqual(select_data[0].get("path"), self.image_path)

        # delete
        # because serilze has been revise, so it neet to test other service.. dbservice.get_tracks etc...

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)
    # _uuid = uuid.uuid4()
    # print(_uuid)

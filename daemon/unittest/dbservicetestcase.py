import unittest
import configparser
import uuid
import sys
sys.path.append('../')
from database import db_init
from database.artistrepo import ArtistRepo
from database.albumrepo import AlbumRepo
from database.trackrepo import TrackRepo
from database.providerrepo import ProviderRepo
from database.entity import Artist, Album, Track

from config import Config
from rpcservice.dbservice import DBService


class DBServiceTestCase(unittest.TestCase):

    def setUp(self):
        try:
            config = Config("../xmusic.cfg")
            db_init(config.db_username,
                    config.db_password,
                    "localhost",
                    config.db_port,
                    config.db_database)

            self.provider = ProviderRepo().get_provider("youtube")[0]

        except:
            self.fail()

    def test_get_albums(self):
        try:
            # artists test data
            artist = Artist("obama II", 123)
            artist.provider = self.provider
            artist.provider_res_id = "res_id_1"
            artist = ArtistRepo().save(artist)
            # album test data
            album = Album("Feel Good", 10000)
            album.provider = self.provider
            album.provider_res_id = "res_id"
            album.artist_id = artist.artist_id
            album = AlbumRepo().save(album)

            # test case 1
            results = DBService().get_albums_by_name("Feel Good")
            is_contain = False
            for result in results:
                if result.get("name") == "Feel Good" and int(result.get("popularity")) == 10000 and result.get("artist_id") == artist.artist_id:
                    is_contain = True
            self.assertEqual(is_contain, True)

            # clean data
            AlbumRepo().delete(album)
            ArtistRepo().delete(artist)
        except:
            self.fail()

    def test_get_tracks(self):
        try:
             # artists test data
            artist = Artist("obama II", 123)
            artist.provider = self.provider
            artist.provider_res_id = "res_id_1"
            artist = ArtistRepo().save(artist)
            # album test data
            album = Album("Feel Good", 10000)
            album.provider = self.provider
            album.provider_res_id = "res_id"
            album.artist_id = artist.artist_id
            album = AlbumRepo().save(album)
            # track test data
            track = Track("happy", 1999, 1)
            track.album_id = album.album_id
            track = TrackRepo().save(track)

            # test case 1
            results = DBService().get_tracks("happy")
            is_contain = False
            for result in results:
                if result.get("name") == "happy" and int(result.get("popularity")) == 1999 and int(result.get("track_number")) == 1:
                    is_contain = True
            self.assertEqual(is_contain, True)

            # clean data
            TrackRepo().delete(track)
            AlbumRepo().delete(album)
            ArtistRepo().delete(artist)
        except:
            self.fail()

        pass

    def test_get_artists(self):
        try:
            # artists test data
            artist = Artist("obama II", 123)
            artist.provider = self.provider
            artist.provider_res_id = "res_id_1"
            artist = ArtistRepo().save(artist)

            # test case 1
            results = DBService().get_artists()
            is_contain = False
            for result in results:
                if result.get("name") == "obama II" and int(result.get("popularity")) == 123:
                    is_contain = True

            self.assertEqual(is_contain, True)

            # test case 2
            results = DBService().get_artists_by_name("obama II")
            is_contain = False
            for result in results:
                if result.get("name") == "obama II" and int(result.get("popularity")) == 123:
                    is_contain = True

            self.assertEqual(is_contain, True)

            # clean data
            ArtistRepo().delete(artist)
        except:
            self.fail()

    def test_raw_sql(self):
        try:
            # raw_sql test case
            self.image_id = uuid.uuid4()
            self.image_width = 90
            self.image_height = 180
            self.image_path = "C:/xmusic/images"

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
            self.assertEqual(select_data[0].get(
                "image_id"), str(self.image_id))
            self.assertEqual(
                int(select_data[0].get("width")), self.image_width)
            self.assertEqual(
                int(select_data[0].get("height")), self.image_height)
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
            self.assertEqual(select_data[0].get(
                "image_id"), str(self.image_id))
            self.assertEqual(
                int(select_data[0].get("width")), self.image_width)
            self.assertEqual(
                int(select_data[0].get("height")), self.image_height)
            self.assertEqual(select_data[0].get("path"), self.image_path)

            # delete
            delete_sql = "DELETE FROM images WHERE image_id = '{0}' AND width = {1} AND height = {2} AND path = '{3}'".format(
                self.image_id, self.image_width, self.image_height, self.image_path)
            DBService().raw_sql(delete_sql)

            # select
            select_sql = "SELECT * FROM images WHERE image_id = '{0}' AND width = {1} AND height = {2} AND path = '{3}'".format(
                self.image_id, self.image_width, self.image_height, self.image_path)
            select_data = DBService().raw_sql(select_sql)

            # test case 3
            self.assertEqual(len(select_data), 0)
        except:
            self.fail()

    def tearDown(self):
        try:
            pass
        except:
            self.fail()

if __name__ == "__main__":
    unittest.main(verbosity=2)

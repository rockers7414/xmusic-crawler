

class RPCService:

    def get_artists(self, index, offset):
        raise NotImplementedError

    def get_artists_by_name(self, artist_name):
        raise NotImplementedError

    def get_albums_by_name(self, album_name):
        raise NotImplementedError

    def get_tracks(self, track_name):
        raise NotImplementedError

    def raw_sql(self, sql):
        raise NotImplementedError

    def message_q(self):
        raise NotImplementedError

    def get_server_version(self):
        raise NotImplementedError

    def get_server_status(self):
        raise NotImplementedError

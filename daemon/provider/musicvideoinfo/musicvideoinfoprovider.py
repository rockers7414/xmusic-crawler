
class MusicVideoInfoProvider:
    def get_artists_by_name(artist_name):
        raise NotImplementedError("get_artists_by_name is not implemented.")

    def get_artists_by_artist_id(artist_id):
        raise NotImplementedError("get_artists_by_artist_id is not \
                                  implemented.")

    def get_albmus_by_name(album_name):
        raise NotImplementedError("get_albums_by_name is not implemented.")

    def get_albums_by_artist_id(artist_id):
        raise NotImplementedError("get_albums_by_artist_id is not \
                                  implemented.")

    def get_tracks_by_album_id(album_id):
        raise NotImplementedError("get_tracks_by_album_id is not implemented.")

    def get_tracks_by_name(track_name):
        raise NotImplementedError("get_tracks_by_name is not implemented.")

    def get_new_release_albums():
        raise NotImplementedError("get_new_release_album is not implemented.")


class MusicVideoInfoProvider:
    def getArtistsByName(artist_name):
        raise NotImplementedError('getArtistsByName is not implemented')

    def getArtistByArtistId(artist_id):
        raise NotImplementedError('getArtistByArtistId is not implemented')

    def getAlbumsByArtistId(artist_id):
        raise NotImplementedError('getAlbumsByArtistId is not implemented')

    def getTracksByAlbumId(album_id):
        raise NotImplementedError('getTracksByAlbumId is not implemented')

	def getNewRelease(offset_count,limit):
        raise NotImplementedError('getNewRelease is not implemented')

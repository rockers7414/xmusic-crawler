import sys

from decorator.datasource import datasource
from provider.musicvideo.youtubeprovider import YoutubeProvider


@datasource('youtube')
class YoutubeDatasource(object):

    def __init__(self):
        self._youtubeProvider = YoutubeProvider()

    def _process(self, datasource, tracks):
        for track in tracks[:1]:
            try:
                repo = self._youtubeProvider.getMusicVideo(
                    track.album.artist.name, track.album.name, track.name)
                repo.track = track
                datasource.repositories.append(repo)
            except:
                e = sys.exc_info()[1]
                self.logger.error(e)

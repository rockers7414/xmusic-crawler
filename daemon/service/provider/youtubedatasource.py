import sys
import logging

from decorator.provider import provider
from provider.musicvideo.youtubeprovider import YoutubeProvider


@provider('youtube')
class YoutubeProviderService(object):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._youtubeProvider = YoutubeProvider()

    def _process(self, provider, tracks):
        for track in tracks:
            try:
                self.logger.info(
                    'fetching artist=%s, album=%s, track=%s',
                    track.album.artist.name, track.album.name, track.name)

                repo = self._youtubeProvider.getMusicVideo(
                    track.album.artist.name, track.album.name, track.name)

                self.logger.info('done. repo=%s', repo)

                # set relationship
                repo.track = track
                provider.repositories.append(repo)
            except:
                e = sys.exc_info()[1]
                self.logger.error(e)

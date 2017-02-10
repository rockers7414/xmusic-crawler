from .youtubedatasource import YoutubeDatasource

class Datasource(object):
    def __init__(self):
        self.__datasources = [
            YoutubeDatasource()
        ]

    def fetch(self):
        for datasource in self.__datasources:
            datasource.fetch()

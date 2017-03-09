import json
import logging
import threading
import socketserver
import psutil

from socketserver import TCPServer, BaseRequestHandler
from jsonrpc import JSONRPCResponseManager, dispatcher
from decorator.serialize import serializeController
from enumtype.datasourcetype import DataSourceType
from enumtype.serializetype import SerializeType
from rpcservice.artistservice import ArtistService
from rpcservice.albumservice import AlbumService
from rpcservice.trackservice import TrackService
from database.sqlcommandrepo import SqlCommandRepo


@dispatcher.add_method
def echo(data):
    return data


@dispatcher.add_method
def get_artists_list(index=None, offset=None, source=DataSourceType.DataBase.value):

    artist_repo = ArtistService(source)
    result = artist_repo.get_artists_list(index, offset)
    return result


@dispatcher.add_method
def get_artist(artist_name, source=DataSourceType.DataBase.value):

    artist_repo = ArtistService(source)
    result = artist_repo.get_artist(artist_name)
    return result


@dispatcher.add_method
def get_album(album_name, source=DataSourceType.DataBase.value):

    album_repo = AlbumService(source)
    result = album_repo.get_album(album_name)
    return result


@dispatcher.add_method
def get_track_by_name(track_name, source=DataSourceType.DataBase.value):

    track_repo = TrackService(source)
    result = track_repo.get_track_by_name(track_name)
    return result


@dispatcher.add_method
def raw_sql(sql):

    @serializeController(SerializeType.JSON.value)
    def execute_sql():
        sql_repo = SqlCommandRepo()
        result = sql_repo.execute(sql)
        return result

    return execute_sql()


@dispatcher.add_method
def get_server_version():
    pass


@dispatcher.add_method
def get_server_status():
    cpu_status = {
        "cpu" : psutil.cpu_percent(),
        "memory" : psutil.virtual_memory().percent
    }

    return cpu_status

class RPCHandler(socketserver.StreamRequestHandler):
    logger = logging.getLogger(__name__)

    def handle(self):
        self.logger.info("Handler thread name = {}/active count = {}".format(
            threading.current_thread().name, threading.active_count()))
        self.data = self.rfile.readline().strip()
        self.logger.info("{0} request = {1}".format(
            self.client_address[0], self.data))
        response = JSONRPCResponseManager.handle(self.data, dispatcher)
        self.logger.info("response for {0} = {1}".format(
            self.client_address[0], response.json))
        self.wfile.write(bytes(response.json, "utf-8"))


class RPCServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    logger = logging.getLogger(__name__)

    def __init__(self, host, port):
        super().__init__((host, int(port)), RPCHandler)

    def start(self):
        self.logger.info("RPCServer is starting.")
        self.serve_forever()

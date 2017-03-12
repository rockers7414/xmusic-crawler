import json
import logging
import threading
import socketserver
import psutil

from socketserver import TCPServer, BaseRequestHandler
from jsonrpc import JSONRPCResponseManager, dispatcher

from enumtype.datasourcetype import DataSourceType

from .dbservice import DBService
from .spotifyservice import SpotifyService
from .systemservice import SystemService


def service_factory(source):
    source = source.upper()
    if(source == DataSourceType.DataBase.value):
        return DBService()
    elif(source == DataSourceType.Spotify.value):
        return SpotifyService()
    elif(source == DataSourceType.System.value):
        return SystemService()
    else
        return None


@dispatcher.add_method
def echo(data):
    return data


@dispatcher.add_method
def get_artists(index=None, offset=None, source=DataSourceType.DataBase.value):
    service = service_factory(source)
    result = service.get_artists(index, offset)
    return result


@dispatcher.add_method
def get_artist(artist_name, source=DataSourceType.DataBase.value):
    service = service_factory(source)
    result = service.get_artist(artist_name)
    return result


@dispatcher.add_method
def get_album(album_name, source=DataSourceType.DataBase.value):
    service = service_factory(source)
    result = service.get_album(album_name)
    return result


@dispatcher.add_method
def get_track(track_name, source=DataSourceType.DataBase.value):
    service = service_factory(source)
    result = service.get_track(track_name)
    return result


@dispatcher.add_method
def raw_sql(sql):
    service = service_factory(DataSourceType.DataBase.value)
    result = service.raw_sql(sql)
    return result


@dispatcher.add_method
def get_server_version():
    service = service_factory(DataSourceType.System.value)
    result = service.get_server_version()
    return result


@dispatcher.add_method
def get_server_status():
    service = service_factory(DataSourceType.System.value)
    result = service.get_server_status()
    return result


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

import json
import logging

from socketserver import TCPServer, BaseRequestHandler
from jsonrpc import JSONRPCResponseManager, dispatcher
from decorator.serialize import serializeController
from database.artistrepo import ArtistRepo
from enumtype.datasourcetype import DataSourceType
from rpcservice.artistservice import ArtistService


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


class RPCHandler(BaseRequestHandler):
    logger = logging.getLogger(__name__)

    # TODO: should define the message header to prevent the data is not
    # complete.
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.logger.info("{0} request = {1}".format(
            self.client_address[0], self.data))
        response = JSONRPCResponseManager.handle(self.data, dispatcher)
        self.logger.info("response for {0} = {1}".format(
            self.client_address[0], response.json))
        self.request.sendall(bytes(response.json, "utf-8"))


class RPCServer:
    logger = logging.getLogger(__name__)

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def start(self):
        self.logger.info("RPCServer is starting.")

        server_addr = (self.host, self.port)
        with TCPServer(server_addr, RPCHandler) as server:
            server.serve_forever()

import json
import logging

from socketserver import TCPServer, BaseRequestHandler
from jsonrpc import JSONRPCResponseManager, dispatcher
from decorator.serialize import serializeController
from database.artistrepo import ArtistRepo
from enumtype.datasourcetype import DataSourceType


@dispatcher.add_method
def echo(data):
    return data


@dispatcher.add_method
def get_all_artists(index, offset, source):

    @serializeController("JSON")
    def fromDB():
        return ArtistRepo().get_all_artists(index, offset)

    @serializeController("JSON")
    def fromSpotify():
        pass

    if (source.upper() == DataSourceType.DataBase.value):
        return fromDB()
    elif (source.upper() == DataSourceType.Spotify.value):
        return fromSpotify()


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

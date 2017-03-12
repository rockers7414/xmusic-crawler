import logging
import threading
import socketserver

from struct import pack, unpack
from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def echo(data):
    return data


class MessageHeader(object):

    HEADER_LENGTH = 4
    HEADER_SEPERATOR = 29

    def __init__(self, data):
        self.data_length = unpack("=BHB", data[:self.HEADER_LENGTH])[1]

    @property
    def length(self):
        return self.data_length

    @staticmethod
    def create(data_length):
        return pack("=BHB",
                    MessageHeader.HEADER_SEPERATOR,
                    data_length,
                    MessageHeader.HEADER_SEPERATOR)


class RPCHandler(socketserver.StreamRequestHandler):
    logger = logging.getLogger(__name__)

    MAX_BUF_LENGTH = 1024

    def handle(self):
        self.logger.info("Handler thread name = {}/active count = {}"
                         .format(threading.current_thread().name,
                                 threading.active_count()))
        header = MessageHeader(self.rfile.read(MessageHeader.HEADER_LENGTH))
        self.logger.info("Message length = {}".format(header.length))
        self.data = ""
        while len(self.data) < header.length:
            buf = self.rfile.read(
                min(self.MAX_BUF_LENGTH, header.length - len(self.data)))
            if not buf:
                return None
            self.data += str(buf, "UTF-8")
            self.logger.info("current length = {}, total length = {}"
                             .format(len(self.data),
                                     header.length))

        self.logger.info("{0} request = {1}"
                         .format(self.client_address[0],
                                 self.data))
        response = JSONRPCResponseManager.handle(self.data, dispatcher)
        self.logger.info("response for {0} = {1}"
                         .format(self.client_address[0],
                                 response.json))
        self.wfile.write(MessageHeader.create(
            len(response.json)) + bytes(response.json, "UTF-8"))


class RPCServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    logger = logging.getLogger(__name__)

    def __init__(self, host, port):
        super().__init__((host, int(port)), RPCHandler)

    def start(self):
        self.logger.info("RPCServer is starting.")
        self.serve_forever()

import logging
import threading
import socketserver

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def echo(data):
    return data


class RPCHandler(socketserver.StreamRequestHandler):
    logger = logging.getLogger(__name__)

    def handle(self):
        self.logger.info(("Handler thread name = {0}/active count = {1}")
                         .format(threading.current_thread().name,
                                 threading.active_count()))
        self.data = self.rfile.readline().strip()
        self.logger.info("{0} request = {1}"
                         .format(self.client_address[0], self.data))
        response = JSONRPCResponseManager.handle(self.data, dispatcher)
        self.logger.info("response for {0} = {1}"
                         .format(self.client_address[0], response.json))
        self.wfile.write(bytes(response.json, "utf-8"))


class RPCServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    logger = logging.getLogger(__name__)

    def __init__(self, host, port):
        super().__init__((host, int(port)), RPCHandler)

    def start(self):
        self.logger.info("RPCServer is starting.")
        self.serve_forever()

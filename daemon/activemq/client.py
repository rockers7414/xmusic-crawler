import logging
import time
import uuid

from service.artist import Artist
from service.datasource import Datasource
from stomp import Connection, ConnectionListener


class MQClient(object):
    """docstring for MQClient"""

    logger = logging.getLogger(__name__)

    def __init__(self, host, port, username, password):
        super(MQClient, self).__init__()
        self.connections = {}

        for i in range(3):
            conn = Connection([(host, port)])
            conn.set_listener('', MessageListener(conn))
            conn.start()
            conn.connect(username, password, wait=True)
            self.connections[uuid.uuid4()] = conn

    def start(self):
        for i, conn in self.connections.items():
            conn.subscribe('/queue/artist', id=i, ack='client')

    def stop(self):
        for i, conn in self.connections.items():
            conn.disconnect()
            conn.stop()


class MessageListener(ConnectionListener):
    logger = logging.getLogger(__name__)

    def __init__(self, conn):
        self.conn = conn

    def on_connected(self, headers, body):
        self.logger.info('connected')

    def on_error(self, headers, message):
        self.logger.error('received an error {}'.format(message))

    def on_message(self, headers, message):
        try:
            self.logger.info('received a message {}'.format(message))
            Artist.fetch(message)
            Datasource.fetch()
            self.conn.ack(headers['message-id'], headers['subscription'])
        except Exception as e:
            self.logger.error(e)
            self.conn.nack(headers['message-id'], headers['subscription'])

    def on_disconnected(self):
        self.logger.info('disconnected')

import logging
import uuid

from stomp import Connection, ConnectionListener


class MQWorker(object):

    def __init__(self, host, port, username, password, queue, numofworkers=1):
        super(MQWorker, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.__connections = {}
        self.__username = username
        self.__password = password
        self.__queue = queue

        for i in range(numofworkers):
            conn = Connection([(host, port)])
            conn.set_listener('', MessageListener(conn))

    def start(self):
        for i, conn in self.__connections.items():
            conn.start()
            conn.connect(self.__username, self.__password, wait=True)
            self.__connections[uuid.uuid4()] = conn
            conn.subscribe(self.__queue, id=i, ack='client')

    def stop(self):
        for i, conn in self.__connections.items():
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
            self.conn.ack(headers['message-id'], headers['subscription'])
        except Exception as e:
            self.logger.error(e)
            self.conn.nack(headers['message-id'], headers['subscription'])

    def on_disconnected(self):
        self.logger.info('disconnected')

import psutil
import json

from rpcservice.rpcservice import RPCService

from decorator.serialize import serialize
from decorator.singleton import singleton


@singleton()
@serialize()
class SystemService(RPCService):

    def get_server_status(self):
        system_status = {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
        }
        json_obj = []
        json_obj.append(system_status)
        return json_obj

    def get_server_version(self):
        pass

    def message_q(self):
        pass

import psutil
import json

from rpcservice.rpcservice import RPCService

from decorator.serialize import json_decorate
from decorator.singleton import singleton


@singleton
@json_decorate
class SystemService(RPCService):

    def get_server_status(self):
        cpu_status = {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
        }
        json_obj = []
        json_obj.append(cpu_status)
        return json_obj

    def get_server_version(self):
        pass

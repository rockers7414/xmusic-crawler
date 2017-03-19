#!/usr/bin/env python

import cmd
import json
import uuid
import socket
import argparse
import readline
import logging
from struct import unpack
from pydoc import locate
from config import Config

from rpcservice.messageheader import MessageHeader


class XMusicRPCClient(object):

    MAX_BUF_LENGTH = 1024

    def __init__(self, server_addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_addr)

    def send_rpcrequest(self, method, params):
        request = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4())
        }
        self.sock.sendall(MessageHeader.create(
            len(json.dumps(request))) + bytes(json.dumps(request), "UTF-8"))

        length = unpack("=BHB", self.sock.recv(MessageHeader.HEADER_LENGTH))[1]
        response = ""
        while len(response) < length:
            buf = self.sock.recv(
                min(self.MAX_BUF_LENGTH, length - len(response)))
            if not buf:
                break
            response += str(buf, "UTF-8")

        return response


class XMusicShell(cmd.Cmd):
    logger = logging.getLogger(__name__)

    intro = "*" * 40 + "\nWelcome to xmusic-cli.\n" + "*" * 40
    prompt = "xmusic> "

    def __init__(self, server_addr):
        super().__init__()
        self.client = XMusicRPCClient(server_addr)
        self.do_reload(None)

    def precmd(self, line):
        prog = line.split(" ")[0]
        if prog != "help" and hasattr(self, "parser_" + prog):
            return super().precmd(prog + " " + line)
        return super().precmd(line)

    def _process(self, arg):
        try:
            prog = arg.split(" ")[0]
            parser = getattr(self, "parser_" + prog)
            args = parser.parse_args(arg.split(" ")[1:])
            response = self.client.send_rpcrequest(prog, vars(args))
            print(response)
        except:
            self.logger.exception("Got exception in _process.")
            pass

    def do_reload(self, arg):
        print("API loading...")
        with open("xmusic-api.json", "r") as f:
            apis = json.load(f)
            for api in apis:
                method = api["method"].replace(" ", "_").lower()
                parser = argparse.ArgumentParser(
                    prog=method,
                    description=api["description"])
                for param in api["parameters"]:
                    parser.add_argument(
                        "--" + param["name"],
                        type=locate(param["type"]),
                        default=param["default"] if "default" in param
                        else None,
                        choices=param["choices"] if "choices" in param
                        else None,
                        required=param["required"],
                        help=param["description"])
                setattr(XMusicShell, "parser_" + method, parser)
                setattr(XMusicShell, "do_" + method, self._process)
                setattr(XMusicShell, "help_" + method, parser.print_help)

    def do_exit(self, arg):
        return True


if __name__ == "__main__":
    config = Config("xmusic-cli.cfg")

    parser = argparse.ArgumentParser(prog="xmusic-cli.py")
    parser.add_argument("--server", default=config.rpcserver_host)
    parser.add_argument("--port", default=int(config.rpcserver_port))
    args = parser.parse_args()

    XMusicShell((args.server, args.port)).cmdloop()

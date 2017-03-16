#!/usr/bin/env python

import json
import socket
import configparser

from struct import pack, unpack

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")

    server_addr = ("localhost", 50000)

    # request = json.dumps({
    #     "method": "echo",
    #     "params": ["xmusic!"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    # request = json.dumps({
    #     "method": "get_artists",
    #     "params": [],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    # request = json.dumps({
    #     "method": "get_artist",
    #     "params": ["obama"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    # request = json.dumps({
    #     "method": "get_album",
    #     "params": ["obama album"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    # request = json.dumps({
    #     "method": "get_track",
    #     "params": ["obama song"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    # request = json.dumps({
    #     "method": "raw_sql",
    #     "params": ["select * from repository"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    request = json.dumps({
        "method": "echo",
        "params": ["xmusic!" * 1000],
        "jsonrpc": "2.0",
        "id": 0,
    })

    print("connect to server({0}:{1})".format("localhost", 50000))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_addr)
        header = pack("=BHB", 29, len(request), 29)
        sock.sendall(header + bytes(request, "UTF-8"))

        length = unpack("=BHB", sock.recv(4))[1]
        response = ""
        while len(response) < length:
            buf = sock.recv(min(1024, length - len(response)))
            if not buf:
                break
            response += str(buf, "UTF-8")

    print("Sent: {0}".format(request))
    print("Received: {0}".format(response))

#!/usr/bin/env python

import json
import socket
import configparser

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
    #     "method": "get_artists_list",
    #     "params": [1, 1, "db"],
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
    #     "params": ["obama_album"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    # request = json.dumps({
    #     "method": "get_track_by_name",
    #     "params": ["obama song11"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    request = json.dumps({
        "method": "raw_sql",
        "params": ["select * from repository"],
        "jsonrpc": "2.0",
        "id": 0,
    })

    # request = json.dumps({
    #     "method": "get_server_status",
    #     "params": [],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # })

    print("connect to server({0}:{1})".format("localhost", 50000))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_addr)
        sock.sendall(bytes(request + "\n", "utf-8"))
        response = str(sock.recv(2048), "utf-8")

    print("Sent: {0}".format(request))
    print("Received: {0}".format(response))

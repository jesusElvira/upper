#!/usr/bin/python
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import os
import time
import socket
import multiprocessing as mp

MAX_CHILDREN = 10


def start_new_process(func, args):
    while len(mp.active_children()) >= MAX_CHILDREN:
        try:
            os.waitpid(0, 0)
        except OSError:
            pass

    ps = mp.Process(target=func, args=args)
    ps.start()


def upper(msg):
    time.sleep(1)
    return msg.upper()


def handle(sock, client):
    print('Client connected: {0}'.format(client))
    while 1:
        data = sock.recv(32)
        if not data:
            break
        sock.sendall(upper(data))

    sock.close()
    print('Client disconnected: {0}'.format(client))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', int(sys.argv[1])))
    sock.listen(5)

    while 1:
        child_sock, client = sock.accept()
        start_new_process(handle, (child_sock, client))


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

try:
    main()
except KeyboardInterrupt:
    sys.exit(0)

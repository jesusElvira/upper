#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import socket
import thread
import threading
import time

lock = threading.Lock()


def upper(msg):
    time.sleep(1)
    return msg.upper()


def handle(sock, msg, client, n):
    print 'New request', n, client
    with lock:
        try:
            sock.sendto(upper(msg), client)
        except socket.error as e:
            print e, client


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', int(sys.argv[1])))

    n = 0
    while 1:
        msg, client = sock.recvfrom(1024)
        n += 1
        thread.start_new_thread(handle, (sock, msg, client, n))


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

try:
    main()
except KeyboardInterrupt:
    pass

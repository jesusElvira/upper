#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import time
import os
from socketserver import StreamRequestHandler, ForkingTCPServer


def upper(msg):
    time.sleep(1)
    return msg.upper()


class UpperHandler(StreamRequestHandler):
    def handle(self):
        print('Client connected: {0}'.format(self.client_address))
        while 1:
            data = os.read(self.rfile.fileno(), 32)
            if not data:
                break

            self.wfile.write(upper(data))


class customForkingTCPServer(ForkingTCPServer):
    allow_reuse_address = True


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

server = customForkingTCPServer(('', int(sys.argv[1])), UpperHandler)
server.serve_forever()

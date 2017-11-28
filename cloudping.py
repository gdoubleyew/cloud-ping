#!/usr/bin/env python3

"""
Description:
Program to measure the latency and bandwidth between client and server
instances. In particular between on-premise and a cloud instance. This is
needed because cloud providers typically block ICMP protocol which ping
uses.
"""

import sys
import getopt
import logging
import socketserver

# TODO - use socketserver framework to make connections.
# https://docs.python.org/3/library/socketserver.html

# GetOpt - http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
# https://docs.python.org/3.1/library/getopt.html

SERVER_MODE = "server"
CLIENT_MODE = "client"

class InvalidInvocation(ValueError):
    pass

class InvalidMode(ValueError):
    pass

class ServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("received: ({}), from {}".format(self.data, self.client_address[0]))
        self.request.sendall(self.data)

class CloudPing():
    def __init__(self, argv):
        self.argv = argv
        self.mode = SERVER_MODE
        self.addr = "127.0.0.1"
        self.port = 5500
        self.parseArgs()

    def printUsage(self):
        usage_format = """Usage:
        {}: <-c | -s> [-a <addr>, -p <port>]
        options:
            -c -- client mode
            -s -- server mode
            -a [--addr] -- server ip address
            -p [--port] -- server port"""
        print(usage_format.format(self.argv[0]))

    def parseArgs(self):
        # parse args
        try:
            opts, _ = getopt.gnu_getopt(self.argv[1:], "a:p:cs",
                                        ["addr=", "port=", CLIENT_MODE, SERVER_MODE])
        except getopt.GetoptError as err:
            logging.error(repr(err))
            raise InvalidInvocation("Invalid parameter specified")

        for opt, arg in opts:
            if opt in ("-a", "--addr"):
                self.addr = arg
            elif opt in ("-p", "--port"):
                self.port = int(arg)
            elif opt in ("-c", "--client"):
                self.mode = CLIENT_MODE
            elif opt in ("-s", "--server"):
                self.mode = SERVER_MODE
            else:
                raise InvalidInvocation("unimplemented option {} {}", opt, arg)

        if self.mode is None:
            raise InvalidInvocation("Must specify either client -c or server -s mode")

    def listen(self):
        if self.mode != SERVER_MODE:
            raise InvalidMode("listen() method can only be called in server mode")
        logging.info("Server mode: listening on %s:%s", self.addr, self.port)
        server = socketserver.TCPServer((self.addr, self.port), ServerRequestHandler)
        server.serve_forever()


def main(argv):
    logging.basicConfig(level=logging.INFO)
    try:
        cloudping = CloudPing(argv)
        if cloudping.mode == SERVER_MODE:
            cloudping.listen()
        elif cloudping.mode == CLIENT_MODE:
            # TODO - implement client side
            pass
    except ValueError as err:
        logging.error(repr(err))
        cloudping.printUsage()
    except KeyboardInterrupt:
        print() # newline

if __name__ == "__main__":
    main(sys.argv)

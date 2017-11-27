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

# TODO - use SocketServer framework to make connections.
# https://docs.python.org/2/library/socketserver.html

# GetOpt - http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
# https://docs.python.org/3.1/library/getopt.html

class InvalidInvocation(ValueError):
    pass

class CloudPing():
    def __init__(self, argv):
        self.argv = argv
        self.mode = None # "server"
        self.addr = None # "127.0.0.1"
        self.port = "0" # "5500"


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
                                        ["addr=", "port=", "client", "server"])
        except getopt.GetoptError as err:
            logging.error(repr(err))
            raise InvalidInvocation("Invalid parameter specified")

        for opt, arg in opts:
            if opt in ("-a", "--addr"):
                self.addr = arg
            elif opt in ("-p", "--port"):
                self.port = arg
            elif opt in ("-c", "--client"):
                self.mode = "client"
            elif opt in ("-s", "--server"):
                self.mode = "server"
            else:
                raise InvalidInvocation("unimplemented option {} {}", opt, arg)

        if self.mode is None:
            raise InvalidInvocation("Must specify either client -c or server -s mode")

def main(argv):
    cloudping = CloudPing(argv)
    try:
        cloudping.parseArgs()
    except ValueError as err:
        logging.error(repr(err))
        cloudping.printUsage()


if __name__ == "__main__":
    main(sys.argv)

import argparse

import socket
import logging

from time import sleep


class PythonSocketClient:
    def __init__(self, host="localhost", port=27017, level=logging.DEBUG):

        self.t = 0
        # keep track of connection status
        # self.connected = False

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.host = socket.gethostname()
        self.host = host
        self.port = port

        FORMAT = '%(asctime)-15s %(clientip)s:%(port)s %(user)-8s %(message)s'
        # logging.basicConfig(format=FORMAT)

        self.logger = logging.getLogger('udpclient')
        self.logger.setLevel(level)
        self.d = {'clientip': 'client', 'user': 'root', 'port': self.port}
        self.logger.info('socket created: %s', 'connection reset')

    # def backoff(self):
    #     if self.t == 0:
    #         self.t = 1
    #     else:
    #         self.t *= 2

    # def connect(self):
    #     # configure socket and connect to server
    #     # host = socket.gethostname()
    #     # port = self.port

    #     self.clientSocket.connect( ( self.host, self.port ) )

    #     self.connected = True
    #     self.d = {'clientip': self.clientSocket.getpeername(), 'user': 'root', 'port': self.port }

    #     self.logger.info('connection established', extra = self.d)

    # def reconnect(self):
    #      # set connection status and recreate socket
    #     self.connected = False
    #     self.clientSocket = socket.socket()

    #     self.logger.warning("connection lost... reconnecting", extra = self.d)

    #     while not self.connected:
    #         t = 0
    #         # attempt to reconnect, otherwise sleep for 2 seconds
    #         try:
    #             self.connect()

    #             self.logger.warning( "re-connection successful" , extra = self.d)

    #         except socket.error:
    #             # self.logger.warning(".")
    #             sleep(self.t)
    #             self.backoff()

    # loop listening for messages
    def listen(self):

        while True:
            self.recv()

        self.clientSocket.close()

    # grab one message at a time
    def recv(self):

        message = ""
        try:
            while (True):
                try:
                    payload, address = self.clientSocket.recvfrom(4096)
                    message += payload.strip().decode("utf-8")
                except:
                    self.logger.warning("cannot receive data", self.d)
                    break

                if not payload:
                    break

        except socket.error:
            self.logger.error("socket err", self.d)
            # self.reconnect()

    def send(self, message):
        try:
            payload = message.encode('utf-8')
            self.clientSocket.sendto(bytes(payload), (self.host, self.port))
        except socket.error as e:
            print(e)
            # pass
            # self.reconnect()


def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', help='host to connect to')
    parser.add_argument('--port', type=int, default=27017, help='port to listen on')
    parser.add_argument('--debug', type=str, default='debug',
                        help='debug logging output level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]')

    # parser.add_argument('--path', type=str, default=28, help='source file', required=True)

    args = parser.parse_args()

    client = PythonSocketClient(args.host, args.port)
    # client.connect()
    client.listen()

#!/usr/bin/env python
import socketserver
import threading
# Credit for much of this code goes to the following:
# https://stackoverflow.com/questions/35279655/connecting-to-multiple-ports-using-python-socketserver


class Ear(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(2048)

        if self.data:
            if "ping" in repr(self.data.strip()):
                print("%s reached us on port %i." % ( self.client_address[0], self.request.getsockname()[1]))
                self.request.sendall(b'pong %i\n' %(self.request.getsockname()[1]))
            else:
                print("Received: '%s' from '%s:%i' on port '%i'." % (repr(self.data), self.client_address[0], self.client_address[1], self.request.getsockname()[1]))
                self.request.sendall(self.data)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    pass


def main():
    global Ears
    global Ear_threads

    Ears = []
    Ear_threads =[]

    for port in range(1,1000):
        Ears.append(ThreadedTCPServer(('', port), Ear))

    for ear in Ears:
        Ear_threads.append(threading.Thread(target=ear.serve_forever))

    for ear_thread in Ear_threads:
        ear_thread.setDaemon(True)
        ear_thread.start()

    while True:
        continue

if __name__ == '__main__':
    main()

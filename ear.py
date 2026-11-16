#!/usr/bin/env python3
import socketserver
import threading
import time
# Credit for much of this code goes to the following:
# https://stackoverflow.com/questions/35279655/connecting-to-multiple-ports-using-python-socketserver


class Ear(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(2048)

        if self.data:
            port = self.request.getsockname()[1]
            if b"ping" in self.data:
                print("%s reached us on port %i." % (self.client_address[0], port))
                self.request.sendall(("pong %i\n" % port).encode())
            else:
                print("Received: '%s' from '%s:%i' on port '%i'." % (repr(self.data), self.client_address[0], self.client_address[1], port))
                self.request.sendall(self.data)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def main():
    ears = []
    failed_ports = []

    for port in range(1, 1001):
        try:
            ears.append(ThreadedTCPServer(('', port), Ear))
        except OSError as e:
            failed_ports.append(port)
            print("Could not listen on port %i: %s" % (port, e))

    for ear in ears:
        ear_thread = threading.Thread(target=ear.serve_forever)
        ear_thread.daemon = True
        ear_thread.start()

    print("Listening on %i ports (%i failed)." % (len(ears), len(failed_ports)))
    if failed_ports:
        print("Failed ports: %s" % ", ".join(str(p) for p in failed_ports))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Listener threads are daemons, so they exit with the main thread.
        print("Shutting down.")


if __name__ == '__main__':
    main()

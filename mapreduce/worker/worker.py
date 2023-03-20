import os
import pathlib
import logging
import socket
import threading
import json
import time

# def send_heartbeat(worker_id):
#     pid = os.getpid()
#     print("Worker {}  pid={}".format(worker_id, pid))
#     while True:
#         print("working")
#     print("wait() shutting down")


def create_listen_socket(self, worker_port):
    print('Starting Worker socket')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Bind the socket to the server
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("localhost", worker_port))
        print('Socket ready')
        sock.listen()

        # Socket accept() and recv() will block for a maximum of 1 second.  If you
        # omit this, it blocks indefinitely, waiting for a connection.
        sock.settimeout(1)

        while not self.signals["shutdown"]:
            # Wait for a connection for 1s.  The socket library avoids consuming
            # CPU while waiting for a connection.
            try:
                clientsocket, address = sock.accept()
            except socket.timeout:
                continue
            print("Connection from", address[0])

            # Receive data, one chunk at a time.  If recv() times out before we can
            # read a chunk, then go back to the top of the loop and try again.
            # When the client closes the connection, recv() returns empty data,
            # which breaks out of the loop.  We make a simplifying assumption that
            # the client will always cleanly close the connection.
            with clientsocket:
                message_chunks = []
                while True:
                    try:
                        data = clientsocket.recv(4096)
                    except socket.timeout:
                        continue
                    if not data:
                        break
                    message_chunks.append(data)

            # Decode list-of-byte-strings to UTF8 and parse JSON data
            message_bytes = b''.join(message_chunks)
            message_str = message_bytes.decode("utf-8")

            try:
                msg = json.loads(message_str)
            except json.JSONDecodeError:
                continue
            print("message to worker", msg)
            self.messages.append(msg)
            self.process_msg(worker_port, msg)
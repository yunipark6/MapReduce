import pathlib
import logging
import socket
import threading
import json
import time
#from mapreduce.worker.worker import send_heartbeat
from mapreduce.manager.process_msg import processMsg

def create_tmp():
    '''Create tmp folder and Delete any old folders in tmp.'''
    # Create path name
    p = pathlib.Path(__file__).parents[2]
    p = p / 'tmp'

    # Create it if it doesn't exist
    if not p.exists():
        p.mkdir(mode=511, parents=False)

    # Delete old folders if they exist
    print("[TODO - delete old mapreduce folders]")


# Create thread to listen to heartbeats from Workers
# def create_thread(self, port_number):
#     '''Create new thread, will listen for UDP heartbeat messages from the Workers'''
#     print('Create Thread')
#     # signals = {"shutdown": False}
#     thread = threading.Thread(name="heartbeat", target=send_heartbeat, args=(signals,))
#     thread.start()
#     time.sleep(3) # This gives up execution to the 'wait' thread
#     # The shutdown variable will be set to true in approximately 1 second
#     signals["shutdown"] = True
#     print("main() shutting down")




# Create socket to listen for messages (from client?)
def create_socket(self, port_number):
    print('Starting socket')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Bind the socket to the server
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("localhost", port_number))
        print('Socket ready')
        sock.listen()

        # Socket accept() and recv() will block for a maximum of 1 second.  If you
        # omit this, it blocks indefinitely, waiting for a connection.
        sock.settimeout(1)
        # time.sleep(0.1)

        while not self.signals["shutdown"]:
            # Wait for a connection for 1s.  The socket library avoids consuming
            # CPU while waiting for a connection.
            try:
                clientsocket, address = sock.accept()
            except socket.timeout:
                continue
            # print("Connection from", address[0])

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
            print(msg)
            self.process_msg(port_number, msg)

        print("server() shutting down")
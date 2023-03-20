"""Utils file.

This file is to house code common between the Manager and the Worker

"""
import socket
import json

def register_message(port_number, msg_type, worker_host, worker_port, worker_pid):
    """Sends a Register Message (register or register-ack)"""
    msg = {
        "message_type": msg_type,
        "worker_host": worker_host,
        "worker_port": worker_port,
        "worker_pid": worker_pid
    }
    msg = json.dumps(msg)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.bind(("localhost", port_number))
        # connect to the server
        sock.connect(("localhost", port_number))
        sock.sendall(msg.encode('utf-8'))

def send_shutdown(portnumber,workers):
    msg = json.dumps({"message_type": "shutdown"})

    print("Workers!", workers)
    for worker in workers:
        print("worker!", worker)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #sock.bind(("localhost", worker['worker_port']))
            # connect to the server
            sock.connect(("localhost", worker['worker_port']))
            # sock.sendall(json.dumps({"message_type": "shutdown",}).encode('utf-8')),
            sock.sendall(msg).encode('utf-8')
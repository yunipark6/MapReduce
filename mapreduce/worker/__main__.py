import os
import logging
import json
import time
import click
import mapreduce.utils
import mapreduce.worker.worker as worker
import mapreduce.worker.process_msg_worker as process_msg
import mapreduce.utils as utils


# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Worker:
    def __init__(self, manager_port, manager_hb_port, worker_port):
        logging.info("Starting worker:%s", worker_port)
        logging.info("Worker:%s PWD %s", worker_port, os.getcwd())

        # This is a fake message to demonstrate pretty printing with logging
        # message_dict = {
        #     "message_type": "register_ack",
        #     "worker_host": "localhost",
        #     "worker_port": 6001,
        #     "worker_pid": 77811
        # }
        # logging.debug(
        #     "Worker:%s received\n%s",
        #     worker_port,
        #     json.dumps(message_dict, indent=2),
        # )

        ### PROCESS COMMAND LINE
        self.manager_port = manager_port
        self.manager_hb_port = manager_hb_port
        self.worker_port = worker_port

        ### THREADS AND SOCKETS
        self.create_listen_socket(self.worker_port) # Create socket to LISTEN for instructions from Manager
        utils.register_message(self.manager_port, "register", self.manager_port, self.manager_hb_port)
        # self.create_heartbeat_thread(manager_hb_port) # Create socket to SEND heartbeats to Manager

    ### MEMBER FUNCTIONS
    create_listen_socket = worker.create_listen_socket
    process_msg = process_msg.processMsg
    # create_heartbeat_thread = worker.create_heartbeat_thread

    ### MEMBER VARIABLES / DATASTRUCTURES
    signals = {"shutdown": False}
    messages = []



@click.command()
@click.argument("manager_port", nargs=1, type=int)
@click.argument("manager_hb_port", nargs=1, type=int)
@click.argument("worker_port", nargs=1, type=int)
def main(manager_port, manager_hb_port, worker_port):
    """Instantiate worker object for this process."""
    Worker(manager_port, manager_hb_port, worker_port)


if __name__ == '__main__':
    main()

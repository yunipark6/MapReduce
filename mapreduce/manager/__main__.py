import os
import logging
import json
import time
import click
from enum import Enum
import mapreduce.utils
import mapreduce.manager.manager as mgr
import mapreduce.manager.process_msg as process_msg


# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Manager:
    def __init__(self, port, hb_port):
        logging.info("Starting manager:%s", port)
        logging.info("Manager:%s PWD %s", port, os.getcwd())

        ### PROCESS COMMAND LINE
        self.port_number = port
        self.hb_port = hb_port

        ### THREADS AND SOCKETS
        mgr.create_tmp()
        # mgr.create_thread(self.hb_port)
        #self.create_thread(self.hb_port)
        self.create_socket(self.port_number)

    ### MEMBER FUNCTIONS
    # create_thread = mgr.create_thread # Create thread to listen for heartbeats
    create_socket = mgr.create_socket # Create socket to listen for messages
    process_msg = process_msg.processMsg # Processes messages

    ### MEMBER VARIABLES / DATASTRUCTURES
    signals = {"shutdown": False}
    workers = [] # keep track of workers (heartbeat state, numbers)
    curJob = {} # current job
    jobsQueue = [] # upcoming jobs (queue)

    class workerState(Enum):
        ready = 1
        busy = 2
        dead = 3

    


@click.command()
@click.argument("port", nargs=1, type=int)
@click.argument("hb_port", nargs=1, type=int)
def main(port, hb_port):
    Manager(port, hb_port)


if __name__ == '__main__':
    main()

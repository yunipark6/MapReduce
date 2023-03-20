import time
import mapreduce.utils as utils

def processMsg(self, worker_port, msg):
    if msg['message_type'] == "shutdown":
        # send message to all workers
        time.sleep(0.1)
        self.signals["shutdown"] = True
    elif msg['message_type'] == "register_ack":
        print("[TODO]: register_ack")

    else:
        self.jobsQueue.append(msg)
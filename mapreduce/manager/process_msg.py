import time
import mapreduce.utils as utils


def processMsg(self, portnumber, msg):
    if msg['message_type'] == "shutdown":
        # send message to all workers
        time.sleep(0.1)
        self.signals["shutdown"] = True
        print("TODO: shutdown")
        utils.send_shutdown(portnumber, self.workers)
    elif msg['message_type'] == "register":
        worker = {'state': self.workerState.ready, 'worker_host': msg['worker_host'], 'worker_port': msg['worker_port'], 'worker_pid': msg['worker_pid']}
        self.workers.append(worker)
        print(self.workers)
        print("worker registered")

        # send message to worker
        #msg = utils.register_message(portnumber, "register_ack", worker['worker_host'], worker['worker_port'], worker['worker_pid'])
        # print("clientsocket", clientsocket)
    elif msg['message_type'] == "new_manager_job":
        print("[TODO]: new_manager_job")
    else:
        self.jobsQueue.append(msg)
import queue
import threading
from queue import Queue
import os
import time
from conf import Config
from disk_cleaner import Disk

c = Config()
logger = c.thread_logger
queue_size = c.queue_size

queue1 = Queue(queue_size)
stop_threads = False


class Producer(threading.Thread):
    """
    Create a thread that put subdirectories of given disk_path on queue
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(Producer, self).__init__(name="Producer")
        self.path = c.path

    def run(self):
        logger.info("starting producer")
        for filename in os.listdir(self.path):
            f = os.path.join(self.path, filename)
            if os.path.isdir(f):
                queue1.put(f)
                logger.info("Producer put " + str(f) + " on queue.")
        logger.info("Producer done with " + str(self.path))


class Consumer(threading.Thread):
    """
    create a thread that get a subdirectory path from queue
    and remove unwanted directories/files on that path using
    a Disk object
    """

    def __init__(self, group=None, target=None, name="Consumer",
                 args=(), kwargs=None, verbose=None):
        super(Consumer, self).__init__(name=name)
        self._stopit = threading.Event()

    def stop(self):
        self._stopit.set()

    def stopped(self):
        return self._stopit.is_set()

    def run(self):
        logger.info("starting " + self.name)
        while True:
            if self.stopped():
                logger.info(self.name + " done")
                return
            try:
                dir_path = queue1.get(timeout=1)
                disk = Disk(Config(dir_path))
                disk.delete()
                logger.info(self.name + " cleaning " + str(dir_path))
            except queue.Empty:
                pass

import os
import shutil
import unittest
from queue import Queue
from unittest.mock import patch, Mock
import conf
import disk_cleaner
import manager
import time

c = conf.Config()
queue_size = c.queue_size
path = c.path


class TestManager(unittest.TestCase):
    """
    test cases must be run separately
    """

    def setUp(self):
        self.main_path = './testing_manager'
        if os.path.exists(self.main_path):
            shutil.rmtree(self.main_path)

        os.mkdir(self.main_path)
        self.dir1 = self.main_path + '/dir1'
        self.dir2 = self.main_path + '/dir2'
        self.dir3 = self.main_path + '/dir3'
        os.mkdir(self.dir1)
        os.mkdir(self.dir2)
        os.mkdir(self.dir3)

        self.queue = Queue(queue_size)
        self.queue.put(self.dir2)
        self.queue.put(self.dir3)
        self.queue.put(self.dir1)


    @patch('manager.c.path', './testing_manager')
    def test_producer(self):
        """
        test the producer puts subdirectory paths on queue and sets done to True
        """
        producer = manager.Producer()
        producer.start()
        while producer.is_alive():
            time.sleep(1)
        if not producer.is_alive():
            print(manager.queue1.queue, self.queue.queue)
            assert manager.queue1.queue == self.queue.queue

    @patch.object(disk_cleaner.Disk, 'delete')
    def test_consumer(self, l):
        """
        tests consumer calls delete
        """
        with patch.object(disk_cleaner.Disk, 'delete', autospec=True) as mock_delete:
            consumer = manager.Consumer()
            consumer.start()
            mock_delete.assert_called_with()

        manager.done = True
        self.assertEqual(consumer.is_alive(), True)
        consumer.stop()
        time.sleep(2)
        self.assertEqual(consumer.is_alive(),False)

    def tearDown(self) -> None:
        if os.path.exists(self.main_path):
            shutil.rmtree(self.main_path)
        if os.path.exists('disk_cleanup_debug.log'):
            os.remove('disk_cleanup_debug.log')
        if os.path.exists('disk_cleanup_error.log'):
            os.remove('disk_cleanup_error.log')
        if os.path.exists('manager.log'):
            os.remove('manager.log')


if __name__ == '__main__':
    unittest.main()

from unittest.mock import patch
import unittest
import os
import datetime
import shutil
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
from bin.disk_cleaner import Disk
from bin.conf import Config
"""
Test cases for disk_cleaner.py
"""


class TestDiskCleaner(unittest.TestCase):
    def setUp(self):
        self.main_path = os.path.dirname(os.path.abspath(__file__)) + '/test_disk_cleaner'
        if os.path.exists(self.main_path):
            shutil.rmtree(self.main_path)

        expired_accessed_time = datetime.datetime(2012, 5, 9).timestamp()
        expired_modified_time = datetime.datetime(2012, 5, 9).timestamp()

        os.mkdir(self.main_path)
        self.disk1 = Disk(Config(self.main_path))
        self.disk1.match_express = ['']

        # make empty directory
        self.path_dir1_empty = self.main_path + '/d41561a3-14ff-4a41-840c-98bd7f00e860'
        os.mkdir(self.path_dir1_empty)
        os.utime(self.path_dir1_empty, (expired_accessed_time, expired_modified_time))

        # make directory with expired files
        self.path_dir2_expired = self.main_path + '/dir2_expired'
        os.mkdir(self.path_dir2_expired)

        #files in dir2
        self.path_expired1 = self.path_dir2_expired + '/expired_file'
        file1 = open(self.path_expired1, 'w')
        os.utime(self.path_expired1, (expired_accessed_time, expired_modified_time))
        file1.close()

        self.path_expired2_uuid = self.path_dir2_expired + '/c3bc0e0a-017e-4628-a35f-0f235bbeeba6'
        file2 = open(self.path_expired2_uuid, 'w')
        os.utime(self.path_expired2_uuid, (expired_accessed_time, expired_modified_time))
        file2.close()

        self.path_not_uuid = self.path_dir2_expired + '/c3bc0e0a-017e-4628-a35f-0f235bbeeba6h'
        file3 = open(self.path_expired2_uuid, 'w')
        os.utime(self.path_expired2_uuid, (expired_accessed_time, expired_modified_time))
        file3.close()

        #make directory with unexpired files
        self.path_dir3_unexpired = self.main_path + '/dir3_not_expired'
        os.mkdir(self.path_dir3_unexpired)

        #files in dir3
        self.path_unexpired = self.path_dir3_unexpired + '/unexpired_file'
        file4 = open(self.path_unexpired, 'w')
        file4.close()

        self.path_locked = self.path_dir3_unexpired + '/.lock.key'
        file5 = open(self.path_locked, 'w')
        os.utime(self.path_locked, (expired_accessed_time, expired_modified_time))
        file5.close()

    def test_disk_cleanup(self):
        patch1 = 'shutil.disk_usage'
        with patch(patch1, return_value=[10, 9.3, 0.7]):
            self.assertEqual(self.disk1.is_over_capacity(), True)
        with patch(patch1, return_value=[10, 2, 8]):
            self.assertEqual(self.disk1.is_over_capacity(), False)
        with patch(patch1, return_value=[10, 9, 1]):
            self.assertEqual(self.disk1.is_over_capacity(), True)

    def test_old_enough(self):
        self.assertEqual(self.disk1.old_enough(self.path_expired1), True)
        self.assertEqual(self.disk1.old_enough(self.path_expired2_uuid), True)
        self.assertEqual(self.disk1.old_enough(self.path_unexpired), False)

    def test_match_expression(self):
        self.assertEqual(self.disk1.match_expression(self.path_expired1), True)
        self.assertEqual(self.disk1.match_expression(self.path_expired2_uuid), True)
        self.disk1.match_express = ['[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$']
        self.assertEqual(self.disk1.match_expression(self.path_expired1), False)
        self.assertEqual(self.disk1.match_expression(self.path_expired2_uuid), True)
        self.assertEqual(self.disk1.match_expression(self.path_not_uuid), False)
        self.disk1.match_express = []

    def test_should_delete(self):
        """
        test should_delete_file for:
        1. unlocked file
        3. locked file
        """
        self.assertEqual(self.disk1.should_delete(self.path_expired1), True)
        self.assertEqual(self.disk1.should_delete(self.path_expired2_uuid), True)
        self.assertEqual(self.disk1.should_delete(self.path_locked), False)

    def test_delete_success(self):
        """
        ensure there are no failed deletions
        """
        self.disk1.delete(self.main_path)
        self.assertEqual(self.disk1.get_failed_deletions(), [])

    def test_delete_locked_file(self):
        """
        don't delete locked file
        """
        self.disk1.delete(self.path_locked)
        print(self.path_locked)
        self.assertEqual(os.path.exists(self.path_locked), True)

    def test_delete_empty_directory(self):
        """
        delete empty directory
        """
        self.disk1.delete(self.path_dir1_empty)
        self.assertEqual(os.path.exists(self.path_dir1_empty), False)

    def test_delete_expired_file(self):
        """
        delete expired_file
        """
        self.disk1.delete(self.path_dir2_expired)
        self.assertEqual(os.path.exists(self.path_expired1), False)
        self.assertEqual(os.path.exists(self.path_expired2_uuid), False)

    def test_delete_recursive(self):
        """
        test delete nested directories/files
        """
        self.disk1.delete(self.main_path)
        self.assertEqual(os.path.exists(self.path_dir1_empty), False)
        self.assertEqual(os.path.exists(self.path_expired1), False)
        self.assertEqual(os.path.exists(self.path_expired2_uuid), False)
        self.assertEqual(os.path.exists(self.path_dir2_expired), True)
        self.assertEqual(os.path.exists(self.path_unexpired), True)
        self.assertEqual(os.path.exists(self.path_locked), True)
        self.assertEqual(os.path.exists(self.path_dir3_unexpired), True)

    def test_failed_deletion(self):
        self.disk1.failed_deletions = ['path1', 'path2']
        self.assertEqual(self.disk1.get_failed_deletions(),  ['path1', 'path2'])

    def tearDown(self):
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

import shutil
import os
from conf import Config
from datetime import datetime
import re


class Disk(object):
    """
    class to represent a disk.
    """

    def __init__(self, config: Config):
        self.path = config.path
        self.logger = config.main_logger
        self.normal_period = config.normal_period
        self.locked_period = config.locked_period
        self.failed_deletions = []
        self.match_express = config.match_express

    def is_over_capacity(self) -> bool:
        """
        check if disk_usage is or exceeds 90%
        """
        total, used, free = shutil.disk_usage(self.path)
        return used / total >= .9

    def delete(self, path: str = None) -> None:
        """
        recursively delete all empty directories or files that should be deleted inside the given directory path.
        """
        if path is None:
            path = self.path
        path = os.path.abspath(path)
        if os.path.isfile(path) and self.should_delete(path) and self.old_enough(path):
            try:
                os.remove(path)
                self.logger.info(f"file {os.path.abspath(path)} is deleted for being inactive for over "
                                 f"{self.normal_period} days")
            except FileNotFoundError as error:
                self.failed_deletions.append(path)
                self.logger.error(f"failed to delete file {path}, file not found", error)
            except PermissionError as error:
                self.failed_deletions.append(path)
                self.logger.error(f"failed {path}, permission denied", error)
            return
        if os.path.isdir(path):
            old_enough = self.old_enough(path)
            for filename in os.listdir(path):
                f = os.path.join(path, filename)
                self.delete(f)
            if len(os.listdir(path)) == 0 and self.should_delete(path) and old_enough:
                try:
                    os.rmdir(path)
                    self.logger.info(
                        f"directory {os.path.abspath(path)} is deleted for being inactive for over {self.normal_period} days")
                except FileNotFoundError as error:
                    self.failed_deletions.append(path)
                    self.logger.error(f"failed to delete folder {path}", error)
                except PermissionError as error:
                    self.failed_deletions.append(path)
                    self.logger.error(f"failed to delete file {path}", error)

    def get_failed_deletions(self):
        return self.failed_deletions

    def should_delete(self, path: str) -> bool:
        if ".lock" in path:
            return self.should_delete_locked_file(path)
        # remove old_enough
        if self.match_expression(path):
            return True
        return False

    def old_enough(self, path: str) -> bool:
        """
        return True if file should be deleted and log accordingly if it should
        """
        days_passed = (datetime.today() - datetime.fromtimestamp(os.path.getmtime(path))).days
        if days_passed >= self.normal_period:
            return True
        return False

    def match_expression(self, path: str) -> bool:
        """
        return True if the last path is one of the expression allowed to delete
        """
        for pattern in self.match_express:
            for sub_path in re.split('/', path):
                if re.match(pattern, sub_path) is not None:
                    return True
        return False

    def should_delete_locked_file(self, path: str) -> bool:
        """
        return True if locked file should be deleted and log accordingly if it should
        """
        return False

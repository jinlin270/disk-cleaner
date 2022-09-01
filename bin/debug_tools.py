import os
from datetime import datetime
import re
import config
c = config.Config()

logger = c.main_logger
match_express = c.match_express
normal_period = c.normal_period


def should_delete(path: str) -> bool:
    if ".lock" in path:
        return should_delete_locked_file(path)
    if match_expression(path):
        return True
    return False


def match_expression(path: str) -> bool:
    """
    return True if the last path is one of the expression allowed to delete
    """
    for pattern in match_express:
        for sub_path in re.split('/', path):
            if re.match(pattern, sub_path) is not None:
                return True
    return False


def should_delete_locked_file(path: str) -> bool:
    """
    return True if locked file should be deleted and log accordingly if it should
    """
    return False


def old_enough(path):
    """
      return True if file should be deleted and log accordingly if it should
      """
    path = os.path.abspath(path)
    days_passed = (datetime.today() - datetime.fromtimestamp(os.path.getmtime(path))).days
    if days_passed >= normal_period:
        return True
    return False


def check(path: str):
    path = os.path.abspath(path)
    if os.path.isfile(path):
        if should_delete(path) and old_enough(path):
            logger.error(f"file {os.path.abspath(path)} should be deleted")
        else:
            logger.error(f"file {os.path.abspath(path)} match_expressions:" +
                         str(match_expression(path)) + ", old_enough:" + str(old_enough(path)))
        return
    if os.path.isdir(path):
        old = old_enough(path)
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            check(f)
        if len(os.listdir(path)) == 0 and should_delete(path) and old:
            logger.error(f"directory {os.path.abspath(path)} should be deleted")
        else:
            logger.error(f"dir {os.path.abspath(path)} match_expressions:" +
                         str(match_expression(path)) + ", old_enough:" + str(old_enough(path)) +
                         "is_empty:" + str(len(os.listdir(path)) == 0))



import requests
import json
from .conf import Config
import shutil


c = Config()
webhook = c.webhook
disk_path = c.path


def send_overflow_message():
    total, used, free = shutil.disk_usage(disk_path)
    overflow_message = {"text": "FATAL_ERROR! disk_usage is over {} percent".format(used / total)}
    return requests.post(webhook, json.dumps(overflow_message))


def send_crashed_message() :
    """
    send error to stack if disk_cleaner program crashed
    """
    cleaner_died_message = {"text": "FATAL_ERROR! disk_cleaner died"}
    return requests.post(webhook, json.dumps(cleaner_died_message))




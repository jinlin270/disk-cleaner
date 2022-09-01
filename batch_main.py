import schedule
import time
import shutil
from bin import conf, slack_client
import onetime_main
import os

c = conf.Config()
disk_path = c.path
disk_usage_trigger = c.disk_usage_trigger
inode_usage_trigger = c.inode_usage_trigger
inode_overflow = c.inode_overflow
disk_overflow = c.disk_overflow


def batch_main():
    total, used, free = shutil.disk_usage(disk_path)
    inode = os.statvfs(disk_path).f_files
    iused = inode - os.statvfs(disk_path).f_ffree
    if used / total >= disk_usage_trigger or iused/inode >= inode_usage_trigger:
        onetime_main.onetime()


def check_disk_usage():
    total, used, free = shutil.disk_usage(disk_path)
    if used/total >= disk_overflow:
        slack_client.send_overflow_message()

def check_inode_usage():
    inode = os.statvfs(disk_path).f_files
    used = inode - os.statvfs(disk_path).f_ffree
    if used/inode >= inode_overflow:
        slack_client.send_overflow_message()

# schedule.every().day.do(start_manager)
schedule.every(5).minutes.do(check_disk_usage)
schedule.every(5).minutes.do(batch_main)


batch_main()
# onetime_main.onetime()

while True:
    n = schedule.idle_seconds()
    if n > 0:
        print("sleeping", n)
        time.sleep(n)
    schedule.run_pending()

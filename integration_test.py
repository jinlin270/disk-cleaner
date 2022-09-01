import os
import shutil
import datetime
import uuid
import random
import schedule
import time
"""
The performance test file for delete. 
"""
max_directories = 5
max_files_per_directory = 1024
byte_per_file = 3072


def set_up():
    """
    makes num_directories expired directories, each containing num_files_per_directory expired file

    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(current_path, 'integration_test')
    if not os.path.exists(test_path):
        print("setting up new integration_test")
        os.mkdir(test_path)

    add_more_files()


def add_more_files():
    num_directories = random.randint(0, max_directories)
    num_files_per_directory = random.randint(0, max_files_per_directory)
    accessed_time = datetime.datetime(2012, 1, 9).timestamp()
    modified_time = datetime.datetime(2012, 1, 9).timestamp()

    for _ in range(num_directories):
        directory_name = str(uuid.uuid4())
        path = os.path.join('integration_test', directory_name)
        os.mkdir(path)
        for _ in range(num_files_per_directory):
            file_name = random.choices(["file" + str(_), "file" + str(_) + ".lock"], weights=[100000000000000000, 1])[0]
            file_path = os.path.join(path, file_name)
            with open(file_path, 'w') as f:
                f.write("0"*byte_per_file)
            os.utime(file_path, (accessed_time, modified_time))
        os.utime(path, (accessed_time, modified_time))
    print("done")


def tear_down():
    if os.path.exists('integration_test'):
        shutil.rmtree('integration_test')


set_up()
schedule.every(1).seconds.do(add_more_files)

while True:
    n = schedule.idle_seconds()
    if n > 0:
        print("sleeping", n)
        time.sleep(n)
    schedule.run_pending()


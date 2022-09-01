import os
import shutil
import datetime
import uuid
# import progressbar
import time
"""
The performance test file for delete. 
"""

num_directories = 10
num_files_per_directory = 1000
byte_per_file = 1024 * 1024

def set_up():
    """
    makes num_directories expired directories, each containing num_files_per_directory expired file

    """
    accessed_time = datetime.datetime(2012, 1, 9).timestamp()
    modified_time = datetime.datetime(2012, 1, 9).timestamp()
    current_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(current_path, 'performance_test')
    print("removing existing performance_test")
    if os.path.exists(test_path):
        shutil.rmtree(test_path)

    print("setting up new performance_test")
    os.mkdir(test_path)
    # with progressbar.ProgressBar(max_value=num_directories) as bar:
    for d in range(num_directories):
        # bar.update(d)
        directory_name = str(uuid.uuid4())
        path = os.path.join('performance_test', directory_name)
        os.mkdir(path)
        for _ in range(num_files_per_directory):
            file_name = str(uuid.uuid4())
            file_path = os.path.join(path, file_name)
            with open(file_path, 'w') as f:
                f.write('0' * byte_per_file)
            os.utime(file_path, (accessed_time, modified_time))

        os.utime(path, (accessed_time, modified_time))

    print("done\n" + "The path to performance_test is: " + test_path)
    return test_path


def tear_down():
    if os.path.exists('performance_test'):
        shutil.rmtree('performance_test')


start = time.time()
set_up()
end = time.time()
print("setup used: " + str(end-start) + "seconds.")

import time
from bin import manager


def onetime():
    manager_thread = manager.Producer()
    print("put files on queue")
    manager_thread.start()

    cleaner1 = manager.Consumer(name="cleaner1")
    cleaner2 = manager.Consumer(name="cleaner2")
    cleaner3 = manager.Consumer(name="cleaner3")

    print("start cleaning")
    cleaner1.start()
    cleaner2.start()
    cleaner3.start()

    while cleaner1.is_alive() or cleaner2.is_alive() or cleaner3.is_alive():
        time.sleep(5)
        if manager.queue1.empty() and (not manager_thread.is_alive()):
            cleaner1.stop()
            cleaner2.stop()
            cleaner3.stop()

    print("Done")


start = time.time()
onetime()
end = time.time()
print("main used: " + str(end-start) + "seconds.")
#encoding=utf-8
import threading
import random
import time
from Queue import Queue
import mutex
 
class Producer(threading.Thread):
 
    def __init__(self, threadname, queue, lock):
        threading.Thread.__init__(self, name = threadname)
        self.sharedata = queue
        self.lock = lock
 
    def run(self):
        for i in range(20):
            #----------------
            #self.lock.acquire()
            print self.getName(),'<< ',i
            #self.lock.release()
            #----------------
            self.sharedata.put(i)
            time.sleep(random.randrange(10)/50.0)
            #time.sleep(1)
        print self.getName(),'Finished'
 
 
# Consumer thread
 
class Consumer(threading.Thread):
 
 
    global lock
    def __init__(self, threadname, queue, lock):
        threading.Thread.__init__(self, name = threadname)
        self.sharedata = queue
        self.lock = lock
 
 
    def run(self):
        for i in range(20):
            #----------------
            #self.lock.acquire()
            print self.getName(),'        >> ',self.sharedata.get()
            #self.lock.release()
            #----------------
            time.sleep(random.randrange(10)/50.0)
            #time.sleep(1)
        print self.getName(),'Finished'
 
 
# Main thread
 
def main():
 
    lock = threading.RLock()
    queue = Queue()
    producer = Producer('Producer', queue, lock)
    consumer0 = Consumer('Consumer', queue, lock)
    consumer1 = Consumer('Consumer', queue, lock)
    consumer2 = Consumer('Consumer', queue, lock)
    print 'Starting threads ...'
    producer.start()
    consumer0.start()
    consumer1.start()
    consumer2.start()
    producer.join()
    consumer0.join()
    consumer1.join()
    consumer2.join()
    print 'All threads have terminated.'
 
if __name__ == '__main__':
    main()

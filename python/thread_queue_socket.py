import threading
import time
import SocketServer
import Queue
import mutex
import random

global producer
global queue

class MyTCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        username = None
        while True:
            self.data = self.rfile.readline().strip()
            cur_thread = threading.currentThread()
            print "thread name:", cur_thread.getName();
            print "RECV from ", self.client_address[0]
            cmd = self.data
            if cmd == None or len(cmd) == 0:
                break;
            print cmd
            # business logic here
            try:
                if cmd.startswith('echo'):
                    result = "queue count: %d" % queue.qsize()
                elif cmd == 'shutdown':
                    producer.shutdown()
                    result = 'shutdowning'
                elif cmd == 'quit':
                    break
                else:
                    result = 'error cmd'
                self.wfile.write(result)
                self.wfile.write('\n')
            except:
                print 'error'
                break
        print self.client_address[0], ' closed.'

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class Producer(threading.Thread):
    def __init__(self, threadname, queue):
        threading.Thread.__init__(self, name = threadname)
        self.sharedata = queue
        self.__is_shut_down = threading.Event()
        self.__running = False
 
    def run(self):
        self.__running = True
        i = 0
        while self.__running:
            print self.getName(),'<< ',i
            if self.sharedata.full():
                time.sleep(1)
                continue
            self.sharedata.put_nowait(i)
            i = i + 1
        self.__is_shut_down.set()
        print self.getName(),'Finished'

    def shutdown(self):
        self.__running = False
        self.__is_shut_down.wait()
 
# Consumer thread
 
class Consumer(threading.Thread):
    def __init__(self, threadname, queue):
        threading.Thread.__init__(self, name = threadname)
        self.sharedata = queue
        self.__is_shut_down = threading.Event()
        self.__running = False
 
    def run(self):
        self.__running = True
        while self.__running:
            if self.sharedata.empty():
                time.sleep(0.01)
                continue
            print self.getName(),'        >> ',self.sharedata.get_nowait()
            self.sharedata.task_done()
            time.sleep(3)
        self.__is_shut_down.set()
        print self.getName(),'Finished'

    def shutdown(self):
        self.__running = False
        self.__is_shut_down.wait()
 

if __name__ == "__main__":
    HOST = "0.0.0.0" 
    PORT = 9999

    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()

    queue = Queue.Queue(10)

    producer = Producer('Producer', queue)
    producer.start()
    consumer0 = Consumer('Consumer0', queue)
    consumer0.start()
    consumer1 = Consumer('Consumer1', queue)
    consumer1.start()

    producer.join()
    print "producer join"
    queue.join()
    print "queue join"
    consumer0.shutdown()
    print "consumer shutdown"
    consumer1.shutdown()
    print "consumer shutdown"
    consumer0.join()
    consumer1.join()
    print "consumer join"
    server.shutdown()
    print "server shutdown"

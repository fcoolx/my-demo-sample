import threading
import time
import SocketServer

users = []

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
                    result = cmd[5:]
                elif cmd.startswith('login'):
                    username = cmd[6:]
                    users.append({username:self.wfile})
                    result = username + ' logined.'
                elif cmd == 'quit':
                    break
                else:
                    result = 'error cmd'
                self.wfile.write(result)
                self.wfile.write('\n')
            except:
                print 'error'
                break
        try:
            if username != None:
                users.remove(username)
        except:
            pass
        print username, ' closed.'

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST = "0.0.0.0" 
    PORT = 9999

    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(False)
    server_thread.start()
    time.sleep(10)
    server.shutdown()

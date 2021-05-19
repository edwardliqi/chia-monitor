import threading
from socket import *
import time

class SocketClient:
    def __init__(self, hostip, port, callback = None):
        self._hostip = hostip
        self._port = port
        self._callback = callback
        self._quit = False
        pass
    def quit(self):
        self._quit = True 
    def connect(self):
        client = socket(AF_INET,SOCK_STREAM)
        try:
            print('connecting')
            client.connect((self._hostip, self._port))
            print('connected')
        except:
            time.sleep(30)
            print('try again')
            pass
        return client
    @staticmethod
    def setup_client(user):
        client = user.connect()    
        while not user._quit and user._callback:
            telegram = user._callback()
            try:
                print('sending', telegram)
                client.send(telegram.encode()) 
            except:
                client = user.connect()
        client.close()

    def run(self):
        server_thread= threading.Thread(
            target=SocketClient.setup_client, args=(self,))
        server_thread.setDaemon(True)
        server_thread.start()

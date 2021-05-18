import threading
from socket import *

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
            client.connect((self._hostip, self._port))
        except:
            pass
        return client
    @staticmethod
    def setup_client(user):
        client = user.connect()    
        while not user._quit and user._callback:
            try:
                telegram = user._callback() 
                client.send(telegram.encode()) 
            except:
                client = user.connect()
        client.close()

    def run(self):
        server_thread= threading.Thread(
            target=SocketClient.setup_client, args=(self,))
        server_thread.setDaemon(True)
        server_thread.start()

from socket import *
import threading
#from io import BlockingIOError

class SockerServer():
    def __init__(self, callback=None):
        self._quit = False
        self._callback = callback 

    def quit(self):
        self._quit = True

    @staticmethod
    def recv_msg(user,client):
        while True:
            recv_data = client.recv(1024)
            if recv_data and user._callback:
                recv_text = recv_data.decode('gbk')
                user._callback(recv_text)
            else:
                break
        client.close()

    @staticmethod
    def setup_server(user):
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        ret = server.bind(("", 18080))
        server.listen(128)
        server.setblocking(False)
        while not user._quit:
            try:
                client, ip_port = server.accept()
                print('get client from',client, ip_port)
                thread_msg = threading.Thread(
                    target=SockerServer.recv_msg,
                    args=(user, client))
                thread_msg.setDaemon(True)
                thread_msg.start()
            except BlockingIOError:
                pass
        server.close()

    def run(self):
        server_thread= threading.Thread(
            target=SockerServer.setup_server, args=(self,))
        server_thread.setDaemon(True)
        server_thread.start()


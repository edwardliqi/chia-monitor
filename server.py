import time
import threading
from socket_server import SockerServer
from telegram import Telegram, Diskinfo

item = []
lock = threading.Lock()

def process_item(telegram):
    tele = Telegram.decoding(telegram)
    lock.acquire()
    print(tele.encoding())
    lock.release()

if __name__ == '__main__': 
    server = SockerServer(callback=process_item)
    server.run()
    time.sleep(60)
    server.quit()

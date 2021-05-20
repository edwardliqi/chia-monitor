import os
import socket
from socket_client import SocketClient
from telegram import Telegram, Diskinfo
from configparser import ConfigParser

def collect_info():
    import psutil
    conn = ConfigParser()
    conn.read(file_path)
    interval = int(conn.get('common','interval'))
    tele = Telegram()
    tele.set_hostname(socket.gethostname())
    tele.set_cpu_usage(str(psutil.cpu_percent(interval)))
    disks = psutil.disk_partitions()
    GB = 1024 * 1024 * 1024
    for x in disks:
        try:
            info = psutil.disk_usage(x.mountpoint)
            tele[x.mountpoint.replace(':\\','')] = \
                Diskinfo(str(int(info.total/GB)),
                         str(int(info.free/GB)))
        except:
            pass
    return tele.encoding()
if __name__ == '__main__':
    file_path = os.path.join(os.path.abspath('.'),'config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError("Config file config.ini doesn't exist")
    conn = ConfigParser()
    conn.read(file_path)
    host_ip_address=conn.get('common','host_ip')

    socket_client = SocketClient(hostip=host_ip_address, port=18080, callback=collect_info)
    socket_client.run()
    while True:
        char = input("Input q to exit")
        if 'q' == char:
            socket_client.quit()
            break
        else:
            pass
    


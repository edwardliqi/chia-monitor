import socket
import psutil
from socket_client import SocketClient
from telegram import Telegram, Diskinfo

def collect_info():
    tele = Telegram()
    tele.set_hostname(socket.gethostname())
    tele.set_cpu_usage(str(psutil.cpu_percent(1)))
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
    socket_client = SocketClient(hostip='192.168.2.123', port=18080, callback=collect_info)
    socket_client.run()
    while True:
        char = input("Input q to exit")
        if 'q' == char:
            socket_client.quit()
            break
        else:
            pass
    


import time
import threading
from socket_server import SockerServer
from telegram import Telegram, Diskinfo
from tkinter import *
import tkinter.ttk as ttk

win = Tk()
win.title("Treeview")
Label(win,text='Chia Management').pack()
col = ['host', 'cpu', 'C', 'D', 'Z']
 
tree = ttk.Treeview(win, columns = col, height = 10, show = "headings")
bar = ttk.Scrollbar(win, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=bar.set)
lock = threading.Lock()
host_dict = dict()

def process_item(telegram):
    tele = Telegram.decoding(telegram)
    lock.acquire()
    if host_dict.__contains__(tele._hostname):
        tree.item(host_dict[tele._hostname], values= [tele._hostname, tele._cpu_usage] + [tele[k]._freespace for k in col[2: ]])
    else:
        this_item = tree.insert('', 'end',text=tele._hostname, values=[tele._hostname, tele._cpu_usage] + [tele[k]._freespace for k in col[2: ]])
        host_dict[tele._hostname] = this_item
        print('insert new item', this_item)
#    tree.update()
    lock.release()

if __name__ == '__main__': 
    server = SockerServer(callback=process_item)
    server.run()
    tree.column('host',width=100,anchor='center')
    tree.column('cpu',width=40,anchor='w')
    tree.column('C',width=100,anchor='center')
    tree.column('D',width=100,anchor='center')
    tree.column('Z',width=100,anchor='center')
    tree.heading('host',text='Host')
    tree.heading('cpu',text='CPU')
    tree.heading('C',text='C')
    tree.heading('D',text='D')
    tree.heading('Z',text='Z')
    tree.pack()
    win.mainloop()

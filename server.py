import time
import threading
from socket_server import SockerServer
from telegram import Telegram, Diskinfo
from tkinter import *
import tkinter.ttk as ttk

win = Tk()
win.title("CHIA Plotting Monitor")
cols = ['host', 'cpu', 'C', 'D', 'Z']
 
tree = ttk.Treeview(win, columns = cols, height = 10, show = "headings")
bar = ttk.Scrollbar(tree, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=bar.set)
bar.pack(side=RIGHT, fill=Y)
lock = threading.Lock()
host_dict = dict()

def process_item(telegram):
    tele = Telegram.decoding(telegram)
    lock.acquire()
    #if host_dict.__contains__(tele._hostname):
    #    tree.item(host_dict[tele._hostname], values= [tele._hostname, tele._cpu_usage] + [tele[k]._freespace for k in cols[2: ]])
    #else:
    this_item = tree.insert('', 'end',text=tele._hostname, values=[tele._hostname, tele._cpu_usage] + [tele[k]._freespace for k in cols[2: ]])
    host_dict[tele._hostname] = this_item
    lock.release()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
 
if __name__ == '__main__': 
    server = SockerServer(callback=process_item)
    server.run()
    tree.column('host',width=100,anchor='center')
    tree.column('cpu',width=40,anchor='w')
    tree.heading('host',text='Host')
    tree.heading('cpu',text='CPU')
    for x in cols:
        tree.heading(x, text=x.upper(), command=lambda _col=x: treeview_sort_column(tree, _col, False))
        tree.column(x,width=100,anchor='center')
    tree.pack(anchor=W, ipadx=100, side=LEFT, expand=True, fill=BOTH)
    win.mainloop()

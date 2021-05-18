import time
import threading
from socket_server import SockerServer
from telegram import Telegram, Diskinfo
import sys
if sys.version_info < (3, 0):
    from Tkinter import *
    import ttk 
else:
    from tkinter import *
    import tkinter.ttk as ttk

win = Tk()
win.title("Treeview")
head_list = ['C', 'D', 'Z'] 
col = ['host', 'cpu', 'C', 'D', 'Z']
 
tree = ttk.Treeview(win, columns = col, height = 10, show = "headings")
bar = ttk.Scrollbar(win, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=bar.set)
lock = threading.Lock()

#use recursion
def process_dict(d, tree, tr):
    for k,v in d.items():
        if type(v) == list:
            print 'this is a list'
            if type(v[0]) == dict:
                print 'this is a dict in list'
                trr = tree.insert(tr, 'end', text=k, open=True)
                for ls in v:
                    process_dict(ls, tree, trr)
            else:
                print 'this is an insert in list'
                tree.insert(tr, 'end', text=k, values= v)
        elif type(v) == dict:
            print 'this is a dict'
            trr = tree.insert(tr, 'end', text=k, open = True)
            process_dict(v, tree, trr)

def process_item(telegram):
    tele = Telegram.decoding(telegram)
    lock.acquire()
    found = False
    items = tree.get_children()
    for item in items:
        if tele._hostname == tree.item(item, 'text'):
            tree.item(item, values= [tele._hostname, tele._cpu_usage] + [tele[k]._freespace for k in head_list])
            found = True
            break
    if not found:
        tree.insert('', 'end',text=tele._hostname, values=[tele._hostname, tele._cpu_usage] + [tele[k]._freespace for k in head_list])
    tree.update()
    lock.release()

if __name__ == '__main__': 
    #server = SockerServer(callback=process_item)
    #server.run()
    #time.sleep(60)
    #server.quit()
    #show = "tree", column 1 will be showed too
    #using show = "headings" to hiden column 1
     
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
    strs = ["TXL6003134INFO00017.26F0    0              C117  8              D59   56             E27   12             ", "TXL6003134INFO00019926F0    0              C117  8              D59   56             E27   12             "]
    for i in range(2):
        process_item(strs[i])
    tree.pack()
    win.mainloop()

"""Python 3.6.0
Georgia Barnes
Allows user to browse to choose specific source and destination folders and transfer all the files that have
been modified in the last 24 hours"""


from tkinter import *
import tkinter as tk
import os
from tkinter import messagebox
from tkinter import filedialog
import datetime
import os,time
import shutil
import datetime as dt
import sqlite3

def create_db(self):
    conn =  sqlite3.connect('fileTransfer.db')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE if not exists tbl_fileTransfer(\
                ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                col_dateTime);")
        conn.commit()
    conn.close()

def transferFiles(self):
    conn = sqlite3.connect('fileTransfer.db')
    with conn:
        cur = conn.cursor()
        cur,count = count_records(cur)
        if count > 1:
            transferLast(self)
        else:
            first_run(self)
    conn.close()

def count_records(cur):
    count = ""
    cur.execute("SELECT COUNT(*) FROM tbl_fileTransfer;")
    count = cur.fetchone()[0]
    return cur,count

def first_run(self):
    now = dt.datetime.now()
    yesterday = now-datetime.timedelta(hours=24)
    for root, dirs, files in os.walk(self.sourceFolder):
        for fname in files:
            path = os.path.join(root,fname)
            st = os.stat(path)
            mtime = datetime.datetime.fromtimestamp(st.st_mtime)
            if mtime > yesterday:
                shutil.copy2(path,self.destFolder)
    print ("{} moved to {}.".format(self.sourceFolder,self.destFolder))
    conn = sqlite3.connect('fileTransfer.db')
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl_fileTransfer (col_dateTime) VALUES(CURRENT_TIMESTAMP);")
        conn.commit()
    conn.close()
    load_gui(self)

def transferLast(self):
    conn = sqlite3.connect('fileTransfer.db')
    with conn:
        cur = conn.cursor()
        for root, dirs, files in os.walk(self.sourceFolder):
            for fname in files:
                path = os.path.join(root,fname)
                st = os.stat(path)
                mtime = datetime.datetime.fromtimestamp(st.st_mtime)
                cur.execute("SELECT col_dateTime FROM tbl_fileTransfer WHERE ID = (SELECT MAX(ID) FROM tbl_fileTransfer);")
                last = cur.fetchone()
                if mtime > last:
                    shutil.copy2(path,self.destFolder)
            ("INSERT INTO col_dateTime VALUES(CURRENT_TIMESTAMP);")
            conn.commit()
        conn.close()
        print ("{} moved to {}.".format(self.sourceFolder,self.destFolder))
    load_gui(self)
                                         

def browseSource(self):
    self.sourceFolder = tk.filedialog.askdirectory()
    source = (str(self.sourceFolder))#makes soure folder a string to insert into entry field
    self.txt_source.delete(0,END)#clears entry field
    self.txt_source.insert(0,source)#populates entry field with source folder path
    print (self.sourceFolder)

def browseDest(self):
    self.destFolder = tk.filedialog.askdirectory()
    dest = (str(self.destFolder))
    self.txt_dest.delete(0,END)
    self.txt_dest.insert(0,dest)
    print (self.destFolder)

#########################################################
#               GUI stuff                               #    
#########################################################
class ParentWindow(Frame):
    def __init__(self,master,*args,**kwargs):
        
        #config master frame
        self.master = master
        self.master.minsize(500,200)
        self.master.maxsize(500,200)
        
        self.master.title("Python File Manager")

        self.master.protocol("WM_DELETE_WINDOW", lambda: ask_quit(self))
        arg = self.master

        create_db(self)
        load_gui(self)
        
def load_gui(self):
   
    #labels
    self.lbl_source = tk.Label(self.master, text = 'Source Folder: ')
    self.lbl_source.grid(row = 0, column = 0, padx = (30,0), pady = (30,0), sticky = 'nw')
    self.lbl_dest = tk.Label(self.master, text = 'Destination Folder: ')
    self.lbl_dest.grid(row = 1, column = 0, padx = (30,0), pady = (30,0), sticky = 'nw')
    self.lbl_last=tk.Label(self.master, text = (""))
    self.lbl_last.grid(row = 2, column= 0, columnspan = 2, padx = (30,0), pady = (30,0), sticky = 'nw')                     
    
    #entry fields (must use browse for folders to be selected)
    self.txt_source = tk.Entry(self.master, text = '')
    self.txt_source.grid(row = 0, column = 1, padx = (30,0), pady = (30,0), sticky = 'new')
    self.txt_dest = tk.Entry(self.master, text = '')
    self.txt_dest.grid(row = 1, column = 1, padx = (30,0), pady = (30,0), sticky = 'new')

    #browse and transfer buttons
    self.btn_source = tk.Button(self.master, width = 12, height = 1, text = "Browse...",command = lambda: browseSource(self))
    self.btn_source.grid(row = 0, column = 2, padx = (30,0), pady = (30,0), sticky = 'w')
    self.btn_dest = tk.Button(self.master, width = 12, height =1, text = "Browse...",command = lambda: browseDest(self))
    self.btn_dest.grid(row = 1, column = 2, padx = (30,0), pady = (30,0), sticky = 'w')
    self.btn_transfer = tk.Button(self.master, width = 12, height = 1, text = "Transfer", command = lambda: transferFiles(self))
    self.btn_transfer.grid(row = 2, column = 2, padx = (30,0), pady = (30,0), sticky = 'w')

    #configure last transfer
    conn = sqlite3.connect('fileTransfer.db')
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT col_dateTime FROM tbl_fileTransfer WHERE ID = (SELECT MAX(ID) FROM tbl_fileTransfer);")
        last = cur.fetchone()
    conn.close()
    self.lbl_last.configure(text = "Last transfered: {}".format(last)) 

def ask_quit(self):
    if messagebox.askokcancel("Exit program","Are you sure you'd like to exit?"):
        self.master.destroy()
        os._exit()

if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainLoop()

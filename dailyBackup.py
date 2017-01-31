import datetime 
import os,time
import shutil
import datetime as dt

now = datetime.datetime.now()
yesterday = now-datetime.timedelta(hours=24)
sourceFolder = 'c:/users/georgia/desktop/importantCompanyDocuments'
destFolder = 'c:/users/georgia/desktop/backups'

def file_transfer():
    for root, dirs, files in os.walk(sourceFolder):
        for fname in files:
            path = os.path.join(root,fname)
            st = os.stat(path)
            mtime = datetime.datetime.fromtimestamp(st.st_mtime)
            if mtime > yesterday:
                print (fname)
                shutil.copy2(path,destFolder)

print file_transfer()



    

